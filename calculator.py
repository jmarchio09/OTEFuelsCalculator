# Importing methods
import numpy as np
from flask import Flask, render_template, request, flash

# Creating the web application
Flask_App = Flask(__name__)     # Flask Instance

Flask_App.secret_key = 'a_random_secret_key'

@Flask_App.route('/', methods = ['GET'])
def fuel_calculator():
    # Displays the fuel_calculator page accessible at '/'
    return render_template('fuel_calculator.html', single_class = 'active')

@Flask_App.route('/calculate-single/', methods = ['POST'])
def calculate_single():

    # request.form looks for:
    # html tags with matching "name= "
    max_weight = float(request.form['MaxWeight'])
    truck_trailer_weight = float(request.form['TandT'])  
    fuel_density = float(request.form['FuelDensity'])
    fuel_temp = float(request.form['FuelTemp'])
    single_class = 'active'

    # Validation for inputs
    if max_weight <= truck_trailer_weight:
        flash("Truck and trailer weight must be less than max weight.", "error")
        return render_template('fuel_calculator.html', max_weight = int(max_weight), truck_trailer_weight = int(truck_trailer_weight), 
                            fuel_density = fuel_density, fuel_temp = fuel_temp, single_class = single_class)

    # Calculate kg available to carry
    available_weight = max_weight - truck_trailer_weight

    # Calculate net literage
    net_literage = (available_weight / fuel_density) * 1000.0

    # Convert this back to the remaining gross literage to request
    correction = VCF(fuel_density, fuel_temp)
    gross_literage = net_literage / correction

    # Return the variables
    return render_template('fuel_calculator.html',
                           max_weight = int(max_weight),
                           truck_trailer_weight = int(truck_trailer_weight),
                           fuel_density = fuel_density,
                           fuel_temp = fuel_temp,
                           available_weight = int(available_weight),
                           net_literage = int(np.round(net_literage, 0)),
                           correction = np.round(correction, 4),
                           gross_literage = int(np.round(gross_literage, 0)),
                           single_class = single_class,
                           calculation_success_single = True
    )
    
# End of function definition

