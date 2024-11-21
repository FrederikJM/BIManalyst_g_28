"""
Authors:
This script is created by:
    Frederik Jønsson Madsen - S183666
    Maria Deliveri          - S240063
At the Technical Unerversity of Denmark in the period of the Fall 2024 semester.

This script executes the function wind_loading() in the file Wind_load.py,
which should be located in the same folder as this main script.

Please specify the file location as the "model_path".


Assumptions regarding the model (IFC-file):
    The investigated model should contain a column and walls at every edge 
    of the building, and at the top and bottom of the building.
    If this is not the case uncommenting some code in the function
    will take slabs and beams into account, however, this might increase the 
    calculation time significantly!
    The function filters out any elements related to a building storey which
    contains "-" followed by a number this, is done as these stories are 
    assumed to be basement levels located underground and they are not
    relevant in the determination of the pressure coefficients for the wind load.
    If basement levels are named differently please chance this in order to use
    the function.

"""

import ifcopenshell
from pathlib import Path


model_path = Path(r'C:\Users\FJM\OneDrive - Danmarks Tekniske Universitet\Dokumenter\Kandidat bygningsdesign\4. semester\Advanced BIM\General\CES_BLD_24_06_STR.ifc')



if not model_path.is_file():
    raise FileNotFoundError(f"No file found at {model_path}!")


model = ifcopenshell.open(model_path)


from Wind_load import wind_loading

wind_loading(model)

