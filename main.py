import ifcopenshell

from rules import windowRule
from rules import doorRule
from rules import storeysRule
from rules import slabheightRule

path_to_model = r'/Users/frederik/Desktop/CES_BLD_24_06_STR.ifc'

model = ifcopenshell.open(path_to_model)

windowResult = windowRule.checkRule(model)
doorResult = doorRule.checkRule(model)
Number_of_storeysResult = storeysRule.checkRule(model)
SlabHeightResult = slabheightRule.checkRule(model)

print("Window result:", windowResult)
print("Door result:", doorResult)
print("Storeys results:", Number_of_storeysResult)
print("Slab height results:", SlabHeightResult)