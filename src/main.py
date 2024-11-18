from src.format_results import format_results
from src.get_result import get_result
from src.parse_xml import parse_xml
from src.process_data import process_data

ADVANCED_ANALYSIS = ["Sebastian Inderst"]
BASIC_ANALYSIS_INCLUDE_SAME_CLUB = True
BASIC_ANALYSIS_POSITIONS = [1, 2, 3] + list(range(10, 100, 10))
# BASIC_ANALYSIS_POSITIONS = list(range(1, 11))
SPLITS_PER_ROW = 7


def _get_names_by_position(positions: list, data: dict) -> list:
    return [
        runner["name"] for runner in data["results"] if runner["position"] in positions
    ]


def _get_names_by_club(clubs: list, data: dict) -> list:
    return [runner["name"] for runner in data["results"] if runner["club"] in clubs]


def _get_clubs_by_name(names: list, data: dict) -> list:
    return [runner["club"] for runner in data["results"] if runner["name"] in names]


def main():
    try:
        url = input("Please enter the Winsplits URL: ")
        xml_content = get_result(url)
        data = parse_xml(xml_content)
        process_data(data)

        basic_analysis = _get_names_by_position(BASIC_ANALYSIS_POSITIONS, data)
        if BASIC_ANALYSIS_INCLUDE_SAME_CLUB:
            clubs = _get_clubs_by_name(ADVANCED_ANALYSIS, data)
            basic_analysis += _get_names_by_club(clubs, data)
        results_text = format_results(
            data, basic_analysis, ADVANCED_ANALYSIS, SPLITS_PER_ROW
        )

        print(results_text)
        input("Press any key to exit...")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
