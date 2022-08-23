import numpy as np
import tkinter as tk
import math
from matplotlib import pyplot as plt

def _custom_plot(x_data, datas_dict, x_label, x_unit, y_label, y_unit, title, style, exclusion):
    datas_dict = {k:v for k,v in datas_dict.items() if k not in exclusion}
    if style=="Combined":
        for label,data in datas_dict.items():
            plt.plot(x_data, data, label=label)
        plt.xlabel(x_label+" "+x_unit)
        plt.ylabel(y_label+" "+y_unit)
        plt.title(title)
        plt.legend()
        plt.show()
    elif style=="Staggered":
        fig, ax = plt.subplots(nrows=len(datas_dict), sharex=True)
        ax[0].set_title(title)
        indx = -1
        for label,data in datas_dict.items():
            indx+=1
            ax[indx].plot(x_data, data)
            ax[indx].set_ylabel(label+" "+y_unit)
        ax[indx].set_xlabel(x_label+" "+x_unit)
        plt.show()
    else:
        print("Please choose a valid style from\n    'Combined'\n    'Staggered'")

def _plot_generalinfo(flight_run, style, exclusion):
    t = flight_run.state_vector[0]
    events_to_annotate = {
        'Recovery device deployment': flight_run.recovery_time,
        'Apogee': flight_run.apogee_time,
    }
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()

    ax1.plot(t, flight_run.state_vector[3], 'b-')
    ax2.plot(t, flight_run.state_vector[6], 'r-')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Altitude (m)', color='b')
    ax2.set_ylabel('Vertical Velocity (m/s)', color='r')
    change_color=lambda ax,col:[x.set_color(col) for x in ax.get_yticklabels()]
    change_color(ax1, 'b')
    change_color(ax2, 'r')

    index_at = lambda time: (np.abs(t - time)).argmin()
    for event, times in events_to_annotate.items():
        for time in times:
            ax1.annotate(event, xy=(time, flight_run.kinematics_dynamics.TYPE_ALTITUDE[index_at(time)]), xycoords='data', xytext=(20, 0), textcoords='offset points',arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
    ax1.grid(True)
    ax1.set_title('General Info')

    plt.show()

def _plot_position(flight_run, style, exclusion):
    t = flight_run.state_vector[0]
    datas_dict = {
        'x Position':flight_run.state_vector[1],
        'y Position':flight_run.state_vector[2],
        'Altitude':flight_run.state_vector[3],
        'l2 normal':np.sqrt(flight_run.state_vector[1]**2 + flight_run.state_vector[2]**2 + flight_run.state_vector[3]**2)
        }
    _custom_plot(t, datas_dict, 'Time', '(s)', 'Position', '(m)', "Position vs. Time Plot", style, exclusion)

def _plot_velocity(flight_run, style, exclusion):
    t = flight_run.state_vector[0]
    datas_dict = {
        'v_x':flight_run.state_vector[4],
        'v_y':flight_run.state_vector[5],
        'v_z':flight_run.state_vector[6],
        'l2 normal':np.sqrt(flight_run.state_vector[4]**2 + flight_run.state_vector[5]**2 + flight_run.state_vector[6]**2)
        }
    _custom_plot(t, datas_dict, 'Time', '(s)', 'Velocity', '(m/s)', "Velocity vs. Time Plot", style, exclusion)

def _plot_acceleration(flight_run, style, exclusion):
    t = flight_run.state_vector[0]
    datas_dict = {
        'a_x':flight_run.state_vector[7],
        'a_y':flight_run.state_vector[8],
        'a_z':flight_run.state_vector[9],
        'l2 normal':np.sqrt(flight_run.state_vector[7]**2 + flight_run.state_vector[8]**2 + flight_run.state_vector[9]**2)
        }
    _custom_plot(t, datas_dict, 'Time', '(s)', 'Acceleration', '(m/s2)', "Acceleration vs. Time Plot", style, exclusion)

def _plot_quaternion(flight_run, style, exclusion):
    t = flight_run.state_vector[0]
    datas_dict = {
        'w':flight_run.state_vector[10],
        'x':flight_run.state_vector[11],
        'y':flight_run.state_vector[12],
        'z':flight_run.state_vector[13]}
    _custom_plot(t, datas_dict, 'Time', '(s)', 'Quaternion', '', "Quaternion vs. Time Plot", style, exclusion)

def _plot_angle(flight_run, style, exclusion):
    t = flight_run.state_vector[0]
    datas_dict = {
        'Pitch':flight_run.euler_angle[0],
        'Yaw':flight_run.euler_angle[1],
        'Roll':flight_run.euler_angle[2]
        }
    _custom_plot(t, datas_dict, 'Time', '(s)', 'Angle', '(rad)', "Euler Angle vs. Time Plot", style, exclusion)

def _plot_omega(flight_run, style, exclusion):
    t = flight_run.state_vector[0]
    datas_dict = {
        'omega_x1':flight_run.state_vector[14],
        'omega_x2':flight_run.state_vector[15],
        'omega_x3':flight_run.state_vector[16],
        'l2 normal':np.sqrt(flight_run.state_vector[14]**2 + flight_run.state_vector[15]**2 + flight_run.state_vector[16]**2)
        }
    _custom_plot(t, datas_dict, 'Time', '(s)', 'Angular Velocity', '(rad/s)', "Angular Velocity vs. Time Plot", style, exclusion)

def _plot_alpha(flight_run, style, exclusion):
    t = flight_run.state_vector[0]
    datas_dict = {
        'alpha_x1':flight_run.state_vector[17],
        'alpha_x2':flight_run.state_vector[18],
        'alpha_x3':flight_run.state_vector[19],
        'l2 normal':np.sqrt(flight_run.state_vector[17]**2 + flight_run.state_vector[18]**2 + flight_run.state_vector[19]**2)}
    _custom_plot(t, datas_dict, 'Time', '(s)', 'Angular Acceleration', '(rad/s2)', "Angular Acceleration vs. Time Plot", style, exclusion)

def _plot_path(flight_run, style, exclusion):
    ax = plt.axes(projection='3d')
    x = flight_run.state_vector[1]
    y = flight_run.state_vector[2]
    z = flight_run.state_vector[3]

    maximum = max(max(x), max(y))
    minimum = min(min(x), min(y))

    maximum = int(math.ceil(maximum / 1000.0)) * 1000
    minimum = abs(int(math.ceil(minimum / 1000.0)) * 1000)

    maximum = max(maximum,minimum)

    ax.plot(x, y, z)
    ax.set_xlim3d([-1*maximum, maximum])
    ax.set_ylim3d([-1*maximum, maximum])
    ax.set_zlim3d([0, int(math.ceil(max(z) / 1000.0)) * 1000])
    plt.show()

def _plot_animation(flight_run, style, exclusion):
    import graphics.engine
    from graphics.item import Item, LineItem
    rocket = Item("Rocket", border='same')
    plane = Item("Plane", prev_item=rocket, border='same')
    trajectory = LineItem("T", [[0,0,0],[0,0,0]], prev_item=plane, color='red')

    canvas = graphics.engine.Engine3D([rocket,plane,trajectory], distance=100, title='Rocket', background='cyan')

    global _animationStep
    _animationStep = 0
    timeMax = flight_run.state_vector[0][-1]
    def animation():
        global _animationStep
        canvas.clear()
        rocket.restore()
        rocket.rotate("y",flight_run.value_of(flight_run.euler_angle[2],_animationStep))
        rocket.rotate("z",np.pi/2-flight_run.value_of(flight_run.euler_angle[0],_animationStep))
        rocket.rotate("y",flight_run.value_of(flight_run.euler_angle[1],_animationStep))
        x = flight_run.value_of(flight_run.euler_axis[0],_animationStep)/100
        y = flight_run.value_of(flight_run.euler_axis[2],_animationStep)/100
        z = flight_run.value_of(flight_run.euler_axis[1],_animationStep)/100
        rocket.move_to((x,y,z))
        trajectory.add_point([x,-y,z])
        _animationStep += 0.05
        canvas.render()
        Round = lambda x, n: eval('"%.'+str(int(n))+'f" % '+repr(int(x)+round(float('.'+str(float(x)).split('.')[1]),n)))
        canvas.screen.image.create_text(10, 10, text='t='+str(Round(_animationStep, 2))+'s', anchor=tk.NW)
        if _animationStep <= timeMax:
            canvas.screen.after(10, animation)

    animation()
    canvas.screen.window.mainloop()

def plot(flight_run, arg="All", style="Combined", exclusion=[]):
    if not flight_run.runned:
        raise Exception("Run the class before calling this function.")
    if type(arg)!=list:
        arg = [arg]
    arg = [elem.lower() for elem in arg]
    if "all" in arg or "generalinfo" in arg:
        _plot_generalinfo(flight_run, style, exclusion)
    if "all" in arg or "position" in arg:
        _plot_position(flight_run, style, exclusion)
    if "all" in arg or "velocity" in arg:
        _plot_velocity(flight_run, style, exclusion)
    if "all" in arg or "acceleration" in arg:
        _plot_acceleration(flight_run, style, exclusion)
    if "all" in arg or "quaternion" in arg:
        _plot_quaternion(flight_run, style, exclusion)
    if "all" in arg or "angle" in arg or "euler angle" in arg:
        _plot_angle(flight_run, style, exclusion)
    if "all" in arg or "omega" in arg:
        _plot_omega(flight_run, style, exclusion)
    if "all" in arg or "alpha" in arg:
        _plot_alpha(flight_run, style, exclusion)
    if "all" in arg or "path" in arg:
        _plot_path(flight_run, style, exclusion)
    if "all" in arg or "3danimation" in arg:
        _plot_animation(flight_run, style, exclusion)
