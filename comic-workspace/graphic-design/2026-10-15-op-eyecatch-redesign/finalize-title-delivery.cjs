const fs=require('fs'),path=require('path'),crypto=require('crypto'),{spawn}=require('child_process');
const sharp=require('sharp');
const ROOT=__dirname,OUT=path.join(ROOT,'exports');
function run(args){return new Promise((resolve,reject)=>{const p=spawn(require('./runtime.cjs').ffmpeg,args,{windowsHide:true});let err='';p.stderr.on('data',x=>err+=x);p.on('exit',c=>c===0?resolve(err):reject(Error(err.slice(-4000))))})}
(async()=>{
 const grid=fs.readFileSync(path.join(ROOT,'qa','title-overlay-grid.png'));
 const title=await sharp(path.join(OUT,'Title-overlay-hold-4K.png')).resize(1920,1080).png().toBuffer();const poster=await sharp(grid).composite([{input:title}]).png().toBuffer();await sharp(poster).resize(1600,900).jpeg({quality:95}).toFile(path.join(ROOT,'title-overlay-poster.jpg'));
 await run(['-y','-v','error','-i',path.join(OUT,'Title-overlay-preview-1080p60.mp4'),'-i',path.join(OUT,'Eyecatch-A-break-1080p60.mp4'),'-i',path.join(OUT,'Eyecatch-B-continue-1080p60.mp4'),'-filter_complex','[0:v]setpts=PTS-STARTPTS[v0];anullsrc=r=48000:cl=stereo,atrim=duration=5[a0];[v0][a0][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[v][a]','-map','[v]','-map','[a]','-c:v','libx264','-crf','17','-preset','fast','-r','60','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-t','13','-movflags','+faststart',path.join(OUT,'Current-deliverables-preview-1080p60.mp4')]);
 let html=fs.readFileSync(path.join(ROOT,'watch.html'),'utf8');
 for(const[a,b]of[
 ['OTHER-SIDE-showreel-1080p60.mp4','Current-deliverables-preview-1080p60.mp4'],['OP-title-1080p60.mp4','Title-overlay-preview-1080p60.mp4'],['OP-title-4K60.mp4','Title-overlay-4K60-alpha.mov'],['完整放映 · 17 秒','完整放映 · 13 秒'],['OP · 9 秒','圆环标题 · 5 秒'],['标题演出与一对中插，完整音效成片。','透明标题入场／离场与一对中插。标题灰格仅用于预览透明区域。'],["fluid-entry-2","ring-overlay-4"],['>OP</a>','>透明标题 MOV</a>'],['href="index.html"','href="title-overlay.html"'],['href="设计说明.md"','href="标题叠加说明.md"']])html=html.split(a).join(b);
 fs.writeFileSync(path.join(ROOT,'watch.html'),html);
 let check=fs.readFileSync(path.join(ROOT,'check_playback.cjs'),'utf8').replace('playback.duration-17','playback.duration-13').replace('video.currentTime=7.4','video.currentTime=2.8');fs.writeFileSync(path.join(ROOT,'check_playback.cjs'),check);
 const names=['Title-overlay-4K60-alpha.mov','Title-overlay-1080p60-alpha.mov','Title-overlay-preview-1080p60.mp4','Title-overlay-hold-4K.png','Current-deliverables-preview-1080p60.mp4','Eyecatch-A-break-4K60.mp4','Eyecatch-B-continue-4K60.mp4'];
 const files=names.map(n=>{const file=path.join(OUT,n),buffer=fs.readFileSync(file);return{file:'exports/'+n,bytes:buffer.length,sha256:crypto.createHash('sha256').update(buffer).digest('hex')}});
 fs.writeFileSync(path.join(ROOT,'delivery-manifest.json'),JSON.stringify({project:'Title overlay and eyecatches',revision:'ring-overlay-4',date:'2026-10-15',titleUse:'Overlay into an existing opening, entrance/hold/exit only',alphaFormat:'ProRes 4444, straight alpha, no audio',titleDuration:5,titleFrames:300,pngSequence:{directory:'exports/title-overlay-png-4K60',frames:300},files},null,2));
 console.log('CURRENT DELIVERY UPDATED: transparent title + existing eyecatches.');
})().catch(e=>{console.error(e);process.exit(1)});
