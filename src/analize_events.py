#!/usr/bin/env python
import gzip
import sys
import os.path
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import csv

WIDTH_OF_CONV = 8
WIDTH_OF_ZCONV = 100
if __name__ == "__main__":


    data = np.loadtxt(gzip.open(sys.argv[1],"rb"),delimiter=",")
    time=(data[:,0]-data[0,0])/60

    convolve = np.convolve(data[:,2], np.transpose(np.ones(WIDTH_OF_CONV)/WIDTH_OF_CONV))
    print(data.shape)
    #plt.plot(data[:, 0],data[:, 2])
    #import code; code.interact(local=dict(globals(), **locals()))
    convole_window =convolve[WIDTH_OF_CONV/2:len(data[:,2]) + WIDTH_OF_CONV/2]


    """
    plt.plot(range(len(convole_window)),convole_window)
    plt.plot(range(len(data[:,2])),data[:,2])
    """
    d=convole_window - data[:,2]
    plt.plot(time,d)
    plt.plot(time,convole_window)
    zeroCross = (-np.sign(d[:-1]*d[1:])+1)/2
    zcc = np.convolve(zeroCross, np.transpose(np.ones(WIDTH_OF_ZCONV)/WIDTH_OF_ZCONV))
    zccw =zcc[WIDTH_OF_ZCONV/2:(len(data[:,2]) + WIDTH_OF_ZCONV/2)]

#    w=np.nonzero(zccw>0)
#    print(w)
 #   plt.plot(time(w),np.ones(len(w)),'o')
 #   plt.plot(time,zccw*10000)

    plt.xlabel('Time [mintues]')
    plt.ylabel('Pressure index [abt units]')
    plt.show()
