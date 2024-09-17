import ifcopenshell #Import IFCOpenShell

def checkRule(model):
    storeys_in_model=len(model.by_type('IfcBuildingStorey'))

    if storeys_in_model == 1:
        result = f"There is {storeys_in_model} storey in the model."
    else:
        result = f"There are {storeys_in_model} storeys in the model."
    
    return result



