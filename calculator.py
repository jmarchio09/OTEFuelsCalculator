# Importing methods
import numpy as np
from flask import Flask, render_template, request, flash

# Creating the web application
Flask_App = Flask(__name__)     # Flask Instance

Flask_App.secret_key = 'a_random_secret_key'

@Flask_App.route('/', methods = ['GET'])
def fuel_calculator():
    # Displays the fuel_calculator page accessible at '/'
    return render_template('fuel_calculator.html', max_weight = None, truck_trailer_weight = None, fuel_density = None,
                           fuel_temp = None, fill_liter = None, avg_temp = None)

@Flask_App.route('/calculation/', methods = ['POST'])
def calculation():

    # request.form looks for:
    # html tags with matching "name= "
    max_weight = float(request.form['MaxWeight'])
    truck_trailer_weight = float(request.form['TandT'])  
    fuel_density = float(request.form['FuelDensity'])
    fuel_temp = float(request.form['FuelTemp'])
    fill_liter = float(request.form['FillLiter'])
    avg_temp = float(request.form["AvgTemp"])

    # Validation for inputs
    if max_weight <= 0.0 or truck_trailer_weight <= 0.0:
        return render_template('fuel_calculator.html', max_weight = int(max_weight), truck_trailer_weight = int(truck_trailer_weight), 
                            fuel_density = fuel_density, fuel_temp = fuel_temp, fill_liter = int(fill_liter), avg_temp = avg_temp)
    elif max_weight <= truck_trailer_weight:
        return render_template('fuel_calculator.html', max_weight = int(max_weight), truck_trailer_weight = int(truck_trailer_weight), 
                            fuel_density = fuel_density, fuel_temp = fuel_temp, fill_liter = int(fill_liter), avg_temp = avg_temp)
    if fuel_density <= 0.0:
        return render_template('fuel_calculator.html', max_weight = int(max_weight), truck_trailer_weight = int(truck_trailer_weight), 
                            fuel_density = fuel_density, fuel_temp = fuel_temp, fill_liter = int(fill_liter), avg_temp = avg_temp)
    elif fuel_density < 100.0 or fuel_density > 1000.0:
        return render_template('fuel_calculator.html', max_weight = int(max_weight), truck_trailer_weight = int(truck_trailer_weight), 
                            fuel_density = fuel_density, fuel_temp = fuel_temp, fill_liter = int(fill_liter), avg_temp = avg_temp)
    if fuel_temp < -50.0 or fuel_temp > 50.0 or avg_temp < -50.0 or avg_temp > 50.0:
        return render_template('fuel_calculator.html', max_weight = int(max_weight), truck_trailer_weight = int(truck_trailer_weight), 
                            fuel_density = fuel_density, fuel_temp = fuel_temp, fill_liter = int(fill_liter), avg_temp = avg_temp)
    if fill_liter < 0.0:
        return render_template('fuel_calculator.html', max_weight = int(max_weight), truck_trailer_weight = int(truck_trailer_weight), 
                            fuel_density = fuel_density, fuel_temp = fuel_temp, fill_liter = int(fill_liter), avg_temp = avg_temp)

    # Calculate kg available to carry
    available_weight = max_weight - truck_trailer_weight

    # Calculate net literage
    net_literage = available_weight / (fuel_density / 1000.0)

    # Calculate the new net literage after removing the gross filled literage
    new_net_literage = net_literage - fill_liter * VCF(fuel_density, avg_temp)

    # Convert this back to the remaining gross literage to request
    correction = VCF(fuel_density, fuel_temp)
    gross_literage = new_net_literage / correction

    if gross_literage < 0.0:
        flash("Specified filled literage results in a negative gross literage to request.", "error")
        return render_template('fuel_calculator.html', max_weight = int(max_weight), truck_trailer_weight = int(truck_trailer_weight), 
                            fuel_density = fuel_density, fuel_temp = fuel_temp, fill_liter = int(fill_liter), avg_temp = avg_temp)

    # Return the variables
    return render_template(
        'fuel_calculator.html',
        max_weight = int(np.round(max_weight, 0)),
        truck_trailer_weight = int(np.round(truck_trailer_weight, 0)),
        fuel_density = np.round(fuel_density, 1),
        fuel_temp = np.round(fuel_temp, 2),
        fill_liter = int(np.round(fill_liter, 0)),
        avg_temp = np.round(avg_temp, 2),
        available_weight = int(np.round(available_weight, 0)),
        net_literage = int(np.round(net_literage, 0)),
        correction = np.round(correction, 4),
        gross_literage = int(np.round(gross_literage, 0)),
        calculation_success = True
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
    Flask_App.debug = True
    Flask_App.run()
