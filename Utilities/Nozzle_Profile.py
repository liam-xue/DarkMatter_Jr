import math
import csv
from csv import reader
from scipy.optimize import fsolve
from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np

#Defining the trig functions in degrees 

def cosd(x):
    return math.cos(math.radians(x))

def acosd(x):
    return math.degrees(math.acos(x))

def sind(x):
    return math.sin(math.radians(x))  

def asind(x):
    return math.degrees(math.asin(x))

def tand(x):
    return math.tan(math.radians(x)) 

print("Input radius of throat [mm], radius of inlet [mm], and inlet angle [degrees] using parameter_check_1(R_t, R_in, inlet_angle)")


def parameter_check_1(R_t, R_in, inlet_angle):
    if R_t >= R_in:                                                                    
        return print("Input failed: R_t >= R_in")
    
    if inlet_angle > 90 or inlet_angle < 0.5:
        return print("Input failed: Stop trying to break my code, fix your inlet angle")
    
    a = 1.5*R_t*sind(inlet_angle - 180) + 2.5*R_t
    if R_in < a:
        return print("Input failed: Angle geometry impossible. Please ensure that inlet radius is greater than", a, "mm")
    
    else:
        parameter_check_1.var1 = R_t
        parameter_check_1.var2 = R_in
        parameter_check_1.var3 = inlet_angle
        
        m = (-1)/(tand(inlet_angle))
        
        a = abs((1/m)*(R_in -(1.5*R_t*sind(inlet_angle - 180) + 2.5*R_t)) + 1.5*R_t*cosd(inlet_angle - 180))
        
        print("With this geometery, the length of the converging section of the nozzle (before the throat) will be ", a, " [mm] long. If this value is too large, try reducing the inlet angle, or increase the inlet radius")
        print("****************************************************************************************************************************")
        print("Please call generate_nozzle and input area ratio, length fraction, gamma, combustion chamber temperature [K], combustion chamber pressure [kPa], the number of converging section (before the throat) data points, the number of diverging section (after the throat) data points")    
        return  

        
        

