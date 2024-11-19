"""
Authors:
This function is created by:
    Frederik Jønsson Madsen - S183666
    Maria Deliveri          - S240063
At the Technical University of Denmark in the period of the Fall 2024 semester.

________________________________________________________________________________
    
The function determines wind load on a rectangular building based on an IFC-file.

The function's name is wind_loading().

INPUT: The function takes an IFC-file as the input.

OUTPUT: The function outputs the extracted outer dimensions of the building, 
        reports the determined wind pressure in the different zones for
        two wind directions and makes two plots illustrating the wind action
        on the building.

Assumptions for wind calculation:
    The calculations are based on DS/EN 1991-1-4 incl. Danish National Annex.
    The terrain is flat.
    The orientation of the building is not taken into account, wind action is
    not reduced for any wind directions.
    The building is located more than 25km from the west coast of Denmark.
    The terrain category is III.
    Building height should be at least 5m.
    Surrounding structures are not taken into account.
    Reduction by construction factor is not taken into account.
    Reduction in terms of building height (different wind pressures 
    at different heights) is not incorporated.


Assumptions regarding the model (IFC-file):
    The investigated model should contain a column and walls at every edge 
    of the building, and at the top and bottom of the building.
    If this is not the case uncommenting the code at lines 128-152
    will take slabs and beams into account, however, this might increase the 
    calculation time significantly!
    The function filters out any elements related to a building storey which
    contains "-" followed by a number this, is done as these stories are 
    assumed to be basement levels located underground and they are not
    relevant in the determination of the pressure coefficients for the wind load.
    

"""
import ifcopenshell
import numpy as np
import ifcopenshell.geom
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import re


