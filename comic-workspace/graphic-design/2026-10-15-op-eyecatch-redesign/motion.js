/* Original direction / timing / choreography, built solely from static SVGs. */
const W=1920,H=1080,TAU=Math.PI*2;
const C={paper:'#FCFCF7',white:'#FFFFFF',blue:'#216AE1',ink:'#173B80',cyan:'#25A9E4',ice:'#CBEFF6',night:'#10285D',lime:'#E2FF8A'};
const duration={op:9,pause:4,resume:4,overlay:5};
const canvas=document.getElementById('film'),ctx=canvas.getContext('2d',{alpha:true});
let art={},sprites={},outlines={},ready,ringOverlayDrawing=false;
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const lerp=(a,b,t)=>a+(b-a)*t;
const ease=x=>1-Math.pow(1-clamp(x),3);
const smooth=x=>{x=clamp(x);return x*x*(3-2*x)};
const expo=x=>x>=1?1:1-Math.pow(2,-10*clamp(x));
const back=x=>{x=clamp(x)-1;return 1+2.70158*x*x*x+1.70158*x*x};
const spring=x=>1-Math.exp(-8*clamp(x))*Math.cos(12*clamp(x));
const range=(t,a,b)=>clamp((t-a)/(b-a));
function layer(fn){ctx.save();fn();ctx.restore()}
function fill(color){if(ringOverlayDrawing)return;ctx.fillStyle=color;ctx.fillRect(0,0,W,H)}
function line(x1,y1,x2,y2,color,width=2){ctx.strokeStyle=color;ctx.lineWidth=width;ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke()}
function circle(x,y,r,color,width=0){if(r<=0)return;ctx.beginPath();ctx.arc(x,y,r,0,TAU);if(width){ctx.strokeStyle=color;ctx.lineWidth=width;ctx.stroke()}else{ctx.fillStyle=color;ctx.fill()}}
function polygon(points,color){ctx.fillStyle=color;ctx.beginPath();points.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();ctx.fill()}
function arc(x,y,r,a,b,color,width=4){ctx.strokeStyle=color;ctx.lineWidth=width;ctx.beginPath();ctx.arc(x,y,r,a,b);ctx.stroke()}
function star(x,y,r,color,rot=0,ratio=.23){layer(()=>{ctx.translate(x,y);ctx.rotate(rot);polygon([[0,-r],[r*ratio,-r*ratio],[r,0],[r*ratio,r*ratio],[0,r],[-r*ratio,r*ratio],[-r,0],[-r*ratio,-r*ratio]],color)})}
function type(text,x,y,size,color,opts={}){if(ringOverlayDrawing)return;ctx.fillStyle=color;ctx.textAlign=opts.align||'left';ctx.textBaseline='middle';ctx.font=`${opts.weight||800} ${size}px "Arial", "Microsoft YaHei", sans-serif`;if(opts.tracking){let xx=x;for(const c of text){ctx.fillText(c,xx,y);xx+=ctx.measureText(c).width+opts.tracking}}else ctx.fillText(text,x,y)}
function img(name,x,y,scale=1,rotation=0,alpha=1,tint){const a=art[name];if(!a||scale<.0001||alpha<=0)return;if(ringOverlayDrawing&&outlines[name]&&!tint){drawOutlined(name,x,y,scale,rotation,ctx.globalAlpha*alpha);return}layer(()=>{ctx.translate(x,y);ctx.rotate(rotation);ctx.globalAlpha*=alpha;const image=tint?sprites[name+'@'+tint]:sprites[name];ctx.drawImage(image,-a.w*scale/2,-a.h*scale/2,a.w*scale,a.h*scale)})}
function glyphAt(i,x,y,s,r=0,a=1,tint){img('glyph-'+i,x,y,s,r,a,tint)}
function glyphFinal(i,scale=1){const a=art['glyph-'+i];return{x:960+(a.x+a.w/2-800)*scale,y:535+(a.y+a.h/2-400)*scale}}
function drawLogo(x=960,y=535,s=1,alpha=1,rot=0){layer(()=>{ctx.translate(x,y);ctx.rotate(rot);ctx.translate(-960,-535);for(let i=0;i<8;i++){const p=glyphFinal(i,s);glyphAt(i,p.x,p.y,s,0,alpha)}const a=art.english;img('english',960+(a.x+a.w/2-800)*s,535+(a.y+a.h/2-400)*s,s,0,alpha)})}
function ticks(x,y,r,phase,color,alpha=1){layer(()=>{ctx.globalAlpha=alpha;for(let i=0;i<48;i++){let a=i*TAU/48+phase;let len=i%6===0?20:7;line(x+Math.cos(a)*r,y+Math.sin(a)*r,x+Math.cos(a)*(r+len),y+Math.sin(a)*(r+len),color,i%6===0?3:1.5)}})}
function speedLines(t,color,alpha=.4){layer(()=>{ctx.globalAlpha=alpha;for(let i=0;i<18;i++){let a=(i/18)*TAU+.09*Math.sin(i*19.3),r=380+((i*71+t*650)%800);let l=80+(i%4)*43;line(960+Math.cos(a)*r,540+Math.sin(a)*r,960+Math.cos(a)*(r+l),540+Math.sin(a)*(r+l),color,i%3===0?5:2)}})}
function tile(x,y,s,angle,color,outline=false){layer(()=>{ctx.translate(x,y);ctx.rotate(angle);ctx.beginPath();ctx.rect(-s/2,-s/2,s,s);if(outline){ctx.strokeStyle=color;ctx.lineWidth=3;ctx.stroke()}else{ctx.fillStyle=color;ctx.fill()}})}
function symbol(x,y,s,kind,color,angle=0){layer(()=>{ctx.translate(x,y);ctx.rotate(angle);circle(0,-s*.16,s*.25,color,s*.065);if(kind===0){line(0,s*.09,0,s*.60,color,s*.065);line(-s*.18,s*.38,s*.18,s*.38,color,s*.065)}else{line(s*.18,-s*.35,s*.49,-s*.66,color,s*.065);line(s*.20,-s*.66,s*.49,-s*.66,color,s*.065);line(s*.49,-s*.66,s*.49,-s*.37,color,s*.065)}})}
function cornerMarks(t,alpha=1){if(ringOverlayDrawing)return;layer(()=>{ctx.globalAlpha=alpha;for(let i=0;i<3;i++){line(106+i*17,128,126+i*17,102,C.cyan,3);line(1776+i*17,978,1796+i*17,952,C.blue,3)}star(1745,154,22,C.cyan,t*.3)})}

