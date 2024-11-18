def _compute_best_split_times(results: list) -> dict:
    """
    Computes the best split times for each control from the parsed results.

    Args:
        results (list): A list of dictionaries, each containing information about a person's result.

    Returns:
        dict: A dictionary where the keys are control codes (str) and the values are the best split times (float).
              The best split time is the minimum split time recorded for each control code.
    """
    best_split_times = {}

    for person in results:
        for split in person["splits"]:
            control_code = split["control_code"]
            split_time = split["split_time"]

            if split_time is None:
                continue
            elif control_code not in best_split_times:
                best_split_times[control_code] = split_time
            elif split_time < best_split_times[control_code]:
                best_split_times[control_code] = split_time

    return best_split_times


def _add_split_analysis(results: list, best_split_times: dict) -> None:
    """
    Adds split analysis information to each runner's splits.

    Args:
        results (list): A list of dictionaries, each containing information about a person's result.
        best_split_times (dict): A dictionary mapping control codes to the best split times
                                    recorded for those control points.

    Modifies:
        results (list): Updates the split information for each runner with split gaps and percentage gaps.
    """
    for person in results:
        for split in person["splits"]:
            control_code = split["control_code"]
            split_time = split["split_time"]
            best_split_time = best_split_times[control_code]

            if split_time is None:
                split_gap = None
                percentage_gap = None
            else:
                split_gap = split_time - best_split_time
                percentage_gap = (split_gap / best_split_time) * 100

            split["split_gap"] = split_gap
            split["percentage_gap"] = percentage_gap


def process_data(data: dict):
    """
    Processes the given data to extract split information and compute the best split times
    for each control point. Updates the results with split analysis and sets the winning time.

    Args:
        data (dict): A dictionary containing race results and other related information.

    Modifies:
        data (dict): Updates the 'results' key with split analysis and adds the 'winning_time' key.
    """
    results = data["results"]
    best_split_times = _compute_best_split_times(results)
    _add_split_analysis(results, best_split_times)

    data["results"] = results
    data["winning_time"] = results[0]["total_time"]
