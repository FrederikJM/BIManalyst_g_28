## Wind load visualization using Matplotlib <br>

### Why is it important?
As engineers, effective communication is often achieved through visual representation of designs. To enhance the clarity of wind load calculations, we incorporated a graphical plot alongside numerical values. This approach allows structural engineers to clearly identify the location and distribution of wind loads on the structure. Specifically, we visualized the floor plan, highlighting the different zones of wind loads and their magnitudes in both directions.<br>
### Step 1
The plot of the applied loads was scaled relative to the size of the building's floor plan to ensure their visibility. A scaling factor of 8 was applied to the loads **(load_scale=8)**.<br>

![Picture 1](https://github.com/FrederikJM/BIManalyst_g_28/blob/main/A4/Picture1.png)
### Step 2
An if statement is used to determine how the plot will be configured based on the zones. It verifies whether a Zone C is present to be plotted and ensures all relevant values are rounded down to two decimal places.<br>
### Step 3
The color scheme for the patches is defined to visually represent the zones and the magnitude of the wind loading.<br>

![Picture 2](https://github.com/FrederikJM/BIManalyst_g_28/blob/main/A4/Picture2.png)
### Step 4
The plot is initialized using **plt.subplots**, which creates a figure and axes. The dimensions of the figure are also specified in this step.
A patch is created using **add.patch**. A rectangle patch is created to represent the building area on the plot. Subsequently, the surrounding zones are plotted based on the same rationale. The presence of Zone C is again checked using an if statement before continuing with the plotting process.<br>

![Picture 3](https://github.com/FrederikJM/BIManalyst_g_28/blob/main/A4/Picture3.png)
### Step 5
Labels for each zone are added and positioned appropriately within the figure.<br>

![Picture 4](https://github.com/FrederikJM/BIManalyst_g_28/blob/main/A4/Picture4.png)
### Step 6
The plot is finalized by setting the axes, labels, title, grid, and other visual elements.<br>

![Picture 5](https://github.com/FrederikJM/BIManalyst_g_28/blob/main/A4/Picture5.png)
### Step 7
Finally, **plt.show()** is called to display the complete figure.<br>