function prologue(t){
 fill(C.paper);
 const p=range(t,0,.7),r=lerp(8,410,expo(p));
 layer(()=>{ctx.translate(960,540);ctx.rotate(-.3+t*.32);ctx.scale(1,.80);arc(0,0,r,-Math.PI*.9,Math.PI*.9,C.blue,5);arc(0,0,r+22,Math.PI*.1,Math.PI*1.45,C.cyan,1.8);ticks(0,0,r+45,.12,C.blue,.3*ease(p))});
 const breath=1+.08*Math.sin(t*8);star(960,540,52*breath*ease(range(t,0,.2)),C.blue,t*.5);
 if(t>.17){type('THE OTHER SIDE',960,765,20,C.ink,{align:'center',tracking:0});line(820,805,1100,805,C.cyan,2)}
 let cut=ease(range(t,.4,.8));line(960-1300*cut,540+650*cut,960+1300*cut,540-650*cut,C.blue,lerp(2,18,cut));
 cornerMarks(t,ease(p)*.5);
}

function panels(t){
 const u=t-.72;fill(C.blue);
 const colors=[C.blue,C.cyan,C.ink],indices=[1,2,4];
 for(let j=0;j<3;j++)layer(()=>{
  let x=j*700-135;let inP=ease(range(u,j*.05,.28+j*.05));let shift=(1-inP)*(j%2?1100:-1100);
  ctx.beginPath();ctx.moveTo(x+200,0);ctx.lineTo(x+850,0);ctx.lineTo(x+490,H);ctx.lineTo(x-160,H);ctx.closePath();ctx.clip();
  ctx.fillStyle=colors[j];ctx.fillRect(0,0,W,H);
  const a=art['glyph-'+indices[j]],sc=3.6+u*.6;
  glyphAt(indices[j],x+350+u*80,540+shift,sc,-.18,1,C.white);
  type(['NEW','WORLD','AWAKENS'][j],x+235,915,24,C.white,{tracking:6});
  line(x+160,130,x+455,130,C.white,4);
 });
 // Intentional two-frame-style photographic sliver, rather than random flicker.
 if(t>1.23){let p=range(t,1.23,1.47);polygon([[W*(1-p),0],[W*(1-p)+260,0],[W*(1-p)-100,H],[W*(1-p)-360,H]],C.paper)}
}

