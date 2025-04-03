# WinsplitParser

**WinsplitParser** is a tool for parsing Winsplits results. It processes results from a given Winsplits URL, performs advanced analysis (e.g., splits, time, and percentage lost on each split), and stores the output in a Word file.

## Features

- Parse Winsplits results directly from a URL.
- Perform advanced analysis of splits, including time and percentage lost.
- Customize analysis parameters for tailored results.

## Prerequisites

Before using WinsplitParser, ensure the following:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/winsplitparser.git
    cd winsplitparser
    ```

2. **Install Python**:  
   Download and install Python from [python.org](https://www.python.org/downloads/).

## Usage

Follow these steps to use WinsplitParser:

1. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

2. **Run the main script**:
    ```sh
    python -m src.main
    ```

3. **Provide the Winsplits URL** when prompted.  
   Example URL:  
   `http://obasen.orientering.se/winsplits/online/sv/default.asp?page=table&databaseId=100310&categoryId=1`

## Custom Parameters

You can customize the analysis by passing arguments to the `main` script:

- `--advanced-analysis`: Specify a list of runner names for advanced analysis.
- `--basic-analysis-include-same-club`: Include runners from the same club in the basic analysis (`True` or `False`).
- `--basic-analysis-positions`: Specify positions to include in the basic analysis (e.g., `"1,2,3"`).
- `--splits-per-row`: Set the number of splits to display per row in the output.

### Example Usage with Parameters

Run the program with custom parameters:
```sh
python -m src.main --advanced-analysis "Runner1,Runner2" \
                   --basic-analysis-include-same-club True \
                   --basic-analysis-positions "1,2,3" \
                   --splits-per-row 5
```

## Development

To run all unit tests:
```sh
python -m unittest discover
```

## Future Enhancements

- **GUI Integration**: Add a graphical interface with dropdown menus for event and class selection, as well as options to modify default parameters.
- **Package Distribution**: Convert WinsplitParser into a proper Python package for easier installation and distribution.
