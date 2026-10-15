const fs=require('fs'),path=require('path');
const root=__dirname;
let ui=fs.readFileSync(path.join(root,'title-overlay.html'),'utf8');
for(const[a,b]of[
 ['标题叠加素材 · 入场与离场','标题叠加素材 · 圆环入场与退场'],
 ['新世界之魔物猎手 · 标题叠加素材','新世界之魔物猎手 · 圆环版标题'],
 ['仅文字入场、停留和离场，用于叠加到现有 OP。','沿用第一版的圆环展开、字形环绕与标题汇聚，补上呼应圆环的退场。'],
 ['总长 3.5 秒','总长 5 秒'],['max="3.5" value="1.5"','max="5" value="2.8"'],['1.50 / 3.50','2.80 / 5.00'],
 ['0–0.8 秒入场 · 0.8–2.6 秒停留 · 2.6–3.5 秒离场。无背景、无附加图形、无音轨。','圆环展开与字形环绕 → 汇聚成标题 → 停留 → 回环收拢退场。透明背景，无音轨。'],
 ['let t=1.5','let t=2.8'],[' / 3.50',' / 5.00'],['%3.5','%5'],['Math.min(3.5,','Math.min(5,'],['title-overlay-3','ring-overlay-4']
])ui=ui.split(a).join(b);
fs.writeFileSync(path.join(root,'title-overlay.html'),ui);
let finalize=fs.readFileSync(path.join(root,'finalize-title-delivery.cjs'),'utf8');
finalize=finalize.replace("['poster.jpg','title-overlay-poster.jpg'],",'');
finalize=finalize.split('duration=3.5').join('duration=5').split("'11.5'").join("'13'").split('完整放映 · 11.5 秒').join('完整放映 · 13 秒').split('标题叠加 · 3.5 秒').join('圆环标题 · 5 秒').split('title-overlay-3').join('ring-overlay-4').split('titleDuration:3.5').join('titleDuration:5').split('titleFrames:210').join('titleFrames:300').split('frames:210').join('frames:300').split('playback.duration-11.5').join('playback.duration-13').split('video.currentTime=1.5').join('video.currentTime=2.8');
fs.writeFileSync(path.join(root,'finalize-title-delivery.cjs'),finalize);
let watch=fs.readFileSync(path.join(root,'watch.html'),'utf8').split('完整放映 · 11.5 秒').join('完整放映 · 13 秒').split('标题叠加 · 3.5 秒').join('圆环标题 · 5 秒').split('title-overlay-3').join('ring-overlay-4');
fs.writeFileSync(path.join(root,'watch.html'),watch);
let check=fs.readFileSync(path.join(root,'check_playback.cjs'),'utf8').split('playback.duration-11.5').join('playback.duration-13').split('video.currentTime=1.5').join('video.currentTime=2.8');
fs.writeFileSync(path.join(root,'check_playback.cjs'),check);
console.log('Ring title delivery UI updated.');
