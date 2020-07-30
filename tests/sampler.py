'''
Test that sampler works
'''


#from dmsl.sampler import *
from dmsl.emcee_sampler import *
import datetime

nn = 1e3

time1 = datetime.datetime.now()
#print('First let`s do a short run with only magnitude of the acceleration.')
s = Sampler(nstars=int(nn), ntune=int(1e3), nsamples=int(5e3))
print('This took',str(datetime.datetime.now()-time1))


# time1 = datetime.datetime.now()
# print('Now let`s do a real 2D run.')
# print('The current time is {}'.format(time1))
# s = Sampler(nstars=int(nn),ndims=2, ncores=4)
# print('This took',str(datetime.datetime.now()-time1))
