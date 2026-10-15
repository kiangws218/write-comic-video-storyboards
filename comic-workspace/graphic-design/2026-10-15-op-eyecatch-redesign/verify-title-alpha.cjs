const fs=require('fs'),path=require('path'),{spawn}=require('child_process');
const sharp=require('sharp');
const ROOT=__dirname,OUT=path.join(ROOT,'exports'),QA=path.join(ROOT,'qa');
function run(args){return new Promise((resolve,reject)=>{const p=spawn(require('./runtime.cjs').ffmpeg,args,{windowsHide:true});let out='',err='';p.stdout.on('data',b=>out+=b);p.stderr.on('data',b=>err+=b);p.on('exit',c=>c===0?resolve(out):reject(Error(err.slice(-3500))))})}
async function verify(){
 const report={duration:5,fps:60,frames:300,masters:[],alphaChecks:[]};
 for(const res of ['4K60','1080p60']){
  const out=await run(['-v','error','-i',path.join(OUT,`Title-overlay-${res}-alpha.mov`),'-an','-f','framemd5','-']);const lines=out.split(/\r?\n/).filter(x=>x&&!x.startsWith('#'));if(lines.length!==300)throw Error('Wrong frames '+res);report.masters.push({resolution:res,frames:lines.length,decodeErrors:0});
 }
 // Inspect the alpha channel of actual decoded RGBA pixels. Extracting alpha into
 // a grayscale YUV image can introduce a limited-range grayscale conversion.
 for(const [label,t]of [['first',0],['hold',2.8],['last',299/60]]){
  const file=path.join(QA,'title-overlay-rgba-'+label+'.png');await run(['-y','-v','error','-ss',String(t),'-i',path.join(OUT,'Title-overlay-4K60-alpha.mov'),'-frames:v','1','-pix_fmt','rgba',file]);
  const data=await sharp(file).ensureAlpha().extractChannel(3).raw().toBuffer();let min=255,max=0,nonzero=0;for(const a of data){min=Math.min(min,a);max=Math.max(max,a);if(a)nonzero++}
  if(label==='hold'&&(min!==0||max!==255||nonzero===0||nonzero===data.length))throw Error('Alpha channel invalid');if(label!=='hold'&&max!==0)throw Error('Edge frame not fully transparent');report.alphaChecks.push({label,min,max,nonzeroPixels:nonzero});
 }
 fs.writeFileSync(path.join(QA,'title-overlay-verification.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));return report;
}
module.exports=verify;if(require.main===module)verify().catch(e=>{console.error(e);process.exit(1)});
