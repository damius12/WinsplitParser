def _format_event_data(event_data: dict) -> str:
    """
    Formats the event data into a string with the event name and date.
    """
    name = event_data["name"]
    class_name = event_data["class"]
    date = event_data["date"]
    return f"{name} - {class_name} ({date})"


def _format_time(total_time_seconds: int) -> str:
    """
    Converts total time from seconds to mm:ss format.
    """
    if total_time_seconds is None:
        return "--"
    minutes, seconds = divmod(total_time_seconds, 60)
    return f"{minutes}.{int(seconds):02}"


def _format_runner_title(result: dict, winning_time: int) -> str:
    """
    Formats a single runner's result into a string with position, name, club, and total time.
    """
    position = result["position"]
    name = result["name"]
    club = result["club"]
    total_time = _format_time(result["total_time"])

    title = ""
    if position is not None:
        title += f"{position:>3}. "
    else:
        title += " --  "

    time_behind = _format_time(result["total_time"] - winning_time)
    title += f"{name[:20]:20} {'('+ club[:23]+ ')':25} {total_time:>6}"
    if position is not None and position > 1:
        title += f" (+{time_behind})"
    elif position is None:
        title += f" ({result['status']})"
    return title


def _format_runner_splits(splits: list, nr_of_elements_per_row: int) -> str:
    """
    Formats a single runner's splits.
    """
    lines = []

    for i in range(0, len(splits), nr_of_elements_per_row):
        total_times = []
        split_times = []
        split_gap_times = []
        split_gap_percentages = []

        for j, split in enumerate(splits[i : i + nr_of_elements_per_row]):
            total_times.append(f"{i + j + 1:>2}. {_format_time(split['time']):>6}")
            split_times.append(
                f"{split['control_code']:>3} {_format_time(split['split_time']):>6}"
            )
            split_gap = split.get("split_gap")
            split_gap_percentage = split.get("percentage_gap")
            if split_gap is not None:
                split_gap_times.append(f"{'+' + _format_time(split_gap):>10}")
                split_gap_percentages.append(
                    f"{'(+' + str(int(split_gap_percentage)) + '%)':>10}"
                )
            else:
                split_gap_times.append(f"{'':>10}")
                split_gap_percentages.append(f"{'':>10}")
        lines.append(" ".join(total_times))
        lines.append(" ".join(split_times))
        lines.append(" ".join(split_gap_times))
        lines.append(" ".join(split_gap_percentages))

    return "\n".join(lines)


def format_results(
    data: dict, analysis: list, detailed_analysis: list, splits_per_row: int
) -> str:
    """
    Formats the results into a string with event data, runner titles, and optionally detailed splits.
    Each runner's result includes position, name, club, total time, and time behind the winner if applicable.

    Args:
        data (dict): The result data from process_xml.
        analysis (list): List of runner names for basic analysis.
        detailed_analysis (list): List of runner names for detailed analysis.
        splits_per_row (int): Number of split times to display per row.

    Returns:
        str: The formatted result string.
    """
    lines = []

    lines.append(_format_event_data(data["event_data"]))

    for result in data["results"]:
        if result["name"] in analysis + detailed_analysis:
            lines.append(_format_runner_title(result, data["winning_time"]))
        if result["name"] in detailed_analysis:
            lines.append(
                _format_runner_splits(result["splits"], splits_per_row)
            )

    return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    from src.process_xml import process_xml

    with open("sample.xml", "r") as file:
        xml_content = file.read()
    analysis = ["Ella Sandberg", "Tilde Jonsson", "Miranda Strand"]
    detailed_analysis = ["Johanna Dahlin"]
    data = process_xml(xml_content)
    formatted_results = format_results(
        data, analysis, detailed_analysis, splits_per_row=7
    )
    print(formatted_results)
