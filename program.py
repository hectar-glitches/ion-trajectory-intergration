# %%
# Libraries used
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from math import radians, cos, sin, asin, sqrt
from mpl_toolkits.mplot3d import Axes3D
import pygame
from pygame.locals import QUIT

# %%
# Data file from "https://uknowledge.uky.edu/ees_data/2/#attach_additional_files"
# Columns are : Longitude (degree), Latitude (degree), Br, Btheta, Bphi and Total Field components
file_path = '.../New Magnetic Field Models of the Moon.dat'

# %%
# Functions to read coordinates and magnetic field data
def read_coordinates(index):
    values = []
    with open(file_path, 'r') as file:
        for line in file:
            columns = line.split()
            values.append(float(columns[index]))
    return values

def read_magnetic_field():
    values = []
    with open(file_path, 'r') as file:
        for line in file:
            columns = line.split()
            values.append(float(columns[2]))
    return values

x_values = read_coordinates(0)
y_values = read_coordinates(1)
field = read_magnetic_field()

# %%
# Calculate differences between consecutive values
def calculate_differences(values):
    differences = np.diff(values)
    return differences.min(), differences.max()

x_diff_min, x_diff_max = calculate_differences(x_values)
y_diff_min, y_diff_max = calculate_differences(y_values)

print("Smallest difference between consecutive x-values:", x_diff_min)
print("Largest difference between consecutive x-values:", x_diff_max)
print("Smallest difference between consecutive y-values:", y_diff_min)
print("Largest difference between consecutive y-values:", y_diff_max)

# %%
# Prepare magnetic-field sample data for plotting and simulation.
# Each row is (x_coordinate, y_coordinate, Bz_strength).
position_fields = list(zip(x_values, y_values, field))
position_field_array = np.array(position_fields)

x_unique = np.unique(x_values)
y_unique = np.unique(y_values)

B_grid = np.zeros((len(y_unique), len(x_unique)))

for i in range(len(x_values)):
    x_idx = np.where(x_unique == x_values[i])[0][0]
    y_idx = np.where(y_unique == y_values[i])[0][0]
    B_grid[y_idx, x_idx] = field[i]

plt.figure(figsize=(8, 6))
plt.imshow(B_grid, cmap='Pastel1', origin='lower', aspect='auto')
plt.colorbar(label='Magnetic Field')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Magnetic Field Surfacemap for Reiner Gamma swirl region')
plt.show()

# %%
# Load data into DataFrame and plot heatmap
df = pd.read_csv(file_path, sep="\s+", header=None)
df.columns = ['Longitude (degree)', 'Latitude (degree)', 'Field Value 1', 'Field Value 2', 'Field Value 3', 'Total Field components']

df_localized = df.head(100)
pivot_data = df_localized.pivot(index='Longitude (degree)', columns='Latitude (degree)', values='Total Field components')

sns.heatmap(pivot_data, cmap="viridis", annot=False)
plt.title('Localized Heatmap')
plt.show()

# %%
# Distance calculation functions
MOON_RADIUS = 1738.1 / 1.6093

