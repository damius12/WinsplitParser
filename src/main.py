from src.format_results import format_results
from src.get_result import get_result
from src.process_xml import process_xml

SPLITS_PER_ROW = 7
POSITIONS = [1, 2, 3] + list(range(10, 100, 10))
DETAILED_ANALYSIS = ["Sebastian Inderst"]


def _get_analysis_names(positions: list, data: dict) -> list:
    return [
        runner["name"] for runner in data["results"] if runner["position"] in positions
    ]


def main():
    try:
        url = input("Please enter the Winsplits URL: ")
        xml_content = get_result(url)
        data = process_xml(xml_content)
        analysis = _get_analysis_names(POSITIONS, data)
        results_text = format_results(data, analysis, DETAILED_ANALYSIS, SPLITS_PER_ROW)
        print(results_text)
        input("Press any key to exit...")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
