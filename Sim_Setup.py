from cea import *
from openRocket_flight import *
import numpy
import os

def CleanUp():
    for file in os.listdir("Result"):
        if file.endswith(".txt"):
            print(os.path.join("Result", file))
            with open(os.path.join("Result", file), 'r') as fin:
                data = fin.read().splitlines(True)
            with open(os.path.join("Result", file), 'w') as fout:
                fout.writelines(data[1:])


class Simulation():
    def __init__(self, ox_mass, fuel_mass, burn_time, Pcc, area_ratio=4.5, run_CEA=True, run_OpenRocket=True, efficiency=0.9):
        self.ox_mass = ox_mass
        self.fuel_mass = fuel_mass
        self.burn_time = burn_time
        self.Pcc = Pcc
        self.area_ratio = area_ratio

        self.efficiency = efficiency
        self.engine_file_path = str(os.path.join('Simulation', "utat_test.rse"))

        self.OF = self.ox_mass/self.fuel_mass
        self.ox_rate = self.ox_mass/self.burn_time
        self.fuel_rate = self.fuel_mass/self.burn_time

        self.Run(run_CEA,run_OpenRocket)

    def Run(self, run_CEA, run_OpenRocket):
        if run_CEA:
            self.cea = CEA(Pcc=self.Pcc, OF=self.OF, area_ratio=self.area_ratio)

            print("CEA run complete...")

            self.Isp = self.cea.Isp
            self.thrust = (self.ox_rate+self.fuel_rate)*9.81*self.Isp*self.efficiency

            self.engine_file = '''<engine-database>
 <engine-list>
  <engine  mfg="UTAT" code="utat_test" Type="Liquid" dia="152.400000" len="1802.422055" initWt="22000" propWt="0.000000"
delays="0" auto-calc-mass="0" auto-calc-cg="1" avgrocket.thrust="''' + format(self.thrust,'.6f') + '" peakrocket.thrust="' + format(self.thrust,'.6f') + '" throatDia="29.509696" exitDia="61.089360" Itot="' + format(self.thrust*self.burn_time,'.6f') + '" burn-time="' + format(self.burn_time,'.6f') + '" massFrac="0" engine.Isp_curve="' + format(self.Isp,'.6f') + '" tDiv="10" tStep="-1." tFix="1" FDiv="10" FStep="-1." FFix="1" mDiv="10" mStep="-1." mFix="1" cgDiv="10" cgStep="-1." cgFix="1">\n\n\t<data>\n'

            for i in numpy.linspace(0,self.burn_time,num=100):
                self.engine_file += '\t <eng-data cg="1.1" f="'+ format(self.thrust, '.6f') +'" m="'+ format(22000 - (self.ox_rate+self.fuel_rate)*i*1000, '.6f') +'" t="'+ format(i,'.6f') +'"/>\n'

            self.engine_file += '''\t</data>
  </engine>
 </engine-list>
</engine-database>'''

            try:
                open(self.engine_file_path, "x")
                print("Engine File Created.")
            except:
                print("Engine File Exist\nOverwriting Engine File...")

            f = open(self.engine_file_path, "w")
            f.write(self.engine_file)
            f.close()

        if run_OpenRocket:
            self.flight_run = openRocket_flight("Houbolt_Jr.ork", "utat_test.rse")
            self.flight_run.run()

            print("OpenRocket run complete.")

if __name__ == '__main__':
    import sys
    function = getattr(sys.modules[__name__], sys.argv[1])
    function()