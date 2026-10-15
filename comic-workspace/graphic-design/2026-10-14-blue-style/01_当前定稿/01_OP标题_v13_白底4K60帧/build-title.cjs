// Code-drawn anime lettering: explicit custom strokes plus controlled outline deformation.
const fs=require('fs'),path=require('path');
const sharp=require('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const R=__dirname,A=path.join(R,'assets');fs.mkdirSync(A,{recursive:true});
const fontFile=path.join(R,'glyphs.json');
if(!fs.existsSync(fontFile))fs.copyFileSync(path.join(R,'../dungeon-design-v4-glyph-fusion/glyphs.json'),fontFile);
const F=JSON.parse(fs.readFileSync(fontFile,'utf8').replace(/^\uFEFF/,''));
const C={royal:'#216AE1',sky:'#25A9E4',navy:'#173B80',paper:'#FFFFFF',white:'#FFFFFF'};
const n=v=>+v.toFixed(3);
const p=(d,c)=>`<path d="${d}" fill="${c}" fill-rule="nonzero"/>`;
const g=(s,t='')=>`<g transform="${t}">${s}</g>`;
const rect=(x,y,w,h,c)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${c}"/>`;
const parts=ch=>F.heavy[ch].d.match(/M[^M]+/g);
// Modify outline control points coherently. Apply the same map to counters and outer contours.
function deform(d,ch){
 const settings={'新':[-.06,-.07,.0008],'界':[.08,.09,.0008],'之':[-.07,-.1,.001],'魔':[-.055,-.065,.001],'物':[.045,-.05,.0005],'猎':[-.02,-.045,.0006]};
 const [shear,rise,bow]=settings[ch]||[0,0,0];
 const tokens=d.match(/[MLCQZ]|-?(?:\d+\.?\d*|\.\d+)/g);let i=0,result='';
 while(i<tokens.length){const cmd=tokens[i++];result+=cmd;if(cmd==='Z')continue;const count=cmd==='C'?3:cmd==='Q'?2:1;for(let j=0;j<count;j++){const x=+tokens[i++],y=+tokens[i++];const xx=x+shear*(y-78)+bow*(x-50)*(y-78);const yy=y+rise*(x-50)+bow*(x-50)**2;result+=`${n(xx)},${n(yy)} `;}}
 return result;
}
const outlines={};
outlines['新']=deform(F.heavy['新'].d,'新');
// 世: three independently drawn, tapered stroke bodies; stepped rising feet.
outlines['世']='M-2,55 L97,50 L101,65 L-4,72 Z M13,35 L31,31 L30,104 L98,102 L96,124 L9,119 Z M40,28 L57,31 L58,79 L72,77 L67,26 L85,24 L91,93 L43,99 Z';
const world=parts('界');
world[0]='M28,61 L29,68 L73,68 L72,58 Z';
world[1]='M28,46 L29,52 L70,51 L71,43 Z';
world[2]='M12,36 L88,30 L90,80 L14,75 Z';
world[6]='M42,38 L59,37 L57,75 L44,76 Z';
world[7]='M58,90 L75,87 L79,128 L58,124 Z';
outlines['界']=deform(world.join(''),'界');
const of=parts('之');of[0]='M6,50 L83,45 L85,61 L9,64 Z';
outlines['之']=deform(of.join('')+'M70,111 Q90,110 108,101 L98,123 L69,124 Z','之');
const magic=parts('魔');
magic[0]='M23,51 L59,49 L59,61 L24,59 Z';
magic[1]='M60,50 L99,53 L95,63 L60,60 Z';
// Roof, left enclosure and upper dot stay recognizable but stop being parallel blocks.
magic[15]='M15,38 L102,34 L98,49 L16,47 Z';
magic[17]='M44,31 L60,28 Q65,35 66,43 L49,45 Q48,37 44,31 Z';
outlines['魔']=deform(magic.join(''),'魔');
// 物: remove every contour belonging to 牜, retain 勿, replace the radical with a drawn ♀.
// Transform 牜 in place: its original centre stem and diagonal second bar remain.
// Only the upper pair of strokes closes into a circular head, in the same radical column.
const female='M44.15,51.7 A17.8,17.8 0 1 1 8.55,51.7 A17.8,17.8 0 1 1 44.15,51.7 Z M35.45,51.7 A9.1,9.1 0 1 0 17.25,51.7 A9.1,9.1 0 1 0 35.45,51.7 Z M19.7,65 L33,65 L33,125.516 L19.7,125.516 Z'+parts('物')[5];
const matter=parts('物').slice(0,5);matter[2]='M54,45 L92,43 L91,58 L48,61 Z';
outlines['物']=deform(matter.join(''),'物');
function matterShape(){return p(outlines['物'],C.sky)+p(female,C.sky);}
// 猎: preserve B's genuinely round ring, add a crossbar inside the circle.
const hunter=parts('猎');
hunter[0]='M39,43 L90,40 L91,53 L38,56 Z';
hunter[1]='M37,62 L87,60 L89,74 L37,76 Z';
hunter[2]='M46,32 L59,32 L61,69 L48,70 Z';
hunter[3]='M68,30 L81,31 L84,68 L71,68 Z';
// 日 occupies x43.6..91.7, y78.4..125.4 in the original. Keep the new ring in that cell.
// The short arrow reuses the far-right end of the upper horizontal, rather than reaching into 手.
const male='M94,102.2 A25,25 0 1 1 44,102.2 A25,25 0 1 1 94,102.2 Z M83.5,102.2 A14.5,14.5 0 1 0 54.5,102.2 A14.5,14.5 0 1 0 83.5,102.2 Z M80,81 L91,70 L84,70 L84,61 L104,61 L104,81 L95,81 L95,77 L87,87 Z';
const hunterLeft=deform(hunter.slice(7).join(''),'猎');
const hunterTop=hunter.slice(0,4).join('');
outlines['猎']=hunterLeft;
function hunterShape(){
 const top=g(p(hunterTop,C.royal),'translate(38 74) skewX(6) scale(.94 .91) translate(-38 -74)');
 const symbol=p(male,C.sky);
 const bar=`<path d="M53,97.7 L85,97.7 L85,106.7 L53,106.7 Z" fill="${C.royal}" clip-path="url(#male-counter)"/>`;
 return p(hunterLeft,C.royal)+top+symbol+bar;
}
// Restore the hand's original customized vertical hook; no bead chain.
outlines['手']='M10,39 Q55,38 83,26 L97,39 Q59,56 12,58 Z M9,64 L96,56 L99,73 L8,80 Z M-5,90 Q43,78 108,84 L103,103 Q46,95 -3,107 Z M40,46 L58,44 L62,108 Q62,128 28,130 L18,112 Q45,116 45,106 Z';
function handShape(c){return p(outlines['手'],c);}
function letter(ch,x,y,scale,c,angle){const shape=ch==='物'?matterShape():ch==='猎'?hunterShape():ch==='手'?handShape(c):p(outlines[ch],c);return g(shape,`translate(${x} ${y}) rotate(${angle}) scale(${scale}) translate(0 -30)`);}
function text(s,x,y,size,c,font='sans',tracking=0,wordExtra=0){let result='';const top=F[font]['H'].y;for(const ch of s){const v=F[font][ch];result+=g(p(v.d,c),`translate(${n(x)} ${n(y-top*size/100)}) scale(${size/100})`);x+=v.w*size/100+tracking+(ch===' '?wordExtra:0);}return result;}
const definitions=`<defs><clipPath id="male-counter"><circle cx="69" cy="102.2" r="14.5"/></clipPath><filter id="white-edge" x="-15%" y="-20%" width="130%" height="140%" color-interpolation-filters="sRGB"><feMorphology in="SourceAlpha" operator="dilate" radius="11" result="edge"/><feFlood flood-color="white"/><feComposite in2="edge" operator="in"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>`;
// Circular baseline with individually rotated glyph paths; letters retain their original aspect ratio.
function archedEnglish(){
 const line='WHAT HAPPENS IN DUNGEON',size=35,wordExtra=14,width=1190,left=177;
 const naturalWidth=[...line].reduce((v,c)=>v+F.sans[c].w*size/100+(c===' '?wordExtra:0),0);
 const tracking=(width-naturalWidth)/([...line].length-1),mid=left+width/2,half=width/2,sag=53;
 const radius=(half*half+sag*sag)/(2*sag),top=649;
 const reference=F.sans.H;let cursor=left,result='';
 for(const ch of line){const v=F.sans[ch],advance=v.w*size/100,x=cursor+advance/2,dx=x-mid;
  const height=radius-Math.sqrt(radius*radius-dx*dx),angle=Math.atan2(dx,Math.sqrt(radius*radius-dx*dx))*180/Math.PI;
  if(v.d)result+=g(p(v.d,C.navy),`translate(${n(x)} ${n(top+height+reference.h*size/200)}) rotate(${n(angle)}) scale(${size/100}) translate(${-v.w/2} ${-reference.y-reference.h/2})`);
  cursor+=advance+tracking+(ch===' '?wordExtra:0);
 }
 return `<g aria-label="What Happens in Dungeon">${result}</g>`;
}
const letters=[
 {ch:'新',x:402,y:205,scale:1.30,c:C.navy,angle:-17},
 {ch:'世',x:551,y:123,scale:2.02,c:C.royal,angle:-10},
 {ch:'界',x:788,y:85,scale:2.27,c:C.sky,angle:8},
 {ch:'之',x:1018,y:197,scale:1.29,c:C.navy,angle:17},
 {ch:'魔',x:145,y:329,scale:3.10,c:C.royal,angle:-8},
 {ch:'物',x:480,y:305,scale:2.87,c:C.sky,angle:5},
 {ch:'猎',x:789,y:328,scale:2.77,c:C.royal,angle:-5},
 {ch:'手',x:1128,y:290,scale:3.03,c:C.navy,angle:12}
];
function title(){let s=letters.map(v=>letter(v.ch,v.x,v.y,v.scale,v.c,v.angle)).join('');
 const english=archedEnglish();
 return `<g id="title-logo" aria-label="新世界之魔物猎手 / What Happens in Dungeon"><g filter="url(#white-edge)">${s}</g>${english}</g>`;
}
const svg=(s,title,w,h)=>`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img"><title>${title}</title>${definitions}${s}</svg>`;
async function save(name,s,title,w,h){const data=svg(s,title,w,h);fs.writeFileSync(path.join(A,name+'.svg'),data);await sharp(Buffer.from(data)).png().toFile(path.join(A,name+'.png'));}
async function main(){
 const previous=JSON.parse(fs.readFileSync(path.join(R,'layout-assets.json'),'utf8'));
 if(!process.argv.includes('--sprites-only')){
 await save('title-final-transparent',title(),'新世界之魔物猎手 · 动画标题定稿',1600,800);
 await save('title-final',rect(0,0,1920,1080,C.paper)+g(title(),'translate(160 140)'),'新世界之魔物猎手 · 定稿预览',1920,1080);
 await sharp(Buffer.from(svg(rect(0,0,1920,1080,C.paper)+g(title(),'translate(160 140)'),'4K title',1920,1080)),{density:144}).png().toFile(path.join(A,'title-final-4k.png'));
 }
 // Large fixed transparent frames preserve exactly the settled layout. Trim into efficient sprites.
 const sprites=[];
 for(const [i,v] of letters.entries()){
  const old=previous.letters[i],frame={x:old.x-2,y:old.y-2,w:old.w+4,h:old.h+4};
  const crop=s=>svg(s,v.ch,frame.w,frame.h).replace(`viewBox="0 0 ${frame.w} ${frame.h}"`,`viewBox="${frame.x-160} ${frame.y-140} ${frame.w} ${frame.h}"`);
  const inkSvg=crop(letter(v.ch,v.x,v.y,v.scale,v.c,v.angle));
  const drawing=crop(`<g filter="url(#white-edge)">${letter(v.ch,v.x,v.y,v.scale,v.c,v.angle)}</g>`);
  // Rasterize original vector paths at four times the layout resolution.
  const data=await sharp(Buffer.from(drawing),{density:288}).png().toBuffer();
  const {data:trimmed,info}=await sharp(data).png().toBuffer({resolveWithObject:true});
  fs.writeFileSync(path.join(A,'glyph-'+i+'.png'),trimmed);
  const raw=await sharp(trimmed).ensureAlpha().raw().toBuffer();for(let k=0;k<raw.length;k+=4)raw[k]=raw[k+1]=raw[k+2]=255;
  await sharp(raw,{raw:{width:info.width,height:info.height,channels:4}}).png().toFile(path.join(A,'edge-'+i+'.png'));
  await sharp(Buffer.from(inkSvg),{density:288}).png().toFile(path.join(A,'ink-'+i+'.png'));
  sprites.push({ch:v.ch,file:'assets/glyph-'+i+'.png',ink:'assets/ink-'+i+'.png',edge:'assets/edge-'+i+'.png',...frame});
  console.log('4x vector texture',v.ch,info.width,info.height);
 }
 const {data:eng,info:engInfo}=await sharp(Buffer.from(svg(archedEnglish(),'English',1600,800)),{density:288}).trim({threshold:1}).png().toBuffer({resolveWithObject:true});
 fs.writeFileSync(path.join(A,'english.png'),eng);
 fs.writeFileSync(path.join(R,'animation-assets.json'),JSON.stringify({width:1920,height:1080,palette:C,letters:sprites,english:{file:'assets/english.png',x:160-engInfo.trimOffsetLeft/4,y:140-engInfo.trimOffsetTop/4,w:engInfo.width/4,h:engInfo.height/4}},null,2));
 fs.writeFileSync(path.join(R,'custom-outlines.json'),JSON.stringify({palette:C,outlines,female,male,hunterTop,hunterLeft},null,2));
 console.log('Rendered final title and animation sprites.');
}
main().catch(e=>{console.error(e);process.exitCode=1});
