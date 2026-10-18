const fs=require('fs'),path=require('path');
const sharp=require('sharp');
const root=__dirname,dir=path.join(root,'assets');
(async()=>{
 const manifest={};
 for(const file of fs.readdirSync(dir).filter(f=>f.endsWith('.svg'))){
  const name=path.basename(file,'.svg'),source=fs.readFileSync(path.join(dir,file));
  const image=sharp(source,{density:144}).ensureAlpha();
  const {data,info}=await image.raw().toBuffer({resolveWithObject:true});
  let x0=info.width,y0=info.height,x1=0,y1=0;
  for(let y=0;y<info.height;y++)for(let x=0;x<info.width;x++)if(data[(y*info.width+x)*4+3]>2){x0=Math.min(x0,x);y0=Math.min(y0,y);x1=Math.max(x1,x);y1=Math.max(y1,y);}
  x0=Math.max(0,x0-3);y0=Math.max(0,y0-3);x1=Math.min(info.width-1,x1+3);y1=Math.min(info.height-1,y1+3);
  await sharp(data,{raw:info}).extract({left:x0,top:y0,width:x1-x0+1,height:y1-y0+1}).png().toFile(path.join(dir,name+'.png'));
  manifest[name]={src:'assets/'+name+'.png',x:x0/2,y:y0/2,w:(x1-x0+1)/2,h:(y1-y0+1)/2};
 }
 fs.writeFileSync(path.join(dir,'manifest.json'),JSON.stringify(manifest,null,2));
 console.log(manifest);
})();
