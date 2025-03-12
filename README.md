1. **3D Trajectory Plot**: Shows the path of each ion in 3D space.
2. **2D Projection Plots**: Projects the 3D trajectories onto 2D planes (XY, XZ, YZ).
3. **Velocity vs. Time Plot**: Plots the velocity components of the ions over time.
4. **Distance Traveled vs. Time Plot**: Plots the total distance traveled by each ion over time.
5. **Histogram of Final Positions**: Shows the distribution of final positions of the ions.
6. **Scatter Plot of Initial vs. Final Velocities**: Compares initial and final velocities of the ions.

## Example

Here is an example of how to generate random ions and simulate their trajectories:

```python
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
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Data from [UKnowledge](https://uknowledge.uky.edu/ees_data/2/#attach_additional_files)
- Voyager 1 mission data

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.