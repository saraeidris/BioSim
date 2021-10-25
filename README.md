# BioSim
This is a modell of the ecosystem on the Rossum Island where carnivores and herbivores reside. 
The ecosystem on Rossumøya is characterized by several different landscape types, lowland, highland and desert. The fauna includes only two species, one species of herbivores (plant eaters), and one of carnivores (predators).

Me and my partner have worked with this project for 1 month only, before we ended the course with an oral presentation. 

### Pause button (GUI)
Added pause button to stop and run simulation. 

(May not work if clicked to early in the simulation. 
Event needs a few seconds to "load". 
If so, restart simulation and try again)

### Island with posibility for disease
We added a possibility for disease on the island if you run check_sim_disease.py. 
Disease input is set to True in BioSim to run 
simulations with pyvid (Pythonvirus disease). Pyvid randomly occurs
some years (on average every 30 years), and will reduce half the animal's weight
instead of the regular yearly weight loss. The chance of being
infected with pyvid increases with the number of animals in the cell.
