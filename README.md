# Solar UAV Flight Simulation
This project represents the code to model flight simulations of a Solar Powered UAV design for a Master's project. 
The flight model consists of a 3 degree of freedom model with integrated Solar power dynamics with cloud cover 
forecasting.

## Code Structure

src - Contains the classes to execute the simulations and store the relevant parameters in each subsystem. 
Use 'Simulation' to generate each flight model.

demo - Multiple demos of executed flight models.

    demo/examples/sampleFlight.py # Contains the basic structure to run any style of flight

    demo/monteCarloFlights # Examples of multiple simulations executed and written to an output file

plot - Functions for plotting any executed results.

data - Simulation results and collected cloud forecast data.

## Required Packages

Python version == 3.10

1. numpy
2. scipy
3. matplotlib
4. pandas
5. pvlib
6. math
7. datetime
8. random