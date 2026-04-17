import ast
from pathlib import Path
from math import radians, cos, sin, asin, sqrt

import numpy as np


PROGRAM_PATH = Path(__file__).resolve().parents[1] / "program.py"


def _load_simulation_symbols():
    source = PROGRAM_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(PROGRAM_PATH))
    wanted = {"MOON_RADIUS", "distance_3d", "derivatives", "runge_kutta", "Ion", "simulate_ions"}
    selected_nodes = []

    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in wanted:
                    selected_nodes.append(node)
                    break
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in wanted:
            selected_nodes.append(node)

    module = ast.Module(body=selected_nodes, type_ignores=[])
    namespace = {
        "np": np,
        "radians": radians,
        "cos": cos,
        "sin": sin,
        "asin": asin,
        "sqrt": sqrt,
    }
    exec(compile(module, filename=str(PROGRAM_PATH), mode="exec"), namespace)
    return namespace


SIM = _load_simulation_symbols()
runge_kutta = SIM["runge_kutta"]
simulate_ions = SIM["simulate_ions"]
Ion = SIM["Ion"]


def _zero_electric_field(_height):
    return np.zeros(3)


def test_runge_kutta_zero_fields_preserves_velocity():
    state = np.array([0.0, 0.0, 0.0, 2.0, -1.0, 0.5])
    dt = 0.1
    q = 1.0
    m = 2.0
    zero_b_field = np.array([[0.0, 0.0, 0.0]])

    new_state = runge_kutta(state, q, m, zero_b_field, _zero_electric_field, dt)

    expected_position = state[:3] + state[3:] * dt
    np.testing.assert_allclose(new_state[:3], expected_position, rtol=1e-10, atol=1e-10)
    np.testing.assert_allclose(new_state[3:], state[3:], rtol=1e-10, atol=1e-10)


def test_runge_kutta_electric_only_matches_parabolic_motion():
    state = np.array([1.0, -1.0, 2.0, 0.2, 0.4, -0.1])
    dt = 0.2
    q = 2.0
    m = 4.0
    electric = np.array([0.0, 0.0, 3.0])
    zero_b_field = np.array([[0.0, 0.0, 0.0]])

    def constant_electric_field(_height):
        return electric

    new_state = runge_kutta(state, q, m, zero_b_field, constant_electric_field, dt)
    acceleration = (q * electric) / m

    expected_position = state[:3] + state[3:] * dt + 0.5 * acceleration * dt**2
    expected_velocity = state[3:] + acceleration * dt

    np.testing.assert_allclose(new_state[:3], expected_position, rtol=1e-10, atol=1e-10)
    np.testing.assert_allclose(new_state[3:], expected_velocity, rtol=1e-10, atol=1e-10)


def test_simulate_ions_magnetic_only_keeps_speed_magnitude():
    ion = Ion(
        mass=1.0,
        charge=0.0,
        initial_position=np.array([0.0, 0.0, 0.0]),
        initial_velocity=np.array([1.0, 0.0, 0.0]),
    )
    dt = 0.001
    steps = 2000
    magnetic_field = np.array([[0.0, 0.0, 5.0]])

    trajectories = simulate_ions([ion], steps, dt, magnetic_field, _zero_electric_field)
    trajectory = np.array(trajectories[ion])
    speeds = np.linalg.norm(trajectory[:, 3:], axis=1)

    np.testing.assert_allclose(speeds, speeds[0], rtol=1e-4, atol=1e-4)
