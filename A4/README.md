## Wind load visualization using Matplotlib <br>

### Why is it important?
As engineers, effective communication is often achieved through visual representation of designs. To enhance the clarity of wind load calculations, we incorporated a graphical plot alongside numerical values. This approach allows structural engineers to clearly identify the location and distribution of wind loads on the structure. Specifically, we visualized the floor plan, highlighting the different zones of wind loads and their magnitudes in both directions.<br>

Figure x |  Figure y
:-------------------------:|:-------------------------:
![Figure 1](https://github.com/FrederikJM/BIManalyst_g_28/blob/main/A4/Figure%20x.png)|
![Figure 2](https://github.com/FrederikJM/BIManalyst_g_28/blob/main/A4/Figure%20y.png)

### Step 1
The plot of the applied loads was scaled relative to the size of the building's floor plan to ensure their visibility. A scaling factor of 8 was applied to the loads **(load_scale=8)**.<br>
```bash
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
```

### Step 2
An if statement is used to determine how the plot will be configured based on the zones. It verifies whether a Zone C is present to be plotted and ensures all relevant values are rounded down to two decimal places.<br>
### Step 3
The color scheme for the patches is defined to visually represent the zones and the magnitude of the wind loading.<br>

```bash
# Color mapping for wind load intensity (you can adjust the color scale)
color_map = {
    "D": "red",
    "E": "blue",
    "A": "blue",
    "B": "blue",
    "C": "blue",
}
```

### Step 4
The plot is initialized using **plt.subplots**, which creates a figure and axes. The dimensions of the figure are also specified in this step.
A patch is created using **add.patch**. A rectangle patch is created to represent the building area on the plot. Subsequently, the surrounding zones are plotted based on the same rationale. The presence of Zone C is again checked using an if statement before continuing with the plotting process.<br>

```bash
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

```

### Step 5
Labels for each zone are added and positioned appropriately within the figure.<br>

```bash
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
    
    
```

### Step 6
The plot is finalized by setting the axes, labels, title, grid, and other visual elements.<br>

```bash
# Set up the plot
ax.set_xlim(-1.5 * -zone_wind_loads["A"]*load_scale, width + 1.5 * -zone_wind_loads["A"]*load_scale)
ax.set_ylim(1.5 * -zone_wind_loads["E"]*load_scale, length + 1.5 * zone_wind_loads["D"]*load_scale)
ax.set_xlabel("Width (m)")
ax.set_ylabel("Length (m)")
ax.set_title("Wind along the long direction of the building - Plan View of Wind Load Zones")
ax.axis('equal')
ax.grid(True)

plt.show()
```

### Step 7
Finally, **plt.show()** is called to display the complete figure.<br>


