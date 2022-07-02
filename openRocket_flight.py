import os
import platform
import shutil

import numpy as np
import tkinter as tk
from matplotlib import pyplot as plt

import orhelper
from orhelper import FlightDataType, FlightEvent


class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def concatenate(arrays):
    ans = []
    for array in arrays:
        if np.ndim(array) == 1:
            ans.append(array)
        else:
            for item in array:
                ans.append(item)
    return np.array(ans)

class openRocket_flight():
    def __init__(self, simulation_file, engine_file=None, file_folder='Simulation'):
        # initialize runned state
        self.runned = False

        # setup simulation file
        self._simulation_file = os.path.join(file_folder, simulation_file)

        # setup engine file
        if (engine_file != None):
            src = str(os.path.join('Simulation', engine_file))
            if (platform.system() == 'Windows'):  # for windows
                dst = str(os.getenv('APPDATA')) + "\\OpenRocket\\ThrustCurves\\"
            elif (platform.system() == 'Darwin'):  # for mac
                dst = str(os.path.expanduser("~/Library/Application Support/OpenRocket/ThrustCurves/"))
            elif (platform.system() == 'Linux'):  # linux
                dst = str(os.path.expanduser("~/.openrocket/ThrustCurves/"))
            else:  # not recognized system
                raise Exception("Unable to store engine file")
            directory = os.path.dirname(dst)
            if not os.path.exists(directory):
                os.makedirs(directory)
            shutil.copy2(src, dst + "utat_test.rse")

        # initialize holders for each family
        self.aerodynamic_coefficients = dotdict()
        self.atmospheric_conditions = dotdict()
        self.forces = dotdict()
        self.kinematics_dynamics = dotdict()
        self.rocket_properties = dotdict()
        self.simulation_information = dotdict()
        self.others = dotdict()

    def run(self):
        # Defining variables for each family
        aerodynamic_coefficients = ['TYPE_FRICTION_DRAG_COEFF', 'TYPE_PRESSURE_DRAG_COEFF', 'TYPE_BASE_DRAG_COEFF',
                                    'TYPE_NORMAL_FORCE_COEFF', 'TYPE_PITCH_MOMENT_COEFF', 'TYPE_YAW_MOMENT_COEFF',
                                    'TYPE_SIDE_FORCE_COEFF', 'TYPE_ROLL_MOMENT_COEFF', 'TYPE_ROLL_FORCING_COEFF',
                                    'TYPE_ROLL_DAMPING_COEFF', 'TYPE_PITCH_DAMPING_MOMENT_COEFF',
                                    'TYPE_YAW_DAMPING_MOMENT_COEFF', 'TYPE_DRAG_COEFF', 'TYPE_AXIAL_DRAG_COEFF']

        atmospheric_conditions = ['TYPE_WIND_VELOCITY', 'TYPE_AIR_TEMPERATURE', 'TYPE_AIR_PRESSURE',
                                  'TYPE_SPEED_OF_SOUND']

        forces = ['TYPE_GRAVITY', 'TYPE_THRUST_FORCE', 'TYPE_DRAG_FORCE']

        kinematics_dynamics = ['TYPE_AOA', 'TYPE_ROLL_RATE', 'TYPE_PITCH_RATE', 'TYPE_YAW_RATE', 'TYPE_MACH_NUMBER',
                               'TYPE_REYNOLDS_NUMBER', 'TYPE_CORIOLIS_ACCELERATION', 'TYPE_POSITION_X',
                               'TYPE_POSITION_Y', 'TYPE_POSITION_XY', 'TYPE_POSITION_DIRECTION', 'TYPE_VELOCITY_XY',
                               'TYPE_ACCELERATION_XY', 'TYPE_LATITUDE', 'TYPE_LONGITUDE', 'TYPE_ORIENTATION_THETA',
                               'TYPE_ORIENTATION_PHI', 'TYPE_VELOCITY_TOTAL', 'TYPE_ACCELERATION_TOTAL',
                               'TYPE_ALTITUDE', 'TYPE_VELOCITY_Z', 'TYPE_ACCELERATION_Z']

        rocket_properties = ['TYPE_REFERENCE_LENGTH', 'TYPE_REFERENCE_AREA', 'TYPE_MASS', 'TYPE_MOTOR_MASS',
                             'TYPE_LONGITUDINAL_INERTIA', 'TYPE_ROTATIONAL_INERTIA', 'TYPE_CP_LOCATION',
                             'TYPE_CG_LOCATION', 'TYPE_STABILITY', 'TYPE_PROPELLANT_MASS']

        simulation_information = ['TYPE_TIME_STEP', 'TYPE_COMPUTATION_TIME', 'TYPE_TIME']

        # simulation
        with orhelper.OpenRocketInstance() as instance:
            print("Begin simulation...",end="\r")

            orh = orhelper.Helper(instance)

            # Load document, run simulation and get data and events
            doc = orh.load_doc(self._simulation_file)
            sim = doc.getSimulation(0)
            orh.run_simulation(sim)

            data = orh.get_timeseries(sim, dir(FlightDataType)[:-4]) # dir returns all valid attributes of the flight data
            self.events = orh.get_events(sim)

            print("Simulation finished.")

        # prepare variables
        print("Preparing variables...",end="\r")
        for t in dir(FlightDataType)[:-4]:
            if t in aerodynamic_coefficients:
                setattr(self.aerodynamic_coefficients, t, data[t])
            elif t in atmospheric_conditions:
                setattr(self.atmospheric_conditions, t, data[t])
            elif t in forces:
                setattr(self.forces, t, data[t])
            elif t in kinematics_dynamics:
                setattr(self.kinematics_dynamics, t, data[t])
            elif t in rocket_properties:
                setattr(self.rocket_properties, t, data[t])
            elif t in simulation_information:
                setattr(self.simulation_information, t, data[t])
            else:  # if not a variable in any simulation type
                setattr(self.others, t, data[t])
                #raise Exception("Unrecognized simulation variable type")

        t = self.simulation_information.TYPE_TIME

        # critical time stamps
        self.begin_time = t[0]
        self.end_time = t[-1]
        self.recovery_time = self.events[FlightEvent.RECOVERY_DEVICE_DEPLOYMENT]
        self.apogee_time = self.events[FlightEvent.APOGEE]

        # position of the rocket wrt the launch site, units in meter and second
        sx = self.kinematics_dynamics.TYPE_POSITION_X
        sy = self.kinematics_dynamics.TYPE_POSITION_Y
        sz = self.kinematics_dynamics.TYPE_ALTITUDE
        vx = np.gradient(sx,t)
        vy = np.gradient(sy,t)
        vz = self.kinematics_dynamics.TYPE_VELOCITY_Z
        ax = np.gradient(vx,t)
        ay = np.gradient(vy,t)
        az = self.kinematics_dynamics.TYPE_ACCELERATION_Z
        self.euler_axis = np.array([sx,sy,sz,vx,vy,vz,ax,ay,az])

        # orientation of the rocket, all angles in radians
        pitch = self.kinematics_dynamics.TYPE_ORIENTATION_THETA
        yaw = self.kinematics_dynamics.TYPE_ORIENTATION_PHI
        roll_i = 0 # assuming the initial roll is 0
        roll = np.array([np.trapz(self.kinematics_dynamics.TYPE_ROLL_RATE[:i], x=t[:i]) for i in range(len(t))]) + roll_i
        self.euler_angle = np.array([pitch,yaw,roll])
        '''
        omega_p = np.gradient(pitch,t)
        omega_y = np.gradient(yaw,t)
        omega_r = self.kinematics_dynamics.TYPE_ROLL_RATE
        alpha_p = np.gradient(omega_p,t)
        alpha_y = np.gradient(omega_y,t)
        alpha_r = np.gradient(omega_r,t)
        self.euler_angles = np.array([pitch,yaw,roll,omega_p,omega_y,omega_r,alpha_p,alpha_y,alpha_r]).T
        # state vector
        self.state_vector = np.concatenate((self.euler_axis,self.euler_angles),axis=1)
        '''
        # quaternions
        phi = yaw
        theta = np.pi/2 - pitch
        psi = roll
        cy = np.cos(phi * 0.5)
        sy = np.sin(phi * 0.5)
        cp = np.cos(theta * 0.5)
        sp = np.sin(theta * 0.5)
        cr = np.cos(psi * 0.5)
        sr = np.sin(psi * 0.5)
        qw = cr * cp * cy + sr * sp * sy;
        qx = sr * cp * cy - cr * sp * sy;
        qy = cr * sp * cy + sr * cp * sy;
        qz = cr * cp * sy - sr * sp * cy;
        self.quaternion = np.array([qw,qx,qy,qz])

        # angular velocity and acceleration
        phi_dot = self.kinematics_dynamics.TYPE_YAW_RATE
        theta_dot = self.kinematics_dynamics.TYPE_PITCH_RATE
        psi_dot = self.kinematics_dynamics.TYPE_ROLL_RATE
        temp_omega = []
        for i in range(len(pitch)):
            M = np.array([[1,0,-1*np.sin(theta[i])],[0,np.cos(phi[i]),np.sin(phi[i])*np.cos(theta[i])],[0,-1*np.sin(phi[i]),np.cos(phi[i])*np.cos(theta[i])]])
            v = np.array([[phi_dot[i]],[theta_dot[i]],[psi_dot[i]]])
            temp_omega.append(np.dot(M,v))
        omega = np.array(temp_omega).T[0]
        alpha = np.array([np.gradient(omega[i],t) for i in range(3)])

        # make state vector in the form of [time, position(xyz), velocity(xyz), acceleration(xyz) ,quaternion(qxyz) ,angular velocity, angular acceleration].T
        # the vector contains 20 variables in total
        self.state_vector = concatenate([t,self.euler_axis,self.quaternion,omega,alpha])

        print("Variables prepared.")

        self.runned = True

    def state_vector_function(self, time):
        if not self.runned:
            raise Exception("Run the class before calling this function.")
        t = self.state_vector[0]
        s = self.state_vector
        if time < t[0] or time > t[-1]:
            print("Given time is out of bounds.")
        return np.array([np.interp(time,t,s[i]) for i in range(len(s))])

    def value_of(self, type, time):
        if not self.runned:
            raise Exception("Run the class before calling this function.")
        t = self.state_vector[0]
        if time < t[0] or time > t[-1]:
            print("Given time is out of bounds.")
        return np.interp(time,t,type)

    def plot(self, arg="All", style="Combined", exclusion=[]):
        import openRocket_plot
        openRocket_plot.plot(self,arg, style, exclusion)
