import ifcopenshell #Import IFCOpenShell

def checkRule(model):
    storeys_in_model=len(model.by_type('IfcBuildingStorey'))

    result = storeys_in_model

    return result

    # if storeys_in_model == 1:
    #     result = print(f"\nThere is {storeys_in_model} storey in the model.")
    # else:
    #     result = print(f"\nThere are {storeys_in_model} storeys in the model.")
    
    # return result



