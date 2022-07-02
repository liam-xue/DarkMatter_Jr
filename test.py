from Sim_Setup import *
from matplotlib import pyplot as plt
import numpy as np
import os


def effect_of_OF(OF):
    OF = float(OF)
    prop_mass = 9.333333
    ox_mass = prop_mass/(OF+1)*OF
    fuel_mass = prop_mass/OF

    sim = Simulation(ox_mass, fuel_mass, burn_time=8.4, Pcc=350)
    apogee = max(sim.flight_run.kinematics_dynamics.TYPE_ALTITUDE)

    f = open(str(os.path.join('Result', "OF.txt")), "a")
    f.write("\n" + format(OF,'.4f'))
    f.close()
    f = open(str(os.path.join('Result', "apogee.txt")), "a")
    f.write("\n" + format(apogee,'.4f'))
    f.close()

def effect_of_Pcc(Pcc):
    Pcc = int(Pcc)
    sim = Simulation(7, 2.3333, 8.4, Pcc)
    apogee = max(sim.flight_run.kinematics_dynamics.TYPE_ALTITUDE)

    f = open(str(os.path.join('Result', "Pcc.txt")), "a")
    f.write("\n" + format(Pcc,'.4f'))
    f.close()
    f = open(str(os.path.join('Result', "apogee.txt")), "a")
    f.write("\n" + format(apogee,'.4f'))
    f.close()


def effect_of_burntime(burn_time):
    burn_time = float(burn_time)
    OF = 3
    prop_mass = 9.333333
    ox_mass = prop_mass/(OF+1)*OF
    fuel_mass = prop_mass/OF

    sim = Simulation(ox_mass, fuel_mass, burn_time, Pcc=450)
    apogee = max(sim.flight_run.kinematics_dynamics.TYPE_ALTITUDE)
    mach = max(sim.flight_run.kinematics_dynamics.TYPE_MACH_NUMBER)

    #f = open(str(os.path.join('Result', "burn_time.txt")), "a")
    #f.write("\n" + format(burn_time,'.4f'))
    #f.close()
    f = open(str(os.path.join('Result', "apogee450.txt")), "a")
    f.write("\n" + format(apogee,'.4f'))
    f.close()
    f = open(str(os.path.join('Result', "mach450.txt")), "a")
    f.write("\n" + format(mach,'.4f'))
    f.close()


'''
sim = Simulation(ox_mass=7, fuel_mass=2.333, burn_time=8.4, Pcc=350)
alt = sim.flight_run.kinematics_dynamics.TYPE_ALTITUDE
print(max(alt))

plt.plot(alt)
plt.show()
'''

if __name__ == '__main__':
    import sys
    function = getattr(sys.modules[__name__], sys.argv[1])
    filename = sys.argv[2]
    function(filename)