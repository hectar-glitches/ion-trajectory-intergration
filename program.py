import numpy as np
import matplotlib.pyplot as plt
import random

random.seed(5)

TIME = 0.000002
ELECTRIC_FIELD = 20
MAGNETIC_FIELD = 1e-5

#for hydrogen
q = 1.6e-19  # Charge of particle (Coulombs)
m = 9.11e-31  # Mass of particle (kg)

dt = 0.0000001  # Time step (seconds)

TIME = 1

STEPS = (TIME / dt)
INITIAL_X_VELOCITY = 1
INITIAL_Y_VELOCITY = 1  
INITIAL_Z_VELOCITY = 0.2  
INITIAL_POSITION = [0, 0, 0]

def electric_field(position):

    z = position[2]
    transition_height = 15

    mean = ELECTRIC_FIELD

    if z <= transition_height:
        strength = -mean + mean * z / transition_height

    else:
        strength = mean + (z - transition_height)  

    return np.array([0, 0, strength])

def magnetic_field(position):

    mean = MAGNETIC_FIELD
    std_dev = 0.00005
    bias_value = np.random.normal(mean, std_dev)

    return np.array([0, 0, 0.0001]) + bias_value * position 

def derivatives(state, q, m):
    """Calculate the derivatives of the state vector."""
    r = state[0:3]
    v = state[3:6]
    E = electric_field(r)
    B = magnetic_field(r)
    drdt = v
    dvdt = (q / m) * (E + np.cross(v, B)) 
    
    return np.concatenate((drdt, dvdt))

def runge_kutta(state):
    """Perform a single Runge-Kutta step"""

    k1 = dt * derivatives(state, q, m)
    k2 = dt * derivatives(state + 0.5 * k1, q, m)
    k3 = dt * derivatives(state + 0.5 * k2, q, m)
    k4 = dt * derivatives(state + k3, q, m)
    
    new_state = state + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return new_state

state = np.array([0, 0, 0, 0.3, 0.1, 0.1])

trajectory = []
for _ in range(int(STEPS)):
    trajectory.append(state[:3])  # Store position for plotting
    state = runge_kutta(state)

# Convert trajectory to a numpy array for easy manipulation
trajectory = np.array(trajectory)


# Create a 2D grid representing a section of the Moon's surface
x = np.linspace(-10, 10, 10)  # X-axis range (in km)
y = np.linspace(-10, 10, 10)  # Y-axis range (in km)
X, Y = np.meshgrid(x, y)

# Moon surface elevation
Z = (X / 150) * np.sin(Y / 100) * 100  # Example surface undulations

# Plotting the surface with a grid
plt.figure(figsize=(12, 8))
contour = plt.contourf(X, Y, Z, alpha=0.8)  # Filled contour plot for the surface
plt.colorbar(label='Surface Elevation (km)')

# Add a grid to represent magnetic field locations
plt.grid(True, linestyle='--', color='black')

# Example magnetic field vectors
Bx = np.sin(Y / 20)  # Magnetic field component in the X-direction
By = np.cos(X / 20)  # Magnetic field component in the Y-direction

# Plot the magnetic field vectors on top of the surface
plt.quiver(X, Y, Bx, By, color='red', label='Magnetic Field Vectors')

# Customize plot
plt.title('Moon Surface with Magnetic Field Grid')
plt.xlabel('X (km)')
plt.ylabel('Y (km)')
plt.legend()

# Create a 3D plot for the ion trajectory
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Extract the x, y, z positions from the trajectory
x_positions = trajectory[:, 0]
y_positions = trajectory[:, 1]
z_positions = trajectory[:, 2]

# Adjust z_positions to represent the height above the surface
# Use the elevation from Z (Moon surface) at corresponding (x, y) positions
z_surface = np.sin(x_positions / random.randint(50, 200)) * np.cos(y_positions / random.randint(30, 70)) * 100
z_positions += z_surface + 0.1  

# Plot the ion trajectory
ax.plot(x_positions, y_positions, z_positions, color='red', label='Ion Trajectory', zorder=5)
ax.scatter(x_positions, y_positions, z_positions, color='red', s=20)  # Red dots for trajectory points

# Customize plot
ax.set_title('Ion Trajectory Above Moon Surface')
ax.set_xlabel('X Position (km)')
ax.set_ylabel('Y Position (km)')
ax.set_zlabel('Z Position (km)')
ax.legend()

# Show the 3D trajectory plot
#plt.show()