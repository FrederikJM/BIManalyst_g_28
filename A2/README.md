## A2a: About our group
Confidence in using Python: 2 <br>
Focus area: Structural <br>
Group 28: Analyst <br>
## A2b: Identification of Claim
Claim Building: #2406 <br> 
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
This tool will be used to generate loads. Gathering information about the locations and geometry is also required. 
#### Use Case Examples 
Although not an exact match, our case might fit to the Use Case Example #8, the engineering analysis, and more specifically, the structural analysis. 
## A2d: Scope the use case
A new tool is needed to easily access and determine the wind load on the structure. 
## A2e: Tool Idea  
The idea for the tool is to easily determine the wind load on a structure based on the outer geometry of the building. An accurate and detailed determination of the wind load is important to secure a safe design. However, in some cases the wind load is simplified on the safe side to ensure easy calculations. With a new tool that easily identifies the wind load acting upon the building an optimal design can be achieved. 
## A2f: Information Requirements 
#### Needed information: 
The outer dimensions of the buildings are needed in order to determine the correct form factors for wind calculation.
The location of the building is important as the surrounding area has an impact on the wind acting on the building.
As the surroundings are not modelled in the IFC an assumption of this will be made. Number of floors and location of floors such that a line load on the individual floors can be determined. 
## A2g: Identify appropriate software licence 
Chosen software license: GPL-3.0<br> ![Picture1](https://github.com/FrederikJM/BIManalyst_g_28/blob/main/A2/BPMN.svg)<br>
![Picture 2](https://github.com/FrederikJM/BIManalyst_g_28/blob/main/A2/BPMN_tool.svg)

 
