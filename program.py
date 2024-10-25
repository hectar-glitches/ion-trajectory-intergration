import numpy as np
import matplotlib.pyplot as plt
import random


#listing the constants


# for hydrogen
q = 1.6e-19  # Charge of particle (Coulombs)
m = 9.11e-31  # Mass of particle (kg)
dt = 0.01  # Time step (seconds)


#Moon conditions

TIME = 1
STEP_SIZE = 0.01
STEPS = TIME / STEP_SIZE
INITIAL_X_VELOCITY = 0
INITIAL_Y_VELOCITY = 0
INITIAL_Z_VELOCITY = 0
INITIAL_POSITION = [0,0,0]


def derivatives(state, E, B, q, m):
    """
    Calculate the derivatives of the state vector.
    
    Parameters:
        state (array): The current state vector [x, y, z, vx, vy, vz].
        E (array): Electric field vector [Ex, Ey, Ez].
        B (array): Magnetic field vector [Bx, By, Bz].
        q (float): Charge of the particle.
        m (float): Mass of the particle.
        
    Returns:
        array: The derivatives [dx/dt, dy/dt, dz/dt, dvx/dt, dy/dt, dvz/dt].
    """
    # Extract position and velocity from the state vector
    r = state[0:3]  # Position [x, y, z]
    v = state[3:6]  # Velocity [vx, vy, vz]
    
    # Derivatives of position are the velocity components
    drdt = v  # [vx, vy, vz]
    
    # Calculate velocity derivatives using the Lorentz force equation
    dvdt = (q / m) * (E + np.cross(v, B))  # [ax, ay, az]
    
    # Return the concatenated derivative vector [drdt, dvdt]
    return np.concatenate((drdt, dvdt))

def runge_kutta(state, E, B, q, m, dt):
    """
    Perform a single Runge-Kutta step.
    
    Parameters:
        state (array): The current state vector [x, y, z, vx, vy, vz].
        E (array): Electric field vector [Ex, Ey, Ez].
        B (array): Magnetic field vector [Bx, By, Bz].
        q (float): Charge of the particle.
        m (float): Mass of the particle.
        dt (float): Time step for the simulation.
        
    Returns:
        array: The updated state vector after the Runge-Kutta step.
    """
    # Compute k1
    k1 = dt * derivatives(state, E, B, q, m)
    
    # Compute k2
    k2 = dt * derivatives(state + 0.5 * k1, E, B, q, m)
    
    # Compute k3
    k3 = dt * derivatives(state + 0.5 * k2, E, B, q, m)
    
    # Compute k4
    k4 = dt * derivatives(state + k3, E, B, q, m)
    
    # Update state using the Runge-Kutta formula
    new_state = state + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    
    return new_state

# Initial conditions for position and velocity
state = np.array([0, 0, 0, INITIAL_X_VELOCITY, INITIAL_X_VELOCITY, INITIAL_Z_VELOCITY])  # [x0, y0, z0, vx0, vy0, vz0]

# Fields (assuming they are constant in this example)
E = np.array([0, 0, 0])  # Electric field (N/C)
B = np.array([0, 0, 1])  # Magnetic field (Tesla)

# Run the simulation for N steps

trajectory = []

for i in range(int(STEPS)):
    trajectory.append(state[:3])  # Store position for plotting
    state = runge_kutta(state, E, B, q, m, dt)

# Convert trajectory to a numpy array for easy manipulation
trajectory = np.array(trajectory)


# Create a 2D grid representing a section of the Moon's surface
x = np.linspace(-1000, 1000, 100)  # X-axis range (in km)
y = np.linspace(-1000, 1000, 100)  # Y-axis range (in km)
X, Y = np.meshgrid(x, y)

# Moon surface elevation
Z = np.sin(X / random.randint(50,200)) * np.cos(Y / random.randint(30,70)) * 100  # Example surface undulations

# Plotting the surface with a grid
plt.figure(figsize=(10, 8))
plt.contourf(X, Y, Z, cmap='gray')  # Filled contour plot for the surface
plt.colorbar(label='Surface Elevation (km)')

# Add a grid to represent magnetic field locations (optional)
plt.grid(True, linestyle='--', color='black')

# Example magnetic field vectors (dummy data, replace with real data)
Bx = np.sin(Y / 200)  # Magnetic field component in the X-direction
By = np.cos(X / 200)  # Magnetic field component in the Y-direction

# Plot the magnetic field vectors on top of the surface
plt.quiver(X, Y, Bx, By, color='red', label='Magnetic Field Vectors')

# Customize plot
plt.title('Moon Surface with Magnetic Field Grid')
plt.xlabel('X (km)')
plt.ylabel('Y (km)')
plt.legend()

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Extract the x, y, z positions from the trajectory
x_positions = trajectory[:, 0]
y_positions = trajectory[:, 1]
z_positions = trajectory[:, 2]

# Plot the trajectory
ax.plot(x_positions, y_positions, z_positions, label='Particle Trajectory', color='b')

# Set labels
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_zlabel('Z Position')

# Set a title
ax.set_title('3D Trajectory of Charged Particle')

# Optionally, you can add a legend
ax.legend()

# Show the plot
plt.show()

plt.show()