import unittest
import xml.etree.ElementTree as ET
from src.parse_xml import (
    _extract_event_data,
    _compute_split_information,
    _extract_person_result,
    _extract_result_list,
    parse_xml,
)

class TestParseXML(unittest.TestCase):

    def setUp(self):
        with open("sample.xml", "r", encoding="utf-8") as file:
            self.xml_content = file.read()
        self.root = ET.fromstring(self.xml_content)
        self.namespace = {"ns": "http://www.orienteering.org/datastandard/3.0"}

    def test_extract_event_data(self):
        event_data = _extract_event_data(self.root, self.namespace)
        self.assertEqual(event_data["name"], "DM, medel, Göteborg")
        self.assertEqual(event_data["class"], "H21")
        self.assertEqual(event_data["date"], "2024-09-14")

    def test_compute_split_information(self):
        person_result = self.root.findall(".//ns:PersonResult", self.namespace)[11]
        splits = _compute_split_information(person_result, self.namespace)
        self.assertEqual(len(splits), 17)
        self.assertEqual(splits[0]["control_code"], "118")
        self.assertEqual(splits[0]["time"], 78)
        self.assertEqual(splits[0]["split_time"], 78)
        self.assertEqual(splits[1]["control_code"], "40")
        self.assertEqual(splits[1]["time"], 238)
        self.assertEqual(splits[1]["split_time"], 160)

    def test_compute_split_information_misspunched(self):
        person_result = self.root.findall(".//ns:PersonResult", self.namespace)[-5]
        splits = _compute_split_information(person_result, self.namespace)
        self.assertEqual(len(splits), 17)
        self.assertEqual(splits[1]["control_code"], "40")
        self.assertEqual(splits[1]["time"], None)
        self.assertEqual(splits[1]["split_time"], None)
        self.assertEqual(splits[2]["control_code"], "36")
        self.assertEqual(splits[2]["time"], 856)
        self.assertEqual(splits[2]["split_time"], None)
        self.assertEqual(splits[3]["control_code"], "58")
        self.assertEqual(splits[3]["time"], 2028)
        self.assertEqual(splits[3]["split_time"], 1172)

    def test_extract_person_result(self):
        person_result = self.root.findall(".//ns:PersonResult", self.namespace)[11]
        person_dict = _extract_person_result(person_result, self.namespace)
        self.assertEqual(person_dict["name"], "Sebastian Inderst")
        self.assertEqual(person_dict["club"], "Göteborg-Majorna OK")
        self.assertEqual(person_dict["status"], "OK")
        self.assertEqual(person_dict["position"], 12)
        self.assertEqual(person_dict["total_time"], 2218)
        self.assertEqual(len(person_dict["splits"]), 17)

    def test_extract_person_result_misspunched(self):
        person_result = self.root.findall(".//ns:PersonResult", self.namespace)[-5]
        person_dict = _extract_person_result(person_result, self.namespace)
        self.assertEqual(person_dict["status"], "MissingPunch")
        self.assertEqual(person_dict["position"], None)
        self.assertEqual(person_dict["total_time"], 5686)
        self.assertEqual(len(person_dict["splits"]), 17)

    def test_extract_result_list(self):
        result_list = _extract_result_list(self.root, self.namespace)
        self.assertEqual(len(result_list), 61)
        self.assertEqual(result_list[11]["name"], "Sebastian Inderst")

    def test_parse_xml(self):
        result = parse_xml(self.xml_content)
        self.assertIn("event_data", result)
        self.assertIn("results", result)

if __name__ == "__main__":
    unittest.main()
