# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 23:27:43 2024

@author: User
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 22:50:24 2024

@author: User
"""

# import sys
import ifcopenshell
import numpy as np
import ifcopenshell.geom
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def wind_loading(file):
    
    # Load the IFC file
    ifc_file = ifcopenshell.open(file)

    # Initialize geometry settings
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)

    # Iterate through the IfcBuildingStoreys and filter based on their elevation
    for storey in ifc_file.by_type('IfcBuildingStorey'):
        if storey.Elevation is not None:
            if storey.Elevation==0 or storey.Elevation>0:
                
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

                for product in ifc_file.by_type("IfcSlab"):
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

                for product in ifc_file.by_type("IfcBeam"):
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

                # print("Building Global Dimensions:")
                # print(f"Length: {length}")
                # print(f"Width: {width}")
                # print(f"Height: {height}")
                
                print("Building Global Dimensions:", f"Length: {length}, Width: {width}, Height: {height}")


                # This script determines the wind load on a structure based on a input of the dimensions (width, length and heigth) of the building.


                # Assumptions
                # The terrain is flat
                # The orientation of the building is not taken into account, max wind on all sides
                # The building is placed more than 25km from the A Coast
                # The terrain category is III
                # Building height should be at lA 5m
                # Surrounding structures are not taken into account
                # Reduction by construction factor is not taken into account
                # Reduction in terms of building height (different wind preassure at different heights) is not incorporated





                # #Dimensions
                # width = 24 #[m]
                # length = 45 #[m]
                # height = 72 #[m]


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

                #print("The form factors for the wind direction acting along the width of the building:")
                #print(formfactor_short)



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

                #print("The form factors for the wind direction acting along the length of the building:")
                #print(formfactor_long)



                ############ Characteristic wind load #################


                if No_C_short == True:
                    wind_load_short = formfactor_short.drop(formfactor_short.columns[[0,5]], axis=1).reset_index(drop=True)*q_p(height)
                else:
                    wind_load_short = formfactor_short.drop(formfactor_short.columns[[0,6]], axis=1).reset_index(drop=True)*q_p(height)


                if No_C_long == True:
                    wind_load_long = formfactor_long.drop(formfactor_long.columns[[0,5]], axis=1).reset_index(drop=True)*q_p(height)
                else:
                    wind_load_long = formfactor_long.drop(formfactor_long.columns[[0,6]], axis=1).reset_index(drop=True)*q_p(height)



                print("The wind load for the wind direction acting along the width of the building:")
                print(wind_load_short)


                print(" ")

                wind_load_long = formfactor_long.drop(formfactor_long.columns[[0,6]], axis=1).reset_index(drop=True)*q_p(height)
                print("The wind load for the wind direction acting along the length of the building:")
                print(wind_load_long)


                #sys.exit()######################################################################################################



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
                ax.add_patch(patches.Rectangle((0, length), width, zone_wind_loads["D"]*load_scale, color=color_map["D"], alpha=0.6, label="Zone D"))

                # Zone E
                ax.add_patch(patches.Rectangle((0,0), width, zone_wind_loads["E"]*load_scale, color=color_map["E"], alpha=0.6, label="Zone E"))

                # A Zone left
                ax.add_patch(patches.Rectangle((0, length-L_A_long), zone_wind_loads["A"]*load_scale, L_A_long, color=color_map["A"], alpha=0.6, label="Zone A"))

                # A Zone right
                ax.add_patch(patches.Rectangle((width, length-L_A_long), -zone_wind_loads["A"]*load_scale, L_A_long, color=color_map["A"], alpha=0.6, label="Zone A"))

                # B Zone left
                ax.add_patch(patches.Rectangle((0, length-L_A_long-L_B_long), zone_wind_loads["B"]*load_scale, L_B_long, color=color_map["B"], alpha=0.6, label="Zone B"))

                # B Zone right
                ax.add_patch(patches.Rectangle((width, length-L_A_long-L_B_long), -zone_wind_loads["B"]*load_scale, L_B_long, color=color_map["B"], alpha=0.6, label="Zone B"))


                if No_C_long == False:
                    # C Zone left
                    ax.add_patch(patches.Rectangle((0, 0), zone_wind_loads["C"]*load_scale, L_C_long, color=color_map["C"], alpha=0.6, label="Zone C"))
                    
                    # C Zone left
                    ax.add_patch(patches.Rectangle((width, 0), -zone_wind_loads["C"]*load_scale, L_C_long, color=color_map["C"], alpha=0.6, label="Zone C"))


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


                # Wind load magnitudes for each zone (example values, in N/m^2)

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
                ax.add_patch(patches.Rectangle((-zone_wind_loads["D"]*load_scale, 0), zone_wind_loads["D"]*load_scale, length, color=color_map["D"], alpha=0.6, label="Zone D"))

                # Zone E
                ax.add_patch(patches.Rectangle((width - zone_wind_loads["E"]*load_scale,0), zone_wind_loads["E"]*load_scale, length, color=color_map["E"], alpha=0.6, label="Zone E"))

                # A Zone left
                ax.add_patch(patches.Rectangle((0, zone_wind_loads["A"]*load_scale), -zone_wind_loads["A"]*load_scale, L_A_short, color=color_map["A"], alpha=0.6, label="Zone A"))

                # A Zone right
                ax.add_patch(patches.Rectangle((0, length - zone_wind_loads["A"]*load_scale), -zone_wind_loads["A"]*load_scale, -L_A_short, color=color_map["A"], alpha=0.6, label="Zone A"))

                # B Zone left
                ax.add_patch(patches.Rectangle((L_A_short,0), L_B_short, zone_wind_loads["B"]*load_scale, color=color_map["B"], alpha=0.6, label="Zone B"))

                # B Zone right
                ax.add_patch(patches.Rectangle((L_A_short,length), L_B_short, -zone_wind_loads["B"]*load_scale, color=color_map["B"], alpha=0.6, label="Zone B"))


                if No_C_short == False:
                    # C Zone left
                    ax.add_patch(patches.Rectangle((width-L_C_short, 0), L_C_short, zone_wind_loads["C"]*load_scale, color=color_map["C"], alpha=0.6, label="Zone C"))
                    
                    # C Zone left
                    ax.add_patch(patches.Rectangle((width-L_C_short, length), L_C_short, -zone_wind_loads["C"]*load_scale, color=color_map["C"], alpha=0.6, label="Zone C"))


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

#Example
wind_loading(r'C:\Users\User\Desktop\BIM 2024\Assignment 3\CES_BLD_24_10_ARC.ifc')
                
            
    