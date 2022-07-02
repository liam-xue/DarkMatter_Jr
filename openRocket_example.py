"""
*** Refer to the openRocket_flight documentation for a more elaborate description of the code's use ***

- This file uses openRocket_flight.py to run an example simulation from the provided data within OpenRocket.

- Ensure that the .ork and .rse files (in this case, Houbolt_Jr.ork and utat_test.rse) are located within the
  'Simulation' folder. The Simulation folder must be located in the same directory as the code.

- When the simulation has been successfully completed, you will see the message,'Simulation finished'.

- When the variables have been successfully classified and organized, you will see the message,'Variables prepared'.

"""

'''Running the simulation'''

from openRocket_flight import *

flight_run = openRocket_flight("Houbolt_Jr - Copy.ork", "utat_test.rse")  # Input .ork and .rse files used for the simulation
flight_run.run()  # This command will run the simulation through the openRocket_flight.py file.

'''To access the variables received from the simulation, use the following format: flight_run.UTAT_family.TYPE'''

print(flight_run.kinematics_dynamics.TYPE_AOA)
print(flight_run.rocket_properties.TYPE_REFERENCE_LENGTH)