function tunnel(t){
 const u=t-1.45,p=range(t,1.45,2.55);fill(C.night);
 layer(()=>{ctx.translate(1120,540);ctx.rotate(-.16+u*.10);
  for(let i=14;i>=0;i--){let z=((i/15+u*.29)%1),s=70+1550*Math.pow(z,2.1),a=.12+.7*z;ctx.globalAlpha=a;ctx.lineWidth=2+7*z;ctx.strokeStyle=i%3===0?C.cyan:C.blue;ctx.strokeRect(-s*.65,-s*.5,s*1.3,s);}
 });
 layer(()=>{ctx.globalAlpha=.12;for(let i=0;i<8;i++)glyphAt(i,1550-(i%3)*480+u*110,260+Math.floor(i/3)*410,2.0,-.3,1,C.white)});
 type('OPEN THE',150,370,105,C.white,{weight:900});type('OTHER SIDE.',143,490,115,C.white,{weight:900});
 line(154,595,635+240*ease(p),595,C.cyan,8);
 type('新世界、起動。',155,660,30,C.ice,{weight:500});
 symbol(1420,395,280,0,C.cyan,-.28-u*.15);symbol(1540,705,260,1,C.white,.2+u*.15);
 star(1290,590,52,C.lime,.4+u*2);speedLines(u,C.ice,.12);
 // A diagonal page turn leads from abstract space into the letters.
 if(t>2.25){const q=expo(range(t,2.25,2.65));polygon([[-600,0],[-550+3200*q,0],[-1150+3200*q,H],[-600,H]],C.paper)}
}

function orbit(t){
 const u=t-2.55,p=range(t,2.55,3.65);fill(C.paper);
 layer(()=>{ctx.translate(960,540);ctx.rotate(-.3+u*.18);ctx.scale(1,.48);circle(0,0,470,C.blue,4);arc(0,0,570,.2,.2+TAU*.65,C.cyan,3);circle(0,0,700,C.ice,1.5)});
 for(let i=0;i<8;i++){
  const pose=orbitPose(i,u),{a,x,y,s,r}=pose;
  glyphAt(i,x,y,s,r,1);
  if(i%2===0)star(x+90,y-105,16,C.cyan,a);
 }
 star(960,540,52+20*Math.sin(p*Math.PI),C.blue,-u*1.5);
 for(let i=0;i<9;i++){let a=i*2.4;tile(960+Math.cos(a)*860,540+Math.sin(a)*430,12+i%3*7,a+u,C.cyan,i%2===0)}
}

function orbitPose(i,u){
 const a=i*TAU/8-Math.PI*.5+u*.35;
 return{a,x:960+Math.cos(a)*680,y:530+Math.sin(a)*338,s:.61+.06*(1+Math.sin(a)),r:Math.cos(a)*.12};
}

function assemble(t){
 fill(C.paper);const u=t-3.65;
 const shake=Math.exp(-Math.max(0,u-.83)*13)*Math.sin(Math.max(0,u-.83)*54)*7;
 layer(()=>{ctx.translate(shake,shake*.4);
  const burst=range(u,.65,1.35);
  if(burst>0)layer(()=>{ctx.globalAlpha=(1-burst)*.7;for(let i=0;i<24;i++){let a=i*TAU/24,r=350+burst*570;polygon([[960+Math.cos(a)*r,540+Math.sin(a)*r],[960+Math.cos(a+.012)*(r+170),540+Math.sin(a+.012)*(r+170)],[960+Math.cos(a+.024)*r,540+Math.sin(a+.024)*r]],i%3?C.cyan:C.blue)}});
  for(let i=0;i<8;i++){
   const delay=[.04,.12,.20,.29,0,.10,.19,.29][i],p=range(u,delay,delay+.76),e=1-Math.exp(-7*p)*Math.cos(10*p);const f=glyphFinal(i,1.08);
   const start=orbitPose(i,1.1);
   const x=lerp(start.x,f.x,e),y=lerp(start.y,f.y,e);
   const rot=(1-e)*start.r,sc=lerp(start.s,1.08,e);
   // Two purposeful smear exposures during fast travel.
   if(p>.08&&p<.6){glyphAt(i,lerp(start.x,f.x,Math.max(0,e-.10)),lerp(start.y,f.y,Math.max(0,e-.10)),sc,rot,.10,C.cyan)}
   glyphAt(i,x,y,sc,rot,1);
  }
  const a=art.english,p=range(u,.56,1.05);
  img('english',960+(a.x+a.w/2-800)*1.08,535+(a.y+a.h/2-400)*1.08+40*(1-ease(p)),1.08,0,ease(p));
 });
 cornerMarks(t,.35*ease(range(u,.7,1.3)));
}

