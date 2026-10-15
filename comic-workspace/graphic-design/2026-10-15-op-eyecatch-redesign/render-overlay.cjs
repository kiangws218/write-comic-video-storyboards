const fs=require('fs'),path=require('path'),http=require('http'),{spawn}=require('child_process');
const {chromium}=require('playwright');
const sharp=require('sharp');
const ROOT=__dirname,OUT=path.join(ROOT,'exports'),FRAMES=path.join(OUT,'title-overlay-png-4K60'),QA=path.join(ROOT,'qa');fs.mkdirSync(FRAMES,{recursive:true});fs.mkdirSync(QA,{recursive:true});fs.mkdirSync(QA,{recursive:true});
function run(args){return new Promise((resolve,reject)=>{const p=spawn(require('./runtime.cjs').ffmpeg,args,{windowsHide:true});let out='',err='';p.stdout.on('data',b=>out+=b);p.stderr.on('data',b=>err+=b);p.on('exit',code=>code===0?resolve({out,err}):reject(Error(err.slice(-5000))))})}
(async()=>{
 const server=http.createServer((req,res)=>{let f=path.resolve(ROOT,'.'+decodeURIComponent(req.url.split('?')[0]));if(!f.startsWith(ROOT+path.sep)){res.writeHead(403);return res.end()}fs.readFile(f,(e,data)=>{if(e){res.writeHead(404);return res.end()}res.setHeader('Content-Type',f.endsWith('.js')?'application/javascript':f.endsWith('.html')?'text/html':f.endsWith('.json')?'application/json':'application/octet-stream');res.end(data)})});await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const browser=await chromium.launch({headless:true,...require('./runtime.cjs').browserOptions}),page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port+'/title-overlay.html');await page.evaluate(()=>film.ready);
 const samples=[0,.25,.50,.80,1.20,1.70,2.30,2.85,3.55,3.90,4.45,4.983333];const thumbs=[];
 const checker=await sharp(Buffer.from('<svg width="1920" height="1080"><defs><pattern id="c" width="80" height="80" patternUnits="userSpaceOnUse"><rect width="80" height="80" fill="#d6d9df"/><path d="M0 0H40V40H0ZM40 40H80V80H40Z" fill="#bec3cb"/></pattern></defs><rect width="1920" height="1080" fill="url(#c)"/></svg>')).png().toBuffer();
 for(let i=0;i<300;i++){
  if(process.argv.includes('--reuse')&&fs.existsSync(path.join(FRAMES,String(i).padStart(4,'0')+'.png')))continue;
  const b=Buffer.from(await page.evaluate(t=>{film.render('overlay',t,3840,2160);return film.canvas.toDataURL('image/png').split(',')[1]},i/60),'base64');fs.writeFileSync(path.join(FRAMES,String(i).padStart(4,'0')+'.png'),b);
  if(i===168)fs.writeFileSync(path.join(OUT,'Title-overlay-hold-4K.png'),b);
  if(i%30===0)console.log('PNG',i,'/ 300');
 }
 for(let i=0;i<samples.length;i++){
  const f=Math.round(samples[i]*60),raw=await sharp(path.join(FRAMES,String(Math.min(f,299)).padStart(4,'0')+'.png')).resize(1920,1080).png().toBuffer();
  const composed=await sharp(checker).composite([{input:raw}]).png().toBuffer();const flat=await sharp(composed).resize(480,270).png().toBuffer();
  const x=(i%4)*480,y=Math.floor(i/4)*304;thumbs.push({input:flat,left:x,top:y},{input:Buffer.from(`<svg width="480" height="34"><rect width="480" height="34" fill="#14263f"/><text x="16" y="23" fill="white" font-family="Arial" font-size="15">TITLE OVERLAY / ${samples[i].toFixed(2)}s</text></svg>`),left:x,top:y+270});
 }
 await sharp({create:{width:1920,height:912,channels:3,background:'#14263f'}}).composite(thumbs).jpeg({quality:94}).toFile(path.join(QA,'title-overlay-contact.jpg'));
 if(errors.length)throw Error(JSON.stringify(errors));await browser.close();server.close();
 const input=path.join(FRAMES,'%04d.png'),master=path.join(OUT,'Title-overlay-4K60-alpha.mov');
 await run(['-y','-v','error','-framerate','60','-i',input,'-c:v','prores_ks','-profile:v','4','-pix_fmt','yuva444p10le','-qscale:v','8','-alpha_bits','16','-vendor','apl0','-an',master]);console.log('MASTER ALPHA 4K EXPORTED');
 await run(['-y','-v','error','-i',master,'-vf','scale=1920:1080:flags=lanczos','-c:v','prores_ks','-profile:v','4','-pix_fmt','yuva444p10le','-qscale:v','8','-alpha_bits','16','-vendor','apl0','-an',path.join(OUT,'Title-overlay-1080p60-alpha.mov')]);console.log('MASTER ALPHA 1080 EXPORTED');
 const grid=path.join(QA,'title-overlay-grid.png');await sharp(checker).png().toFile(grid);
 await run(['-y','-v','error','-loop','1','-i',grid,'-framerate','60','-i',input,'-filter_complex','[1:v]scale=1920:1080:flags=lanczos[title];[0:v][title]overlay=shortest=1:format=auto,format=yuv420p[v]','-map','[v]','-c:v','libx264','-crf','16','-preset','fast','-r','60','-an','-t','5','-movflags','+faststart',path.join(OUT,'Title-overlay-preview-1080p60.mp4')]);console.log('CHECKER PREVIEW EXPORTED');
 await require('./verify-title-alpha.cjs')();
})().catch(e=>{console.error(e);process.exit(1)});
