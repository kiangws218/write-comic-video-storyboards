(function(){
 'use strict';
 const A=window.EYE_ASSETS,canvas=document.getElementById('eyecatch'),ctx=canvas.getContext('2d',{alpha:false});
 canvas.width=1920;canvas.height=1080;
 const C={blue:'#216AE1',sky:'#25A9E4',navy:'#173B80',white:'#FFFFFF'};
 const duration=3.8,clamp=x=>Math.max(0,Math.min(1,x)),ease=x=>1-(1-clamp(x))**3;
 const letters=[],outer=new Path2D(A.outer),english=new Path2D(A.english);
 let current=0,variant='pause',playing=false,loop=true,epoch=0,raf=0;
 const load=url=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src=url});
 function path(d,color){ctx.fillStyle=color;ctx.fill(new Path2D(d))}
 function star(x,y,size,color){ctx.save();ctx.translate(x,y);ctx.scale(size,size);path('M0,-1 Q.1,-.12 1,0 Q.1,.12 0,1 Q-.1,.12 -1,0 Q-.1,-.12 0,-1Z',color);ctx.restore()}
 function ringAt(p,radius){
  if(p>=1){ctx.stroke(radius===450?outer:new Path2D(A.inner));return}
  ctx.beginPath();const count=Math.max(1,Math.ceil(160*p));
  for(let i=0;i<=count;i++){const a=-Math.PI/2+Math.PI*2*p*i/count,r=radius*(1+.0035*Math.sin(3*a+.4)+.002*Math.sin(7*a));const x=960+r*Math.cos(a),y=532+r*Math.sin(a);if(i)ctx.lineTo(x,y);else ctx.moveTo(x,y)}
  if(p>=1)ctx.closePath();ctx.stroke();
 }
 function door(t,dark,alpha){
  const ink=dark?C.white:C.navy,accent=dark?C.sky:C.blue;
  ctx.save();ctx.globalAlpha=alpha;ctx.translate(960,211);ctx.scale(.60,.60);
  path('M-43,44 L-43,-10 C-43,-63 43,-61 43,-10 L43,44 L30,44 L30,-10 C30,-45 -30,-46 -30,-10 L-30,44Z',ink);
  path('M-28,42 L-28,-8 C-28,-44 29,-44 29,-8 L29,42Z',dark?C.navy:C.blue);
  const open=ease((t-2.00)/.25),width=51-15*open;
  ctx.save();ctx.translate(-29,-7);ctx.transform(1,0,.05*open,1,0,0);path(`M0,0 Q${width*.5},-39 ${width},0 L${width},49 L0,49Z`,accent);ctx.fillStyle=dark?C.white:C.sky;ctx.fillRect(width-10,24,4,7);ctx.restore();
  if(open>.05){const blink=1-Math.max(0,1-Math.abs(t-2.62)/.065)*.92;ctx.fillStyle=C.white;for(const x of [18,26]){ctx.beginPath();ctx.ellipse(x,14,2.2,3.7*blink,0,0,Math.PI*2);ctx.fill()}}
  path('M-51,47 L51,44 L54,51 L-50,53Z',ink);ctx.restore();
 }
 function glyphState(i,t){
  const q=A.layout[i],v=A.letters[i];if(t<q.start)return null;
  const u=clamp((t-q.start)/(q.hit-q.start)),tau=t-q.hit;
  let x=q.cx,y=q.cy,sx=q.scale,sy=q.scale,angle=q.roll;
  if(tau<0){
   const top=-v.h*q.scale/2-70;
   y=top+(q.cy-top)*u*u;
   x+=q.dx*(1-ease(u));angle+=q.turn*(1-ease(u));
   const stretch=.11*Math.sin(Math.PI*u);sx/=Math.sqrt(1+stretch);sy*=1+stretch;
  }else if(tau<.76){
   // Bottom-anchored squash keeps the letter planted, then two diminishing jumps.
   const keys=[[0,0,1],[.06,0,.74],[.115,-23,1.12],[.23,-60,1],[.36,0,1],[.405,0,.86],[.46,-10,1.055],[.53,-22,1],[.62,0,1],[.665,0,.96],[.76,0,1]];
   let j=1;while(tau>keys[j][0])j++;
   const a=keys[j-1],b=keys[j],f=clamp((tau-a[0])/(b[0]-a[0]));
   const smooth=f*f*(3-2*f),motion=b[1]>a[1]?f*f:1-(1-f)**2;
   const stretch=a[2]+(b[2]-a[2])*smooth;
   y+=a[1]+(b[1]-a[1])*motion+v.h*q.scale*.5*(1-stretch);
   sy*=stretch;sx/=Math.sqrt(stretch);
   angle+=(q.turn>0?1:-1)*3.2*Math.sin(tau*19)*Math.exp(-tau*5);
  }
  return {x,y,sx,sy,angle};
 }
 function letteringRotation(t){
  if(t<.22)return -5;
  if(t<.80)return -5+7*(t-.22)/.58;
  const u=t-.80,velocity=7/.58;
  return Math.exp(-2.6*u)*(2*Math.cos(5*u)+(velocity+2.6*2)/5*Math.sin(5*u))*(1-ease((t-2.1)/.5));
 }
 function perimeterRotation(t,p){
  if(p<1)return -.36*(1-p);
  const u=t-.71;return .36/.65*u*Math.exp(-5*u)*(1-ease((t-1.9)/.6));
 }
 function drawGlyph(im,v,s){ctx.save();ctx.translate(s.x,s.y);ctx.rotate(s.angle*Math.PI/180);ctx.scale(s.sx,s.sy);ctx.drawImage(im,-v.w/2,-v.h/2,v.w,v.h);ctx.restore()}
 function renderAt(t,options={}){
  current=Math.max(0,Math.min(duration,t));ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle=C.white;ctx.fillRect(0,0,canvas.width,canvas.height);ctx.setTransform(canvas.width/1920,0,0,canvas.height/1080,0,0);
  const dark=(options.variant||variant)==='resume',p=clamp((current-.06)/.65),innerP=clamp((current-.15)/.65),fill=dark?ease((current-.40)/.40):0;
  if(fill>0){ctx.save();ctx.globalAlpha=fill;ctx.fillStyle=C.blue;ctx.fill(outer);ctx.restore()}
  if(p>0){
   ctx.lineCap='round';ctx.lineJoin='round';ctx.lineWidth=7;ctx.strokeStyle=C.blue;ringAt(p,450);
   if(fill>0){ctx.save();ctx.globalAlpha=fill;ctx.strokeStyle=C.white;ringAt(p,450);ctx.restore()}
   ctx.lineWidth=2.5;ctx.strokeStyle=dark&&fill>.5?C.sky:C.navy;ringAt(innerP,380);
   // The perimeter retains a little clockwise angular momentum after closure.
   ctx.save();ctx.beginPath();ctx.moveTo(960,532);ctx.arc(960,532,490,-Math.PI/2,-Math.PI/2+2*Math.PI*p);ctx.closePath();ctx.clip();
   ctx.translate(960,532);ctx.rotate(perimeterRotation(current,p));ctx.translate(-960,-532);
   ctx.fillStyle=dark?C.white:C.navy;ctx.globalAlpha=dark?fill:clamp(p*2);ctx.fill(english);ctx.restore();
   if(p<1){const a=-Math.PI/2+2*Math.PI*p;ctx.save();ctx.translate(960+450*Math.cos(a),532+450*Math.sin(a));ctx.rotate(a);path('M-4,-5 L13,0 L-4,5Z',C.sky);ctx.restore()}
  }
  const accents=ease((current-.72)/.16);
  if(accents>0){ctx.save();ctx.globalAlpha=accents;for(const side of [-1,1])star(960+side*409,532,10,dark?C.white:C.blue);ctx.restore()}
  const states=A.layout.map((_,i)=>glyphState(i,current));
  ctx.save();ctx.translate(960,532);ctx.rotate(letteringRotation(current)*Math.PI/180);ctx.translate(-960,-532);
  if(!dark)for(let i=0;i<A.letters.length;i++)if(states[i])drawGlyph(letters[i].edge,A.letters[i],states[i]);
  // Crossfade the letters as the blue disc forms; both versions drop immediately.
  if(dark){
   for(let i=0;i<A.letters.length;i++)if(states[i])drawGlyph(letters[i].ink,A.letters[i],states[i]);
   if(fill>0){ctx.save();
    // Clip in screen coordinates while keeping the lettering group's rotation.
    ctx.setTransform(canvas.width/1920,0,0,canvas.height/1080,0,0);ctx.clip(outer);
    ctx.translate(960,532);ctx.rotate(letteringRotation(current)*Math.PI/180);ctx.translate(-960,-532);
    ctx.globalAlpha=fill;for(let i=0;i<A.letters.length;i++)if(states[i])drawGlyph(letters[i].white,A.letters[i],states[i]);ctx.restore();
   }
  }else for(let i=0;i<A.letters.length;i++)if(states[i])drawGlyph(letters[i].ink,A.letters[i],states[i]);
  ctx.restore();
  const slider=document.getElementById('progress');if(slider)slider.value=current;
  const time=document.getElementById('time');if(time)time.textContent=current.toFixed(1)+' / '+duration+' s';
 }
 function sync(){const b=document.getElementById('pause');if(b)b.textContent=playing?'暂停':'播放'}
 function pause(){playing=false;cancelAnimationFrame(raf);sync()}
 function tick(now){if(!playing)return;const t=(now-epoch)/1000;if(t<=duration)renderAt(t);else if(loop){epoch=now;renderAt(0)}else{renderAt(duration);playing=false;sync();return}raf=requestAnimationFrame(tick)}
 function play(){if(current>=duration)current=0;cancelAnimationFrame(raf);epoch=performance.now()-current*1000;playing=true;sync();raf=requestAnimationFrame(tick)}
 function replay(){pause();renderAt(0);play()}
 function select(value){variant=value;document.querySelectorAll('[data-variant]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.variant===value)));replay()}
 const ready=Promise.all(A.letters.map(async v=>({ink:await load(v.inkData),edge:await load(v.edgeData),white:await load(v.whiteData)}))).then(im=>{
  letters.push(...im);renderAt(0);document.getElementById('replay')?.addEventListener('click',replay);document.getElementById('pause')?.addEventListener('click',()=>playing?pause():play());document.getElementById('progress')?.addEventListener('input',e=>{pause();renderAt(+e.target.value)});document.getElementById('loop')?.addEventListener('change',e=>loop=e.target.checked);document.querySelectorAll('[data-variant]').forEach(b=>b.addEventListener('click',()=>select(b.dataset.variant)));if(!new URLSearchParams(location.search).has('render'))play();
 });
 window.EYE={ready,renderAt,pause,play,replay,duration,select,letteringRotation,perimeterRotation,characters:A.letters.map(v=>v.ch).join(''),getStates:t=>A.layout.map((_,i)=>glyphState(i,t))};
})();
