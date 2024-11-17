import unittest
import xml.etree.ElementTree as ET
from src.process_xml import (
    _extract_event_data,
    _compute_split_information,
    _extract_person_result,
    _extract_result_list,
    _compute_best_split_times,
    _add_split_analysis,
    process_xml,
)

class TestProcessXML(unittest.TestCase):

    def setUp(self):
        with open("sample.xml", "r", encoding='utf-8') as file:
            self.xml_content = file.read()
        self.root = ET.fromstring(self.xml_content)
        self.namespace = {"ns": "http://www.orienteering.org/datastandard/3.0"}

    def test_extract_event_data(self):
        event_data = _extract_event_data(self.root, self.namespace)
        self.assertEqual(event_data["name"], "Gävle Indoor , etapp 1")
        self.assertEqual(event_data["class"], "Damer")
        self.assertEqual(event_data["date"], "2024-11-16")

    def test_compute_split_information(self):
        person_result = self.root.find(".//ns:PersonResult", self.namespace)
        splits = _compute_split_information(person_result, self.namespace)
        self.assertEqual(len(splits), 25)
        self.assertEqual(splits[0]["control_code"], "31")
        self.assertEqual(splits[0]["time"], 52)
        self.assertEqual(splits[0]["split_time"], 52)

    def test_extract_person_result(self):
        person_result = self.root.find(".//ns:PersonResult", self.namespace)
        person_dict = _extract_person_result(person_result, self.namespace)
        self.assertEqual(person_dict["name"], "Ella Sandberg")
        self.assertEqual(person_dict["club"], "Alfta-Ösa OK")
        self.assertEqual(person_dict["status"], "OK")
        self.assertEqual(person_dict["position"], 1)
        self.assertEqual(person_dict["total_time"], 2254)
        self.assertEqual(len(person_dict["splits"]), 25)

    def test_extract_result_list(self):
        result_list = _extract_result_list(self.root, self.namespace)
        self.assertEqual(len(result_list), 45)
        self.assertEqual(result_list[0]["name"], "Ella Sandberg")
        self.assertEqual(result_list[1]["name"], "Linnea Persson")

    def test_compute_best_split_times(self):
        result_list = _extract_result_list(self.root, self.namespace)
        best_split_times = _compute_best_split_times(result_list)
        self.assertEqual(best_split_times["31"], 44)
        self.assertEqual(best_split_times["33"], 9)

    def test_add_split_analysis(self):
        result_list = _extract_result_list(self.root, self.namespace)
        best_split_times = _compute_best_split_times(result_list)
        _add_split_analysis(result_list, best_split_times)
        self.assertEqual(result_list[0]["splits"][0]["split_gap"], 8)
        self.assertEqual(int(result_list[0]["splits"][0]["percentage_gap"]), 18)

    def test_process_xml(self):
        result = process_xml(self.xml_content)
        self.assertEqual(result["event_data"]["name"], "Gävle Indoor , etapp 1")
        self.assertEqual(result["results"][0]["name"], "Ella Sandberg")
        self.assertEqual(result["winning_time"], 2254)

if __name__ == "__main__":
    unittest.main()