function hero(t){
 fill(C.paper);const u=t-5.05;
 // Large off-canvas geometry frames the logo, keeping its interior quiet.
 layer(()=>{ctx.globalAlpha=.65;arc(-120,1130,580,-1.6,-.05,C.ice,85);arc(2050,-90,530,.2,3.05,C.ice,65)});
 const settle=Math.exp(-u*5)*Math.sin(u*9)*.012,s=1.08+settle;
 // One crisp offset, rather than a soft drop shadow, keeps the graphic flat.
 for(let j=0;j<8;j++){let p=glyphFinal(j,s);glyphAt(j,p.x+4,p.y+6,s,0,.12,C.ink)}
 drawLogo(960,535,s);
 const p=range(t,5.05,5.8),a=-.8+u*.13;
 layer(()=>{ctx.globalAlpha=.75*ease(p);arc(960,535,755,a,a+.32,C.blue,3);arc(960,535,755,a+Math.PI,a+Math.PI+.22,C.cyan,8)});
 star(327,243,32,C.cyan,-.15+Math.sin(u*.9)*.08);star(1623,792,27,C.blue,.3+Math.sin(u)*.1);star(1515,206,14,C.cyan,.4);
 tile(216,714,17,.4,C.blue);tile(1672,470,14,-.2,C.cyan,true);
 cornerMarks(t,.65);
 // Final 1.4 seconds deliberately settle into an editorially usable title hold.
}

function op(t){
 if(t<.72)prologue(t);else if(t<1.45)panels(t);else if(t<2.55)tunnel(t);else if(t<3.65)orbit(t);else if(t<5.05)assemble(t);else hero(t);
}

function eyePose(i,t,resume){
 const homes=[[805,386],[1110,386],[805,664],[1110,664]];
 // Each letter has its own uninterrupted curved flight. No card or clipping plane.
 const paths=resume?[
  [[-230,750],[180,970],[920,790]],
  [[2150,820],[1750,1120],[1010,790]],
  [[160,-240],[60,170],[550,820]],
  [[1810,-240],[1920,180],[1390,820]]
 ]:[
  [[-260,130],[240,-210],[1015,100]],
  [[2180,160],[1730,-190],[930,70]],
  [[-260,1100],[110,1380],[1000,980]],
  [[2190,1160],[1760,1380],[920,1020]]
 ];
 const start=.54+i*.075,travel=.82,p=range(t,start,start+travel),q=smooth(p);
 const [a,b,c]=paths[i],d=homes[i],v=1-q;
 let x=v*v*v*a[0]+3*v*v*q*b[0]+3*v*q*q*c[0]+q*q*q*d[0];
 let y=v*v*v*a[1]+3*v*v*q*b[1]+3*v*q*q*c[1]+q*q*q*d[1];
 const dx=3*v*v*(b[0]-a[0])+6*v*q*(c[0]-b[0])+3*q*q*(d[0]-c[0]);
 const dy=3*v*v*(b[1]-a[1])+6*v*q*(c[1]-b[1])+3*q*q*(d[1]-c[1]);
 const after=t-start-travel;
 let settle=0;
 if(after>0&&after<.46){settle=Math.sin(after*22)*Math.exp(-after*13);const n=Math.hypot(d[0]-c[0],d[1]-c[1]);x+=(d[0]-c[0])/n*13*settle;y+=(d[1]-c[1])/n*13*settle}
 const energy=Math.sin(Math.PI*p),turn=(i%2?1:-1)*(resume?-1:1);
 return{x,y,p,angle:Math.atan2(dy,dx),rotation:turn*(.23*energy-.035*settle),stretch:.17*energy*energy-.025*settle,size:(i===0?.92:i===1?.99:i===2?.98:1)*(.94+.06*smooth(p)),visible:t>start};
}

