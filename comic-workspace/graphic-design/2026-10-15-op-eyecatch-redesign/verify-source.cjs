const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert');
const {chromium}=require('playwright');
(async()=>{
 const root=__dirname;
 const server=http.createServer((req,res)=>{
  const file=path.resolve(root,'.'+decodeURIComponent(req.url.split('?')[0]));
  if(!file.startsWith(root+path.sep)){res.writeHead(403);return res.end()}
  fs.readFile(file,(err,data)=>{if(err){res.writeHead(404);return res.end()}res.setHeader('Content-Type',file.endsWith('.js')?'application/javascript':file.endsWith('.html')?'text/html':file.endsWith('.json')?'application/json':'application/octet-stream');res.end(data)});
 });
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 let browser;
 try{
  browser=await chromium.launch({headless:true,...require('./runtime.cjs').browserOptions});
  const page=await browser.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/index.html');await page.evaluate(()=>film.ready);
  const result=await page.evaluate(async()=>{
   const alpha=t=>{film.render('overlay',t,640,360);const pixels=film.canvas.getContext('2d').getImageData(0,0,640,360).data;let max=0,count=0;for(let i=3;i<pixels.length;i+=4){max=Math.max(max,pixels[i]);if(pixels[i])count++}return {max,count}};
   const first=alpha(0),hold=alpha(2.8),last=alpha(299/60);
   film.render('pause',4,640,360);const a=film.canvas.toDataURL();film.render('resume',0,640,360);const boundary=a===film.canvas.toDataURL();
   const config={codec:'avc1.64002a',width:640,height:360,bitrate:2000000,framerate:60,latencyMode:'realtime',avc:{format:'annexb'}};
   const support=await VideoEncoder.isConfigSupported(config);if(!support.supported)throw Error('Chrome must support H.264 WebCodecs encoding');
   let chunks=0,encodeError;const encoder=new VideoEncoder({output(){chunks++},error(e){encodeError=e.message}});encoder.configure(config);
   for(let i=0;i<5;i++){film.render('pause',i/60,640,360);const frame=new VideoFrame(film.canvas,{timestamp:Math.round(i*1e6/60)});encoder.encode(frame);frame.close()}
   await encoder.flush();encoder.close();if(encodeError)throw Error(encodeError);
   return {first,hold,last,boundary,encodedFrames:chunks};
  });
  assert.equal(result.first.max,0);assert.equal(result.last.max,0);assert(result.hold.count>0);assert.equal(result.boundary,true);assert.equal(result.encodedFrames,5);assert.deepEqual(errors,[]);
  console.log(JSON.stringify({sourceCheck:'passed',...result},null,2));
 }finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve))}
})().catch(error=>{console.error(error);process.exit(1)});