def distance(lat1, lat2, lon1, lon2):
    lon1, lon2, lat1, lat2 = map(radians, [lon1, lon2, lat1, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    return round(c * MOON_RADIUS, 3)

lat1, lat2 = x_values[1], x_values[1]
lon1, lon2 = y_values[1], y_values[2]
print(f"The distance between two points on the same latitude is {distance(lat1, lat2, lon1, lon2) * 1000} meters")

# %%
# Constants for simulation
INITIAL_X_VELOCITY = 1
INITIAL_Y_VELOCITY = 2
INITIAL_Z_VELOCITY = 1
INITIAL_HEIGHT = 2

dt = 0.01
TIME = 0.1
STEPS = 10
ELECTRIC_FIELD = 20

q = 1.6e-19
m = 9.11e-1

# %%
# Electric field calculation
def electric_field(height):
    transition_height = 15
    mean = ELECTRIC_FIELD
    if height <= transition_height:
        strength = mean * height / transition_height
    else:
        strength = mean + (height - transition_height)
    return np.array([0, 0, strength])

# %%
# 3D distance calculation
def distance_3d(lat1, lat2, lon1, lon2, z1, z2):
    lon1, lon2, lat1, lat2 = map(radians, [lon1, lon2, lat1, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    a = np.clip(a, 0, 1)
    c = 2 * asin(sqrt(a))
    spherical_distance = c * MOON_RADIUS
    vertical_distance = abs(z1 - z2)
    return sqrt(spherical_distance**2 + vertical_distance**2)

# %%
# Derivatives and Runge-Kutta functions
def derivatives(state, q, m, position_field_array, electric_field):
    """
    Compute [dr/dt, dv/dt] using the Lorentz force F = q(E + v x B).

    `position_field_array` is an array-like of magnetic-field samples where each
    row is (x_coordinate, y_coordinate, Bz_strength). The nearest (x, y) sample
    is selected and treated as a local magnetic-field vector [0, 0, Bz_strength].
    """
    position = state[0:3]
    velocity = state[3:6]
    height = position[2]
    E = electric_field(height)
    position_field_array = np.array(position_field_array)
    distance_xy_values = np.linalg.norm(position_field_array[:, 0:2] - position[0:2], axis=1)
    closest_index = np.argmin(distance_xy_values)
    Bz_strength = position_field_array[closest_index, 2]
    B = np.array([0.0, 0.0, Bz_strength])
    total_force = q * (E + np.cross(velocity, B))
    acceleration = total_force / m
    drdt = velocity
    dvdt = acceleration
    return np.concatenate((drdt, dvdt))

def runge_kutta(state, q, m, position_field_array, electric_field_fun, dt):
    k1 = dt * derivatives(state, q, m, position_field_array, electric_field_fun)
    k2 = dt * derivatives(state + 0.5 * k1, q, m, position_field_array, electric_field_fun)
    k3 = dt * derivatives(state + 0.5 * k2, q, m, position_field_array, electric_field_fun)
    k4 = dt * derivatives(state + k3, q, m, position_field_array, electric_field_fun)
    new_state = state + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return new_state

# %%
# Ion class and simulation functions
class Ion:
    def __init__(self, mass, charge, initial_position, initial_velocity):
        self.mass = mass
        self.charge = charge
        self.state = np.concatenate((initial_position, initial_velocity))

    def update_state(self, position_field_array, electric_field_fun, dt):
        self.state = runge_kutta(self.state, self.charge, self.mass, position_field_array, electric_field_fun, dt)

def generate_random_ions(num_ions):
    ions = []
    for _ in range(num_ions):
        mass = np.random.uniform(1e-1, 1e1)
        charge = np.random.uniform(1e-19, 1e-18)
        initial_position = np.random.uniform(-10, 10, 3)
        initial_velocity = np.random.uniform(-5, 5, 3)
        ions.append(Ion(mass, charge, initial_position, initial_velocity))
    return ions

def simulate_ions(ions, steps, dt, position_field_array, electric_field_fun):
    trajectories = {ion: [] for ion in ions}
    for step in range(steps):
        for ion in ions:
            ion.update_state(position_field_array, electric_field_fun, dt)
            trajectories[ion].append(ion.state.copy())
    return trajectories

def plot_trajectories(trajectories):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    for ion, traj in trajectories.items():
        traj = np.array(traj)
        ax.plot(traj[:, 0], traj[:, 1], traj[:, 2], label=f"Ion (m={ion.mass:.2e}, q={ion.charge:.2e})")
    ax.set_xlabel('X Position (m)')
    ax.set_ylabel('Y Position (m)')
    ax.set_zlabel('Z Position (m)')
    ax.set_title('Ion Trajectory Simulation')
    plt.legend()
    plt.show()

def plot_2d_projections(trajectories):
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    for ion, traj in trajectories.items():
        traj = np.array(traj)
        axs[0].plot(traj[:, 0], traj[:, 1], label=f"Ion (m={ion.mass:.2e}, q={ion.charge:.2e})")
        axs[1].plot(traj[:, 0], traj[:, 2], label=f"Ion (m={ion.mass:.2e}, q={ion.charge:.2e})")
        axs[2].plot(traj[:, 1], traj[:, 2], label=f"Ion (m={ion.mass:.2e}, q={ion.charge:.2e})")
    axs[0].set_xlabel('X Position (m)')
    axs[0].set_ylabel('Y Position (m)')
    axs[0].set_title('XY Projection')
    axs[1].set_xlabel('X Position (m)')
    axs[1].set_ylabel('Z Position (m)')
    axs[1].set_title('XZ Projection')
    axs[2].set_xlabel('Y Position (m)')
    axs[2].set_ylabel('Z Position (m)')
    axs[2].set_title('YZ Projection')
    plt.legend()
    plt.show()

def plot_velocity_vs_time(trajectories, dt):
    fig, axs = plt.subplots(3, 1, figsize=(10, 18))
    for ion, traj in trajectories.items():
        traj = np.array(traj)
        time = np.arange(len(traj)) * dt
        axs[0].plot(time, traj[:, 3], label=f"Ion (m={ion.mass:.2e}, q={ion.charge:.2e})")
        axs[1].plot(time, traj[:, 4], label=f"Ion (m={ion.mass:.2e}, q={ion.charge:.2e})")
        axs[2].plot(time, traj[:, 5], label=f"Ion (m={ion.mass:.2e}, q={ion.charge:.2e})")
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Vx (m/s)')
    axs[0].set_title('Velocity in X direction')
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Vy (m/s)')
    axs[1].set_title('Velocity in Y direction')
    axs[2].set_xlabel('Time (s)')
    axs[2].set_ylabel('Vz (m/s)')
    axs[2].set_title('Velocity in Z direction')
    plt.legend()
    plt.show()

def plot_distance_vs_time(trajectories, dt):
    fig = plt.figure(figsize=(10, 7))
    for ion, traj in trajectories.items():
        traj = np.array(traj)
        time = np.arange(len(traj)) * dt
        distances = np.sqrt(np.sum(np.diff(traj[:, 0:3], axis=0)**2, axis=1))
        cumulative_distance = np.cumsum(distances)
        plt.plot(time[1:], cumulative_distance, label=f"Ion (m={ion.mass:.2e}, q={ion.charge:.2e})")
    plt.xlabel('Time (s)')
    plt.ylabel('Distance Traveled (m)')
    plt.title('Distance Traveled vs. Time')
    plt.legend()
    plt.show()

def plot_histogram_final_positions(trajectories):
    final_positions = np.array([traj[-1, 0:3] for traj in trajectories.values()])
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.hist(final_positions[:, 0], bins=20, alpha=0.6, label='X Position')
    ax.hist(final_positions[:, 1], bins=20, alpha=0.6, label='Y Position')
    ax.hist(final_positions[:, 2], bins=20, alpha=0.6, label='Z Position')
    ax.set_xlabel('Position (m)')
    ax.set_ylabel('Frequency')
    ax.set_title('Histogram of Final Positions')
    plt.legend()
    plt.show()

def plot_initial_vs_final_velocities(trajectories):
    initial_velocities = np.array([traj[0, 3:6] for traj in trajectories.values()])
    final_velocities = np.array([traj[-1, 3:6] for traj in trajectories.values()])
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    axs[0].scatter(initial_velocities[:, 0], final_velocities[:, 0], label='Vx')
    axs[1].scatter(initial_velocities[:, 1], final_velocities[:, 1], label='Vy')
    axs[2].scatter(initial_velocities[:, 2], final_velocities[:, 2], label='Vz')
    axs[0].set_xlabel('Initial Vx (m/s)')
    axs[0].set_ylabel('Final Vx (m/s)')
    axs[0].set_title('Initial vs. Final Vx')
    axs[1].set_xlabel('Initial Vy (m/s)')
    axs[1].set_ylabel('Final Vy (m/s)')
    axs[1].set_title('Initial vs. Final Vy')
    axs[2].set_xlabel('Initial Vz (m/s)')
    axs[2].set_ylabel('Final Vz (m/s)')
    axs[2].set_title('Initial vs. Final Vz')
    plt.legend()
    plt.show()

# Main simulation parameters
NUM_IONS = 10
STEPS = 100
DT = 0.01

# Generate random ions
ions = generate_random_ions(NUM_IONS)

# Simulate ion trajectories
trajectories = simulate_ions(ions, STEPS, DT, position_fields, electric_field)

# Plot the trajectories
plot_trajectories(trajectories)

# Additional visualizations
plot_2d_projections(trajectories)
plot_velocity_vs_time(trajectories, DT)
plot_distance_vs_time(trajectories, DT)
plot_histogram_final_positions(trajectories)
plot_initial_vs_final_velocities(trajectories)

# %%
# Data file from Voyager 1 mission
# Columns are : Longitude (degree), Latitude (degree), Br, Btheta, Bphi and Total Field components
voyager_file_path = '/Users/hectar/Downloads/Voyager1_Magnetic_Field_Data.dat'

# Functions to read coordinates and magnetic field data from Voyager 1
def read_voyager_coordinates(index):
    values = []
    with open(voyager_file_path, 'r') as file:
        for line in file:
            columns = line.split()
            values.append(float(columns[index]))
    return values

def read_voyager_magnetic_field():
    values = []
    with open(voyager_file_path, 'r') as file:
        for line in file:
            columns = line.split()
            values.append(float(columns[2]))
    return values

voyager_x_values = read_voyager_coordinates(0)
voyager_y_values = read_voyager_coordinates(1)
voyager_field = read_voyager_magnetic_field()

# %%
# Prepare Voyager 1 magnetic field data for plotting
voyager_position_fields = list(zip(voyager_x_values, voyager_y_values, voyager_field))
voyager_position_field_array = np.array(voyager_position_fields)

voyager_x_unique = np.unique(voyager_x_values)
voyager_y_unique = np.unique(voyager_y_values)

voyager_B_grid = np.zeros((len(voyager_y_unique), len(voyager_x_unique)))

for i in range(len(voyager_x_values)):
    x_idx = np.where(voyager_x_unique == voyager_x_values[i])[0][0]
    y_idx = np.where(voyager_y_unique == voyager_y_values[i])[0][0]
    voyager_B_grid[y_idx, x_idx] = voyager_field[i]

plt.figure(figsize=(8, 6))
plt.imshow(voyager_B_grid, cmap='Pastel1', origin='lower', aspect='auto')
plt.colorbar(label='Magnetic Field')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Magnetic Field Surfacemap for Voyager 1 Data')
plt.show()

# %%
# Load Voyager 1 data into DataFrame and plot heatmap
voyager_df = pd.read_csv(voyager_file_path, sep="\s+", header=None)
voyager_df.columns = ['Longitude (degree)', 'Latitude (degree)', 'Field Value 1', 'Field Value 2', 'Field Value 3', 'Total Field components']

voyager_df_localized = voyager_df.head(100)
voyager_pivot_data = voyager_df_localized.pivot(index='Longitude (degree)', columns='Latitude (degree)', values='Total Field components')

sns.heatmap(voyager_pivot_data, cmap="viridis", annot=False)
plt.title('Localized Heatmap for Voyager 1 Data')
plt.show()

# %%
# Compare and calibrate ion particle activity using both datasets
def compare_datasets(position_field_array_1, position_field_array_2):
    # Example comparison: Calculate the mean magnetic field strength for both datasets
    mean_field_1 = np.mean(position_field_array_1[:, 2])
    mean_field_2 = np.mean(position_field_array_2[:, 2])
    print(f"Mean Magnetic Field Strength (Dataset 1): {mean_field_1}")
    print(f"Mean Magnetic Field Strength (Dataset 2): {mean_field_2}")

    # Additional comparisons and calibrations can be added here

# Compare the datasets
compare_datasets(position_field_array, voyager_position_field_array)

# %%
# Main simulation parameters
NUM_IONS = 10
STEPS = 100
DT = 0.01

# Generate random ions
ions = generate_random_ions(NUM_IONS)

# Simulate ion trajectories using the original dataset
trajectories = simulate_ions(ions, STEPS, DT, position_fields, electric_field)

# Simulate ion trajectories using the Voyager 1 dataset
voyager_trajectories = simulate_ions(ions, STEPS, DT, voyager_position_fields, electric_field)

# Plot the trajectories for both datasets
plot_trajectories(trajectories)
plot_trajectories(voyager_trajectories)

# Additional visualizations for both datasets
plot_2d_projections(trajectories)
plot_2d_projections(voyager_trajectories)
plot_velocity_vs_time(trajectories, DT)
plot_velocity_vs_time(voyager_trajectories, DT)
plot_distance_vs_time(trajectories, DT)
plot_distance_vs_time(voyager_trajectories, DT)
plot_histogram_final_positions(trajectories)
plot_histogram_final_positions(voyager_trajectories)
plot_initial_vs_final_velocities(trajectories)
plot_initial_vs_final_velocities(voyager_trajectories)

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Ion Trajectory Simulation')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ION_COLOR = (0, 255, 0)

def draw_trajectories_pygame(trajectories):
    running = True
    clock = pygame.time.Clock()
    scale = 10  # Scale factor for visualization

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        screen.fill(BLACK)

        for ion, traj in trajectories.items():
            traj = np.array(traj)
            for i in range(len(traj) - 1):
                start_pos = (int(traj[i, 0] * scale + width // 2), int(traj[i, 1] * scale + height // 2))
                end_pos = (int(traj[i + 1, 0] * scale + width // 2), int(traj[i + 1, 1] * scale + height // 2))
                pygame.draw.line(screen, ION_COLOR, start_pos, end_pos, 2)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Main simulation parameters
NUM_IONS = 10
STEPS = 100
DT = 0.01

# Generate random ions
ions = generate_random_ions(NUM_IONS)

# Simulate ion trajectories
trajectories = simulate_ions(ions, STEPS, DT, position_fields, electric_field)

# Plot the trajectories using Pygame
draw_trajectories_pygame(trajectories)
