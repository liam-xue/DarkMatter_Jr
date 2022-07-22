from cea import *
import numpy
from scipy.optimize import fsolve
from CoolProp.CoolProp import PropsSI

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

Pcc = 400                       # psia
OF = 4
prop_mass = 9.25                # kg
burn_time = 6                   # s
area_ratio = 4.2
L_star = 1                      # m
chamber_diameter = 0.09         # m

T_inj = 270                     # K
P_inj = 700                     # psia
C_d = 1
Ox_hole_diameter = 1/64.0       # in
L_over_d = 10
injector_diameter = 0.03        # m
fuel_velocity = 20              # m/s


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


## Chamber Sizing Calc
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


## Engine Spec
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


## Injector Sizing Calc
print("\nAssuming injector temperature T_inj =", T_inj, "K")
kappa = numpy.sqrt((P_inj-Pcc)/(PropsSI('P', 'T', T_inj, 'Q', 0, 'N2O')/6894.76-Pcc))
G_SPI = C_d*numpy.sqrt(2*PropsSI('D', 'T', T_inj, 'P', P_inj*6894.76, 'N2O')*(P_inj-Pcc)*6894.76)
G_HEM = C_d*PropsSI('D', 'T', 1000, 'P', Pcc*6894.76, 'N2O')*numpy.sqrt(2*(PropsSI('H','P',P_inj*6894.76,'Q',0,'N2O')-PropsSI('H','P',Pcc*6894.76,'Q',0,'N2O')))
G = (1-1/(1+kappa))*G_SPI + 1/(1+kappa)*G_HEM
print("Mass Flux G =", G, "kg/m2/s")
A_inj_Ox = m_dot/(OF+1)*OF / G
print("Ox injector area =", A_inj_Ox, "m2")
print("Assuming hole size of d =", BC.GREEN, Ox_hole_diameter, "in", BC.END)
print("each hole has A =", numpy.pi*(Ox_hole_diameter/39.37)**2, "m2")
N = A_inj_Ox/(numpy.pi*(Ox_hole_diameter/39.37)**2)
print("We need", BC.GREEN, N, "holes"+BC.END+" with", Ox_hole_diameter/39.37*L_over_d*1000, "mm depth")
print("coverage factor =", BC.BLUE, Ox_hole_diameter/39.37*N/numpy.pi/injector_diameter, BC.END)
print("Assuming Fuel injection velocity of", fuel_velocity, "m/s")
V_dot_fuel = m_dot/(OF+1)/PropsSI('D', 'T', 295, 'P', Pcc*6894.76, 'C2H6O')
print("with mass flow rate", m_dot/(OF+1), "kg/s, aka volume flow rate", V_dot_fuel, "m3/s")
A_inj_fuel = V_dot_fuel / fuel_velocity
print("Area needed =", A_inj_fuel, "m2")
fuel_inj_gap = (numpy.sqrt((numpy.pi/4*injector_diameter**2+A_inj_fuel)*4/numpy.pi)-injector_diameter)/2  # one sided
print("the one-sided gap is", BC.GREEN, fuel_inj_gap*1000, "mm", BC.END)
P_inj_fuel = ((m_dot/(OF+1)/A_inj_fuel/C_d)**2)/2/PropsSI('D', 'T', 295, 'P', Pcc*6894.76, 'C2H6O')/6894.76+Pcc
print("with upstream pressure of", BC.BLUE, P_inj_fuel, "psia", BC.END)



print("\n\n\n")