# ion-trajectory-intergration
Project with Professor Wendy Tseng on simulations involving ion movement in Titan's exobase

Certainly! Here’s a sample README file for your project. You can adjust or add more details as needed.

---

# Ion Trajectory Visualization

This project visualizes the trajectory of ions in a uniform magnetic and electric field using Pygame. It calculates and displays the paths of ions as they move under the influence of these fields.

## Overview

The simulation considers the trajectory of ions as cycloidal paths based on provided physical parameters. The paths are calculated using the ion's charge, mass, and the strengths of the electric and magnetic fields.

## Features

- Visualize ion trajectories in a 2D plane.
- Adjust the parameters of the ions, including charge, mass, and simulation time.
- Use Pygame to render the trajectories on a graphical window.

## Installation

To get started, ensure you have Python and Pygame installed. You can install Pygame using pip:

```bash
pip install pygame
```

## Usage

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/ion-trajectory.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd ion-trajectory
    ```

3. **Run the simulation:**

    ```bash
    python program.py
    ```

4. **Adjust the Parameters:**

    Open `program.py` to modify the following parameters:

    - `E`: Electric field strength.
    - `B`: Magnetic field strength.
    - `theta_0`: Initial gyrophase.
    - `time`: Duration of the simulation.
    - `charge`: Charge of the ion.
    - `mass`: Mass of the ion.

    You can also adjust the display window dimensions and colors as needed.

- **Ion Class:** Manages the properties of each ion and calculates its trajectory based on physical parameters.
  - `__init__(self, x, y, charge, mass, time, color)`: Initializes the ion with its starting position, charge, mass, simulation time, and color.
  - `trajectory(self)`: Computes the trajectory of the ion over time and returns a list of points.
  - `draw(self, WIN)`: Draws the computed trajectory on the Pygame window.

- **Main Function:**
  - Sets up the Pygame window and initializes ions.
  - Continuously updates the display and draws the ion trajectories.

## Debugging

If you encounter issues with the visualization:
- Ensure that the trajectory points are within the bounds of the display window.
- Check the debug output to verify coordinates.

## Contributing

Feel free to contribute to this project by submitting issues or pull requests. 

## Contact

For questions or feedback, please contact hectarcarson@gmail.com
