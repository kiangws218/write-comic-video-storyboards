// A short anime title sting: outside anchors, inside pair, crown, English signature.
(function(){
 'use strict';
 const A=window.OP_ASSETS,canvas=document.getElementById('op-canvas'),ctx=canvas.getContext('2d',{alpha:true});
 canvas.width=A.width;canvas.height=A.height;
 const duration=5.2,clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
 const cues=[
  {start:.71,hit:1.11,dx:-42,dy:-112,roll:-13,arc:18},
  {start:.80,hit:1.19,dx:-18,dy:-128,roll:-9,arc:10},
  {start:.89,hit:1.27,dx:22,dy:-128,roll:9,arc:10},
  {start:.98,hit:1.35,dx:44,dy:-104,roll:13,arc:18},
  {start:.12,hit:.61,dx:-450,dy:145,roll:-16,arc:94},
  {start:.34,hit:.83,dx:-92,dy:235,roll:-12,arc:24},
  {start:.41,hit:.91,dx:94,dy:235,roll:12,arc:24},
  {start:.19,hit:.69,dx:450,dy:145,roll:16,arc:94}
 ];
 let images=[],english,playing=false,loop=true,current=0,epoch=0,raf=0;
 const centre=i=>{const v=A.letters[i];return [v.x+v.w/2,v.y+v.h/2]};
 const loadImage=url=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src=url});
 function state(i,t){
  const q=cues[i],[tx,ty]=centre(i);if(t<q.start)return null;
  const tau=t-q.hit;let x=tx,y=ty,sx=1,sy=1,angle=0,alpha=1;
  if(tau<0){
   const u=clamp((t-q.start)/(q.hit-q.start)),e=1-(1-u)**2;
   x+=q.dx*(1-e);y+=q.dy*(1-e)-4*q.arc*e*(1-e);
   angle=q.roll*(1-e);const size=.96+.04*e;sx=size;sy=size;
   alpha=clamp(u/.12);
  }else if(tau<.65){
   // A single crisp impact followed by a much smaller after-bounce.
   const spring=Math.exp(-11*tau)*Math.sin(24*tau);
   const impact=Math.exp(-17*tau)*Math.cos(24*tau);
   y-= (i<4?9:21)*spring;
   x+=(i===4?-10:i===7?10:0)*spring;
   sy=1-(i<4?.055:.105)*impact;sx=1/(sy**.55);
   angle=(q.roll>0?1:-1)*(i<4?2.2:3.4)*spring;
  }
  // Adjacent big characters acknowledge the inside pair's arrival.
  if(i===4||i===7){const dt=t-(i===4?cues[5].hit:cues[6].hit);if(dt>=0&&dt<.45){const p=Math.exp(-12*dt)*Math.sin(26*dt);x+=(i===4?-8:8)*p;angle+=(i===4?-1.5:1.5)*p}}
  return {x,y,sx,sy,angle,alpha};
 }
 function draw(im,v,s,alpha=1){
  ctx.save();ctx.globalAlpha=s.alpha*alpha;ctx.translate(s.x,s.y);ctx.rotate(s.angle*Math.PI/180);ctx.scale(s.sx,s.sy);ctx.drawImage(im,-v.w/2,-v.h/2,v.w,v.h);ctx.restore();
 }
 function ribbon(points,width,color,alpha){
  ctx.save();ctx.globalAlpha=alpha;ctx.fillStyle=color;
  const [x,y,cx,cy,ex,ey]=points;
  ctx.beginPath();ctx.moveTo(x,y);ctx.quadraticCurveTo(cx,cy,ex,ey);ctx.quadraticCurveTo(cx,cy+width,x,y+width*.12);ctx.closePath();ctx.fill();ctx.restore();
 }
 function accents(t){
  // Brief drawn swishes support the outside arrivals and then disappear.
  for(const q of [{at:.23,dir:1},{at:.33,dir:-1}]){
   const dt=t-q.at;if(dt<0||dt>.43)continue;
   const p=dt/.43,a=Math.sin(Math.PI*p)*.42;
   ctx.save();if(q.dir<0){ctx.translate(A.width,0);ctx.scale(-1,1)}
   ribbon([65+235*p,727-40*p,236+265*p,541-65*p,395+190*p,545],10*(1-p),A.palette.sky,a);
   ribbon([77+245*p,752-35*p,251+260*p,583-65*p,381+190*p,576],4*(1-p),A.palette.royal,a*.65);
   ctx.restore();
  }
 }
 function impact(t){
  // Small hand-drawn impact ticks at the two outside corners, no persistent ornament.
  for(const q of [{at:.61,x:305,y:598,side:-1},{at:.69,x:1630,y:612,side:1}]){
   const dt=t-q.at;if(dt<0||dt>.24)continue;const p=dt/.24;
   ctx.save();ctx.strokeStyle=A.palette.sky;ctx.globalAlpha=.65*(1-p);ctx.lineCap='butt';ctx.lineWidth=5*(1-p);
   for(let k=0;k<3;k++){const a=(-.7+k*.65),r=16+35*p,length=15*(1-p);ctx.beginPath();ctx.moveTo(q.x+q.side*Math.cos(a)*r,q.y+Math.sin(a)*r);ctx.lineTo(q.x+q.side*Math.cos(a)*(r+length),q.y+Math.sin(a)*(r+length));ctx.stroke()}
   ctx.restore();
  }
 }
 function renderAt(t,options={}){
  current=clamp(t,0,duration);ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.setTransform(canvas.width/A.width,0,0,canvas.height/A.height,0,0);
  if(!options.transparent){ctx.fillStyle=A.palette.paper;ctx.fillRect(0,0,A.width,A.height)}
  const states=A.letters.map((_,i)=>state(i,current));
  // The logo breathes outward once as the main word locks together.
  const dt=current-.91,pulse=dt>=0&&dt<.55?.014*Math.exp(-8*dt)*Math.sin(19*dt):0;
  ctx.save();ctx.translate(960,560);ctx.scale(1+pulse,1+pulse);ctx.translate(-960,-560);
  accents(current);
  // One short exposure echo during fast motion, rather than oversized camera planes.
  for(let i=4;i<8;i++){
   const s=states[i],prev=state(i,current-.025);if(!s||!prev||current>=cues[i].hit-.08)continue;
   const speed=Math.hypot(s.x-prev.x,s.y-prev.y)/.025;if(speed<650)continue;
   draw(images[i].ink,A.letters[i],prev,.12);
  }
  for(let i=0;i<8;i++)if(states[i])draw(images[i].edge,A.letters[i],states[i]);
  for(let i=0;i<8;i++)if(states[i])draw(images[i].ink,A.letters[i],states[i]);
  impact(current);
  const e=A.english,u=clamp((current-1.44)/.40);
  if(u>0){
   const reveal=1-(1-u)**3;ctx.save();ctx.beginPath();ctx.rect(e.x-8,e.y-12,(e.w+16)*reveal,e.h+45);ctx.clip();
   ctx.globalAlpha=clamp(u*5);ctx.drawImage(english,e.x,e.y+9*(1-reveal),e.w,e.h);ctx.restore();
  }
  ctx.restore();
  const progress=document.getElementById('progress');if(progress)progress.value=current;
  const time=document.getElementById('time');if(time)time.textContent=current.toFixed(1)+' / '+duration.toFixed(1)+' s';
  return states;
 }
 function syncButtons(){const b=document.getElementById('pause');if(b)b.textContent=playing?'暂停':'播放'}
 function tick(now){if(!playing)return;const t=(now-epoch)/1000;if(t<=duration)renderAt(t);else if(loop){epoch=now;renderAt(0)}else{renderAt(duration);playing=false;syncButtons();return}raf=requestAnimationFrame(tick)}
 function play(){if(current>=duration)current=0;cancelAnimationFrame(raf);epoch=performance.now()-current*1000;playing=true;syncButtons();raf=requestAnimationFrame(tick)}
 function pause(){playing=false;cancelAnimationFrame(raf);syncButtons()}
 function replay(){pause();renderAt(0);play()}
 const ready=Promise.all([Promise.all(A.letters.map(async v=>({edge:await loadImage(v.edgeData),ink:await loadImage(v.inkData)}))),loadImage(A.english.data)]).then(([glyphImages,eng])=>{
  images=glyphImages;english=eng;renderAt(0);
  document.getElementById('replay')?.addEventListener('click',replay);
  document.getElementById('pause')?.addEventListener('click',()=>playing?pause():play());
  document.getElementById('progress')?.addEventListener('input',e=>{pause();renderAt(+e.target.value)});
  document.getElementById('loop')?.addEventListener('change',e=>loop=e.target.checked);
  if(!new URLSearchParams(location.search).has('render'))play();
 });
 window.OP={ready,renderAt,play,pause,replay,duration,getStates:t=>A.letters.map((_,i)=>state(i,t))};
})();
