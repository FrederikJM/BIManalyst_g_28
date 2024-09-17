import ifcopenshell

from rules import windowRule
from rules import doorRule
from rules import storeysRule



#model = ifcopenshell.open("C:\\Users\\User\\Desktop\\BIM 2024\\Assignment 1\\CES_BLD_24_06_STR.ifc")
#base_dir = r'/Users/frederik/Desktop/CES_BLD_24_06_ARC.ifc'


path_to_model = r'/Users/frederik/Desktop/CES_BLD_24_06_STR.ifc'


model = ifcopenshell.open(path_to_model)

windowResult = windowRule.checkRule(model)
doorResult = doorRule.checkRule(model)
Number_of_storeysResult = Number_of_storeys.checkRule(model)

print("Window result:", windowResult)
print("Door result:", doorResult)
print("Storeys results:", Number_of_storeysResult)
