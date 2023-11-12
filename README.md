# Chess Analysis Program

## Description
This program analyzes chess games provided in a PGN file format. It utilizes the OpenAI API to generate commentary for each move in the game and outputs a new PGN file with this commentary included.

## Requirements
- Python 3.x
- `python-chess` library for handling chess logic and PGN file manipulation.
- `openai` library for interacting with the OpenAI API to generate move commentary.
- An OpenAI API key set as an environment variable `OPENAI_API_KEY`.

## Installation
1. Ensure you have Python 3.x installed on your system.
2. Install the required Python packages:
   ```
   pip install python-chess openai
   ```
3. Set your OpenAI API key in your environment variables:
   ```
   # On Windows
   set OPENAI_API_KEY=your_api_key_here
   # On Unix/Linux/macOS
   export OPENAI_API_KEY=your_api_key_here
   ```

## Usage
Run the program from the command line, providing the path to the PGN file:
```
python chessanalysis.py path_to_your_pgn_file.pgn
```

## Features
- Command-line interface for easy use.
- Automatic generation of move commentary using AI.
- Outputs a new PGN file with the original game content and AI-generated commentary.

## Functions
- `get_move_commentary(move_san, fen)`: Retrieves commentary for a given move from the OpenAI API.
- `sanitize_filename(name)`: Sanitizes names to create a valid filename for the output PGN file.
- `analyze(pgn_file_path)`: Main function that reads the input PGN file, processes each move, adds commentary, and writes the output to a new PGN file.

## Output
- A new PGN file named `{white_player}_vs_{black_player}.pgn` containing the analyzed game with commentary.

## Note
Ensure you have a valid OpenAI API key and internet connection before running the program.
