import ast
import pathlib
import unittest

import numpy as np


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
PROGRAM_PATH = REPO_ROOT / "program.py"


def load_derivatives_function():
    source = PROGRAM_PATH.read_text()
    module = ast.parse(source, filename=str(PROGRAM_PATH))
    derivatives_node = next(
        node for node in module.body if isinstance(node, ast.FunctionDef) and node.name == "derivatives"
    )
    isolated_module = ast.Module(body=[derivatives_node], type_ignores=[])
    namespace = {"np": np}
    exec(compile(ast.fix_missing_locations(isolated_module), str(PROGRAM_PATH), "exec"), namespace)
    return namespace["derivatives"]


class DerivativesLorentzForceTests(unittest.TestCase):
    def setUp(self):
        self.derivatives = load_derivatives_function()

    def test_magnetic_force_is_scaled_by_charge(self):
        state = np.array([0.0, 0.0, 0.0, 1.0, 0.0, 0.0])  # position + velocity
        q = 2.0
        m = 4.0
        position_field_array = np.array(
            [
                [0.0, 0.0, 3.0],  # nearest sample -> B = [0, 0, 3]
                [10.0, 10.0, 99.0],
            ]
        )

        def zero_electric_field(_):
            return np.zeros(3)

        result = self.derivatives(state, q, m, position_field_array, zero_electric_field)

        np.testing.assert_allclose(result[:3], np.array([1.0, 0.0, 0.0]))
        np.testing.assert_allclose(result[3:], np.array([0.0, -1.5, 0.0]))

    def test_lorentz_force_combines_electric_and_magnetic_terms(self):
        state = np.array([0.0, 0.0, 0.0, 0.0, 2.0, 0.0])  # velocity = [0, 2, 0]
        q = -1.0
        m = 2.0
        position_field_array = np.array([[0.0, 0.0, 4.0]])  # B = [0, 0, 4]

        def constant_electric_field(_):
            return np.array([0.0, 0.0, 5.0])

        result = self.derivatives(state, q, m, position_field_array, constant_electric_field)

        np.testing.assert_allclose(result[:3], np.array([0.0, 2.0, 0.0]))
        np.testing.assert_allclose(result[3:], np.array([-4.0, 0.0, -2.5]))


if __name__ == "__main__":
    unittest.main()
