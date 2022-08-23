#from Sim_Setup import *
#from cea import *
from openRocket_flight import *
import numpy
import os

#sim = Simulation(7.44, 1.86, burn_time=6.0, Pcc=300, area_ratio=3.6)
#sim.flight_run.plot()

flight_run = openRocket_flight("Houbolt_Jr.ork", "utat_test.rse")
flight_run.run()

flight_run.rocket_properties.TYPE_MASS
#print(sim.flight_run.rocket_properties.TYPE_MASS)