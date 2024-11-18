import unittest

from src.process_data import (
    _add_split_analysis,
    _compute_best_split_times,
    process_data,
)


class TestProcessData(unittest.TestCase):

    def setUp(self):
        self.data = {
            "results": [
                {
                    "name": "Sebastian Inderst",
                    "club": "Göteborg-Majorna OK",
                    "total_time": 379,
                    "status": "OK",
                    "position": 1,
                    "splits": [
                        {"control_code": "118", "time": 72, "split_time": 72},
                        {"control_code": "40", "time": 202, "split_time": 130},
                        {"control_code": "36", "time": 259, "split_time": 57},
                        {"control_code": "58", "time": 379, "split_time": 120},
                    ],
                },
                {
                    "name": "Mispunched Runner",
                    "club": "Unknown Club",
                    "total_time": 380,
                    "status": "MissingPunch",
                    "position": None,
                    "splits": [
                        {"control_code": "118", "time": 80, "split_time": 80},
                        {"control_code": "40", "time": None, "split_time": None},
                        {"control_code": "36", "time": 280, "split_time": None},
                        {"control_code": "58", "time": 380, "split_time": 100},
                    ],
                },
            ]
        }

    def test_compute_best_split_times(self):
        best_split_times = _compute_best_split_times(self.data["results"])
        self.assertEqual(best_split_times["118"], 72)
        self.assertEqual(best_split_times["40"], 130)
        self.assertEqual(best_split_times["36"], 57)
        self.assertEqual(best_split_times["58"], 100)

    def test_add_split_analysis(self):
        best_split_times = _compute_best_split_times(self.data["results"])
        _add_split_analysis(self.data["results"], best_split_times)
        self.assertEqual(self.data["results"][0]["splits"][0]["split_gap"], 0)
        self.assertEqual(self.data["results"][0]["splits"][0]["percentage_gap"], 0.0)
        self.assertEqual(self.data["results"][1]["splits"][0]["split_gap"], 8)
        self.assertAlmostEqual(
            self.data["results"][1]["splits"][0]["percentage_gap"], 11.11, 2
        )
        self.assertEqual(self.data["results"][1]["splits"][1]["split_gap"], None)
        self.assertEqual(self.data["results"][1]["splits"][1]["percentage_gap"], None)

    def test_process_data(self):
        process_data(self.data)
        self.assertEqual(self.data["winning_time"], 379)
        self.assertIn("split_gap", self.data["results"][0]["splits"][0])
        self.assertIn("percentage_gap", self.data["results"][0]["splits"][0])


if __name__ == "__main__":
    unittest.main()
