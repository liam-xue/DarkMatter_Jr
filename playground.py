from Sim_Setup import *
from cea import *
from openRocket_flight import *
import numpy
import os

sim = Simulation(7, 2.333, burn_time=8.4, Pcc=350)

cea = CEA(400, 4, area_ratio=3.887)

print("Temperature", cea.Temperatures)
print("SonicVelocities", cea.SonicVelocities)
print("Densities", cea.Densities)