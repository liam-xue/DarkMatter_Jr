from Sim_Setup import *
from cea import *
from openRocket_flight import *
import numpy
import os

sim = Simulation(7, 2.3, burn_time=8.4, Pcc=350)
