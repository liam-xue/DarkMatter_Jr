from cea import *
import numpy
from scipy.optimize import fsolve

class BC:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



#### Inputs

Pcc = 400
OF = 4
prop_mass = 9.25
burn_time = 8.4
area_ratio = 4.2
L_star = 1
chamber_diameter = 0.09

####



print(BC.HEADER, "\n\n\n\tEngine Critical Dimensions Calculator", BC.END)
## Nozzle Sizing Calc
print("Acoustic velocity in ideal gas: a=\\sqrt{kRT}")
cea = CEA(Pcc, OF, area_ratio)
a = cea.SonicVelocities[1]
print("from rocketCEA, a =", BC.BLUE, a, "m/s", BC.END)

m_dot = prop_mass/burn_time
print("\nKnown mass flow rate m_dot =", m_dot, "kg/s")
rho = cea.Densities[1]
print("from rocketCEA, density \\rho =", rho, "kg/m3")
V_dot = m_dot/rho
print("Therefore volumetric flowrate V_dot = m_dot/\\rho =", V_dot, "m3/s")
A = V_dot/a
print("throat area, A = V_dot/a =", BC.GREEN, A, "m^2", BC.END)
throat_diameter = numpy.sqrt(A/numpy.pi)
print("throat diameter, d =", BC.GREEN, throat_diameter, "m", BC.END, "OR", throat_diameter*1000, "mm")
print("exit diameter =", throat_diameter*1000*numpy.sqrt(area_ratio), "mm")

A_x = A
A_y = A*area_ratio
k = cea.exit_MolWt_gamma[1]
func = lambda M_y : A_y/A_x - 1/M_y*numpy.power(((1+(k-1)*M_y*M_y/2)/(1+(k-1)/2)), (k+1)/(k-1)/2)
Ma_e = fsolve(func, 2)
print("\nFrom RPE eq. 3-14, Ma_e =", Ma_e)
Ma_e = cea.MachNumber
print("from rocketCEA, Ma_e =", BC.BLUE, Ma_e, BC.END)
P_e = Pcc/numpy.power(1+0.5*(k-1)*Ma_e*Ma_e,k/(k-1))
print("From RPE eq. 3-13, P_e =", P_e, "psia")
P_e = cea.P_e
print("from rocketCEA, P_e =", BC.BLUE, P_e, "psia", BC.END)

print("Assuming L* =", L_star, "m")
V_c = L_star*A
print("chamber volume, V_c =", V_c, "m^3")
t_s = V_c*cea.Densities[0]/m_dot
print("from RPE eq. 8-10, stay time, t_s =", t_s, "s")
print("chamber sizing:", BC.GREEN, "D =", chamber_diameter, "m; L =", V_c/(numpy.pi*chamber_diameter*chamber_diameter/4), "m", BC.END)

print(BC.BLUE, "\nIn conclusion,", BC.END, "assuming ideal engine, \nOF ratio = ", OF, ":1", sep='')
print("Fuel Mass =", prop_mass/(OF+1), "kg")
print("Ox Mass =", prop_mass/(OF+1)*OF, "kg")
print("Engine Pressure (Chamber) =", Pcc, "psia")
print("Chamber Temp =", cea.Temperatures[0], "K")
print("Exhause Velocity =", Ma_e*cea.SonicVelocities[2], "m/s")
print("Thrust =", m_dot*9.81*cea.Isp, "N")
print("Burn time =", burn_time, "s")
print("Ox flow rate =", prop_mass/(OF+1)*OF/burn_time, "kg/s")
print("Fuel flow rate =", prop_mass/(OF+1)/burn_time, "kg/s")
print("Expansion Ratio =", area_ratio)
print("Exit Mach number =", Ma_e)


print("\n\n\n")