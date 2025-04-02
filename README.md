# OTE Fuels Calculator

A fuel calculation tool for Of The Earth Fuel Services. The calculator is hosted at: https://otefuels.ca/ote-fuels-calculator.

The purpose of this calculator is to determine the amount of fuel that can be loaded into a tanker without exceeding provincial weight restrictions. This is a preloading tool that can help you pick a **target gross literage** before making on the fly adjustments when loading. The calculator has several inputs required to determine the gross fuel literage to request.

| <div style="width:115px">Input</div>    | Description |
| :-------- | :------- |
| Max Weight (kg)  | The maximum total combined weight (including payload) allowed under regional weight restrictions.   |
| Truck & Trailer Tare Weight (kg) | The combined tare weight of the truck and trailer (excluding payload). This includes the weight of the CDSL and DEF fuel in your fuel tanks. Here you might want to include buffer (e.g. +25 kg) overestimating this weight by a small amount to ensure you remain under the max weight. You should also adjust this value depending on the weight of any snow you are carrying, the actual fuel level at the time you are checked for compliance, etc.     |
| Fuel Density (g/cm³)    | The expected density of the fuel at loading. This value is restricted to between 100 and 1000 g/cm³.    |
| Average Fuel Temperature (°C)    | The expected average temperature of the fuel at loading. This value is restricted to between -50 and 50°C.    |

After entering values for these fields, click **"Calculate"**. The results for the calculation will then be displayed. The most important of these is the **"Target Gross Literage to Request"** which tells you the gross payload you can carry based on the input parameters. However, when loading, the fuel density and temperature may be different from your expectations. The gross literage will then need to be adjusted on the fly based on the actual fuel density and temperature. Simple formulae to do this for **diesel** are as follows:

* Increase the gross literage by 40 L for every 1°C increase in temperature.
* Decrease the gross literage by 40 L for every 1°C decrease in temperature.
* Increase the gross literage by 60 L for every 1 g/cm³ decrease in density.
* Decrease the gross literage by 60 L for every 1 g/cm³ increase in density.

These assume an expected temperature of 15°C and an expected fuel density of 840 g/cm³. For example, if the actual temperature was 7°C and the actual fuel density was 842 g/cm³, then the gross literage adjustment would be -440 L from the gross literage given by the calculator.

Similarly, for **gas** we can use the formulae:

* Increase the gross literage by 75 L for every 1°C increase in temperature.
* Decrease the gross literage by 75 L for every 1°C decrease in temperature.
* Increase the gross literage by 80 L for every 1 g/cm³ decrease in density.
* Decrease the gross literage by 80 L for every 1 g/cm³ increase in density.

These assume an expected temperature of 15°C and an expected fuel density of 725 g/cm³. Note that these formulae are only accurate for actual fuel temperatures and densities that are near the expected temperature and density used to define them. The calculator can be used to set up your own scaling relations centered around other expected fuel temperatures and densities.

Another (**more precise**) way of doing this would be to build a **spreadsheet** of target gross literages that varies with fuel density and temperature using the calculator. This can be done using the **"Spreadsheet"** function. The input fields are the same as with the "Single" version except "Fuel Density" and "Fuel Temperature" now have three input fields corresponding to the minimum value to consider, the maximum value to consider, and the step size. The "step size" is restricted to between 0.5 to 5 g/cm³ for fuel density and 0.5 to 5°C for fuel temperature.

Click **"Calculate"** to generate the spreadsheet. Each entry in the spreadsheet tells you the gross payload you can carry based on the input weights as well as the fuel density and temperature for that cell. The spreadsheet itself can be printed by clicking **"Print"**. By default, the margins and page layout should be set so that the entire table is visible, however, printing in landscape orientation should prevent any issues.

Note that the size of the spreadsheet is restricted due to printing limitations:

* A maximum of 10 fuel densities can be considered at once.
* A maximum of 20 fuel temperatures can be considered at once.

As an example, suppose the max weight was 62500 kg and the truck and trailer tare weight was 20000 kg. In this case, we will use a precision of 1°C for fuel temperature and 1 g/cm³ for fuel density. This should be accurate to within 20 L.

Then for **diesel**, our gross literage targets would be as follows:

https://github.com/jmarchio09/OTEFuelsCalculator/blob/main/static/Example-Spreadsheet.pdf
