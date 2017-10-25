#!/usr/bin/env python3

import datetime as dt
import matplotlib.dates as md
import matplotlib.pyplot as plt
import sys

def getTimestamp(fname):
    num = float(fname.split(".")[1]) / 10.0
    return md.date2num(dt.datetime.fromtimestamp(num))

if __name__=="__main__":
    f = open(sys.argv[1], 'r')
    time = []
    counts = []
    for l in f.readlines():
        sp = l.split('\t')
        time.append(sp[0])
        counts.append(int(sp[2]))
    plt.hist(counts, bins=30)
    plt.show()
    time = [getTimestamp(i) for i in time]
    print(time)
    plt.scatter(time, counts)
    plt.xticks( rotation=25 )
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax=plt.gca()
    ax.xaxis.set_major_formatter(xfmt)
    plt.show()