function drawFlyingEye(i,pose,resume,scale,alpha,tint){
 if(!pose.visible||alpha<=0)return;
 layer(()=>{
  ctx.translate(960+(pose.x-960)*scale,540+(pose.y-540)*scale);
  ctx.rotate(pose.angle);ctx.scale(1+pose.stretch,1/(1+pose.stretch*.64));ctx.rotate(-pose.angle+pose.rotation);
  img('eye-'+i,0,0,pose.size*scale,0,alpha,tint||(resume?C.white:undefined));
 });
}

function eyeText(t,resume,scale=1,opacity=1){
 for(let i=0;i<4;i++){
  const pose=eyePose(i,t,resume),energy=Math.sin(Math.PI*pose.p);
  // The only smear is the letter's own silhouette; empty space stays transparent.
  if(pose.p>.12&&pose.p<.91){
   drawFlyingEye(i,eyePose(i,t-.040,resume),resume,scale,opacity*.055*energy,resume?C.ice:C.cyan);
   drawFlyingEye(i,eyePose(i,t-.018,resume),resume,scale,opacity*.12*energy,resume?C.ice:C.cyan);
  }
  drawFlyingEye(i,pose,resume,scale,opacity);
 }
}

function eye(t,resume){
 const main=resume?C.white:C.blue,bg=resume?C.blue:C.paper;
 fill(bg);
 const dir=resume?-1:1;
 if(t<.65){
  if(resume){
   fill(C.night);let p=expo(range(t,0,.65));circle(960,540,1400*smooth(range(t,.06,.64)),C.blue);star(960,540,1250*p,C.blue,.2+t*.5);star(960,540,18+450*p,C.cyan,.2-t);star(960,540,350*p,C.blue,.2+t*.5);
  }else{
   const p=expo(range(t,0,.48));polygon([[-500+2400*p,0],[150+2400*p,0],[-350+2400*p,H],[-1000+2400*p,H]],C.blue);
   line(0,1060-t*1400,1920,100-t*1400,C.cyan,7);
  }
 }
 if(t>=.48){
  const p=range(t,.48,1.38),e=expo(p),radius=lerp(900,367,e),spin=(1-e)*dir*1.4;
  layer(()=>{ctx.translate(960,540);ctx.rotate(spin);
   for(let i=0;i<4;i++){
    const a=i*Math.PI/2+.12;
    arc(0,0,radius,a,a+Math.PI*.5-.17,main,14);
    arc(0,0,radius+32,a+.05,a+.97,resume?C.cyan:C.ice,5);
   }
   ticks(0,0,radius+59,-spin*.5,main,.5*ease(p));
  });
  let endScale=1,endAlpha=1;
  if(t>3.25){const q=range(t,3.25,4);endScale=resume?1+expo(q)*4.5:1-expo(q);endAlpha=1-ease(range(t,3.25,3.7));}
  eyeText(t,resume,endScale,endAlpha);
  layer(()=>{ctx.globalAlpha=ease(range(t,1.45,1.95))*(t>3.25?1-ease(range(t,3.25,3.6)):1);
   star(493,540,24,resume?C.ice:C.cyan,.2);star(1427,540,24,main,.2);
   const a=.12+(t-1.6)*.055;arc(960,540,452,a,a+.29,resume?C.ice:C.blue,10);arc(960,540,452,a+Math.PI,a+Math.PI+.16,resume?C.ice:C.cyan,6);
  });
  if(t>3.25){const q=range(t,3.25,4);
   if(resume){circle(960,540,1135*smooth(q),C.paper);star(960,540,38*(1-ease(q)),C.blue,q)}
   else{layer(()=>{ctx.fillStyle=C.night;ctx.beginPath();ctx.rect(0,0,W,H);ctx.arc(960,540,1420*(1-expo(q)),0,TAU,true);ctx.fill('evenodd')});star(960,540,18*ease(range(t,3.55,3.9)),C.cyan,.2)}
  }
 }
}

function drawOutlined(name,x,y,s,rotation,alpha){
 if(alpha<=0||s<=0)return;const a=outlines[name];
 layer(()=>{ctx.translate(x,y);ctx.rotate(rotation);ctx.globalAlpha=alpha;ctx.drawImage(a.image,-a.w*s/2,-a.h*s/2,a.w*s,a.h*s)});
}

