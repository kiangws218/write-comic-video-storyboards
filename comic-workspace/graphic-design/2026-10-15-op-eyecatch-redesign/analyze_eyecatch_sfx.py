from pathlib import Path
import wave,json
import numpy as np
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parent;DIR=ROOT/'audio'/'sound-design-v1'
reports=[]
for kind in ['pause','resume']:
    p=DIR/(kind+'-master-48k24.wav')
    with wave.open(str(p),'rb') as f:
        params=f.getparams();raw=f.readframes(f.getnframes())
    b=np.frombuffer(raw,np.uint8).reshape(-1,3).astype(np.int32)
    integers=b[:,0]+(b[:,1]<<8)+(b[:,2]<<16);integers=np.where(integers>=8388608,integers-16777216,integers)
    audio=integers.reshape(-1,2)/8388608
    assert params.sampwidth==3 and params.framerate==48000 and len(audio)==192000
    assert np.max(np.abs(audio))<1 and np.max(np.abs(audio[0]))<2e-6 and np.max(np.abs(audio[-1]))<2e-6
    mono=audio.mean(axis=1);stereo_rms=np.sqrt(np.mean(audio**2));mono_rms=np.sqrt(np.mean(mono**2))
    spec=np.abs(np.fft.rfft(mono))**2;freq=np.fft.rfftfreq(len(mono),1/48000)
    stat={'kind':kind,'seconds':4,'rate':48000,'bits':24,'channels':2,'samples':len(audio),
          'sample_peak_dbfs':float(20*np.log10(np.max(np.abs(audio)))),'rms_dbfs':float(20*np.log10(stereo_rms)),
          'dc_offset':audio.mean(axis=0).tolist(),'stereo_correlation':float(np.corrcoef(audio.T)[0,1]),
          'mono_rms_difference_db':float(20*np.log10(mono_rms/stereo_rms)),
          'energy_above_7khz_fraction':float(spec[freq>7000].sum()/spec.sum()),
          'last_10ms_rms_dbfs':float(20*np.log10(max(1e-12,np.sqrt(np.mean(audio[-480:]**2)))))}
    reports.append(stat)
    image=Image.new('RGB',(1600,550),'#101d31');d=ImageDraw.Draw(image)
    for j in range(9):
        x=80+j*180;d.line((x,65,x,490),fill='#30425a');d.text((x-5,505),str(j*.5),fill='#aabdd5')
    for ch,cy,color in [(0,185,'#56c6ef'),(1,380,'#b4dffd')]:
        d.line((80,cy,1520,cy),fill='#53637b')
        for x in range(1440):
            a=round(x/1440*len(audio));b=round((x+1)/1440*len(audio));v=audio[a:b,ch]
            d.line((80+x,cy-int(v.max()*145),80+x,cy-int(v.min()*145)),fill=color)
    for time in [1.36,1.435,1.51,1.585,3.25]:
        x=80+time*360;d.line((x,65,x,490),fill='#d6d991')
    d.text((80,24),kind.upper()+' / 48 kHz / 24-bit stereo / gesture-aligned master',fill='#eff5ff')
    image.save(DIR/(kind+'-waveform.png'))
(DIR/'signal-analysis.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(reports,ensure_ascii=False,indent=2))
