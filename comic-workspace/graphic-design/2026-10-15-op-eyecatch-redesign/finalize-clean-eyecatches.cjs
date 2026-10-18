const fs=require('fs'),path=require('path'),crypto=require('crypto'),{spawn}=require('child_process');
const sharp=require('sharp');
const ROOT=__dirname,OUT=path.join(ROOT,'exports'),QA=path.join(ROOT,'qa');
function run(args){return new Promise((resolve,reject)=>{const p=spawn(require('./runtime.cjs').ffmpeg,args,{windowsHide:true});let out='',err='';p.stdout.on('data',b=>out+=b);p.stderr.on('data',b=>err+=b);p.on('exit',c=>c===0?resolve(out):reject(Error(err.slice(-4000))))})}
async function hashFile(file){const h=crypto.createHash('sha256');for await(const chunk of fs.createReadStream(file))h.update(chunk);return h.digest('hex')}
(async()=>{
 const report={revision:'clean-eyecatches-5',removed:['intro background 魔 / 手','peripheral male/female symbols','both upper English lines','both lower English lines and their underline'],clips:[]};
 for(const name of ['Eyecatch-A-break','Eyecatch-B-continue']){
  for(const res of ['4K60','1080p60']){
   const file=path.join(OUT,`${name}-${res}.mp4`),out=await run(['-v','error','-i',file,'-map','0:v:0','-an','-f','framemd5','-']);
   const frames=out.split(/\r?\n/).filter(x=>x&&!x.startsWith('#')).length;if(frames!==240)throw Error(name+' frame count '+frames);
   report.clips.push({file:path.basename(file),frames,decodeErrors:0,sha256:await hashFile(file)});console.log('VERIFIED',name,res);
  }
  const t=name.endsWith('break')?2.1:2.15;
  await run(['-y','-v','error','-ss',String(t),'-i',path.join(OUT,name+'-4K60.mp4'),'-frames:v','1','-vf','scale=1920:1080:flags=lanczos',path.join(QA,name+'-encoded.png')]);
  const ref=path.join(QA,name.endsWith('break')?'pause-2_1.png':'resume-2_15.png');
  const a=await sharp(path.join(QA,name+'-encoded.png')).removeAlpha().raw().toBuffer(),b=await sharp(ref).removeAlpha().raw().toBuffer();let sq=0;for(let i=0;i<a.length;i++)sq+=(a[i]-b[i])**2;const rmse=Math.sqrt(sq/a.length);if(rmse>12)throw Error('Unexpected encoded image deviation');report.clips.push({imageCheck:name,rgbRMSE:rmse});
 }
 await run(['-y','-v','error','-i',path.join(OUT,'Eyecatch-A-break-1080p60.mp4'),'-i',path.join(OUT,'Eyecatch-B-continue-1080p60.mp4'),'-filter_complex','[0:v:0][0:a:0][1:v:0][1:a:0]concat=n=2:v=1:a=1[v][a]','-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-r','60','-c:a','aac','-b:a','256k','-t','8','-movflags','+faststart',path.join(OUT,'Eyecatch-pair-clean-1080p60.mp4')]);
 await run(['-y','-v','error','-i',path.join(OUT,'Title-overlay-preview-1080p60.mp4'),'-i',path.join(OUT,'Eyecatch-A-break-1080p60.mp4'),'-i',path.join(OUT,'Eyecatch-B-continue-1080p60.mp4'),'-filter_complex','[0:v]setpts=PTS-STARTPTS[v0];anullsrc=r=48000:cl=stereo,atrim=duration=5[a0];[v0][a0][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[v][a]','-map','[v]','-map','[a]','-c:v','libx264','-crf','17','-preset','fast','-r','60','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-t','13','-movflags','+faststart',path.join(OUT,'Current-deliverables-preview-1080p60.mp4')]);
 report.opMasterSHA256=await hashFile(path.join(OUT,'Title-overlay-4K60-alpha.mov'));
 if(report.opMasterSHA256!=='57a1651c1125286c508f64d6e47825c5e1f55c1f1d6ef87a893809ca71cdf10b')throw Error('OP master unexpectedly changed');
 report.opUnchanged=true;
 let watch=fs.readFileSync(path.join(ROOT,'watch.html'),'utf8');watch=watch.replace("const revision='ring-overlay-4'","const revision='clean-eyecatches-5'");fs.writeFileSync(path.join(ROOT,'watch.html'),watch);
 const mfile=path.join(ROOT,'delivery-manifest.json'),manifest=JSON.parse(fs.readFileSync(mfile));manifest.revision=report.revision;
 for(const f of manifest.files){const target=path.join(ROOT,f.file);f.bytes=fs.statSync(target).size;f.sha256=await hashFile(target)}
 manifest.eyecatchRevision={removed:report.removed,opUnchanged:true,pairPreview:'exports/Eyecatch-pair-clean-1080p60.mp4'};
 fs.writeFileSync(mfile,JSON.stringify(manifest,null,2));fs.writeFileSync(path.join(QA,'clean-eyecatches-verification.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
})().catch(e=>{console.error(e);process.exit(1)});
