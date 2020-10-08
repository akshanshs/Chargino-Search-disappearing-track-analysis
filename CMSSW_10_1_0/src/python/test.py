from ROOT import *
import sys
import numpy as np
from DataFormats.FWLite import Events, Handle
import scipy.constants as scc
import math
from glob import glob
from FWCore.ParameterSet.VarParsing import VarParsing
from random import shuffle
from utils import *
import random



def main():
    E = 0
    O = 0
    for x in range(200):
        r =  random.randint(1,2)
        if r == 1: O += 1
        if r == 2: E += 1
    print 'E:', E, 'and O:', O
main()
