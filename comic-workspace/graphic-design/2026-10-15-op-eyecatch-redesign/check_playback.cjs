const fs=require('fs'),path=require('path');
const {chromium}=require('playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,...require('./runtime.cjs').browserOptions});
 const page=await browser.newPage({viewport:{width:1440,height:1140}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:4188/watch.html');await page.waitForFunction(()=>document.querySelector('video').readyState>=2);
 const playback=await page.evaluate(async()=>{const v=document.querySelector('video');v.muted=true;await v.play();await new Promise((resolve,reject)=>{v.onended=resolve;v.onerror=()=>reject(Error('Media decode failed'));setTimeout(()=>reject(Error('Playback timeout')),25000)});const q=v.getVideoPlaybackQuality();return{duration:v.duration,width:v.videoWidth,height:v.videoHeight,ended:v.ended,totalVideoFrames:q.totalVideoFrames,droppedVideoFrames:q.droppedVideoFrames}});
 if(!playback.ended||Math.abs(playback.duration-13)>.1)throw Error('Showreel playback incomplete');
 const switches=[];
 for(let i=1;i<=3;i++){
  await page.locator(`[data-i="${i}"]`).click();await page.waitForFunction(()=>{const v=document.querySelector('video');return v.readyState>=2&&!v.paused});
  switches.push(await page.evaluate(()=>({duration:video.duration,width:video.videoWidth,height:video.videoHeight,source:video.currentSrc.split('/').pop()})));await page.evaluate(()=>video.pause());
 }
 await page.locator('[data-i="1"]').click();await page.waitForFunction(()=>video.readyState>=2);await page.evaluate(()=>{video.pause();video.currentTime=2.8});await page.waitForFunction(()=>!video.seeking);
 await page.screenshot({path:path.join(__dirname,'qa','watch-preview.png'),fullPage:true});
 await page.goto('http://127.0.0.1:4188/index.html');await page.evaluate(()=>film.ready);
 const boundary=await page.evaluate(()=>{film.render('pause',4,1920,1080);const a=film.canvas.toDataURL();film.render('resume',0,1920,1080);const b=film.canvas.toDataURL();return{exactPixelMatch:a===b}});
 if(!boundary.exactPixelMatch)throw Error('Paired boundary is not identical');
 if(errors.length)throw Error(JSON.stringify(errors));
 const report={playback,switches,boundary,pageErrors:errors};fs.writeFileSync(path.join(__dirname,'qa','playback-verification.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
