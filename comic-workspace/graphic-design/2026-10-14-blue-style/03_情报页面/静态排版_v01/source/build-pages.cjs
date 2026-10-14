const fs=require('fs'),path=require('path');
const sharp=require('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const R=path.dirname(__dirname),out=path.join(R,'assets');
const F=JSON.parse(fs.readFileSync(path.join(__dirname,'text-outlines.json'),'utf8').replace(/^\uFEFF/,''));
const C={blue:'#216AE1',sky:'#25A9E4',navy:'#173B80',white:'#FFFFFF'};
const logoPath=path.join(R,'../../01_当前定稿/01_OP标题_v13_白底4K60帧/assets/title-final-transparent.svg');
const logo=fs.readFileSync(logoPath,'utf8').replace(/^<svg[^>]*>/,'').replace(/<\/svg>\s*$/,'').replace(/<title>[\s\S]*?<\/title>/,'');
const widths=[];
const wrap=(content,transform)=>`<g transform="${transform}">${content}</g>`;
function text(s,x,y,size=38,font='body',color=C.navy,angle=0){
 const v=F[font][s];if(!v)throw Error('Missing outline: '+s);
 widths.push({text:s,font,size,width:v.w*size/100,x,y,angle});
 return wrap(`<path d="${v.d}" fill="${color}"/>`,`translate(${x} ${y}) rotate(${angle}) scale(${size/100}) translate(${-v.x} ${-v.y})`);
}
const line=(d,color=C.blue,width=5)=>`<path d="${d}" fill="none" stroke="${color}" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round"/>`;
function header(){
 const title='现在可以公开的情报',angles=[-4,-1,3,-3,2,-2,2,-3,2],sizes=[1.06,.96,1.05,.96,1.05,1.04,.88,1.06,1];
 let s=text('FIELD NOTES',124,75,19,'latin',C.navy);
 [...title].forEach((ch,i)=>{
  const original=F.heavy[ch].d,v=F.heavy[ch];
  const tokens=original.match(/[MLCZ]|-?(?:\d+\.?\d*|\.\d+)/g);let j=0,d='';
  while(j<tokens.length){const cmd=tokens[j++];d+=cmd;if(cmd==='Z')continue;for(let k=0;k<(cmd==='C'?3:1);k++){const x=+tokens[j++],y=+tokens[j++],dx=x-v.x-v.w/2,dy=y-v.y-v.h/2;d+=(x+((i%2)?-.045:.045)*dy).toFixed(3)+','+(y-.05*dx+.0007*dx*dx).toFixed(3)+' ';}}
  v.d=d;s+=text(ch,124+i*111,125+3*Math.cos(i*.8),105*sizes[i],'heavy',[4,5].includes(i)?C.sky:C.blue,angles[i]);v.d=original;
 });
 s+='<path d="M125,248 Q628,233 1129,248 L1127,256 Q634,245 122,255Z" fill="#216AE1"/>'+line('M132,264 Q600,253 1033,261',C.sky,2.5);
 s+=`<svg x="1455" y="54" width="350" height="175" viewBox="0 0 1600 800">${logo}</svg>`;
 return s;
}
function footer(record,index){
 return line('M122,953 Q856,949 1799,956',C.navy,2)+text(record,124,987,19,'latin',C.navy)+text(index,1748,976,38,'latin',C.blue);
}
function ticket(){
 let s='<path d="M20,6 L642,-4 L653,111 Q626,127 654,143 L663,398 L23,413 L12,303 Q39,289 12,272Z" fill="white" stroke="#216AE1" stroke-width="7" stroke-linejoin="round"/>';
 s+=line('M48,117 Q320,106 621,113',C.sky,3)+line('M50,361 L617,350',C.blue,2);
 s+=text('善行收集',60,35,58,'heavy',C.blue);
 for(let i=0;i<4;i++){
  const x=111+i*146;s+=`<rect x="${x-57}" y="162" width="114" height="150" rx="4" fill="none" stroke="${C.navy}" stroke-width="2.5"/>`;
  const a=i===3?0:-8+i*5;
  let stamp=`<circle cx="0" cy="0" r="42" fill="none" stroke="${i===3?C.sky:C.blue}" stroke-width="5"/>`;
  if(i<3)stamp+=line('M-23,0 L-6,17 L25,-19',C.blue,9);
  s+=wrap(stamp,`translate(${x} 233) rotate(${a})`);
 }
 s+=text('第四栏 · 待确认',316,324,24,'note',C.navy);
 return wrap(s,'translate(175 387) rotate(-5 332 207)');
}
function sword(){
 const shape='<path d="M-31,-205 L4,-262 L37,-205 L24,85 L-24,85Z" fill="#216AE1"/><path d="M4,-225 L8,73 L-7,72 L-9,-199Z" fill="#25A9E4"/><path d="M-74,72 Q0,50 74,73 L65,94 L-64,94Z" fill="#173B80"/><path d="M-20,94 L22,94 L16,194 L-13,194Z" fill="#216AE1"/><path d="M-26,190 L31,189 L23,218 L-23,220Z" fill="#173B80"/>';
 return line('M1230,460 C1201,349 1417,296 1559,387 C1743,505 1692,785 1501,838',C.sky,4)+wrap(shape,'translate(1430 610) rotate(-30)')+wrap(shape,'translate(1510 610) rotate(32)')+line('M1283,809 Q1462,848 1677,802',C.blue,7);
}
function bottle(){
 let s='<path d="M-99,-214 L91,-219 L99,-158 L-95,-153Z" fill="#173B80"/><path d="M-66,-152 L64,-152 L66,-78 Q160,-37 161,58 L158,245 Q152,286 105,292 L-101,296 Q-149,290 -155,245 L-161,61 Q-160,-34 -66,-78Z" fill="white" stroke="#216AE1" stroke-width="8" stroke-linejoin="round"/><path d="M-147,71 Q-87,100 -13,71 T148,66 L146,243 Q138,279 103,280 L-96,283 Q-137,278 -143,241Z" fill="#25A9E4"/><path d="M-142,172 Q-72,147 5,174 T147,161 L145,244 Q134,275 101,280 L-96,283 Q-132,277 -141,238Z" fill="#216AE1"/><path d="M-114,-7 Q-134,33 -132,88" fill="none" stroke="#173B80" stroke-width="5" stroke-linecap="round"/>';
 s+='<circle cx="-83" cy="128" r="11" fill="white"/><circle cx="32" cy="98" r="7" fill="white"/><circle cx="91" cy="132" r="15" fill="white"/>';
 s+=text('醒酒药',-102,206,47,'heavy',C.white);
 return wrap(s,'translate(488 571) rotate(-8)');
}
function pageA(){let s=header()+ticket();
 s+=text('善行收集券',980,342,73,'heavy',C.blue,-1);
 ['两名男子需要各自完成四次善行，','才被妻子允许彻夜不归。','纸券上的第四栏，正等待确认。','而少女误会了他们所说的“回报”。'].forEach((v,i)=>s+=text(v,982,504+i*65,38,'body'));
 s+=line('M983,806 Q1288,795 1695,806',C.sky,4)+text('集齐四次，获得彻夜不归的许可。',984,837,31,'note',C.blue);
 return s+footer('RECORD 001  /  GOOD DEEDS','01');}
function pageB(){let s=header();
 s+=text('魔物猎手',126,351,81,'heavy',C.blue,-1.5)+text('一条来自酒馆的求职建议。',128,456,33,'note',C.sky);
 ['少女在酒馆寻找佣兵或守卫工作时，','一位兜帽男子建议她试试魔物猎手。','他称，这是一份荣耀的工作，','只要具备能打的本事，便可以尝试。'].forEach((v,i)=>s+=text(v,130,545+i*62,41,'body'));
 s+=text('新的求职方向，就此出现。',131,841,35,'note',C.blue)+sword();
 return s+footer('RECORD 002  /  MONSTER HUNTER','02');}
function pageC(){let s=header()+bottle();
 s+=text('醒酒药',907,338,83,'heavy',C.blue,-1)+text('被误解的善意。',908,441,33,'note',C.sky);
 const rows=[['来源','高个男子自制'],['服用后','头痛与宿醉消失'],['相关事件','一场关于“报答”的误会']];
 rows.forEach(([label,value],i)=>{const y=546+i*104;s+=text(label,908,y,32,'heavy',C.blue);s+=text(value,1150,y+1,37,'body');s+=line(`M908,${y+66} Q1283,${y+62} 1782,${y+66}`,C.sky,1.5)});
 return s+footer('RECORD 003  /  HANGOVER CURE','03');}
const specs=[['01_图文主版_善行收集券',pageA,'图文主版 · 善行收集券'],['02_文字版_魔物猎手',pageB,'文字版 · 魔物猎手'],['03_条目版_醒酒药',pageC,'条目版 · 醒酒药']];
async function main(){
 for(const [name,draw,title] of specs){const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080"><title>${title}</title><rect width="1920" height="1080" fill="white"/>${draw()}</svg>`;
  fs.writeFileSync(path.join(out,name+'.svg'),svg);
  await sharp(Buffer.from(svg)).png().toFile(path.join(out,name+'_1080.png'));
  await sharp(Buffer.from(svg),{density:144}).png().toFile(path.join(out,name+'_4K.png'));
 }
 for(const v of widths)if(v.x>=0&&v.x+v.width>1815&&v.angle===0)throw Error('Text crosses safe margin: '+v.text);
 fs.writeFileSync(path.join(__dirname,'text-widths.json'),JSON.stringify(widths,null,2));
 const tiles=await Promise.all(specs.map(async([name],i)=>({input:await sharp(path.join(out,name+'_1080.png')).resize(960,540).png().toBuffer(),left:0,top:i*558})));
 await sharp({create:{width:960,height:1656,channels:4,background:'#eef3fc'}}).composite(tiles).png().toFile(path.join(out,'三版排版总览.png'));
 const html=`<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>现在可以公开的情报 · 静态排版</title><style>*{box-sizing:border-box}body{margin:0;background:#f4f7fc;color:#173b80;font-family:"Microsoft YaHei",sans-serif}main{max-width:1440px;margin:auto;padding:30px 24px 70px}h1{font-size:24px;margin:0 0 12px}p{font-size:14px;line-height:1.8;max-width:970px;margin:0 0 22px}nav{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px}button{font:inherit;border:1px solid #173b80;background:white;color:#173b80;padding:10px 18px;cursor:pointer}button[aria-pressed=true]{color:white;background:#173b80}.frame{background:white}#design{display:block;width:100%;aspect-ratio:16/9;border:1px solid #dce4ef}footer{display:flex;gap:22px;margin-top:20px;flex-wrap:wrap}a{color:#173b80}.all{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:44px}.all img{width:100%;display:block}.all p{margin:8px 0;font-size:13px}figure{margin:0}@media(max-width:700px){.all{grid-template-columns:1fr}}</style><main><h1>现在可以公开的情报 · 静态排版</h1><p>沿用标题与中插的白底、蓝色和艺术字。先看三种内容排版：图文主版、文字版、条目版。本轮为静态设计。文案是取自第一集工作稿的排版示例，插图是代码绘制的示意图。</p><nav>${specs.map(([n,,title],i)=>`<button data-index="${i}" aria-pressed="${i===0}">${title}</button>`).join('')}</nav><div class="frame"><img id="design" src="assets/${specs[0][0]}_1080.png" alt="${specs[0][2]}"></div><footer><a id="png" href="assets/${specs[0][0]}_4K.png" download>下载 4K 静态图</a><a id="svg" href="assets/${specs[0][0]}.svg" download>下载矢量图</a><a href="../../index.html">返回平面素材目录</a></footer><div class="all">${specs.map(([n,,title],i)=>`<figure><a href="#" data-select="${i}"><img src="assets/${n}_1080.png" alt="${title}"></a><p>${title}</p></figure>`).join('')}</div></main><script>const specs=${JSON.stringify(specs.map(([n,,title])=>({name:n,title})))};function select(i){const s=specs[i],img=document.getElementById('design');img.src='assets/'+s.name+'_1080.png';img.alt=s.title;document.getElementById('png').href='assets/'+s.name+'_4K.png';document.getElementById('svg').href='assets/'+s.name+'.svg';document.querySelectorAll('[data-index]').forEach(b=>b.setAttribute('aria-pressed',String(+b.dataset.index===i)))}document.querySelectorAll('[data-index]').forEach(b=>b.onclick=()=>select(+b.dataset.index));document.querySelectorAll('[data-select]').forEach(b=>b.onclick=e=>{e.preventDefault();select(+b.dataset.select);document.getElementById('design').scrollIntoView({behavior:'smooth'})});window.PAGE_DESIGNS=specs;</script></html>`;
 fs.writeFileSync(path.join(R,'preview.html'),html);console.log('Three static code-drawn pages, 1080p / 4K / vector, ready');
}
main().catch(e=>{console.error(e);process.exitCode=1});
