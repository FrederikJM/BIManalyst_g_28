# BIManalyst group 28

# Focus area: Structural
# Claim to evaluate: The height of all slabs is 180mm
# Claim found at: Report: CES_BLD_24_06_STR, pg.1
# Description of the script: The script takes an IFC file as input and filters all beams and isolates HCS-elements from spæncom (whose name starts with EX).
#                            Then the script checks if the height of all these elements is 180mm.
#                            If no errors are found the script outputs "Check complete" otherwise the script will output "The slabs do not have the desired height".
