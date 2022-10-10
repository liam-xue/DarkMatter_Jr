#from Sim_Setup import *
from cea import *
from openRocket_flight import *
import numpy
import os

cea = CEA(300, 4, 3.7)
print(cea.Densities)
print([cea.P_c, cea.P_t, cea.P_e])
