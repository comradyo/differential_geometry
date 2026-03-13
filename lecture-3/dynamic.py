import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

# Create figure and a 3D axes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Generate initial data for the points (e.g., a simple spiral)
num_points = 50
z_data = np.linspace(0, 10 * np.pi, num_points)
x_data = np.sin(z_data)
y_data = np.cos(z_data)

# Create an initial scatter plot and get the artist object
# The plot function returns a list, we need the first element
scatter = ax.scatter(x_data, y_data, z_data, c=z_data, cmap='viridis')

# Set axis limits
ax.set_xlim([-1.5, 1.5])
ax.set_ylim([-1.5, 1.5])
ax.set_zlim([0, 35]) # Set a larger z-limit for movement

ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')
ax.set_title('Dynamic 3D Scatter Plot')

def update(frame):
    """Update the data for the scatter plot for each frame."""
    # Simulate data change over time (e.g., points moving up)
    new_z = z_data + frame * 0.1
    new_x = np.sin(new_z)
    new_y = np.cos(new_z)

    # Update the data in place. scatter._offsets3d is a tuple of (xs, ys, zs)
    scatter._offsets3d = (new_x, new_y, new_z)

    # You can also update the color if needed
    # scatter.set_array(new_z)

    return scatter, # Return the artist object(s) being updated

# Create the animation
# 'frames' defines the range of values passed to the update function
# 'interval' is the delay between frames in milliseconds
# 'blit=False' is often necessary for 3D plots
#       Для себя: frames - от 0 до 100, и FuncAnimation внутри себя вызывает каждые 50 миллисекунд update, 
#       и передает туда очередной frame
ani = animation.FuncAnimation(fig, update, frames=range(100), interval=50, blit=False)

# To display the animation:
# In a standard Python script:
plt.show()

# In a Jupyter notebook, you might need to use specific magic commands
# like %matplotlib notebook or save it as a video/gif file:
# ani.save('dynamic_3d_plot.gif', writer='pillow')
