const fs=require('fs'),path=require('path'),{spawn}=require('child_process');
const sharp=require('sharp');
const ROOT=__dirname,OUT=path.join(ROOT,'exports'),QA=path.join(ROOT,'qa');
function run(args){return new Promise((resolve,reject)=>{const p=spawn(require('./runtime.cjs').ffmpeg,args,{windowsHide:true});let stdout='',stderr='';p.stdout.on('data',b=>stdout+=b);p.stderr.on('data',b=>stderr+=b);p.on('exit',code=>code===0?resolve({stdout,stderr}):reject(Error(stderr.slice(-4000))))})}
(async()=>{
const clips=[['OP-title',540,9,7.4,'op-7_4.png'],['Eyecatch-A-break',240,4,2.1,'pause-2_1.png'],['Eyecatch-B-continue',240,4,2.15,'resume-2_15.png']];
const reports=[];
for(const[name,frames,seconds,t,reference]of clips){
 for(const res of ['4K60','1080p60']){
  const file=path.join(OUT,name+'-'+res+'.mp4');
  const result=await run(['-v','error','-i',file,'-map','0:v:0','-an','-f','framemd5','-']);
  const lines=result.stdout.split(/\r?\n/).filter(x=>x&&!x.startsWith('#'));
  if(lines.length!==frames)throw Error(name+' wrong frame count '+lines.length);
  const dimension=result.stdout.split(/\r?\n/).find(x=>x.startsWith('#dimensions'));
  const rate=result.stdout.split(/\r?\n/).find(x=>x.startsWith('#tb'));
  reports.push({file:path.basename(file),frames:lines.length,seconds,dimension,timebase:rate,bytes:fs.statSync(file).size,decodeErrors:0});
  console.log('VERIFIED',name,res,lines.length);
 }
 await run(['-y','-v','error','-ss',String(t),'-i',path.join(OUT,name+'-4K60.mp4'),'-frames:v','1','-vf','scale=1920:1080:flags=lanczos',path.join(QA,name+'-encoded.png')]);
 const a=await sharp(path.join(QA,name+'-encoded.png')).removeAlpha().raw().toBuffer();
 const b=await sharp(path.join(QA,reference)).removeAlpha().raw().toBuffer();
 let error=0;for(let i=0;i<a.length;i++)error+=(a[i]-b[i])**2;
 const rmse=Math.sqrt(error/a.length);if(rmse>12)throw Error('Unexpected color/image deviation '+rmse);
 reports.push({imageCheck:name,rgbRMSE:rmse});
}
await run(['-y','-v','error','-i',path.join(OUT,'OP-title-1080p60.mp4'),'-i',path.join(OUT,'Eyecatch-A-break-1080p60.mp4'),'-i',path.join(OUT,'Eyecatch-B-continue-1080p60.mp4'),'-filter_complex','[0:v:0][0:a:0][1:v:0][1:a:0][2:v:0][2:a:0]concat=n=3:v=1:a=1[v][a]','-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-r','60','-c:a','aac','-b:a','256k','-t','17','-movflags','+faststart',path.join(OUT,'OTHER-SIDE-showreel-1080p60.mp4')]);
console.log('SHOWREEL CREATED');
await sharp(path.join(QA,'op-7_4.png')).resize(1600,900).jpeg({quality:95}).toFile(path.join(ROOT,'poster.jpg'));
fs.writeFileSync(path.join(QA,'verification.json'),JSON.stringify(reports,null,2));
console.log(JSON.stringify(reports,null,2));
})().catch(e=>{console.error(e);process.exit(1)});
