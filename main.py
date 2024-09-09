import ifcopenshell

from .rules import windowRule
from .rules import doorRule

model = ifcopenshell.open("path/to/ifcfile.ifc")

storeys_in_model=len(model.by_type('IfcBuildingStorey'))

if storeys_in_model == 1:
    print(f"\nThere is {storeys_in_model} storey in the model.")
else:
    print(f"\nThere are {storeys_in_model} storeys in the model.")


#windowResult = windowRule.checkRule(model)
#doorResult = doorRule.checkRule(model)

#print("Window result:", windowResult)
#print("Door result:", doorResult)
