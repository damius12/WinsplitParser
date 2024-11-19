import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="WinsplitParser")
    parser.add_argument("--url", help="Winsplits URL", default=None)
    parser.add_argument(
        "--advanced_analysis",
        nargs="+",
        default=["Sebastian Inderst"],
        help="List of runner names for advanced analysis",
    )
    parser.add_argument(
        "--basic_analysis_include_same_club",
        action="store_true",
        default=True,
        help="Include runners from the same club in the basic analysis",
    )
    parser.add_argument(
        "--basic_analysis_positions",
        nargs="+",
        type=int,
        default=[1, 2, 3] + list(range(10, 60, 10)),
        help="List of positions for basic analysis",
    )
    parser.add_argument(
        "--splits_per_row",
        type=int,
        default=7,
        help="Number of splits to display per row in the output",
    )
    return parser.parse_args()
