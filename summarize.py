#!/usr/bin/env python3

import math
import numpy as np
import scipy.signal as sig
import sys

def readADIDump(fname):
    x = np.fromfile(fname, dtype=np.short)
    real = x[0::2]
    imag = x[1::2]
    return real + 1j*imag

def brickwall(flo, fhi, fsamp = 20.0e6, numtaps = 128, deltaf=5e3):
    fpoints = np.array(( 0.0, (flo - deltaf), flo, fhi, (fhi + deltaf), fsamp ))
    fgains  = np.array(( 0.0, 0.0,            1.0, 1.0, 0.0,            0.0))

    return sig.firwin2(numtaps=numtaps, freq=fpoints, gain=fgains, nyq=fsamp)

def splitADIDump(vec, numSplits):
    nsamps = vec.size
    sampsPerSplit = int(math.ceil(float(nsamps) / float(numSplits)))
    vecs = [vec[i*sampsPerSplit:(i+1)*sampsPerSplit] for i in range(numSplits)]
    return vecs

def countCompleteCycles(vec):
    # Thanks https://stackoverflow.com/questions/3843017/efficiently-detect-sign-changes-in-python
    signs = np.sign(vec.real)
    signs[signs == 0] = -1
    zero_crossings = np.where(np.diff(signs))[0]
    return len(zero_crossings)

def generateTone(SNRdB):
    sigma = 10 ** (-SNRdB / 10.0)
    t = np.arange(0, 16000000)
    signal = np.cos(2*np.pi*t * 250e3/20e6) + 1j*np.sin(2*np.pi*t * 250e3/20e6)
    signal = signal + (sigma / 2.0) * (np.random.randn(signal.size) + 1j * np.random.randn(signal.size))
    signalShortImag = (signal.imag * (2**14)).astype(np.short)
    signalShortReal = (signal.real * (2**14)).astype(np.short)
    signalShort = np.empty((signalShortReal.size + signalShortImag.size, ), dtype=np.short)
    signalShort[::2] = signalShortReal
    signalShort[1::2] = signalShortImag
    return signalShort

def completeCyclesAddToFile(vec, vecname, fcounts):
    # filt = brickwall(100.0e3, 270.0e3)
    # vec  = np.convolve(vec, filt)
    cycles = countCompleteCycles(vec)
    with open(fcounts, 'a') as histfile:
        histfile.write(vecname)
        histfile.write("\t\t")
        histfile.write(str(cycles))
        histfile.write("\n")

def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

def fnameSuffix(fname, suffix):
    return rreplace(fname, ".", suffix+".", 1)

if __name__ == "__main__":
    vec = readADIDump(sys.argv[1])
    nSplits = int(sys.argv[2])
    vec = splitADIDump(vec, nSplits)
    for i in range(len(vec)):
        v = vec[i]
        completeCyclesAddToFile(v, fnameSuffix(sys.argv[1], "_" + str(i)), sys.argv[3])

