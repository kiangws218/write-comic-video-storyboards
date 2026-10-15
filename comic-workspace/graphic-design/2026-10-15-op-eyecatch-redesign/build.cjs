const fs=require('fs'),path=require('path'),{spawnSync}=require('child_process');
const root=__dirname, mode=process.argv[2]||'all';
function run(command,args){const result=spawnSync(command,args,{cwd:root,stdio:'inherit',windowsHide:true});if(result.error)throw result.error;if(result.status!==0)throw Error(command+' failed: '+result.status)}
function node(file,...args){run(process.execPath,[file,...args])}
for(const name of ['assets','audio','exports','qa'])fs.mkdirSync(path.join(root,name),{recursive:true});
if(!['all','sound','eyes','title'].includes(mode))throw Error('Use all, sound, eyes or title');
if(mode==='all')node('rasterize.cjs');
if(mode==='all'||mode==='sound'){
 run(process.env.PYTHON||'python',['design_eyecatch_sfx.py']);node('master_eyecatch_sfx.cjs');
 run(process.env.PYTHON||'python',['analyze_eyecatch_sfx.py']);
 for(const kind of ['pause','resume'])fs.copyFileSync(path.join(root,'audio','sound-design-v1',kind+'-master-48k24.wav'),path.join(root,'audio',kind+'.wav'));
}
if(mode==='all'||mode==='eyes')node('render.cjs','export-eyes');
if(mode==='all'||mode==='title')node('render-overlay.cjs');
if(mode==='all'){node('finalize-title-delivery.cjs');node('attach_eyecatch_sound.cjs')}
