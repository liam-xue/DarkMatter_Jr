from cea import *
from openRocket_flight import *

class Simulation():
    def __init__(self, ox_mass, fuel_mass, burn_time, Pcc, area_ratio=3.887):
        self.ox_mass = ox_mass
        self.fuel_mass = fuel_mass
        self.burn_time = burn_time
        self.Pcc = Pcc
        self.area_ratio = area_ratio

        self.OF = self.ox_mass/self.fuel_mass
        self.ox_rate = self.ox_mass/self.burn_time
        self.fuel_rate = self.fuel_mass/self.burn_time

        print(self.OF)

        self.cea = CEA(Pcc=self.Pcc, OF=self.OF, area_ratio=self.area_ratio)