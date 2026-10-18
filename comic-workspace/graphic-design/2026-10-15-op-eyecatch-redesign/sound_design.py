"""Original restrained sound logos; no samples, borrowed tracks or external API."""
from pathlib import Path
import wave,json
import numpy as np
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'audio';OUT.mkdir(exist_ok=True)
SR=48000
rng=np.random.default_rng(6151)

def make(kind,seconds):
    n=round(seconds*SR);mix=np.zeros((n,2))
    def add(sig,start,gain=1,pan=0):
        j=round(start*SR);k=min(n-j,len(sig))
        if k<=0:return
        p=(pan+1)*np.pi/4
        mix[j:j+k,0]+=sig[:k]*gain*np.cos(p);mix[j:j+k,1]+=sig[:k]*gain*np.sin(p)
    def ping(start,midi,hold=.7,gain=.15,pan=0):
        t=np.arange(round(hold*SR))/SR;f=440*2**((midi-69)/12)
        e=np.minimum(t/.003,1)*np.exp(-t*7)*(np.minimum((hold-t)/.04,1))
        sig=(np.sin(2*np.pi*f*t)+.24*np.sin(2*np.pi*f*2.003*t)+.08*np.sin(2*np.pi*f*4.01*t))*e
        add(sig,start,gain,pan)
    def whoosh(start,hold=.36,gain=.12,reverse=False,pan=0):
        t=np.arange(round(hold*SR))/SR
        z=rng.normal(0,1,len(t));z=np.convolve(z,np.ones(9)/9,mode='same')
        env=np.sin(np.pi*t/hold)**1.6
        freq=180+1800*(t/hold if not reverse else 1-t/hold)**2
        sig=(z*.7+.14*np.sin(2*np.pi*np.cumsum(freq)/SR))*env
        add(sig,start,gain,pan)
    def impact(start,gain=.18):
        t=np.arange(round(.8*SR))/SR
        sig=np.sin(2*np.pi*(47*t+90*.025*(1-np.exp(-t/.025))))*np.exp(-t*9)
        sig+=.15*rng.normal(0,1,len(t))*np.exp(-t*70)
        sig*=np.minimum(t/.001,1)
        add(sig,start,gain)
    def chord(start,notes,hold=1.5,gain=.06):
        t=np.arange(round(hold*SR))/SR
        for i,midi in enumerate(notes):
            f=440*2**((midi-69)/12)
            sig=(np.sin(2*np.pi*f*t)+.20*np.sin(2*np.pi*f*2*t))*np.minimum(t/.06,1)*np.exp(-t*2.4)*np.minimum((hold-t)/.2,1)
            add(sig,start,gain,(-.6+i*.4))
    if kind=='op':
        ping(.02,83,1,.13);whoosh(.35,.4,.18);impact(.73,.16)
        ping(.78,76,.4,.1,-.4);ping(.90,83,.4,.1,.4);whoosh(1.20,.25,.19)
        impact(1.46,.17);chord(1.48,[52,59,66,71],1.2,.045)
        whoosh(2.25,.38,.2,pan=-.3);ping(2.58,88,.6,.12)
        for i,m in enumerate([71,74,78,81,83,86,90,95]):ping(3.67+i*.065,m,.8,.085,(-.65+i*.18))
        whoosh(4.12,.35,.20);impact(4.45,.30);chord(4.45,[47,59,66,71,74],2.9,.075)
        ping(4.48,95,1.6,.15,.4);ping(5.05,90,1.3,.08,-.3);ping(5.34,95,1.2,.065,.3)
    elif kind=='pause':
        whoosh(0,.4,.21);impact(.52,.18)
        for i,m in enumerate([83,81,78,74]):ping(1.05+i*.07,m,.7,.12,(i-1.5)*.3)
        chord(1.38,[59,66,71,74],1.4,.07);ping(1.72,90,.9,.07,.4)
        whoosh(3.24,.48,.18,True);ping(3.65,71,.34,.08)
    else:
        ping(.015,71,.65,.11);whoosh(.1,.5,.2);impact(.54,.16)
        for i,m in enumerate([74,78,81,83]):ping(1.05+i*.07,m,.75,.12,(1.5-i)*.3)
        chord(1.38,[59,66,71,78],1.6,.07);ping(1.78,95,1,.09,-.3)
        whoosh(3.22,.50,.23);ping(3.45,95,.54,.09)
    # A short stereo room, then a finite fade, leaves no cut-off tails.
    dry=mix.copy()
    for delay,gain in [(.071,.12),(.113,.09),(.179,.08),(.269,.055),(.387,.035)]:
        k=round(delay*SR);mix[k:]+=dry[:-k,::-1]*gain
    mix*=1.6
    mix=.9*np.tanh(mix/.9)
    edge=round(.06*SR);mix[:edge]*=np.linspace(0,1,edge)[:,None];mix[-edge:]*=np.linspace(1,0,edge)[:,None]
    pcm=np.round(np.clip(mix,-.99,.99)*32767).astype('<i2')
    with wave.open(str(OUT/(kind+'.wav')),'wb') as f:
        f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes(pcm.tobytes())
    print(kind,seconds,'peak dBFS',round(20*np.log10(np.max(np.abs(mix))),2))

for k,s in [('op',9),('pause',4),('resume',4)]:make(k,s)
