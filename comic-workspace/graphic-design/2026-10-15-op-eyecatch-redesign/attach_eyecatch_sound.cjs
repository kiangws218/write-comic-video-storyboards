const fs=require('fs'),path=require('path'),crypto=require('crypto'),{spawn}=require('child_process');
const ROOT=__dirname,OUT=path.join(ROOT,'exports'),AUDIO=path.join(ROOT,'audio','sound-design-v1'),QA=path.join(ROOT,'qa');
function run(args){return new Promise((resolve,reject)=>{const p=spawn(require('./runtime.cjs').ffmpeg,args,{windowsHide:true});let out='',err='';p.stdout.on('data',b=>out+=b);p.stderr.on('data',b=>err+=b);p.on('exit',c=>c===0?resolve({out,err}):reject(Error(err.slice(-4000))))})}
async function fileHash(f){const h=crypto.createHash('sha256');for await(const b of fs.createReadStream(f))h.update(b);return h.digest('hex')}
async function videoHash(f){return(await run(['-v','error','-i',f,'-map','0:v:0','-c:v','copy','-f','hash','-hash','sha256','-'])).out.trim()}
function loudness(s){return JSON.parse([...s.matchAll(/\{\s*"input_i"[\s\S]*?\}/g)].at(-1)[0])}
(async()=>{
 const report={revision:'sound-design-6',visuals:[],encodedAudio:[],masters:JSON.parse(fs.readFileSync(path.join(AUDIO,'mastering-report.json')))};
 const opBefore=await fileHash(path.join(OUT,'Title-overlay-4K60-alpha.mov'));
 for(const[kind,name]of [['pause','Eyecatch-A-break'],['resume','Eyecatch-B-continue']]){
  const wav=path.join(AUDIO,kind+'-master-48k24.wav');
  for(const res of ['4K60','1080p60']){
   const file=path.join(OUT,name+'-'+res+'.mp4'),temp=path.join(OUT,name+'-'+res+'.sound.tmp.mp4'),before=await videoHash(file);
   await run(['-y','-v','error','-i',file,'-i',wav,'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-ac','2','-t','4','-movflags','+faststart',temp]);
   const after=await videoHash(temp);if(after!==before)throw Error('Visual bitstream changed');fs.renameSync(temp,file);
   report.visuals.push({file:path.basename(file),videoBitstreamUnchanged:true,videoSHA256:after});
  }
  fs.copyFileSync(wav,path.join(ROOT,'audio',kind+'.wav'));
  const encoded=path.join(OUT,name+'-1080p60.mp4');
  const measure=loudness((await run(['-hide_banner','-i',encoded,'-map','0:a:0','-af','loudnorm=I=-19:TP=-2:LRA=7:print_format=json','-f','null','-'])).err);
  if(Number(measure.input_tp)>-1)throw Error('AAC true peak is too high');report.encodedAudio.push({kind,lufs:Number(measure.input_i),truePeakDBTP:Number(measure.input_tp)});
 }
 await run(['-y','-v','error','-i',path.join(OUT,'Eyecatch-A-break-1080p60.mp4'),'-i',path.join(OUT,'Eyecatch-B-continue-1080p60.mp4'),'-filter_complex','[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]','-map','[v]','-map','[a]','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-r','60','-c:a','aac','-b:a','256k','-t','8','-movflags','+faststart',path.join(OUT,'Eyecatch-pair-sound-design-1080p60.mp4')]);
 await run(['-y','-v','error','-i',path.join(OUT,'Title-overlay-preview-1080p60.mp4'),'-i',path.join(OUT,'Eyecatch-A-break-1080p60.mp4'),'-i',path.join(OUT,'Eyecatch-B-continue-1080p60.mp4'),'-filter_complex','[0:v]setpts=PTS-STARTPTS[v0];anullsrc=r=48000:cl=stereo,atrim=duration=5[a0];[v0][a0][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[v][a]','-map','[v]','-map','[a]','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-r','60','-c:a','aac','-b:a','256k','-t','13','-movflags','+faststart',path.join(OUT,'Current-deliverables-preview-1080p60.mp4')]);
 report.opUnchanged=opBefore===await fileHash(path.join(OUT,'Title-overlay-4K60-alpha.mov'));if(!report.opUnchanged)throw Error('OP unexpectedly changed');
 let watch=fs.readFileSync(path.join(ROOT,'watch.html'),'utf8').replace(/const revision='[^']*'/,"const revision='sound-design-6'");
 if(!watch.includes('48k24.wav'))watch=watch.replace('</footer>','<br>音效母版：<a class="text" href="audio/sound-design-v1/pause-master-48k24.wav" download>中插 A · WAV</a> · <a class="text" href="audio/sound-design-v1/resume-master-48k24.wav" download>中插 B · WAV</a></footer>');
 fs.writeFileSync(path.join(ROOT,'watch.html'),watch);
 const mf=path.join(ROOT,'delivery-manifest.json'),manifest=JSON.parse(fs.readFileSync(mf));manifest.revision=report.revision;
 for(const f of manifest.files){const p=path.join(ROOT,f.file);f.bytes=fs.statSync(p).size;f.sha256=await fileHash(p)}
 manifest.soundDesign={directory:'audio/sound-design-v1',masters:['pause-master-48k24.wav','resume-master-48k24.wav'],sampleRate:48000,bits:24,channels:2,durationEach:4,pairPreview:'exports/Eyecatch-pair-sound-design-1080p60.mp4',stems:'audio/sound-design-v1/stems'};
 fs.writeFileSync(mf,JSON.stringify(manifest,null,2));fs.writeFileSync(path.join(QA,'sound-design-verification.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
})().catch(e=>{console.error(e);process.exit(1)});
