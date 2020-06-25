'''
test full acceleration form
'''

import pymc3 as pm
import numpy as np
import exoplanet as xo

from dmsl.lensing_model import *


with pm.Model() as model:
    r = 1.0
    theta =-np.pi/2
    pmprint(make_xyvec(r,theta))


# with pm.Model() as model:
#     ml = 1.e8
#     b = 0.1
#     vl = 100.
#     btheta = np.pi/2
#     vltheta = np.pi/2
#     print("first test vec expression function")
#     a = alphal_vec_exp(b, vl, btheta, vltheta)
#     print(xo.eval_in_model(a))
#     print("Now test magnitude only alphal")
#     f = alphal(ml, b,vl)
#     print(xo.eval_in_model(f))
#     print("Finally, test the 2D version")
#     c = alphal(ml, b,vl, btheta, vltheta)
#     print(xo.eval_in_model(c))
