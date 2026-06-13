import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# 1. Setup the figure and subplots
fig = plt.figure(figsize=(14, 6))
plt.subplots_adjust(bottom=0.25)  # Leave room at the bottom for sliders

# Left plot: 2D Grid
ax2d = fig.add_subplot(1, 2, 1)
ax2d.set_xlim(-3, 3)
ax2d.set_ylim(-3, 3)
ax2d.grid(True)
ax2d.set_title("2D Grid Position")

# Right plot: 3D Surface
ax3d = fig.add_subplot(1, 2, 2, projection='3d')
ax3d.set_xlim(-3, 3)
ax3d.set_ylim(-3, 3)
ax3d.set_zlim(-2, 2)
ax3d.set_title("3D Surface Position")

# 2. Generate and plot static 3D surface data
x_range = np.linspace(-3, 3, 50)
y_range = np.linspace(-3, 3, 50)
X, Y = np.meshgrid(x_range, y_range)
# A simple saddle surface function: Z = sin(X) * cos(Y)
Z = np.sin(X) * np.cos(Y)
ax3d.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6)

# 3. Initialize the moving dots (starting at X=0, Y=0)
init_x, init_y = 0.0, 0.0
init_z = np.sin(init_x) * np.cos(init_y)

# Plot initial 2D dot (returns a list, we take the first element)
dot2d, = ax2d.plot([init_x], [init_y], 'ro', markersize=10, zorder=5)

# Plot initial 3D dot
dot3d, = ax3d.plot([init_x], [init_y], [init_z], 'ro', markersize=10, zorder=10)

# 4. Create UI Sliders
ax_sl_x = plt.axes([0.25, 0.1, 0.5, 0.03])
ax_sl_y = plt.axes([0.25, 0.05, 0.5, 0.03])

slider_x = Slider(ax_sl_x, 'X Coordinate', -3.0, 3.0, valinit=init_x)
slider_y = Slider(ax_sl_y, 'Y Coordinate', -3.0, 3.0, valinit=init_y)

# 5. Define the update function
def update(val):
    # Get current slider positions
    current_x = slider_x.val
    current_y = slider_y.val
    # Calculate corresponding Z on the surface
    current_z = np.sin(current_x) * np.cos(current_y)
    
    # Update 2D dot data
    dot2d.set_data([current_x], [current_y])
    
    # Update 3D dot data (3D lines use set_3d_properties for the Z axis)
    dot3d.set_data([current_x], [current_y])
    dot3d.set_3d_properties([current_z])
    
    # Redraw the canvas to show changes
    fig.canvas.draw_idle()

# Link sliders to the update function
slider_x.on_changed(update)
slider_y.on_changed(update)

plt.show()
