#!/usr/bin/env python
# Modified from https://gist.github.com/shunsukeaihara/4602848#file-karaoke_spectral_subtruction-py
import scipy as sp
import numpy as np
import math
import optparse
import tempfile
import wave
from itertools import izip

def read_signal(filename, winsize):
    wf=wave.open(filename,'rb')
    n=wf.getnframes()
    str=wf.readframes(n)
    params = ((wf.getnchannels(), wf.getsampwidth(),
               wf.getframerate(), wf.getnframes(),
               wf.getcomptype(), wf.getcompname()))
    siglen=((int )(len(str)/2/winsize) + 1) * winsize
    signal=sp.zeros(siglen, sp.float32)
    signal[0:len(str)/2] = sp.float32(sp.fromstring(str,sp.int16))/32767.0
    return [signal, params]


def get_frame(signal, winsize, no):
    shift=winsize/2
    start=no*shift
    end = start+winsize
    return signal[start:end]


def add_signal(signal, frame, winsize, no ):
    shift=winsize/2
    start=no*shift
    end=start+winsize
    signal[start:end] = signal[start:end] + frame

def separate_channels(signal):
    return signal[0::2],signal[1::2]

def uniting_channles(leftsignal,rightsignal):
    ret=[]
    for i,j in izip(leftsignal,rightsignal):
        ret.append(i)
        ret.append(j)
    return np.array(ret,sp.float32)


class KaraokeFileLoader():
    def __init__(self,winsize):
        self._winsize = winsize

    def load_file(self,songfile,karaokefile):
        ssignal, params = read_signal(songfile,self._winsize)
        ksignal, params = read_signal(karaokefile,self._winsize)
        sindex,kindex = self._alignment(ssignal,ksignal)
        s,k = self._reshape_signal(sindex,kindex,ssignal,ksignal)
        return s,k,params

    def _reshape_signal(self,sindex,kindex,ssignal,ksignal):
        def reshape(signal,siglen,winsize):
            length =(siglen/winsize+1)*winsize
            ret=sp.zeros(length, sp.float32)
            ret[0:siglen] = signal
            return ret
        slen = len(ssignal)-sindex
        klen = len(ksignal)-kindex
        length = 0
        if slen>klen:
            length = klen
        else:
            length = slen
        ssignal=reshape(ssignal[sindex:sindex+length],length,self._winsize)
        ksignal=reshape(ksignal[kindex:kindex+length],length,self._winsize)
        return ssignal,ksignal

    def _alignment(self,ssignal,ksignal):
        starta = 0
        for i in range(len(ssignal))[0::2]:
            if ssignal[i]<-100/32767.0 or ssignal[i]>100/32767.0:
                starta = i
                break
        startb=0
        for i in range(len(ksignal))[0::2]:
            if ksignal[i]<-100/32767.0 or ksignal[i]>100/32767.0:
                startb = i
                break
        start=starta-100
        base = ssignal[start:start+5000]
        small=1000000
        index=0
        for i in range(startb-1000,startb-1000+10000)[0::2]:
            signal = ksignal[i:i+5000]
            score =  math.sqrt(sp.sum(sp.square(sp.array(list(base-signal),sp.float32))))
            if score<small:
                index=i
                small=score
        return  start,index

class SpectralSubtruction():
    def __init__(self,winsize,window,coefficient=5.0,ratio=1.0):
        self._window=window
        self._coefficient=coefficient
        self._ratio=ratio

    def compute(self,signal,noise):
        n_spec = sp.fft(noise*self._window)
        n_pow = sp.absolute(n_spec)**2.0
        return self.compute_by_noise_pow(signal,n_pow)

    def compute_by_noise_pow(self,signal,n_pow):
        s_spec = sp.fft(signal*self._window)
        s_amp = sp.absolute(s_spec)
        s_phase = sp.angle(s_spec)
        amp = s_amp**2.0 - n_pow*self._coefficient
        amp = sp.maximum(amp,0.0)
        amp = sp.sqrt(amp)
        amp = self._ratio*amp + (1.0-self._ratio)*s_amp
        spec = amp * sp.exp(s_phase*1j)
        return sp.real(sp.ifft(spec))


def subtruction(ssignal,ksignal,window,winsize,method):
    nf = len(ssignal)/(winsize/2) - 1
    out=sp.zeros(len(ssignal),sp.float32)
    for no in xrange(nf):
        s = get_frame(ssignal, winsize, no)
        k = get_frame(ksignal, winsize, no)
        add_signal(out, method.compute(s,k), winsize, no)
    return out

def write(param,signal):
    st = tempfile.TemporaryFile()
    wf=wave.open(st,'wb')
    wf.setparams(params)
    s=sp.int16(signal*32767.0).tostring()
    wf.writeframes(s)
    st.seek(0)
    print st.read()


if __name__ == "__main__":
    parser = optparse.OptionParser(usage="%prog [-w WINSIZE] SONGFILE KARAOKEFILE")

    parser.add_option("-w", type="int", dest="winsize", default=1024)

    (options, args) = parser.parse_args()
    if len(args)!=2:
        parser.print_help()
        exit(2)

    kl = KaraokeFileLoader(options.winsize*2)

    ssignal,ksignal,params = kl.load_file(args[0],args[1])
    ssignal_l,ssignal_r = separate_channels(ssignal)
    ksignal_l,ksignal_r = separate_channels(ksignal)

    window = sp.hanning(options.winsize)

    method = SpectralSubtruction(options.winsize,window)

    sig_out_l = subtruction(ssignal_l,ksignal_l,window,options.winsize,method)
    sig_out_r = subtruction(ssignal_r,ksignal_r,window,options.winsize,method)

    sig_out_l[sp.isnan(sig_out_l)+sp.isinf(sig_out_l)]=0.0
    sig_out_r[sp.isnan(sig_out_r)+sp.isinf(sig_out_r)]=0.0


    result = uniting_channles(sig_out_l, sig_out_r)
    write(params, result)