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

    print(sim.flight_run.kinematics_dynamics.TYPE_ALTITUDE)

    f = open(str(os.path.join('Result', "OF.txt")), "a")
    f.write("\n" + format(OF,'.4f'))
    f.close()
    f = open(str(os.path.join('Result', "apogee.txt")), "a")
    f.write("\n" + format(apogee,'.4f'))
    f.close()

def effect_of_Pcc(Pcc):
    Pcc = int(Pcc)

    area_ratio = 2
    while Simulation(7.44, 1.86, 6, Pcc, area_ratio, run_OpenRocket=False).cea.P_e > 14:
        area_ratio += 0.02

    sim = Simulation(7.44, 1.86, 6, Pcc, area_ratio, run_OpenRocket=False)
    #apogee = max(sim.flight_run.kinematics_dynamics.TYPE_ALTITUDE)
    Isp = sim.Isp

    print(Pcc,area_ratio, Simulation(7.44, 1.86, 6, Pcc, area_ratio, run_OpenRocket=False).cea.P_e, Isp, sep="\t")

    f = open(str(os.path.join('Result', "Pcc.txt")), "a")
    f.write("\n" + format(Pcc,'.4f'))
    f.close()
    f = open(str(os.path.join('Result', "Isp.txt")), "a")
    f.write("\n" + format(Isp,'.4f'))
    f.close()


def effect_of_burntime(burn_time,efficiency=90):
    burn_time = float(burn_time)
    efficiency = int(efficiency)
    OF = 4
    prop_mass = 9.3
    ox_mass = prop_mass/(OF+1)*OF
    fuel_mass = prop_mass/OF

    sim = Simulation(ox_mass, fuel_mass, burn_time, 300, 3.6, efficiency=efficiency/100.0)
    thrust = sim.thrust
    apogee = max(sim.flight_run.kinematics_dynamics.TYPE_ALTITUDE)
    mach = max(sim.flight_run.kinematics_dynamics.TYPE_MACH_NUMBER)

    print(thrust, apogee, mach)

    f = open(str(os.path.join('Result', "burn_time.txt")), "a")
    f.write("\n" + format(burn_time,'.4f'))
    f.close()
    f = open(str(os.path.join('Result', "thrust.txt")), "a")
    f.write("\n" + format(thrust,'.4f'))
    f.close()
    f = open(str(os.path.join('Result', "apogee.txt")), "a")
    f.write("\n" + format(apogee,'.4f'))
    f.close()
    f = open(str(os.path.join('Result', "mach.txt")), "a")
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
    arg1 = sys.argv[2]
    try:
        arg2 = sys.argv[3]
        print(function, arg1, arg2)
        function(arg1,arg2)
    except:
        function(arg1)