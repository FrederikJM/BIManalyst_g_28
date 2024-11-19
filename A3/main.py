"""
This is the main script







"""

import ifcopenshell
from pathlib import Path


model_path = Path(r'C:\Users\FJM\OneDrive - Danmarks Tekniske Universitet\Dokumenter\Kandidat bygningsdesign\4. semester\Advanced BIM\General\CES_BLD_24_06_STR.ifc')



if not model_path.is_file():
    raise FileNotFoundError(f"No file found at {model_path}!")


model = ifcopenshell.open(model_path)


from Wind_load import wind_loading

wind_loading(model)

