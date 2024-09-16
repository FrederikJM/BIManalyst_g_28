import ifcopenshell

from .rules import windowRule
from .rules import doorRule

model = ifcopenshell.open("path/to/ifcfile.ifc")

windowResult = windowRule.checkRule(model)
doorResult = doorRule.checkRule(model)
Number_of_storeysResult = Number_of_storeys.checkRule(model)

print("Window result:", windowResult)
print("Door result:", doorResult)
print("Storeys results:", Number_of_storeysResult)
