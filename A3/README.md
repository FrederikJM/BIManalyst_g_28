# About the tool
## The problem that the tool solves

In the early design stage of a building, the structural engineer's task is to 
identify all the loads acting on a building. Especially wind load can be tedious 
to determine and simplifications often lead to loads that are too conservative
which in the end has an impact on the amount of material used to keep the 
building stable. 

Therefore, this tool should be an efficient way to determine wind load on a
building.


## The problem is found at...
The problem is found at CES_BLD_24_06_STR p. 8 (pdf=12) and in the appendix
p. 41 (pdf) where wind load is faulty determined! The group has used the values
of the shape coefficents which is equivalent to 1m². For stability calculations,
the values regarding an area of 10m² should be used.  

## Description of the tool
The tool determines wind load on a rectangular building based on an IFC-file.

Firstly, the tool filters out basement levels and looks at the structure which is
located above ground. From the remaining floors, a bounding box around the building
is created. The dimensions of this box are then extracted as the width, length 
, and height.

By these three dimensions, the tool determines the peak velocity pressure, and
the wind loads in zones A, B, C, D, and E.

Lastly, these results are plotted as a wind load plan showcasing the different
loads at the different zones.


Assumptions for wind calculation:
- The calculations are based on DS/EN 1991-1-4 incl. Danish National Annex.
- The terrain is flat.
- The orientation of the building is not taken into account, and wind action is
  not reduced for any wind direction.
- The building is located more than 25km from the west coast of Denmark.
- The terrain category is III.
- Building height should be at least 5m.
- Surrounding structures are not taken into account.
- Reduction by construction factor is not taken into account.
- Reduction in terms of building height (different wind pressures at different 
  heights) is not incorporated.


Assumptions regarding the model (IFC-file):
- The investigated model should contain a column and walls at every edge of the building, 
  and at the top and bottom of the building. If this is not the case uncommenting some
  code in the function will take slabs and beams into account, however, 
  this might increase the calculation time significantly!
- The function filters out any elements related to a building story which
  contains "-" followed by a number this, is done as these stories are 
  assumed to be basement levels located underground and they are not
  relevant in the determination of the pressure coefficients and the peak pressure of the wind load.
- If basement levels are named differently please change this to use
  the function.

The function's name is wind_loading().

INPUT: The function takes an IFC-file as the input.

OUTPUT: The function outputs the extracted outer dimensions of the building, 
        reports the determined wind pressure in the different zones for
        two wind directions and makes two plots illustrating the wind action
        on the building. 

### Overview of the function


![Picture1](https://github.com/FrederikJM/BIManalyst_g_28/blob/main/A3/BPMN.svg)<br>


## Instructions to run the tool
To run the tool please follow the steps below:
- Check that the model you want to investigate satisfies the criteria specified in
  the IDS section of this markdown.
- Open `main.py` and specify the location of the IFC-model as the model_path at line 33.
- Run the script `main.py`.
- Evaluate the text output in the console and the plots. 


# Advanced Building Design
## What Advanced Building Design Stage (A, B, C or D) would your tool be useful?
This tool is to be used in the early design phases where a quick determination
of the wind load on the building is needed, this would be in Design Stages 
A, B, and C.

## What subjects might use it?
This tool is meant to be used by the structural subject.

## What information is required in the model for your tool to work?
Below are stated what criteria should be fulfilled to use the tool
successfully.
- The IFC-file should contain only the geometry of the investigated building.
- The building should not have any cantilever parts.
- The building should have the geometry of a box with vertical outer walls and
  a flat roof.
- The building envelope should not be tapered.
- The IFC-file should have a wall or a column at every edge of the building's plan.
- Basement stories that are located underground should have a name that contains
  "-n", where n is an integer.

# IDS

 



