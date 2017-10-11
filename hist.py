#!/usr/bin/env python3

import matplotlib.pyplot as plt

if __name__=="__main__":
    f = open("9_27_17_cycle_counts.txt", 'r')
    time = []
    counts = []
    for l in f.readlines():
        sp = l.split('\t')
        time.append(sp[0])
        counts.append(int(sp[2]))
    plt.hist(counts, bins=30)
    plt.show()
    plt.plot(counts)
    plt.show()
