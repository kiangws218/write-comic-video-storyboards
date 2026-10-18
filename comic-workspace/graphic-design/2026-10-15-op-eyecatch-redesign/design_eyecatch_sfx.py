"""Air / tactile lettering / crystal / soft pressure. Original synthesized SFX.

The timing is derived from the FINAL clean eyecatch animation, not its old sound.
Every gesture is sample-accurate at 48 kHz. No imported sample or music is used.
"""
from pathlib import Path
import json,wave
import numpy as np

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'audio'/'sound-design-v1';OUT.mkdir(parents=True,exist_ok=True)
SR=48000;DURATION=4;N=SR*DURATION
rng=np.random.default_rng(61511015)

def smooth(x):
    x=np.clip(x,0,1);return x*x*(3-2*x)

def hz(midi):return 440*2**((midi-69)/12)

def bandnoise(length,lo,hi):
    n=max(16,round(length*SR));freq=np.fft.rfftfreq(n,1/SR)
    phase=rng.normal(size=len(freq))+1j*rng.normal(size=len(freq))
    # Butterworth-like skirts prevent harsh rectangular spectral edges.
    shape=(1-np.exp(-(freq/max(lo,1))**4))*np.exp(-(freq/hi)**4)
    signal=np.fft.irfft(phase*shape,n)
    return signal/max(np.sqrt(np.mean(signal**2)),1e-12)

def write24(file,data):
    file.parent.mkdir(parents=True,exist_ok=True)
    data=np.asarray(data);assert np.max(np.abs(data))<1
    dither=(rng.random(data.shape)-rng.random(data.shape))/16777216
    values=np.round((data+dither)*8388607).astype(np.int32).reshape(-1)
    packed=np.empty((len(values),3),np.uint8)
    for k in range(3):packed[:,k]=(values>>(8*k))&255
    with wave.open(str(file),'wb') as w:
        w.setnchannels(2);w.setsampwidth(3);w.setframerate(SR);w.writeframes(packed.tobytes())

