# ion-trajectory-intergration
Project with a Professor on simulations involving replicating the observed ion movement in Titan's exobase to our own moon


# Ion Trajectory Visualization

This project visualizes the trajectory of ions in a uniform magnetic and electric field using Pygame. It calculates and displays the paths of ions as they move under the influence of these fields.

## Overview

The simulation considers the trajectory of ions as cycloidal paths based on the provided physical parameters. The paths are calculated using the ion's charge, mass, and the strengths of the electric and magnetic fields.

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

3. **Download dataset files (required):**

    Place data files in a `data/` directory at the project root:

    - `data/New Magnetic Field Models of the Moon.dat`  
      Source: [UKnowledge](https://uknowledge.uky.edu/ees_data/2/#attach_additional_files)
    - `data/Voyager1_Magnetic_Field_Data.dat`  
      Source: Voyager 1 mission data

    > Backward compatibility: both `New Magnetic Field Models of the Moon.dat` and `Voyager1_Magnetic_Field_Data.dat` in the project root are still supported.

4. **Run the simulation:**

    ```bash
    python program.py
    ```

    You can also pass explicit paths:

    ```bash
    python program.py --moon-data /path/to/New\ Magnetic\ Field\ Models\ of\ the\ Moon.dat --voyager-data /path/to/Voyager1_Magnetic_Field_Data.dat
    ```

    Or use environment variables:

    ```bash
    export MOON_DATA_PATH=/path/to/New\ Magnetic\ Field\ Models\ of\ the\ Moon.dat
    export VOYAGER_DATA_PATH=/path/to/Voyager1_Magnetic_Field_Data.dat
    python program.py
    ```

5. **Adjust the Parameters:**

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

## Acknowledgements

- Data from [UKnowledge](https://uknowledge.uky.edu/ees_data/2/#attach_additional_files)
- Voyager 1 mission data

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
