# Importing methods
import numpy as np
from flask import Flask, render_template, request, flash

# Creating the web application
Flask_App = Flask(__name__)     # Flask Instance

Flask_App.secret_key = 'a_random_secret_key'

@Flask_App.route('/', methods = ['GET'])
def fuel_calculator():
    # Displays the fuel_calculator page accessible at '/'
    return render_template('fuel_calculator.html')

@Flask_App.route('/calculation/', methods = ['POST'])
def calculation():
    # Route where we send the calculator form input
    error = None
    result = None

    # request.form looks for:
    # html tags with matching "name= "
    max_weight = request.form['MaxWeight']
    truck_trailer_weight = request.form['TandT']  
    fuel_density = request.form['FD']
    avg_temp = request.form['Temp']

    try:
        
        # Convert the values into a usable form
        max_weight = float(max_weight)
        truck_trailer_weight = float(truck_trailer_weight)
        fuel_density = float(fuel_density)
        avg_temp = float(avg_temp)

        # Validation: Max Weight should be larger than Truck and Trailer Weight, and both should be non-negative
        if max_weight < 0 or truck_trailer_weight < 0:
            flash("Weights cannot be negative.", "error")
            return render_template('fuel_calculator.html', max_weight = int(max_weight), truck_trailer_weight = int(truck_trailer_weight), fuel_density = fuel_density, avg_temp = avg_temp)

        if max_weight < truck_trailer_weight:
            flash("Max Weight must be larger than the Truck and Trailer Weight.", "error")
            return render_template('fuel_calculator.html', max_weight = int(max_weight), truck_trailer_weight = int(truck_trailer_weight), fuel_density = fuel_density, avg_temp = avg_temp)

        # Calculate kg available to carry
        available_weight = max_weight - truck_trailer_weight

        # Calculate net literage
        net_literage = available_weight / (fuel_density / 1000.0)

        # Calculate VCF
        correction = VCF(fuel_density, avg_temp)

        # Calculate gross literage
        gross_literage = net_literage / correction

        # Return the variables
        return render_template(
            'fuel_calculator.html',
            max_weight = int(np.round(max_weight, 0)),
            truck_trailer_weight = int(np.round(truck_trailer_weight, 0)),
            fuel_density = np.round(fuel_density, 1),
            avg_temp = np.round(avg_temp, 2),
            available_weight = int(np.round(available_weight, 0)),
            net_literage = int(np.round(net_literage, 0)),
            correction = np.round(correction, 4),
            gross_literage = int(np.round(gross_literage, 0)),
            calculation_success = True
        )
        
    except ZeroDivisionError:
        return render_template(
            'fuel_calculator.html',
            calculation_success = False,
            error = "Fuel density cannot be zero."
        )
        
    except ValueError:
        flash("Please enter valid numeric values for all fields.", "error")
        return render_template('fuel_calculator.html')
        
    
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
