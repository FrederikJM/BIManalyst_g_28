# About the tool
## The problem that the tool solves

In the early design stage of a building the structural engineer's task is to 
identify all the loads acting on a building. Especially wind load can be tedious 
to determine and simplifications often lead to loads which are too conservative
which in the end has an impact on the amount of material used to keep the 
building stable. 

Therefore, this tool should be a efficient way to determine wind load on a
building.


## The problem is found at...
The problem is found at CES_BLD_24_06_STR p. 8 (pdf=12) and in the apppendix
p. 41 (pdf) where wind load is faulty determined! The group has used the values
of the shape coefficents which is equivalent to 1m². For stability calculations
the values regarding an area of 10m² should be used.  

## Description of the tool
The tool determines wind load on a rectangular building based on an IFC-file.

Firstly, the tool filters out basement levels and looks at the structure which is
located above ground. From the remaing floors a bounding box around the building
is created. The dimensions of this box is then extracted as the width, length 
and height.

By these three dimensions the tool determines the peak velocity pressure, and
the wind loads in zone A, B, C, D and E.

Lastly these results are plotted as a wind load plan showcasing the different
loads at the different zones.


Assumptions for wind calculation: <br>
- The calculations are based on DS/EN 1991-1-4 incl. Danish National Annex.
- The terrain is flat.
- The orientation of the building is not taken into account, wind action is not reduced for any wind directions.
- The building is located more than 25km from the west coast of Denmark.
- The terrain category is III.
- Building height should be at least 5m.
- Surrounding structures are not taken into account.
- Reduction by construction factor is not taken into account.
- Reduction in terms of building height (different wind pressures at different heights) is not incorporated.


Assumptions regarding the model (IFC-file): <br>
    The investigated model should contain a column and walls at every edge 
    of the building, and at the top and bottom of the building.
    If this is not the case uncommenting some code in the function
    will take slabs and beams into account, however, this might increase the 
    calculation time significantly!
    The function filters out any elements related to a building storey which
    contains "-" followed by a number this, is done as these stories are 
    assumed to be basement levels located underground and they are not
    relevant in the determination of the pressure coefficients for the wind load.
    If basement levels are named differently please chance this in order to use
    the function.

The function's name is wind_loading().

INPUT: The function takes an IFC-file as the input.

OUTPUT: The function outputs the extracted outer dimensions of the building, 
        reports the determined wind pressure in the different zones for
        two wind directions and makes two plots illustrating the wind action
        on the building.


## Instructions to run the tool





# Advanced Building Design

## What Advanced Building Design Stage (A, B, C or D) would your tool be useful?

## What subjects might use it?

## What information is required in the model for your tool to work?


# IDS
Below is stated what criterions should be fulfilled in order to use the tool
successfully.




# OLD_____________________________________

## A2b: Identification of Claim
Claim Building: #2410 <br> 
Issue: Wind loading <br>
Description: We will calculate the wind loads and check if they align with the calculations in the report. <br>
Why we chose this claim: Wind loads are an important part of the design in high buildings especially in Denmark. Since the seismic load is much smaller, the wind load is dominant in horizontal loading. An optimized wind load can minimize the climate impact of the building, as weaker or less material can be used. 
## A2c: Use Case
#### How would this claim be checked?
We will import the model. We will extract information about the main geometry of the building (width, height and length) and the location of the structure (from the coordinates of the elements). We will investigate if there are wind loads in the ifc file. We will calculate the wind loads according to Eurocode 1 based on this information about the structure. We will check if the calculations align with the values in the report. 
#### When would this claim need to be checked?
After the preliminary dimensioning of the elements, in the beginning of structural analysis (load definition). 
#### What information does this claim rely on? 
The wind loads are defined based on the geometry of the structure and the location of the structure. For this we need to extract data from the existing model. 
#### What phase? planning, design, build or operation 
The load calculation is part of the design phase. 
#### What BIM purpose is required? Gather, generate, analyse, communicate or realise? 
Gathering information about the locations and geometry is required. This tool will be analyzing the said information to generate loads.
#### Use Case Examples 
Although not an exact match, our case might fit to the Use Case Example #8, the engineering analysis, and more specifically, the structural analysis. 
## A2d: Scope the use case
A new tool is needed to easily access and determine the wind load on the structure. <br>
![Picture 2](https://github.com/FrederikJM/BIManalyst_g_28/blob/main/A2/BPMN_tool.svg)
## A2e: Tool Idea  
The idea for the tool is to easily determine the wind load on a structure based on the outer geometry of the building. An accurate and detailed determination of the wind load is important to secure a safe design. However, in some cases the wind load is simplified on the safe side to ensure easy calculations. With a new tool that easily identifies the wind load acting upon the building an optimal design can be achieved. <br>
![Picture1](https://github.com/FrederikJM/BIManalyst_g_28/blob/main/A2/BPMN.svg)<br>
## A2f: Information Requirements 
#### Needed information: 
The outer dimensions of the buildings are needed in order to determine the correct form factors for wind calculation.
The location of the building is important as the surrounding area has an impact on the wind acting on the building.
As the surroundings are not modelled in the IFC an assumption of this will be made. Number of floors and location of floors such that a line load on the individual floors can be determined. 
## A2g: Identify appropriate software licence 
Chosen software license: GPL-3.0<br> 


 