def generate_nozzle(area_ratio,ln_frac, gamma, cc_t, cc_p, con_points, div_points):
    
    # BRINGING IN R_t, R_in, inlet_angle 
    
    R_t = parameter_check_1.var1
    R_in = parameter_check_1.var2
    inlet_angle = parameter_check_1.var3
    
    # READING IN E/ N FILES 
    
    f = open("N_Nozzle_Profile.txt")
    n_text = f.read()
    N_matrix = n_text.split("\n")
    
    for i in range(0, len(N_matrix)): 
        
        N_matrix[i] = N_matrix[i].split("\t")
        
        N_matrix[i] = [float(item) for item in N_matrix[i]]
            
    f = open("E_Nozzle_Profile.txt")
    e_text = f.read()
    E_matrix = e_text.split("\n")
        
    for i in range(0, len(E_matrix)): 
            
        E_matrix[i] = E_matrix[i].split("\t")
    
        E_matrix[i] = [float(item) for item in E_matrix[i]]    
    
    
    x = [0.6, 0.7, 0.8, 0.9, 1]
    y = [N_matrix[i][0] for i in range(0,len(N_matrix))]
    z = [N_matrix[i][1:] for i in range(0,len(N_matrix))]
    f = interpolate.interp2d(x, y, z, kind='cubic')
    N_angle = f(ln_frac, area_ratio)[0]  
      
    y = [E_matrix[i][0] for i in range(0,len(E_matrix))]
    z = [E_matrix[i][1:] for i in range(0,len(E_matrix))]
    f = interpolate.interp2d(x, y, z, kind='cubic')
    E_angle = f(ln_frac, area_ratio)[0]

    
    #Defining the x-coordinate list 
    
    length_diverging = ln_frac*(((math.sqrt(area_ratio)-1)*R_t)/tand(15))
    
    #define a to be length of connecting tangent line from converging curve, b to be horizontal displacement of converging curv, m to be the slope of the tangent connecting line
    
    m = (-1)/(tand(inlet_angle))
    
    #b = abs(1.5*R_t*cosd(inlet_angle - 180))
    
    a = abs((R_in/m) + (1.5*R_t*cosd(inlet_angle - 180)) -(1.5*R_t*sind(inlet_angle - 180) + 2.5*R_t)/m)
    
         
    length_converging = a
    
    length = abs(length_diverging) + abs(length_converging)
    
    #if spacing = 0.5 mm, generate list on range (-length converging, +length divergering) with length / 0.5 elements 
    #the radius contour generation will now be done "on" this list
    
    x_list_converging = np.linspace(-1*length_converging, 0, con_points)
    x_list_diverging  = np.linspace(0, length_diverging, div_points+1)
    x_list_new = sorted(set(x_list_diverging) - set(x_list_converging))
    x_list = list(x_list_converging) + list(x_list_new)
    
    
    # Generate the first portion of the nozzle contour (straight line portion from the leftmost end to the convergant curve
    
    def curve_1(x):
        
        y_1 = m*x - m*(1.5*R_t*cosd(inlet_angle-180)) + (1.5*R_t*sind(inlet_angle-180) + 2.5*R_t)
        
        return y_1
    
    # Initialising the y_coordinate (radius) list, in [mm]
    
    y_list = []
    
    # Looping over the 0.5 mm spaced x_list and determining the first portion of the curve by evaluating curve_1(x) at each in a certain range of x values. The range of x values will be determined below, for all curve sections that follow:
    
    curve_12_xtrans = 1.5*R_t*cosd(inlet_angle - 180)
    
    curve_23_xtrans = 0 
    
    curve_34_xtrans = 0.382*R_t*cosd(N_angle - 90)   #Defined in TOP documentation 
    
    # First portion of TOP curve 
    
    #counter will be used for all curves
    i = 0
    
    while x_list[i] < curve_12_xtrans:
        
        y_list.append(curve_1(x_list[i]))
        
        i = i+1
    
    #Second Portion of TOP curve 
    
    #x= 1.5*R_t*cosd(t)
    #y= 1.5*R_t*sind(t) + 2.5*R_t
    
    
    def curve_2(x):
        
        y_2 = 1.5*R_t*sind(acosd(-x/(1.5*R_t))-180) + 2.5*R_t
        
        return y_2
    
    while x_list[i] < curve_23_xtrans:
        
        y_list.append(curve_2(x_list[i]))
        
        i = i+1
        
    #Third Potion of TOP curve
    
    def curve_3(x):
        
        y_3 = 0.382*R_t*sind(-acosd(x/(0.382*R_t))) + 1.382*R_t
        
        return y_3
    
    
    while x_list[i] < curve_34_xtrans:
        
        y_list.append(curve_3(x_list[i]))
        
        i = i+1
    
    #Last Portion of TOP curve
    
    #Define (N_x, N_y)
     
    N = [0.382*R_t*cosd(N_angle-90), 1.382*R_t + 0.382*R_t*sind(N_angle-90)]
     
    #2. Define (E_x, E_y)
    
    E = [ln_frac*(((math.sqrt(area_ratio)-1)*R_t)/tand(15)), math.sqrt(area_ratio)*R_t] 
    
    #3. Define (Q_x, Q_y)
    
    m_1 = tand(N_angle)
    m_2 = tand(E_angle)
        
    c_1 = N[1] - m_1*N[0]
    c_2 = E[1] - m_2*E[0]
    
    Q_x = (c_2-c_1)/(m_1-m_2)
    Q_y = (m_1*c_2 - m_2*c_1)/(m_1-m_2)
    
    Q = [Q_x,Q_y]
    
    #4. Define x(t), y(t) for the parametric bezier curves 
    
    def x_D(t):
        return (1-t)*(1-t)*N[0] + 2*(1-t)*t*Q[0] + t*t*E[0]
    
    def y_D(t):
        return (1-t)*(1-t)*N[1] + 2*(1-t)*t*Q[1] + t*t*E[1]     
    
    #5. Define t(x)
    
    def get_t(x):
        return (N[0] - Q[0] + math.sqrt(N[0]*x + E[0]*x - N[0]*E[0] +Q[0]*Q[0] - 2*x*Q[0]))/(N[0]+E[0]-2*Q[0])
    
    t_list = []
    
    for items in x_list:
        if i <= len(x_list) - 1:
            
            if items >= curve_34_xtrans:
                
                y_list.append(y_D(get_t(items)))
        
                i = i+1
    
    #Thermodynamic Property Determination 
    
    zeta = (gamma+1)/(2*(gamma-1))
    mach_list = []
    
    z = 0
    for items in y_list:
        def func(x):
            return [((items)**2 / (R_t)**2) - (((gamma+1)/2)**(-1*zeta))*((((1+((gamma-1)/2)*(x[0]**2))**zeta))/x[0])]
        
        if x_list[z] <= 0:
            mach_list.append(float(fsolve(func, [0.1])))
            z = z+1
            
        else:
            mach_list.append(float(fsolve(func, [10])))
            z = z+1

    pressure_list = []
    
    for items in mach_list:
        def pressure(items):
            return cc_p * ((1 +((gamma-1)/2)*(items**2))**((-1*gamma)/(gamma-1)))
        
        pressure_list.append(float(pressure(items)))
    
    temperature_list = []
        
    for items in mach_list:
        def temperature(items):
            return cc_t * ((1 +((gamma-1)/2)*(items**2))**(-1))
        
        temperature_list.append(float(temperature(items)))   
    
    
    #Curve Plotting
    
    #renormalising x_list so leftmost point = 0
        
    x_list_mod = []
    
    for items in x_list:
        x_list_mod.append(items + a)
     
    f1 = plt.figure()
    
    plt.plot(x_list_mod, y_list, color = 'g')
    plt.title("Nozzle Contour [mm]")
     
    plt.gca().set_aspect('equal', adjustable = 'box')
    plt.draw()
    
    plt.show()
    
    f2 = plt.figure()
    
    plt.plot(x_list_mod, mach_list, color = 'r')
    plt.title("Mach Number Variation")
    plt.draw()
    
    f3 = plt.figure()
    
    plt.plot(x_list_mod, pressure_list, color = 'g')
    plt.title("Pressure Variation [Pa]")
    plt.draw()    
    
    f4 = plt.figure()
    
    plt.plot(x_list_mod, temperature_list, color = 'g')
    plt.title("Temperature Variation [K]")
    plt.draw()    
    
    # plt.show()
    
    #Writing CSV output file
    
    z_list = [0]*len(x_list)
    
    f = open('Nozzle_Spline-Rt'+format(R_t, '.2f')+'-Rin'+format(R_in, '.2f')+'-theta'+format(inlet_angle, '.2f')+'-AR'+format(area_ratio, '.2f')+'-lf'+format(ln_frac, '.2f')+'-gamma'+format(gamma, '.2f')+'.txt', 'w')
    
    writer = csv.writer(f)
    aa = 0
    for items in x_list:
        # writer.writerow([x_list_mod[aa], y_list[aa], z_list[aa], pressure_list[aa]])
        writer.writerow([x_list_mod[aa], y_list[aa], z_list[aa]])
        aa = aa + 1
    
    f.close()    
    
    con_space = length_converging/(con_points -1)
    div_space = length_diverging/(div_points -1)
    d = [ ["Length Converging_________", length_converging, ''],
         ["Length Diverging__________", length_diverging, ''],
         ["Length Total______________", length, ''],
         ["Max Pressure______________", max(pressure_list), x_list_mod[pressure_list.index(max(pressure_list))]],
         ["Max Temperature___________", max(temperature_list), x_list_mod[temperature_list.index(max(temperature_list))]],
         ["Max Mach Value____________", max(mach_list), x_list_mod[mach_list.index(max(mach_list))]],
         ["Length x_list_____________", len(x_list), ''],
         ["Length y_list_____________", len(y_list), ''],
         ["Length mach_list__________", len(mach_list), ''],
         ["Converging Spacing________", con_space, ''],
         ["Diverging Spacing_________", div_space, '']]
         
    print ("{:<8} {:<15} {:<10}".format('Parameter', 'Value', 'Location (if applicable)'))
    
    for v in d:
        one, two, three = v
        print ("{:<8} {:<15} {:<10}".format( one, two, three))    
    
    return print("The output has been written to Nozzle_Spline.txt in the form of NORMALISED X - Y - Z [mm]")

if __name__ == "__main__":
    parameter_check_1(16.75/2,0.09*1000/2,40) 
    generate_nozzle(4.2,1,1.4,3060,2758,100,100)