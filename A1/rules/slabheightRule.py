import ifcopenshell
import ifcopenshell.util.element

def checkRule(model):
    beams = model.by_type('IfcBeam')

    stated_height = 180

    # Isolate the ID's of all HCS in the model
    HCS_list = []

    for entity in beams:
        if entity[2].startswith("EX"):
            HCS_list.append(entity[0])
        else:
            continue
        
    # Pick out the HCS from ID's and check if height is modelled as stated
    for entity in beams:
        if entity[0] in HCS_list:
            psets = ifcopenshell.util.element.get_psets(entity)
            if psets['Dimensions']['Height'] == stated_height:
                continue
            else:
                result = f"The slabs height is not as desired"
                return result
                break

    result = f"Check complete"
    return result




# def checkRule(model):
#     storeys_in_model=len(model.by_type('IfcBuildingStorey'))

#     if storeys_in_model == 1:
#         result = f"There is {storeys_in_model} storey in the model."
#     else:
#         result = f"There are {storeys_in_model} storeys in the model."
    
#     return result