import unittest
from unittest.mock import MagicMock, patch

from src.main import main


class TestMainIntegration(unittest.TestCase):

    def setUp(self):
        self.url = "http://example.com/winsplits"
        self.advanced_analysis = []
        self.basic_analysis_include_same_club = False
        self.basic_analysis_positions = []
        self.splits_per_row = 5

        # Mock the fetching of the xml file
        patcher = patch("src.main.get_result")
        self.mock_get_result = patcher.start()
        self.addCleanup(patcher.stop)

        with open("sample.xml", "r", encoding="utf-8") as file:
            self.mock_get_result.return_value = file.read()

    def run_main(self):
        return main(
            self.url,
            self.advanced_analysis,
            self.basic_analysis_include_same_club,
            self.basic_analysis_positions,
            self.splits_per_row,
        )

    def test_main_integration(self):
        results_text = self.run_main()
        self.mock_get_result.assert_called_once_with(self.url)
        self.assertIsNotNone(results_text)

    def test_advanced_analysis(self):
        self.advanced_analysis = ["Sebastian Inderst"]
        results_text = self.run_main()
        lines = results_text.split("\n")
        self.assertIn("Sebastian Inderst", lines[1])
        self.assertGreater(len(lines), 2)

    def test_basic_analysis_include_same_club(self):
        self.basic_analysis_include_same_club = True
        self.advanced_analysis = ["Sebastian Inderst"]
        results_text = self.run_main()
        self.assertEqual(results_text.count("Göteborg-Majorna OK"), 12)

    def test_basic_analysis_positions(self):
        self.basic_analysis_positions = [1, 2, 5, 20]
        results_text = self.run_main()
        lines = results_text.split("\n")
        for expected_position, line in zip(self.basic_analysis_positions, lines[1:]):
            position = int(line.split()[0][:-1])
            self.assertEqual(position, expected_position)

    def test_splits_per_row(self):
        self.advanced_analysis = ["Sebastian Inderst"]

        self.splits_per_row = 3
        results_text = self.run_main()
        lines_3 = results_text.split("\n")[2:]

        self.splits_per_row = 6
        results_text = self.run_main()
        lines_6 = results_text.split("\n")[2:]

        self.assertEqual(len(lines_3), 2 * len(lines_6))
        self.assertEqual(int(len(lines_6[0])/len(lines_3[0])), 2)
        self.assertEqual(lines_3[0], lines_6[0][:len(lines_3[0])])


if __name__ == "__main__":
    unittest.main()
