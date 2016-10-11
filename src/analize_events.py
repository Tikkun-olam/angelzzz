#!/usr/bin/env python
import gzip
import sys
import os.path
import numpy as np
import matplotlib.pyplot as plt
import csv

WIDTH_OF_CONV = 30
if __name__ == "__main__":

    
    data = np.loadtxt(gzip.open(sys.argv[1],"rb"),delimiter=",",skiprows=1)
    
    convolve = np.convolve(data[:,2], np.transpose(np.ones(WIDTH_OF_CONV)/WIDTH_OF_CONV))
    print(data.shape)
    #plt.plot(data[:, 0],data[:, 2])
    #import code; code.interact(local=dict(globals(), **locals())) 
    convole_window =convolve[WIDTH_OF_CONV/2:len(data[:,2]) + WIDTH_OF_CONV/2]
    
    
    """
    plt.plot(range(len(convole_window)),convole_window)
    plt.plot(range(len(data[:,2])),data[:,2])
    """
    plt.plot(range(len(data[:,2])),convole_window - data[:,2])
    plt.plot(range(len(data[:,2])),convole_window)
    
    plt.ylabel('some numbers')
    plt.show()
