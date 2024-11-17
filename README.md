# WinsplitParser

WinsplitParser is a tool for parsing Winsplits results. It processes the results from a given Winsplits URL and provides advanced analysis, including splits, time, and percentage lost on each split.

## Features

- Parses Winsplits results from a given URL.
- Provides advanced analysis of splits, including time and percentage lost.
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

4. **Enter the Winsplits URL** when prompted, for example:
http://obasen.orientering.se/winsplits/online/sv/default.asp?page=table&databaseId=100310&categoryId=1

## Parameters

You can customize the analysis by setting parameters in the `main` function in `src/main.py`:

- `ADVANCED_ANALYSIS`: List of runner names for advanced analysis.
- `BASIC_ANALYSIS_INCLUDE_SAME_CLUB`: Whether to include the clubs of the advanced analysis runners in the basic analysis.
- `BASIC_ANALYSIS_POSITIONS`: List of positions to include in the basic analysis.
- `SPLITS_PER_ROW`: Number of splits to display per row in the output.

## Development

Run all unittests with:
```sh
python -m unittest discover
```

## Future ideas

- Add a graph for visually analysing the performance, based on the gap to the mean of the top 3 splits on each leg (similar to the feature present on [swiss orienteering](https://www.o-l.ch/cgi-bin/results?type=rang&year=2024&rl_id=7592&kat=HAL&zwizt=1&graph=1)).
- Add a GUI where the event list is shown as a dropdown menu, and then a class can be chosen in a dropdown menu, as well as the possibility to change the default parameters.
- Make it a proper python package and distribute it.