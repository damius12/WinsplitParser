import os

from src.create_word import create_word
from src.format_results import format_event_data, format_results, get_file_title
from src.get_result import get_result
from src.parse_xml import parse_xml
from src.plot_results import plot_results
from src.process_data import process_data


def _get_names_by_position(positions: list, data: dict) -> list:
    return [
        runner["name"] for runner in data["results"] if runner["position"] in positions
    ]


def _get_names_by_club(clubs: list, data: dict) -> list:
    return [runner["name"] for runner in data["results"] if runner["club"] in clubs]


def _get_clubs_by_name(names: list, data: dict) -> list:
    return [runner["club"] for runner in data["results"] if runner["name"] in names]


def main(
    url: str,
    advanced_analysis: list,
    basic_analysis_include_same_club: bool,
    basic_analysis_positions: list,
    splits_per_row: int,
) -> str:
    """
    Main function to process Winsplits results and save to a Word document.

    Args:
        url (str): The Winsplits URL.
        advanced_analysis (list): List of runner names for advanced analysis.
        basic_analysis_include_same_club (bool): Include runners from the same club in the basic analysis.
        basic_analysis_positions (list): List of positions to include in the basic analysis.
        splits_per_row (int): Number of splits to display per row in the output.

    Returns:
        str: The formatted results text.
    """
    try:
        xml_content = get_result(url)
        data = parse_xml(xml_content)
        process_data(data)

        basic_analysis = _get_names_by_position(basic_analysis_positions, data)
        if basic_analysis_include_same_club:
            clubs = _get_clubs_by_name(advanced_analysis, data)
            basic_analysis += _get_names_by_club(clubs, data)
        file_title = get_file_title(data["event_data"])
        event_title = format_event_data(data["event_data"])
        results_text = format_results(
            data, basic_analysis, advanced_analysis, splits_per_row
        )

        # Save the plot to a file
        temporary_image = "tmp.png"
        if advanced_analysis:
            plot_results(data, advanced_analysis, temporary_image)

        create_word(event_title, results_text, temporary_image, file_title)

        if os.path.exists(temporary_image):
            os.remove(temporary_image)

        return event_title + "\n" + results_text

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    from src.argument_parser import parse_args

    args = parse_args()

    if args.url is None:
        args.url = input("Please enter the Winsplits URL: ")

    results_text = main(
        args.url,
        args.advanced_analysis,
        args.basic_analysis_include_same_club,
        args.basic_analysis_positions,
        args.splits_per_row,
    )
