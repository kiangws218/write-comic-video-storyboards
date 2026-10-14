const fs=require('fs'),path=require('path');
const {chromium}=require('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const sharp=require('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const mux=require('./mp4-muxer.cjs');
async function main(){
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const page=await browser.newPage({viewport:{width:1920,height:1200},deviceScaleFactor:1});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('file:///'+path.join(__dirname,'preview.html').replace(/\\/g,'/')+'?render=1');
 await page.evaluate(()=>window.OP.ready);await page.evaluate(()=>OP.pause());
 const tiles=[],times=[.24,.46,.72,1.15,1.65,2.4];
 for(const [i,t] of times.entries()){
  await page.evaluate(t=>OP.renderAt(t),t);
  const data=await page.evaluate(()=>document.getElementById('op-canvas').toDataURL('image/png'));
  const buffer=Buffer.from(data.split(',')[1],'base64');
  fs.writeFileSync(path.join(__dirname,'assets','frame-'+i+'.png'),buffer);
  tiles.push({input:await sharp(buffer).resize(640,360).png().toBuffer(),left:(i%3)*640,top:Math.floor(i/3)*360});
 }
 await sharp({create:{width:1920,height:720,channels:4,background:'#ffffff'}}).composite(tiles).png().toFile(path.join(__dirname,'assets','animation-contact-sheet.png'));
 await page.exposeFunction('exportProgress',v=>console.log(v));
 for(const variant of [{width:3840,height:2160,fps:60,bitrate:50000000,codec:'avc1.640034',name:'op-title-white-4k60.mp4'},{width:1920,height:1080,fps:60,bitrate:18000000,codec:'avc1.64002a',name:'op-title-white-1080p60.mp4'}]){
  console.log('Rendering',variant.name);
  const result=await page.evaluate(async v=>{
   const canvas=document.getElementById('op-canvas');canvas.width=v.width;canvas.height=v.height;
   const samples=[];let description,failure;
   const encoder=new VideoEncoder({
    output:(chunk,meta)=>{const data=new Uint8Array(chunk.byteLength);chunk.copyTo(data);samples.push({timestamp:chunk.timestamp,type:chunk.type,data});if(meta?.decoderConfig?.description)description=new Uint8Array(meta.decoderConfig.description)},
    error:e=>{failure=e.message}
   });
   const config={codec:v.codec,width:v.width,height:v.height,framerate:v.fps,bitrate:v.bitrate,bitrateMode:'variable',latencyMode:'realtime',hardwareAcceleration:'prefer-software',avc:{format:'avc'}};
   if(!(await VideoEncoder.isConfigSupported(config)).supported)throw Error('Unsupported video encoding');
   encoder.configure(config);const count=Math.round(OP.duration*v.fps);
   for(let i=0;i<count;i++){
    OP.renderAt(i/v.fps);
    const timestamp=Math.round(i*1e6/v.fps),duration=Math.round((i+1)*1e6/v.fps)-timestamp;
    const frame=new VideoFrame(canvas,{timestamp,duration,alpha:'discard'});
    encoder.encode(frame,{keyFrame:i%v.fps===0});frame.close();
    if(encoder.encodeQueueSize>=8)await encoder.flush();
    if(failure)throw Error(failure);
    if((i+1)%60===0)await window.exportProgress(v.width+'px: '+(i+1)+' / '+count+' frames');
   }
   await encoder.flush();encoder.close();if(failure)throw Error(failure);
   if(samples.length!==count)throw Error('Encoded frame count mismatch');
   const base64=data=>new Promise(resolve=>{const reader=new FileReader();reader.onload=()=>resolve(reader.result.split(',')[1]);reader.readAsDataURL(new Blob([data]))});
   return {description:await base64(description),samples:await Promise.all(samples.map(async s=>({...s,data:await base64(s.data)})))};
  },variant);
  const samples=result.samples.map(s=>({...s,data:Buffer.from(s.data,'base64')}));
  const output=path.join(__dirname,variant.name);
  fs.writeFileSync(output,mux({...variant,description:Buffer.from(result.description,'base64'),samples}));
  console.log(JSON.stringify({output,width:variant.width,height:variant.height,fps:variant.fps,frames:samples.length,duration:samples.length/variant.fps,bytes:fs.statSync(output).size}));
 }
 console.log('Page errors',errors);await browser.close();if(errors.length)throw Error(errors.join('; '));
}
main().catch(e=>{console.error(e);process.exitCode=1});
