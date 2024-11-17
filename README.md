# WinsplitParser

WinsplitParser is a tool for parsing Winsplits results. It processes the results from a given Winsplits URL and provides detailed analysis, including splits, time, and percentage lost on each split.

## Features

- Parses Winsplits results from a given URL.
- Provides detailed analysis of splits, including time and percentage lost.
- Allows customization of analysis parameters.

## Usage

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/winsplitparser.git
    cd winsplitparser
    ```

2. **Install the required dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the main script**:
    ```sh
    python -m src.main
    ```

4. **Enter the Winsplits URL** when prompted.

## Parameters

You can customize the analysis by setting parameters in the `main` function in `src/main.py`:

- `SPLITS_PER_ROW`: Number of splits to display per row in the output.
- `POSITIONS`: List of positions to include in the analysis.
- `DETAILED_ANALYSIS`: List of runner names for detailed analysis.