def make(kind):
    resume=kind=='resume'
    buses={name:np.zeros((N,2)) for name in ['01-air','02-letter-touch','03-crystal','04-body']}
    cues=[]
    def put(bus,mono,start,gain,pan0=0,pan1=None,width=.0):
        j=round(start*SR);k=min(len(mono),N-j)
        if k<=0:return
        sig=mono[:k];u=np.linspace(0,1,k)
        pan=np.full(k,pan0) if pan1 is None else pan0+(pan1-pan0)*smooth(u)
        angle=(np.clip(pan,-1,1)+1)*np.pi/4
        pair=np.stack((sig*np.cos(angle),sig*np.sin(angle)),axis=1)
        # A small high-frequency side component; primary transient stays solid in mono.
        if width:
            delayed=np.concatenate((np.zeros(29),sig[:-29]))
            side=(sig-delayed)*width*.25
            pair[:,0]+=side;pair[:,1]-=side
        buses[bus][j:j+k]+=pair*gain
    def cue(name,time,**extra):cues.append(dict(name=name,seconds=time,frame=round(time*60),**extra))
    def air(start,length,gain,pan0,pan1,rise=True,peak=.48,width=.32):
        t=np.arange(round(length*SR))/SR;u=t/length
        low=bandnoise(length,240,1150);mid=bandnoise(length,1200,4600);high=bandnoise(length,4300,8500)
        travel=smooth(u) if rise else 1-smooth(u)
        spectrum=.35*(1-travel)*low+(.65-.15*travel)*mid+(.12+.30*travel)*high
        # Smooth asymmetric breath envelope, normalized to its intended peak.
        a=1.5+4*peak;b=1.5+4*(1-peak)
        env=(u**a)*((1-u)**b);env/=max(env.max(),1e-9)
        flutter=1+.065*np.sin(2*np.pi*(17*t+5*t*t))
        put('01-air',spectrum*env*flutter,start,gain,pan0,pan1,width)
    def glass(start,midi,gain=.10,pan=0,length=.63,soft=False):
        t=np.arange(round(length*SR))/SR;f=hz(midi)
        ratios=[1,2.76,5.41,8.93];weights=[.79,.16,.055,.016]
        sig=np.zeros(len(t))
        for i,(ratio,weight) in enumerate(zip(ratios,weights)):
            if f*ratio>10500:continue
            damping=(5.7 if not soft else 4.6)+i*7
            sig+=weight*np.sin(2*np.pi*f*ratio*t+.11*i)*np.exp(-t*damping)
        sig*=smooth(t/(.004 if not soft else .013))*smooth((length-t)/.055)
        put('03-crystal',sig,start,gain,pan,pan*.45,.16)
    def touch(start,gain=.04,pan=0,variant=0):
        t=np.arange(round(.16*SR))/SR
        sig=(np.sin(2*np.pi*(225+17*variant)*t)*np.exp(-t*48)
             +.46*np.sin(2*np.pi*(532+29*variant)*t)*np.exp(-t*79)
             +.18*bandnoise(.16,650,2400)*np.exp(-t*95))
        sig*=smooth(t/.0018)*smooth((.16-t)/.025)
        put('02-letter-touch',sig,start,gain,pan)
    def pressure(start,gain=.09,length=.34):
        t=np.arange(round(length*SR))/SR
        phase=2*np.pi*(79*t+32*.028*(1-np.exp(-t/.028)))
        sig=(np.sin(phase)*np.exp(-t*16)+.13*np.sin(2*np.pi*178*t)*np.exp(-t*28))
        sig*=smooth(t/.004)*smooth((length-t)/.05)
        put('04-body',sig,start,gain,0)
    def bloom(start,gain=.027):
        length=.82;t=np.arange(round(length*SR))/SR
        sig=np.zeros(len(t))
        for i,midi in enumerate([62,69,76]):
            f=hz(midi);sig+=(np.sin(2*np.pi*f*t)+.12*np.sin(2*np.pi*f*2.003*t))*np.exp(-t*(5+i))/3
        sig*=smooth(t/.045)*smooth((length-t)/.12)
        put('03-crystal',sig,start,gain,0,0,.20)

    if not resume:
        # The blue diagonal blade crosses first; the ring contracts at 0.48 s.
        air(0,.38,.105,-.62,.58,False,.30);cue('diagonal silk sweep',.10)
        air(.43,.39,.077,.42,-.30,False,.31);pressure(.49,.060,.26);cue('ring catches the sweep',.49)
    else:
        # Same crystal identity as the tiny star that ends A, now opening outward.
        glass(.018,86,.052,0,.64,True);cue('shared star opens',.018)
        air(.035,.59,.106,0,.18,True,.48,.50);pressure(.30,.050,.27);cue('portal expands',.31)
        air(.46,.29,.047,-.22,.24,True,.42);cue('ring resolves',.49)

    notes=[81,78,76,74] if not resume else [74,76,78,81]
    for i,midi in enumerate(notes):
        start=.54+i*.075
        pan=-.69 if i%2==0 else .69
        # Four quiet air strokes follow the actual curved flights, not square cards.
        air(start+.055,.60,.037 if i<2 else .032,pan,pan*.26,rise=(i>=2) != resume,peak=.58,width=.19)
        arrival=start+.82
        touch(arrival,.043 if i<3 else .057,pan*.31,i)
        glass(arrival+.003,midi,[.057,.054,.056,.074][i],pan*.34,.67)
        cue('letter settles',arrival,letter=['魔','物','猎','手'][i],midi=midi)
    bloom(1.59,.052 if resume else .044)
    pressure(1.585,.061 if resume else .050,.31)
    cue('logo settles / bloom',1.585)
    # There is intentionally no new event during the readable title hold.
    if not resume:
        air(3.235,.39,.092,.49,0,False,.30,.22)
        pressure(3.34,.041,.27);cue('iris closes inward',3.34)
        glass(3.705,86,.044,0,.285,True);cue('small star / shared signature',3.705)
    else:
        air(3.235,.67,.126,-.15,.37,True,.57,.47)
        # A tiny bright edge, rather than a bass hit, hands the scene back cleanly.
        glass(3.665,93,.034,.21,.32,True);cue('white wipe opens / handoff',3.62)

    def room(source,amount):
        wet=np.zeros_like(source)
        for delay,gain,swap in [(.019,.24,False),(.033,.18,True),(.051,.13,False),(.077,.095,True),(.113,.06,True),(.163,.035,False)]:
            k=round(delay*SR)
            src=source[:-k,::-1] if swap else source[:-k]
            wet[k:]+=src*gain
        # A short diffuse tail avoids a conspicuous delayed 'echo' repeat.
        n=round(.42*SR);t=np.arange(n)/SR
        for ch in range(2):
            ir=rng.normal(0,1,n)*np.exp(-t*15)*smooth(t/.012)
            ir=np.convolve(ir,np.ones(6)/6,mode='same')
            ir*=.0025
            size=1<<(N+n-1).bit_length()
            mono=source.mean(axis=1)
            wet[:,ch]+=np.fft.irfft(np.fft.rfft(mono,size)*np.fft.rfft(ir,size),size)[:N]
        return wet*amount

    wet=np.zeros((N,2))
    for name,amount in [('01-air',.14),('02-letter-touch',.18),('03-crystal',.31),('04-body',.055)]:wet+=room(buses[name],amount)
    buses['05-room']=wet
    # Linear, finite filtering; no circular tail or loop is introduced.
    for name,data in buses.items():
        size=1<<(N+SR//10-1).bit_length();f=np.fft.rfftfreq(size,1/SR)
        response=(1-np.exp(-(f/42)**4))*np.exp(-(f/11200)**8)
        buses[name]=np.fft.irfft(np.fft.rfft(data,size,axis=0)*response[:,None],size,axis=0)[:N]
        buses[name]*=smooth(np.arange(N)/SR/.003)[:,None]
        buses[name]*=smooth((DURATION-np.arange(N)/SR)/.037)[:,None]
    mix=sum(buses.values())
    # A single shared gain keeps A/B and the stem relationship coherent.
    gain=2.2;mix*=gain
    assert np.max(np.abs(mix))<.95
    stemdir=OUT/'stems'/kind
    for name,data in buses.items():write24(stemdir/(name+'.wav'),data*gain)
    write24(OUT/(kind+'-premaster.wav'),mix)
    cue_path=OUT/(kind+'-cue-sheet.json');cue_path.write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
    stat={'kind':kind,'duration':DURATION,'rate':SR,'bit_depth':24,'peak_dbfs':float(20*np.log10(np.max(np.abs(mix)))),
          'rms_dbfs':float(20*np.log10(np.sqrt(np.mean(mix**2)))),'stereo_correlation':float(np.corrcoef(mix.T)[0,1]),
          'first_sample':mix[0].tolist(),'last_sample':mix[-1].tolist()}
    print(json.dumps(stat,ensure_ascii=False))
    return stat

reports=[make('pause'),make('resume')]
(OUT/'premaster-analysis.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8')
