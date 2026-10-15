const fs=require('fs'),path=require('path'),http=require('http'),{spawn}=require('child_process');
const {chromium}=require('playwright');
const sharp=require('sharp');
const ROOT=__dirname,OUT=path.join(ROOT,'exports'),QA=path.join(ROOT,'qa');fs.mkdirSync(OUT,{recursive:true});fs.mkdirSync(QA,{recursive:true});
const mime={'.html':'text/html','.js':'application/javascript','.json':'application/json','.png':'image/png','.svg':'image/svg+xml','.wav':'audio/wav','.mp4':'video/mp4'};
function serve(){return new Promise(resolve=>{const server=http.createServer((req,res)=>{const rel=decodeURIComponent(req.url.split('?')[0]);const f=path.resolve(ROOT,'.'+(rel==='/'?'/index.html':rel));if(!f.startsWith(ROOT+path.sep)){res.writeHead(403);return res.end()}fs.readFile(f,(e,data)=>{if(e){res.writeHead(404);return res.end('Not found')}res.setHeader('Content-Type',mime[path.extname(f)]||'application/octet-stream');res.end(data)})});server.listen(0,'127.0.0.1',()=>resolve(server))})}
function run(args){return new Promise((resolve,reject)=>{const p=spawn(require('./runtime.cjs').ffmpeg,args,{windowsHide:true});let err='';p.stderr.on('data',x=>err+=x);p.on('exit',code=>code===0?resolve(err):reject(Error(err.slice(-4000))))})}
async function snapshots(page,entryOnly=false){
 const sheets={op:[.18,.58,.84,1.13,1.65,2.10,2.72,3.12,3.76,4.02,4.44,4.83,5.4,6.4,7.4,8.7],pause:[.2,.58,.85,1.14,1.40,1.72,2.10,2.80,3.26,3.45,3.70,3.98],resume:[.12,.42,.75,1.10,1.40,1.80,2.15,2.80,3.25,3.48,3.75,3.98]};
 if(entryOnly){delete sheets.op;sheets.pause=[.18,.40,.60,.92,1.24,1.60,2.10,2.80,3.25,3.50,3.70,3.98];sheets.resume=[.18,.40,.60,.92,1.24,1.60,2.15,2.80,3.25,3.50,3.70,3.98]}
 for(const[kind,times]of Object.entries(sheets)){
  const comps=[];
  for(let i=0;i<times.length;i++){
   const t=times[i];const data=await page.evaluate(({kind,t})=>{film.render(kind,t,1920,1080);return film.canvas.toDataURL('image/png').split(',')[1]},{kind,t});
   const b=Buffer.from(data,'base64');fs.writeFileSync(path.join(QA,`${kind}-${String(t).replace('.','_')}.png`),b);
   const thumb=await sharp(b).resize(480,270).png().toBuffer();const x=(i%4)*480,y=Math.floor(i/4)*304;
   comps.push({input:thumb,left:x,top:y});
   comps.push({input:Buffer.from(`<svg width="480" height="34"><rect width="480" height="34" fill="#14263f"/><text x="16" y="23" fill="#cee0fa" font-family="Arial" font-size="15">${kind.toUpperCase()} / ${t.toFixed(2)}s</text></svg>`),left:x,top:y+270});
  }
  await sharp({create:{width:1920,height:Math.ceil(times.length/4)*304,channels:3,background:'#14263f'}}).composite(comps).jpeg({quality:94}).toFile(path.join(QA,`${kind}-contact.jpg`));
  console.log('CONTACT',kind);
 }
}
async function encode(page,kind,width,height){
 const names={op:'OP-title',pause:'Eyecatch-A-break',resume:'Eyecatch-B-continue'};
 const tag=width===3840?'4K60':'1080p60',stem=names[kind]+'-'+tag;
 const raw=path.join(OUT,stem+'.h264');
 const downloadPromise=page.waitForEvent('download',{timeout:600000});
 const stats=await page.evaluate(async({kind,width,height})=>{
  const chunks=[];let bytes=0,error;
  const config={codec:width===3840?'avc1.640034':'avc1.64002a',width,height,bitrate:width===3840?48000000:18000000,framerate:60,latencyMode:'realtime',avc:{format:'annexb'}};
  const support=await VideoEncoder.isConfigSupported(config);if(!support.supported)throw Error('Unsupported encoder '+JSON.stringify(config));
  const encoder=new VideoEncoder({output(chunk){const b=new Uint8Array(chunk.byteLength);chunk.copyTo(b);chunks.push(b);bytes+=b.length},error(e){error=String(e)}});encoder.configure(config);
  const frames=Math.round(film.duration[kind]*60),start=performance.now();
  for(let i=0;i<frames;i++){
   film.render(kind,i/60,width,height);
   const f=new VideoFrame(film.canvas,{timestamp:Math.round(i*1e6/60),duration:Math.round(1e6/60)});encoder.encode(f,{keyFrame:i%120===0});f.close();
   if(i%20===19){await encoder.flush();if(error)throw Error(error)}
   if(i%120===0)console.log('ENCODE',kind,width,i+'/'+frames);
  }
  await encoder.flush();encoder.close();if(error)throw Error(error);
  const blob=new Blob(chunks,{type:'video/h264'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='render.h264';a.click();
  return{frames,bytes,seconds:(performance.now()-start)/1000};
 },{kind,width,height});
 const d=await downloadPromise;await d.saveAs(raw);
 await run(['-y','-r','60','-i',raw,'-i',path.join(ROOT,'audio',kind+'.wav'),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart','-shortest',path.join(OUT,stem+'.mp4')]);
 fs.unlinkSync(raw);console.log('EXPORTED',stem,stats);return{kind,width,height,...stats};
}
(async()=>{
 const server=await serve(),port=server.address().port;
 const browser=await chromium.launch({headless:true,...require('./runtime.cjs').browserOptions,args:['--disable-background-timer-throttling','--disable-renderer-backgrounding']});
 const page=await browser.newPage({viewport:{width:1440,height:1120},acceptDownloads:true});page.on('pageerror',e=>console.error('PAGE ERROR',e.message));page.on('console',m=>{if(m.text().startsWith('ENCODE'))console.log(m.text())});
 await page.goto('http://127.0.0.1:'+port);await page.evaluate(()=>film.ready);
 const mode=process.argv[2]||'preview';
 console.log('ENCODER',await page.evaluate(async()=>({api:typeof VideoEncoder,h264:await VideoEncoder.isConfigSupported({codec:'avc1.640034',width:3840,height:2160,bitrate:48000000,framerate:60,latencyMode:'realtime',avc:{format:'annexb'}})})));
 if(mode==='preview'||mode==='preview-eye')await snapshots(page,mode==='preview-eye');
 else if(mode==='export'||mode==='export-op'||mode==='export-eyes'){
  const kinds=mode==='export-op'?['op']:mode==='export-eyes'?['pause','resume']:['op','pause','resume'];
  const old=path.join(OUT,'render-stats.json');const stats=fs.existsSync(old)?JSON.parse(fs.readFileSync(old)).filter(x=>!kinds.includes(x.kind)):[];
  for(const kind of kinds)stats.push(await encode(page,kind,3840,2160));
  for(const kind of kinds){const names={op:'OP-title',pause:'Eyecatch-A-break',resume:'Eyecatch-B-continue'};await run(['-y','-i',path.join(OUT,names[kind]+'-4K60.mp4'),'-vf','scale=1920:1080:flags=lanczos','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',path.join(OUT,names[kind]+'-1080p60.mp4')]);console.log('DOWNSCALED',kind)}
  fs.writeFileSync(path.join(OUT,'render-stats.json'),JSON.stringify(stats,null,2));
 }else if(mode==='test')await encode(page,'pause',1920,1080);
 await browser.close();server.close();
})().catch(e=>{console.error(e);process.exit(1)});