function overlay(t){
 ctx.clearRect(0,0,W,H);
 ringOverlayDrawing=true;
 // Reuse the FIRST design's ring/orbit/assembly choreography, without its matte
 // or unrelated full-screen cuts. Extend that exact visual idea with an exit.
 if(t<.70)layer(()=>{ctx.globalAlpha=ease(range(t,0,.08))*(1-smooth(range(t,.43,.70)));prologue(t)});
 if(t>=.38&&t<1.15)layer(()=>{ctx.globalAlpha=smooth(range(t,.38,.68));orbit(2.55+range(t,.38,1.15)*1.10)});
 if(t>=1.15&&t<2.55){
  ringBackdrop(t,1-smooth(range(t,1.15,2.20))*.60);
  assemble(3.65+t-1.15);
 }
 if(t>=2.55&&t<3.55){ringBackdrop(t,.40);drawLogo(960,535,1.08)}
 if(t>=3.55&&t<4.96){
  const unfold=range(t,3.55,4.12),collapse=1-smooth(range(t,4.12,4.92));
  ringBackdrop(t,.40+.60*smooth(unfold),collapse);
  for(let i=0;i<8;i++){
   const p=range(t,3.55+i*.016,4.01+i*.016),e=smooth(p),home=glyphFinal(i,1.08),end=orbitPose(i,1.1+unfold*.30);
   const bend=Math.sin(e*Math.PI)*42*(i%2?1:-1);
   const x=960+(lerp(home.x,end.x,e)-960)*collapse,y=535+(lerp(home.y,end.y,e)-535+bend)*collapse;
   glyphAt(i,x,y,lerp(1.08,end.s,e)*collapse,end.r*e,1-smooth(range(t,4.58,4.88)));
  }
  const a=art.english,fade=1-smooth(range(t,3.55,3.92));
  img('english',960+(a.x+a.w/2-800)*1.08,535+(a.y+a.h/2-400)*1.08+22*(1-fade),1.08,0,fade);
  if(t>4.39)layer(()=>{ctx.globalAlpha=smooth(range(t,4.39,4.57))*(1-smooth(range(t,4.77,4.96)));star(960,535,18,C.cyan,.2)});
 }
 ringOverlayDrawing=false;
}

function ringBackdrop(t,opacity=1,scale=1){
 if(scale<=0)return;layer(()=>{ctx.globalAlpha=opacity;ctx.translate(960,540);ctx.rotate(-.102+(t-1.15)*.035);ctx.scale(scale,scale*.48);circle(0,0,470,C.blue,4);arc(0,0,570,.2+(t-1.15)*.10,.2+(t-1.15)*.10+TAU*.65,C.cyan,3);circle(0,0,700,C.ice,1.5)});
}

function render(kind,t,width=1920,height=1080){
 if(canvas.width!==width||canvas.height!==height){canvas.width=width;canvas.height=height}
 ctx.setTransform(width/W,0,0,height/H,0,0);ctx.globalAlpha=1;ctx.imageSmoothingEnabled=true;ctx.imageSmoothingQuality='high';
 if(kind==='overlay')overlay(t);else if(kind==='op')op(t);else eye(t,kind==='resume');
}
ready=(async()=>{
 art=await(await fetch('assets/manifest.json')).json();
 for(const [name,a] of Object.entries(art)){
  const image=new Image();image.src=a.src;await image.decode();sprites[name]=image;
  for(const tint of [C.white,C.blue,C.cyan,C.ink,C.ice]){const off=document.createElement('canvas');off.width=image.width;off.height=image.height;const c=off.getContext('2d');c.drawImage(image,0,0);c.globalCompositeOperation='source-in';c.fillStyle=tint;c.fillRect(0,0,off.width,off.height);sprites[name+'@'+tint]=off}
  if(name.startsWith('glyph-')||name==='english'){
   const pad=name==='english'?7:20,r=name==='english'?3:13,off=document.createElement('canvas');off.width=image.width+pad*2;off.height=image.height+pad*2;
   const c=off.getContext('2d');for(let j=0;j<40;j++){const a=j*TAU/40;c.drawImage(image,pad+Math.cos(a)*r,pad+Math.sin(a)*r)}
   c.globalCompositeOperation='source-in';c.fillStyle='#FFFFFF';c.fillRect(0,0,off.width,off.height);c.globalCompositeOperation='source-over';c.drawImage(image,pad,pad);
   outlines[name]={image:off,w:a.w+pad,h:a.h+pad};
  }
 }
 render('op',7);return true;
})();
window.film={ready,render,duration,canvas};
