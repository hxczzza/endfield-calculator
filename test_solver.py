import unittest

from solver import solve


class SolverTests(unittest.TestCase):
    def test_original_mode_still_works(self):
        self.assertEqual(len(solve(3, [1, 1, 1], [1, 1, 1])), 6)

    def test_blocked_cell_is_never_filled(self):
        solutions = solve(3, [1, 1, 1], [1, 1, 1], {(0, 0)})
        self.assertEqual(len(solutions), 4)
        self.assertTrue(all(solution[0][0] == -1 for solution in solutions))

    def test_matrix_style_obstacles(self):
        blocked = [[-1, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(len(solve(3, [1, 1, 1], [1, 1, 1], blocked)), 4)

    def test_impossible_target_with_obstacles(self):
        blocked = {(0, 0), (0, 1), (0, 2)}
        self.assertEqual(solve(3, [1, 0, 0], [1, 0, 0], blocked), [])

    def test_invalid_obstacle_is_rejected(self):
        self.assertEqual(solve(3, [0, 0, 0], [0, 0, 0], {(3, 0)}), [])


if __name__ == "__main__":
    unittest.main()
