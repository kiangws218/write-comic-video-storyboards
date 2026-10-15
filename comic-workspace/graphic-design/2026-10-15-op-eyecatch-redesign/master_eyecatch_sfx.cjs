const fs=require('fs'),path=require('path'),{spawn}=require('child_process');
const ROOT=__dirname,DIR=path.join(ROOT,'audio','sound-design-v1');
function run(args){return new Promise((resolve,reject)=>{const p=spawn(require('./runtime.cjs').ffmpeg,args,{windowsHide:true});let out='',err='';p.stdout.on('data',x=>out+=x);p.stderr.on('data',x=>err+=x);p.on('exit',c=>c===0?resolve({out,err}):reject(Error(err.slice(-4500))))})}
function stats(s){const matches=[...s.matchAll(/\{\s*"input_i"[\s\S]*?\}/g)];if(!matches.length)throw Error('No loudness analysis');return JSON.parse(matches.at(-1)[0])}
(async()=>{
 const results=[];
 for(const kind of ['pause','resume']){
  const target=kind==='pause'?-19.5:-18.5;
  const input=path.join(DIR,kind+'-premaster.wav');
  const first=stats((await run(['-hide_banner','-i',input,'-af',`loudnorm=I=${target}:TP=-2:LRA=7:print_format=json`,'-f','null','-'])).err);
  const filter=`loudnorm=I=${target}:TP=-2:LRA=7:measured_I=${first.input_i}:measured_TP=${first.input_tp}:measured_LRA=${first.input_lra}:measured_thresh=${first.input_thresh}:offset=${first.target_offset}:linear=true:print_format=json,afade=t=in:st=0:d=0.002,afade=t=out:st=3.963:d=0.037`;
  const file=path.join(DIR,kind+'-master-48k24.wav');
  await run(['-y','-hide_banner','-i',input,'-af',filter,'-ar','48000','-ac','2','-c:a','pcm_s24le','-t','4','-metadata',`title=${kind==='pause'?'Intermission A - Close':'Intermission B - Open'}`,'-metadata','comment=Original synthesized sound design; sample-aligned to clean eyecatch revision',file]);
  const actual=stats((await run(['-hide_banner','-i',file,'-af',`loudnorm=I=${target}:TP=-2:LRA=7:print_format=json`,'-f','null','-'])).err);
  if(Number(actual.input_tp)>-1.6)throw Error('Insufficient true peak headroom');
  results.push({kind,targetLUFS:target,actualLUFS:Number(actual.input_i),truePeakDBTP:Number(actual.input_tp),loudnessRangeLU:Number(actual.input_lra),premaster:first});
  await run(['-y','-v','error','-i',file,'-c:a','libmp3lame','-b:a','128k',path.join(DIR,kind+'-audition.mp3')]);
 }
 fs.writeFileSync(path.join(DIR,'mastering-report.json'),JSON.stringify(results,null,2));console.log(JSON.stringify(results,null,2));
})();