def wind_loading(file):
    
    ### IMPORT ###
    ifc_file = file
    
    ### REMOVE BASEMENT LEVELS ###
    def contains_hyphen_number(s):
        return bool(re.search(r'-\d+', s))

    storeys = ifc_file.by_type('IfcBuildingStorey')
    storeys_below_ground = []

    for i in storeys:
        if contains_hyphen_number(i.Name):
            storeys_below_ground.append(i.GlobalId)
    
    storeys_to_delete_ids = storeys_below_ground

    # Loop through the storeys in the model
    for storey_id in storeys_to_delete_ids:
        # Find the storey object by GlobalId
        storey = next((s for s in ifc_file.by_type("IfcBuildingStorey") if s.GlobalId == storey_id), None)

        # Get all inverse relationships for the storey
        related_items = ifc_file.get_inverse(storey)   
                # Loop through related items to delete elements
        for rel in related_items:
            if rel.is_a("IfcRelContainedInSpatialStructure"):
                # Remove each element in RelatedElements
                for element in rel.RelatedElements:
                    #print(f"Deleting element: {element.GlobalId} (Type: {element.is_a()})")
                    ifc_file.remove(element)
                
                # Remove the relationship itself
                ifc_file.remove(rel)

    ### GETTING DIMENSIONS ###
    # Initialize geometry settings
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)       
    # Initialize variables to store min and max coordinates
    min_x = min_y = min_z = float('inf')
    max_x = max_y = max_z = float('-inf')

    # Iterate over all products in the IFC file (could be IfcBuilding, IfcWall, etc.)
    for product in ifc_file.by_type("IfcWall"):
        # Check if the product has a geometry representation
        if product.Representation:
            shape = ifcopenshell.geom.create_shape(settings, product)
            
            # Access the vertices
            vertices = shape.geometry.verts
            for i in range(0, len(vertices), 3):
                x, y, z = vertices[i], vertices[i+1], vertices[i+2]
                min_x, max_x = min(min_x, x), max(max_x, x)
                min_y, max_y = min(min_y, y), max(max_y, y)
                min_z, max_z = min(min_z, z), max(max_z, z)

    for product in ifc_file.by_type("IfcColumn"):
        # Check if the product has a geometry representation
        if product.Representation:
            shape = ifcopenshell.geom.create_shape(settings, product)
            
            # Access the vertices
            vertices = shape.geometry.verts
            for i in range(0, len(vertices), 3):
                x, y, z = vertices[i], vertices[i+1], vertices[i+2]
                min_x, max_x = min(min_x, x), max(max_x, x)
                min_y, max_y = min(min_y, y), max(max_y, y)
                min_z, max_z = min(min_z, z), max(max_z, z)

    # for product in ifc_file.by_type("IfcSlab"):
    #     # Check if the product has a geometry representation
    #     if product.Representation:
    #         shape = ifcopenshell.geom.create_shape(settings, product)
            
    #         # Access the vertices
    #         vertices = shape.geometry.verts
    #         for i in range(0, len(vertices), 3):
    #             x, y, z = vertices[i], vertices[i+1], vertices[i+2]
    #             min_x, max_x = min(min_x, x), max(max_x, x)
    #             min_y, max_y = min(min_y, y), max(max_y, y)
    #             min_z, max_z = min(min_z, z), max(max_z, z)

    # for product in ifc_file.by_type("IfcBeam"):
    #     # Check if the product has a geometry representation
    #     if product.Representation:
    #         shape = ifcopenshell.geom.create_shape(settings, product)
            
    #         # Access the vertices
    #         vertices = shape.geometry.verts
    #         for i in range(0, len(vertices), 3):
    #             x, y, z = vertices[i], vertices[i+1], vertices[i+2]
    #             min_x, max_x = min(min_x, x), max(max_x, x)
    #             min_y, max_y = min(min_y, y), max(max_y, y)
    #             min_z, max_z = min(min_z, z), max(max_z, z)


    # Calculate global dimensions

    X = max_x - min_x
    Y = max_y - min_y
    height = max_z - min_z

    if X>Y:
        length = X
        width = Y
    else:
        length = Y
        width = X

    length_print = round(length,2)
    width_print = round(width,2)
    height_print = round(height,2)
    print("Building Global Dimensions:")
    print(f"Length: {length_print}m")
    print(f"Width: {width_print}m")
    print(f"Height: {height_print}m")


    ############## Determination of the length of A, B and C #########

    e_short = min(length,2*height) 
    e_long = min(width,2*height) 


    L_A_short = e_short/5
    L_A_long = e_long/5


    if e_short > width:
        No_C_short = True
    else:
        No_C_short = False

    if e_long > length:
        No_C_long = True
    else:
        No_C_long = False

    if No_C_short == True:
        L_B_short = width - L_A_short
        L_C_short = 0
    else:
        L_B_short = 4/5*e_short
        L_C_short = width - e_short
        
    if No_C_long == True:
        L_B_long = length - L_A_long
        L_C_long = 0
    else:
        L_B_long = 4/5*e_long
        L_C_long = length - e_long



    ##################################

    z = height

    ### Determining peak wind pressure ###
    # Direction factor
    c_dir = 1 #Assuming worst case

    #Season factor
    c_season = 1 # All year

    #Fundamental value of the basic wind velocity
    v_b0 = 24 # [m/s]

    # Base wind velocity (4.1)
    v_b=c_dir*c_season*v_b0

    # Height variation
    # The "ruhed" of the terrain
    z_0     = 0.3       #[m]
    z_0II   = 0.05    #[m]
    z_min   = 5       #[m]
    k_r = 0.19*(z_0/z_0II)**0.07

    def c_r(z):
        return k_r * np.log(z/z_0)

    # Wind turbulence 
    k_I = 1.0 #The recommended value
    c_0 = 1.0 # Orthography factor, assuming flat surroundings

    def I_v(z):
        return k_I/(c_0*np.log(z/z_0))


    # Mean vind
    def V_m(z):
        return c_r(z)*c_0*v_b


    # Peak wind preassure

    rho_air = 1.25 #[kg/m3]

    def q_p(z):
        return (1+7*I_v(z))*0.5*rho_air*V_m(z)**2/1000 #[kN/m2]

    ########################################

    # Determination of formfactors
    #Create table with form factors
    formfactor = {'h/d': [5, 1, 0.25], 
                  'A':[-1.2,-1.2,-1.2],
                  'B':[-0.8,-0.8,-0.8],
                  'C':[-0.5,-0.5,-0.5],
                  'D':[0.8,0.8,0.7], 
                  'E':[-0.7,-0.5,-0.3],
                  'rho':[0.85,1,1]}
    tab_formfactor = pd.DataFrame(formfactor)

    #Calculate height to depth ratio
    hd_short = height/width
    hd_long = height/length


    ####### Formfactors short direction, wind along the shortest direction #######
    hd = hd_short

    if No_C_short == True:
        formfactor_short = tab_formfactor.drop(tab_formfactor.columns[3], axis=1)
    else:
        formfactor_short = tab_formfactor

    if hd>= 5:
        formfactor_short = formfactor_short.iloc[[0]].reset_index(drop=True)
    elif hd<=0.25:
        formfactor_short = formfactor_short.iloc[[2]].reset_index(drop=True)
    else:
        if No_C_short == True:
            new_row = pd.DataFrame({'h/d': [hd], 
                                    'A':[np.nan],
                                    'B':[np.nan],
                                    'D':[np.nan],
                                    'E':[np.nan],
                                    'rho':[np.nan],})
        else:
            new_row = pd.DataFrame({'h/d': [hd], 
                                    'A':[np.nan],
                                    'B':[np.nan],
                                    'C':[np.nan],
                                    'D':[np.nan],
                                    'E':[np.nan],
                                    'rho':[np.nan],})
        # Adding new row
        formfactor_short = pd.concat([formfactor_short, new_row], ignore_index=True)
        
        #Sort table by h/d values
        formfactor_short = formfactor_short.sort_values(by='h/d', ascending=False)
        
        # Setting interpolation index
        formfactor_short.set_index('h/d', inplace=True)  # Set 'h/d' as the index
        
        #Filling out the table / interpolation
        formfactor_short = formfactor_short.interpolate(method='index').reset_index()
        
        # Extract the row with the form factors
        formfactor_short = formfactor_short.loc[formfactor_short['h/d'] == hd].reset_index(drop=True)



    ####### Formfactors long direction #######
    hd = hd_long


    if No_C_long == True:
        formfactor_long = tab_formfactor.drop(tab_formfactor.columns[3], axis=1)
    else:
        formfactor_long = tab_formfactor

    if hd>= 5:
        formfactor_long = tab_formfactor.iloc[[0]]
    elif hd<=0.25:
        formfactor_short = tab_formfactor.iloc[[2]]
    else:
        if No_C_long == True:
            new_row = pd.DataFrame({'h/d': [hd], 
                                    'A':[np.nan],
                                    'B':[np.nan],
                                    'D':[np.nan],
                                    'E':[np.nan],
                                    'rho':[np.nan],})
        else:
            new_row = pd.DataFrame({'h/d': [hd], 
                                    'A':[np.nan],
                                    'B':[np.nan],
                                    'C':[np.nan],
                                    'D':[np.nan],
                                    'E':[np.nan],
                                    'rho':[np.nan],})
        # Adding new row
        df_long = pd.concat([tab_formfactor, new_row], ignore_index=True)
        
        #Sort table by h/d values
        df_long = df_long.sort_values(by='h/d', ascending=False)
        
        # Setting interpolation index
        df_long.set_index('h/d', inplace=True)  # Set 'h/d' as the index
        
        #Filling out the table / interpolation
        df_long = df_long.interpolate(method='index').reset_index()
        
        # Extract the row with the form factors
        formfactor_long = df_long.loc[df_long['h/d'] == hd].reset_index(drop=True)




    ############ Characteristic wind load #################


    if No_C_short == True:
        wind_load_short = formfactor_short.drop(formfactor_short.columns[[0,5]], axis=1).reset_index(drop=True)*q_p(height)
    else:
        wind_load_short = formfactor_short.drop(formfactor_short.columns[[0,6]], axis=1).reset_index(drop=True)*q_p(height)


    if No_C_long == True:
        wind_load_long = formfactor_long.drop(formfactor_long.columns[[0,5]], axis=1).reset_index(drop=True)*q_p(height)
    else:
        wind_load_long = formfactor_long.drop(formfactor_long.columns[[0,6]], axis=1).reset_index(drop=True)*q_p(height)


    print("")
    print("The wind load for the wind direction acting along the width of the building [kN/m²]:")
    print(wind_load_short)


    print(" ")

    wind_load_long = formfactor_long.drop(formfactor_long.columns[[0,6]], axis=1).reset_index(drop=True)*q_p(height)
    print("The wind load for the wind direction acting along the length of the building [kN/m²]:")
    print(wind_load_long)


    ################################
    ########## PLOT ################
    ################################

    # Scale the size of the loads
    load_scale = 8                  # Make load scale relative to building size

    ######## PLOT of wind along the long length of the building###

    # Wind load magnitudes for each zone (example values, in kN/m^2)

    if No_C_long == True:
        zone_wind_loads = {
            "A": round(wind_load_long.iloc[0,0],2),
            "B": round(wind_load_long.iloc[0,1],2),
            "D": round(wind_load_long.iloc[0,2],2),
            "E": round(wind_load_long.iloc[0,3],2),
        }
    else:
        zone_wind_loads = {
            "A": round(wind_load_long.iloc[0,0],2),
            "B": round(wind_load_long.iloc[0,1],2),
            "C": round(wind_load_long.iloc[0,2],2),
            "D": round(wind_load_long.iloc[0,3],2),
            "E": round(wind_load_long.iloc[0,4],2),
        }

    # Color mapping for wind load intensity (you can adjust the color scale)
    color_map = {
        "D": "red",
        "E": "blue",
        "A": "blue",
        "B": "blue",
        "C": "blue",
    }

    # Create the plot
    fig, ax = plt.subplots(figsize=(8,8))

    # Plot the building outline
    building_rect = patches.Rectangle((0, 0), width, length, 
                                      linewidth=4, edgecolor='black', facecolor='grey', fill=True)
    ax.add_patch(building_rect)

    # Plot the zones around the building
    # Zone D
    ax.add_patch(patches.Rectangle((0, length), width, zone_wind_loads["D"]*load_scale, color=color_map["D"],linewidth=2, alpha=0.6, label="Zone D"))

    # Zone E
    ax.add_patch(patches.Rectangle((0,0), width, zone_wind_loads["E"]*load_scale, color=color_map["E"],linewidth=2, alpha=0.6, label="Zone E"))

    # A Zone left
    ax.add_patch(patches.Rectangle((0, length-L_A_long), zone_wind_loads["A"]*load_scale, L_A_long, color=color_map["A"],linewidth=2, alpha=0.6, label="Zone A"))

    # A Zone right
    ax.add_patch(patches.Rectangle((width, length-L_A_long), -zone_wind_loads["A"]*load_scale, L_A_long, color=color_map["A"],linewidth=2, alpha=0.6, label="Zone A"))

    # B Zone left
    ax.add_patch(patches.Rectangle((0, length-L_A_long-L_B_long), zone_wind_loads["B"]*load_scale, L_B_long, color=color_map["B"],linewidth=2, alpha=0.6, label="Zone B"))

    # B Zone right
    ax.add_patch(patches.Rectangle((width, length-L_A_long-L_B_long), -zone_wind_loads["B"]*load_scale, L_B_long, color=color_map["B"],linewidth=2, alpha=0.6, label="Zone B"))


    if No_C_long == False:
        # C Zone left
        ax.add_patch(patches.Rectangle((0, 0), zone_wind_loads["C"]*load_scale, L_C_long, color=color_map["C"],linewidth=2, alpha=0.6, label="Zone C"))
        
        # C Zone left
        ax.add_patch(patches.Rectangle((width, 0), -zone_wind_loads["C"]*load_scale, L_C_long, color=color_map["C"],linewidth=2, alpha=0.6, label="Zone C"))


    # Add labels and annotations
    if No_C_long == True:
        for zone, load in zone_wind_loads.items():
            if zone == "D":
                ax.text(width / 2, length + zone_wind_loads["D"]*load_scale + 1, f"Zone D = {load} kN/m²", 
                        ha="center", va="center", color=color_map["D"])
            elif zone == "E":
                ax.text(width / 2, zone_wind_loads["E"]*load_scale - 1, f"Zone E = {load} kN/m²", 
                        ha="center", va="center", color=color_map["E"])
            elif zone == "A":
                ax.text(width - zone_wind_loads["A"]*load_scale + 2, length - L_A_long/2, f"Zone A {load} kN/m²", 
                        ha="center", va="center", color=color_map["A"], rotation=90)
            elif zone == "B":
                ax.text(width - zone_wind_loads["B"]*load_scale + 2, length - L_A_long - L_B_long/2, f"Zone B {load} kN/m²", 
                        ha="center", va="center", color=color_map["B"], rotation=90)
            elif zone == "C":
                ax.text(width - zone_wind_loads["C"]*load_scale + 2, L_C_long/2, f"Zone C {load} kN/m²", 
                        ha="center", va="center", color=color_map["C"], rotation=90)
    else:
        for zone, load in zone_wind_loads.items():
            if zone == "D":
                ax.text(width / 2, length + zone_wind_loads["D"]*load_scale + 1, f"Zone D = {load} kN/m²", 
                        ha="center", va="center", color=color_map["D"])
            elif zone == "E":
                ax.text(width / 2, zone_wind_loads["E"]*load_scale - 1, f"Zone E = {load} kN/m²", 
                        ha="center", va="center", color=color_map["E"])
            elif zone == "A":
                ax.text(width - zone_wind_loads["A"]*load_scale + 2, length - L_A_long/2, f"Zone A {load} kN/m²", 
                        ha="center", va="center", color=color_map["A"], rotation=90)
            elif zone == "B":
                ax.text(width - zone_wind_loads["B"]*load_scale + 2, length - L_A_long - L_B_long/2, f"Zone B {load} kN/m²", 
                        ha="center", va="center", color=color_map["B"], rotation=90)
            elif zone == "C":
                ax.text(width - zone_wind_loads["C"]*load_scale + 2, L_C_long/2, f"Zone C {load} kN/m²", 
                        ha="center", va="center", color=color_map["C"], rotation=90)
        
        
    # Set up the plot
    ax.set_xlim(-1.5 * -zone_wind_loads["A"]*load_scale, width + 1.5 * -zone_wind_loads["A"]*load_scale)
    ax.set_ylim(1.5 * -zone_wind_loads["E"]*load_scale, length + 1.5 * zone_wind_loads["D"]*load_scale)
    ax.set_xlabel("Width (m)")
    ax.set_ylabel("Length (m)")
    ax.set_title("Wind along the long direction of the building - Plan View of Wind Load Zones")
    ax.axis('equal')
    ax.grid(True)

    plt.show()



    ######## PLOT along the short direction of the builing ########


    # Wind load magnitudes for each zone in kN/m^2

    if No_C_short == True:
        zone_wind_loads = {
            "A": round(wind_load_short.iloc[0,0],2),
            "B": round(wind_load_short.iloc[0,1],2),
            "D": round(wind_load_short.iloc[0,2],2),
            "E": round(wind_load_short.iloc[0,3],2),
        }
    else:
        zone_wind_loads = {
            "A": round(wind_load_short.iloc[0,0],2),
            "B": round(wind_load_short.iloc[0,1],2),
            "C": round(wind_load_short.iloc[0,2],2),
            "D": round(wind_load_short.iloc[0,3],2),
            "E": round(wind_load_short.iloc[0,4],2),
        }


    # Create the plot
    fig, ax = plt.subplots(figsize=(8,8))

    # Plot the building outline
    building_rect = patches.Rectangle((0, 0), width, length, 
                                      linewidth=4, edgecolor='black', facecolor='grey', fill=True)
    ax.add_patch(building_rect)

    # Plot the zones around the building
    # Zone D
    ax.add_patch(patches.Rectangle((-zone_wind_loads["D"]*load_scale, 0), zone_wind_loads["D"]*load_scale, length, color=color_map["D"],linewidth=2, alpha=0.6, label="Zone D"))

    # Zone E
    ax.add_patch(patches.Rectangle((width - zone_wind_loads["E"]*load_scale,0), zone_wind_loads["E"]*load_scale, length, color=color_map["E"],linewidth=2, alpha=0.6, label="Zone E"))

    # A Zone left
    ax.add_patch(patches.Rectangle((0, zone_wind_loads["A"]*load_scale),L_A_short, -zone_wind_loads["A"]*load_scale, color=color_map["A"],linewidth=2, alpha=0.6, label="Zone A"))

    # A Zone right
    ax.add_patch(patches.Rectangle((0, length), L_A_short, -zone_wind_loads["A"]*load_scale, color=color_map["A"],linewidth=2, alpha=0.6, label="Zone A"))

    # B Zone left
    ax.add_patch(patches.Rectangle((L_A_short,0), L_B_short, zone_wind_loads["B"]*load_scale, color=color_map["B"],linewidth=2, alpha=0.6, label="Zone B"))

    # B Zone right
    ax.add_patch(patches.Rectangle((L_A_short,length), L_B_short, -zone_wind_loads["B"]*load_scale, color=color_map["B"],linewidth=2, alpha=0.6, label="Zone B"))


    if No_C_short == False:
        # C Zone left
        ax.add_patch(patches.Rectangle((width-L_C_short, 0), L_C_short, zone_wind_loads["C"]*load_scale, color=color_map["C"], linewidth=2, alpha=0.6, label="Zone C"))
        
        # C Zone left
        ax.add_patch(patches.Rectangle((width-L_C_short, length), L_C_short, -zone_wind_loads["C"]*load_scale, color=color_map["C"], linewidth=2, alpha=0.6, label="Zone C"))


    # Add labels and annotations

    if No_C_short == True:
        for zone, load in zone_wind_loads.items():
            if zone == "D":
                ax.text( -zone_wind_loads["D"]*load_scale - 1, length / 2, f"Zone D = {load} kN/m²", 
                        ha="center", va="center", color=color_map["D"], rotation=90)
            elif zone == "E":
                ax.text(width - zone_wind_loads["E"]*load_scale + 2, length/2, f"Zone E = {load} kN/m²", 
                        ha="center", va="center", color=color_map["E"], rotation=90)
            elif zone == "A":
                ax.text( L_A_short/2, zone_wind_loads["A"]*load_scale - 2, f"Zone A {load} kN/m²", 
                        ha="center", va="center", color=color_map["A"])
            elif zone == "B":
                ax.text(width - L_B_short/2, zone_wind_loads["B"]*load_scale - 2,  f"Zone B {load} kN/m²", 
                        ha="center", va="center", color=color_map["B"])           
    else:
        for zone, load in zone_wind_loads.items():
            if zone == "D":
                ax.text( -zone_wind_loads["D"]*load_scale - 1, length / 2, f"Zone D = {load} kN/m²", 
                        ha="center", va="center", color=color_map["D"], rotation=90)
            elif zone == "E":
                ax.text(width - zone_wind_loads["E"]*load_scale + 2, length/2, f"Zone E = {load} kN/m²", 
                        ha="center", va="center", color=color_map["E"], rotation=90)
            elif zone == "A":
                ax.text( L_A_short/2, zone_wind_loads["A"]*load_scale - 2, f"Zone A {load} kN/m²", 
                        ha="center", va="center", color=color_map["A"])
            elif zone == "B":
                ax.text(width - L_B_short/2, zone_wind_loads["B"]*load_scale - 2,  f"Zone B {load} kN/m²", 
                        ha="center", va="center", color=color_map["B"])           
            elif zone == "C":
                ax.text(width - L_C_short/2, zone_wind_loads["C"]*load_scale - 2,  f"Zone C {load} kN/m²", 
                        ha="center", va="center", color=color_map["C"])
    # Set up the plot
    ax.set_xlim(-1.5 * -zone_wind_loads["A"]*load_scale, width + 1.5 * -zone_wind_loads["A"]*load_scale)
    ax.set_ylim(1.5 * -zone_wind_loads["E"]*load_scale, length + 1.5 * zone_wind_loads["D"]*load_scale)
    ax.set_xlabel("Width (m)")
    ax.set_ylabel("Length (m)")
    ax.set_title("Wind along the short direction of the building - Plan View of Wind Load Zones")
    ax.axis('equal')
    ax.grid(True)

    plt.show()