'''
defines the pdf for the impact parameter
'''

import numpy as np
from scipy.stats import rv_continuous
from scipy.integrate import cumtrapz

from dmsl.convenience import *

def gs(s, a1, a2):
    gs = np.piecewise(s,
                      [s<a1**2, (a1**2<=s) & (s<a2**2), (a2**2<=s) & (s<(a1**2 + a2**2)), (s>(a1**2+a2**2))],
                   [lambda s: -2.*np.sqrt(s)/(a1**2*a2) - 2.*np.sqrt(s)/(a1*a2**2) + np.pi/(a1*a2) + s/(a1**2*a2**2),
                    lambda s: -2.*np.sqrt(s)/(a1**2*a2) -1./a2**2 + 2./(a1*a2)*np.arcsin(a1/np.sqrt(s)) + 2./(a1**2*a2)*np.sqrt(s-a1**2),
                   lambda s:-1./a2**2 + 2./(a1*a2)*np.arcsin(a1/np.sqrt(s)) + 2./(a1**2*a2)*np.sqrt(s-a1**2) - 1./a1**2 + 2./(a1*a2)*np.arcsin(a2/np.sqrt(s))+ 2./(a1*a2**2)*np.sqrt(s - a2**2) - np.pi/(a1*a2) -  s/(a1**2*a2**2),
                   lambda s: 0])
    return gs

def pdf(b,a1,a2,n):
    G = cumtrapz(gs(b**2, a1,a2),x=b**2, initial=0)
    Q = 1-(1-G)**n
    tot = np.gradient(Q, b**2)
    return 2*b*tot
