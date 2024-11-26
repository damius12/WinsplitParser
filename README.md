# WinsplitParser

WinsplitParser is a tool for parsing Winsplits results. It processes the results from a given Winsplits URL and provides advanced analysis, including splits, time, and percentage lost on each split, and stores it in a Word file.

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

You can customize the analysis by passing arguments to the `main` script:

- `--advanced-analysis`: List of runner names for advanced analysis.
- `--basic-analysis-include-same-club`: Whether to include the clubs of the advanced analysis runners in the basic analysis.
- `--basic-analysis-positions`: List of positions to include in the basic analysis.
- `--splits-per-row`: Number of splits to display per row in the output.

### Example

Run the program with custom parameters:
```sh
python -m src.main --advanced-analysis "Runner1,Runner2" --basic-analysis-include-same-club True --basic-analysis-positions "1,2,3" --splits-per-row 5
```

## Development

Run all unittests with:
```sh
python -m unittest discover
```

## Future ideas

- Add a GUI where the event list is shown as a dropdown menu, and then a class can be chosen in a dropdown menu, as well as the possibility to change the default parameters.
- Make it a proper python package and distribute it.
