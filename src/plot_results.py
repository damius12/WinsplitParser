from itertools import accumulate

import matplotlib.pyplot as plt


def plot_results(data: dict, advanced_analysis: list, output_file: str) -> None:
    """
    Plots the comparison to the reference splits.

    Args:
        data (dict): The processed data.
        advanced_analysis (list): List of runners for advanced analysis.
    """
    reference_times = [0] + list(accumulate(data["reference_split_times"].values()))

    for person in data["results"]:
        if person["name"] in advanced_analysis:
            times = [0] + [split["time"] for split in person["splits"]]
            delta_times = [
                time - reference_time if time is not None else None
                for time, reference_time in zip(times, reference_times)
            ]
            plt.plot(reference_times, delta_times, label=person["name"])

    plt.gca().invert_yaxis()
    plt.xticks(
        ticks=reference_times,
        labels=["S"] + list(range(1, len(reference_times) - 1)) + ["F"],
    )
    plt.xlim(reference_times[0], reference_times[-1])
    plt.xlabel("Control")
    plt.ylabel("Time (s)")
    plt.grid()
    plt.legend()

    plt.savefig(output_file)
    plt.close()
