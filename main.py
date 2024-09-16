import ifcopenshell

from .rules import windowRule
from .rules import doorRule
#from .rules import Number_of_Storeys

#model = ifcopenshell.open("C:\\Users\\User\\Desktop\\BIM 2024\\Assignment 1\\CES_BLD_24_06_STR.ifc")

model = ifcopenshell.open("/Users/frederik/Library/CloudStorage/OneDrive-DanmarksTekniskeUniversitet/Dokumenter/Kandidat bygningsdesign/4. semester/Advanced BIM")



windowResult = windowRule.checkRule(model)
doorResult = doorRule.checkRule(model)
#Number_of_storeysResult = Number_of_storeys.checkRule(model)

print("Window result:", windowResult)
print("Door result:", doorResult)
#print("Storeys results:", Number_of_storeysResult)
