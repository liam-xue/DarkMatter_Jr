import sys, os, numpy
from CoolProp.CoolProp import PropsSI
from scipy.optimize import fsolve

# convert all to SI units before using

def get_omega(T_i, P_i):
    v_l = 1/PropsSI("D", "T", T_i, "Q", 0, "N2O")
    v_g = 1/PropsSI("D", "T", T_i, "Q", 1, "N2O")
    v_lgi = v_g - v_l
    v_i = v_l
    c_li = PropsSI("C", "T", T_i, "Q", 0, "N2O")
    h_l = PropsSI("H", "T", T_i, "Q", 0, "N2O")
    h_g = PropsSI("H", "T", T_i, "Q", 1, "N2O")
    h_lgi = h_g - h_l
    return c_li*T_i*P_i/v_i*(v_lgi/h_lgi)**2

def get_mass_flux(T_i, P_i, P_o):
    P_sat = PropsSI("P", "T", T_i, "Q", 0, "N2O")
    omega = get_omega(T_i, P_i)
    omega_sat = get_omega(T_i, P_sat)
    eta_st = 2*omega_sat/(1+2*omega_sat)

    # G_crit,sat
    func = lambda eta_crit: eta_crit**2 + (omega_sat**2 - 2*omega_sat)*(1-eta_crit)**2 + 2*(omega_sat**2)*numpy.log(eta_crit) + 2*(omega_sat**2)*(1-eta_crit)
    eta_crit = fsolve(func,1)[0]
    v_l = 1/PropsSI("D", "T", T_i, "Q", 0, "N2O")
    G_crit_sat = eta_crit / numpy.sqrt(omega_sat) * numpy.sqrt(P_i * 1/v_l);

    # G_low
    eta_sat = P_sat / P_i;
    func = lambda eta_crit_low: (omega_sat+(1/omega_sat)-2)/(2*eta_sat)*(eta_crit_low**2) - 2*(omega_sat-1)*eta_crit_low + omega_sat*eta_sat*numpy.log(eta_crit_low/eta_sat) + 3/2*omega_sat*eta_sat - 1
    eta_crit_low = fsolve(func,1)[0]
    if P_o < eta_crit_low*P_i:
        eta = eta_crit_low
    else:
        print("Combustion Chamber Pressure does not exceed critical pressure drop; flow is not choked\n")
    G_low = numpy.sqrt(P_i/v_l) * numpy.sqrt(2*(1-eta_sat) + 2*(omega_sat*eta_sat*numpy.log(eta_sat/eta) - (omega_sat-1)*(eta_sat-eta)))/(omega_sat*(eta_sat/eta - 1) + 1)

    G = (P_sat/P_i)*G_crit_sat + (1-P_sat/P_i)*G_low;
    return G

if __name__ == "__main__":
    print(get_mass_flux(295, 700*6895, 400*6895))