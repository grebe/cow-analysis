#!/usr/bin/env python3

import matplotlib.pyplot as plt
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

def completeCyclesAddToFile(fvec, fcounts):
    vec  = readADIDump(fvec)
    filt = brickwall(100.0e3, 270.0e3)
    vec  = np.convolve(vec, filt)
    cycles = countCompleteCycles(vec)
    with open(fcounts, 'a') as histfile:
        histfile.write(fvec)
        histfile.write("\t\t")
        histfile.write(str(cycles))
        histfile.write("\n")
        # histfile.write(f"{fvec}:\t\t{cycles}\n")

if __name__ == "__main__":
    completeCyclesAddToFile(sys.argv[1], sys.argv[2])

def oldMain():
    fname = sys.argv[1]
    nfft = 2**18
    sig = readADIDump(fname)
    plt.plot(sig[:4*2048].real)
    plt.show()
    timestep = 400e-9 # ns
    #timestep = 50e-9
    # trim to multiples of nfft
    nwindows = int(len(sig)/nfft)
    sig = sig[:nwindows*nfft]
    # average windows
    print(sig.shape)
    sig = np.reshape(sig, (nwindows, nfft))
    sig = np.mean(sig, axis=0)
    print(sig.shape)

    window = np.hanning(nfft)
    ps = 20 * np.log10(np.abs(np.fft.fft(sig * window)))
    freqs = np.fft.fftfreq(sig.size, timestep)
    idx = np.argsort(freqs)

    plt.plot(freqs[idx], ps[idx])
    plt.show()

    plt.specgram(sig, NFFT=int(2**12), Fs=1.0/timestep, Fc=0, noverlap=int(2**10))
    plt.show()