@Flask_App.route('/calculate-spreadsheet/', methods = ['POST'])
def calculate_spreadsheet():

    # request.form looks for:
    # html tags with matching "name= "
    max_weight = float(request.form['MaxWeight'])
    truck_trailer_weight = float(request.form['TandT'])  
    fuel_density_min = float(request.form['FuelDensityMin'])
    fuel_density_max = float(request.form['FuelDensityMax'])
    fuel_density_step = float(request.form['FuelDensityStep'])
    fuel_temp_min = float(request.form['FuelTempMin'])
    fuel_temp_max = float(request.form['FuelTempMax'])
    fuel_temp_step = float(request.form['FuelTempStep'])
    spread_class = 'active'

    # Validation for inputs
    if max_weight <= truck_trailer_weight:
        flash("Truck and trailer weight must be less than max weight.", "error")
        return render_template('fuel_calculator.html', max_weight = int(max_weight), truck_trailer_weight = int(truck_trailer_weight), fuel_density_min = fuel_density_min,
                               fuel_density_max = fuel_density_max, fuel_density_step = fuel_density_step, fuel_temp_min = fuel_temp_min,
                               fuel_temp_max = fuel_temp_max, fuel_temp_step = fuel_temp_step, spread_class = spread_class)
    if fuel_density_max <= fuel_density_min or fuel_temp_max <= fuel_temp_min:
        flash("Maximum values must be greater than minimum values.", "error")
        return render_template('fuel_calculator.html', max_weight = int(max_weight), truck_trailer_weight = int(truck_trailer_weight), fuel_density_min = fuel_density_min,
                               fuel_density_max = fuel_density_max, fuel_density_step = fuel_density_step, fuel_temp_min = fuel_temp_min,
                               fuel_temp_max = fuel_temp_max, fuel_temp_step = fuel_temp_step, spread_class = spread_class)
    if fuel_density_step > (fuel_density_max - fuel_density_min) or fuel_temp_step > (fuel_temp_max - fuel_temp_min):
        flash("Step sizes must be smaller for the values considered.", "error")
        return render_template('fuel_calculator.html', max_weight = int(max_weight), truck_trailer_weight = int(truck_trailer_weight), fuel_density_min = fuel_density_min,
                               fuel_density_max = fuel_density_max, fuel_density_step = fuel_density_step, fuel_temp_min = fuel_temp_min,
                               fuel_temp_max = fuel_temp_max, fuel_temp_step = fuel_temp_step, spread_class = spread_class)

    # Create the density and temperature lists
    densities = np.arange(fuel_density_min, fuel_density_max + fuel_density_step, fuel_density_step)
    temperatures = np.arange(fuel_temp_min, fuel_temp_max + fuel_temp_step, fuel_temp_step)

    # Filter out values greater than max
    densities = densities[densities <= fuel_density_max]
    temperatures = temperatures[temperatures <= fuel_temp_max]

    # Reverse the densities in the table
    densities = np.flip(densities, axis = 0)

    # Valdiate the size of the output table
    if len(densities) > 10 or len(temperatures) > 20:
        flash("Maximum spreadsheet size is 20 temperatures by 10 densities.", "error")
        return render_template('fuel_calculator.html', max_weight = int(max_weight), truck_trailer_weight = int(truck_trailer_weight), fuel_density_min = fuel_density_min,
                               fuel_density_max = fuel_density_max, fuel_density_step = fuel_density_step, fuel_temp_min = fuel_temp_min,
                               fuel_temp_max = fuel_temp_max, fuel_temp_step = fuel_temp_step, spread_class = spread_class)
    
    # Calculate kg available to carry
    available_weight = max_weight - truck_trailer_weight
    
    # Loop through each entry
    output = np.zeros((len(temperatures), len(densities)), dtype = int)
    for i in range(0, len(temperatures)):
        for j in range(0, len(densities)):

            # Calculate gross literage
            net_literage = (available_weight / densities[j]) * 1000.0
            gross_literage = net_literage / VCF(densities[j], temperatures[i])

            # Update the table
            output[i, j] = int(np.round(gross_literage, 0))

        # End of for loop
    # End of for loop

    # Return the variables
    return render_template('fuel_calculator.html', 
                           max_weight = int(max_weight), 
                           truck_trailer_weight = int(truck_trailer_weight), 
                           fuel_density_min = fuel_density_min,
                           fuel_density_max = fuel_density_max,
                           fuel_density_step = fuel_density_step,
                           fuel_temp_min = fuel_temp_min,
                           fuel_temp_max = fuel_temp_max,
                           fuel_temp_step = fuel_temp_step,
                           temperatures = temperatures,
                           densities = densities,
                           literage = output.tolist(),
                           spread_class = spread_class,
                           calculation_success_spread = True
    )

# End of function definition

# Define a function to calculate the volume correction factor
# given a density and temperature (in g/m^3 and C) respectively
# Note: This assumes a known density at 15°C
def VCF(density, temperature):

    # Calculate the thermal expansion coefficient
    if (density <= 770.0):
        alpha = (346.42278 + 0.43884 * density) / density**2
    elif (770.0 < density < 778.0):
        alpha = -0.0033612 + (2680.32 / density**2)
    elif (778.0 <= density < 839.0):
        alpha = (594.5418 + 0.0 * density) / density**2
    elif (density >= 839.0):
        alpha = (186.9696 + 0.48618 * density) / density**2
    # End of if

    # Calculate the temperature difference (in celsius)
    dT = temperature - 15

    return np.exp(-alpha * dT * (1 + 0.8 * alpha * dT))

# End of function definition

if __name__ == '__main__':
    Flask_App.debug = False
    Flask_App.run()
