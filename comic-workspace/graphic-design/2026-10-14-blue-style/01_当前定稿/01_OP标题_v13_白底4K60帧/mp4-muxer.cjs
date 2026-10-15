// Single video track, constant frame duration, no B frames. Fast-start ISO BMFF.
const u16=v=>{const b=Buffer.alloc(2);b.writeUInt16BE(v);return b};
const u32=v=>{const b=Buffer.alloc(4);b.writeUInt32BE(v);return b};
const bytes=s=>Buffer.from(s,'ascii');
const zero=n=>Buffer.alloc(n);
const box=(type,...parts)=>{const payload=Buffer.concat(parts);return Buffer.concat([u32(payload.length+8),bytes(type),payload])};
const full=(type,flags,...parts)=>box(type,u32(flags),...parts);
const matrix=Buffer.concat([u32(65536),u32(0),u32(0),u32(0),u32(65536),u32(0),u32(0),u32(0),u32(1073741824)]);
module.exports=function mux({width,height,fps,bitrate,description,samples}){
 if(!description?.length||!samples.length)throw Error('Missing AVC decoder description or samples');
 const timescale=60000,step=timescale/fps,duration=step*samples.length;
 if(!Number.isInteger(step))throw Error('Unsupported frame rate');
 for(let i=0;i<samples.length;i++)if(Math.abs(samples[i].timestamp-Math.round(i*1e6/fps))>1)throw Error('Non-monotonic encoded frames or B frames');
 const ftyp=box('ftyp',bytes('isom'),u32(512),bytes('isomiso2avc1mp41'));
 const moov=offset=>{
  const mvhd=full('mvhd',0,u32(0),u32(0),u32(timescale),u32(duration),u32(65536),u16(256),zero(10),matrix,zero(24),u32(2));
  const tkhd=full('tkhd',7,u32(0),u32(0),u32(1),u32(0),u32(duration),zero(8),u16(0),u16(0),u16(0),u16(0),matrix,u32(width*65536),u32(height*65536));
  const mdhd=full('mdhd',0,u32(0),u32(0),u32(timescale),u32(duration),u16(0x55c4),u16(0));
  const hdlr=full('hdlr',0,u32(0),bytes('vide'),zero(12),bytes('VideoHandler\0'));
  const compressor=Buffer.alloc(32),name=bytes('Code-rendered title');compressor[0]=name.length;name.copy(compressor,1);
  // Preserve the encoder's BT.709 matrix and sRGB transfer metadata.
  const colr=box('colr',bytes('nclx'),u16(1),u16(13),u16(1),Buffer.from([0]));
  const avc1=box('avc1',zero(6),u16(1),zero(16),u16(width),u16(height),u32(72*65536),u32(72*65536),u32(0),u16(1),compressor,u16(24),u16(65535),box('avcC',description),colr,box('btrt',u32(0),u32(bitrate),u32(bitrate)));
  const stsd=full('stsd',0,u32(1),avc1);
  const stts=full('stts',0,u32(1),u32(samples.length),u32(step));
  const stsc=full('stsc',0,u32(1),u32(1),u32(samples.length),u32(1));
  const stsz=full('stsz',0,u32(0),u32(samples.length),...samples.map(s=>u32(s.data.length)));
  const stco=full('stco',0,u32(1),u32(offset));
  const keys=samples.flatMap((s,i)=>s.type==='key'?[u32(i+1)]:[]);
  const stss=full('stss',0,u32(keys.length),...keys);
  const stbl=box('stbl',stsd,stts,stsc,stsz,stco,stss);
  const vmhd=full('vmhd',1,u16(0),zero(6));
  const dinf=box('dinf',full('dref',0,u32(1),full('url ',1)));
  const minf=box('minf',vmhd,dinf,stbl);
  return box('moov',mvhd,box('trak',tkhd,box('mdia',mdhd,hdlr,minf)));
 };
 const header=moov(0),finalHeader=moov(ftyp.length+header.length+8);
 return Buffer.concat([ftyp,finalHeader,box('mdat',...samples.map(s=>s.data))]);
};
