const fs=require('fs'),path=require('path');
const sharp=require('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const R=__dirname,C={blue:'#216AE1',sky:'#25A9E4',navy:'#173B80',white:'#FFFFFF'};
const F=JSON.parse(fs.readFileSync(path.join(R,'lettering.json'),'utf8'));
const manifest=JSON.parse(fs.readFileSync(path.join(R,'animation-assets.json'),'utf8'));
const n=v=>Number(v.toFixed(3));
function transform(d,fn){const tokens=d.match(/[MLCQZ]|-?(?:\d+\.?\d*|\.\d+)/g);let i=0,result='';while(i<tokens.length){const cmd=tokens[i++];result+=cmd;if(cmd==='Z')continue;const count=cmd==='C'?3:cmd==='Q'?2:1;for(let j=0;j<count;j++){const [x,y]=fn(+tokens[i++],+tokens[i++]);result+=`${n(x)},${n(y)} `}}return result}
function ring(radius){let d='';for(let i=0;i<=144;i++){const a=-Math.PI/2+i/144*Math.PI*2,r=radius*(1+.0035*Math.sin(3*a+.4)+.002*Math.sin(7*a));d+=(i?'L':'M')+n(960+r*Math.cos(a))+','+n(532+r*Math.sin(a))}return d+'Z'}
function arcText(bottom){const line='WHAT HAPPENS IN DUNGEON',size=25,tracking=10,radius=414;
 const widths=[...line].map(c=>F[c].w*size/100),total=widths.reduce((a,b)=>a+b,0)+tracking*(line.length-1);let cursor=-total/2,d='';
 for(const [i,ch] of [...line].entries()){const v=F[ch],distance=cursor+widths[i]/2,theta=bottom?Math.PI/2-distance/radius:-Math.PI/2+distance/radius,angle=bottom?theta-Math.PI/2:theta+Math.PI/2;
  if(v.d)d+=transform(v.d,(x,y)=>{const xx=(x-v.w/2)*size/100,yy=(y-F.H.y-F.H.h/2)*size/100;return [960+radius*Math.cos(theta)+xx*Math.cos(angle)-yy*Math.sin(angle),532+radius*Math.sin(theta)+xx*Math.sin(angle)+yy*Math.cos(angle)]});cursor+=widths[i]+tracking;
 }return d}
const A={letters:manifest.letters.slice(4),layout:JSON.parse(fs.readFileSync(path.join(R,'layout.json'),'utf8')),outer:ring(450),inner:ring(380),english:arcText(false)+arcText(true)};
async function main(){
const source=fs.readFileSync(path.join(R,'assets','source-title.svg'),'utf8');
const defs=source.match(/<defs>[\s\S]*?<\/defs>/)[0];
const body=source.match(/<g filter="url\(#white-edge\)">([\s\S]*?)<\/g><g aria-label="What Happens in Dungeon">/)[1];
const groups=[];let depth=0,start=0;for(const m of body.matchAll(/<\/?g(?:\s[^>]*?)?>/g)){if(m[0].startsWith('</')){depth--;if(depth===0)groups.push(body.slice(start,m.index+m[0].length))}else{if(depth===0)start=m.index;depth++}}
if(groups.length!==8)throw Error('Expected eight separate source glyphs');
groups.splice(0,4);
for(const [i,v] of A.letters.entries()){
 const whiteSvg=`<svg xmlns="http://www.w3.org/2000/svg" width="${v.w}" height="${v.h}" viewBox="${v.x-160} ${v.y-140} ${v.w} ${v.h}">${defs}${groups[i].replace(/#[0-9A-Fa-f]{6}/g,C.white)}</svg>`;
 await sharp(Buffer.from(whiteSvg),{density:288}).png().toFile(path.join(R,'assets',`white-${i}.png`));
}
function mapped(i,monochrome=false,edge=false){const v=A.letters[i],q=A.layout[i];let s=groups[i];if(monochrome||edge)s=s.replace(/#[0-9A-Fa-f]{6}/g,C.white);if(edge)s=`<g filter="url(#white-edge)">${s}</g>`;return `<g transform="translate(${q.cx} ${q.cy}) rotate(${q.roll}) scale(${q.scale}) translate(${-v.x+160-v.w/2} ${-v.y+140-v.h/2})">${s}</g>`}
const star=(x,y,s,c)=>`<path d="M0,-1 Q.1,-.12 1,0 Q.1,.12 0,1 Q-.1,.12 -1,0 Q-.1,-.12 0,-1Z" fill="${c}" transform="translate(${x} ${y}) scale(${s})"/>`;
function staticSVG(dark){const ink=dark?C.white:C.navy,accent=dark?C.sky:C.blue;
 const door=`<g transform="translate(960 211) scale(.60)"><path d="M-43,44 L-43,-10 C-43,-63 43,-61 43,-10 L43,44 L30,44 L30,-10 C30,-45 -30,-46 -30,-10 L-30,44Z" fill="${ink}"/><path d="M-28,42 L-28,-8 C-28,-44 29,-44 29,-8 L29,42Z" fill="${dark?C.navy:C.blue}"/><g transform="translate(-29 -7) skewX(2.86)"><path d="M0,0 Q18,-39 36,0 L36,49 L0,49Z" fill="${accent}"/><path d="M26,24H30V31H26Z" fill="${dark?C.white:C.sky}"/></g><g fill="white"><ellipse cx="18" cy="14" rx="2.2" ry="3.7"/><ellipse cx="26" cy="14" rx="2.2" ry="3.7"/></g><path d="M-51,47 L51,44 L54,51 L-50,53Z" fill="${ink}"/></g>`;
 const cn=(!dark?A.letters.map((_,i)=>mapped(i,false,true)).join(''):'')+A.letters.map((_,i)=>mapped(i,dark)).join('');
 return `<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080"><title>魔物猎手 · ${dark?'继续':'暂停'}中插</title>${defs}<rect width="1920" height="1080" fill="white"/><path d="${A.outer}" fill="${dark?C.blue:'none'}" stroke="${dark?C.white:C.blue}" stroke-width="7" stroke-linejoin="round"/><path d="${A.inner}" fill="none" stroke="${dark?C.sky:C.navy}" stroke-width="2.5"/><path d="${A.english}" fill="${ink}"/>${[-1,1].map(s=>star(960+s*409,532,10,dark?C.white:C.blue)).join('')}${cn}</svg>`;
}
for(const variant of ['pause','resume'])fs.writeFileSync(path.join(R,'assets',`eyecatch-${variant}.svg`),staticSVG(variant==='resume'));
const data=file=>'data:image/png;base64,'+fs.readFileSync(path.join(R,file)).toString('base64');
A.letters.forEach((v,i)=>{v.inkData=data(v.ink);v.edgeData=data(v.edge);v.whiteData=data(`assets/white-${i}.png`)});
const html=`<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>魔物猎手 · 中插</title><style>*{box-sizing:border-box}body{margin:0;background:white;color:#173b80;font-family:"Microsoft YaHei",sans-serif}main{max-width:1480px;margin:auto;padding:26px 24px 60px}h1{font-size:24px;margin:0 0 12px}p{font-size:14px;line-height:1.8;margin:0 0 20px}canvas{display:block;width:100%;aspect-ratio:16/9;border:1px solid #e5eaf0}.variants,.controls,.links{display:flex;gap:14px;flex-wrap:wrap;align-items:center;margin:18px 0}button{font:inherit;color:#173b80;background:white;border:1px solid #173b80;padding:10px 20px;border-radius:3px;cursor:pointer}button[aria-pressed=true],#replay{background:#173b80;color:white}input[type=range]{flex:1;accent-color:#216ae1;min-width:180px}#time{font-variant-numeric:tabular-nums;font-size:13px}label{font-size:14px}a{color:#173b80}.stills{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:36px}.stills img{display:block;width:100%;border:1px solid #e5eaf0}h2{font-size:18px}figcaption{font-size:14px;margin-top:10px}figure{margin:0}@media(max-width:650px){.stills{grid-template-columns:1fr}}</style><main><h1>魔物猎手 · 圆形中插</h1><p>白底蓝字用于段落暂停，白底蓝章用于接回剧情。圆内四字加大 18%。魔最快落地，物稍缓，猎与手更慢地落下；画圆同步进行，保留 Q 弹与惯性轻转。</p><div class="variants"><button data-variant="pause" aria-pressed="true">暂停篇</button><button data-variant="resume" aria-pressed="false">继续篇</button></div><canvas id="eyecatch" aria-label="圆形中插动画"></canvas><div class="controls"><button id="replay">重新播放</button><button id="pause">暂停</button><input id="progress" type="range" min="0" max="3.8" step=".01" value="0" aria-label="时间"><span id="time">0 / 3.8 s</span><label><input id="loop" type="checkbox" checked> 循环</label></div><div class="links"><a href="eyecatch-pause-big-stagger-4k60.mp4" download>暂停篇 · 4K MP4</a><a href="eyecatch-resume-big-stagger-4k60.mp4" download>继续篇 · 4K MP4</a><a href="eyecatch-big-stagger-package.zip" download>静态图、矢量图与代码</a></div><div class="stills"><figure><img src="assets/eyecatch-pause-1080.png" alt="暂停篇中插"><figcaption>暂停篇 · 白底蓝字</figcaption></figure><figure><img src="assets/eyecatch-resume-1080.png" alt="继续篇中插"><figcaption>继续篇 · 白底蓝章</figcaption></figure></div></main><script>window.EYE_ASSETS=${JSON.stringify(A)};</script><script>${fs.readFileSync(path.join(R,'eyecatch.js'),'utf8')}</script></html>`;
fs.writeFileSync(path.join(R,'preview.html'),html);console.log('Built paired eyecatch vectors and standalone preview');
}
main().catch(e=>{console.error(e);process.exitCode=1});
