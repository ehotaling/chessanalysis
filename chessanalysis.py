import chess.pgn
import os
import argparse
from openai import OpenAI
import re

# Initialize the argument parser to receive a PGN file path from the command line.
parser = argparse.ArgumentParser(description="Analyze a chess PGN file and provide commentary on each move.")
parser.add_argument("pgn_file_path", help="Path to the PGN file to be analyzed")

# Parse the provided command line arguments.
args = parser.parse_args()

# Initialize the OpenAI client with the API key from environment variables.
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],
)

# Define a function to get commentary for a chess move using the OpenAI API.
def get_move_commentary(move_san, fen):
    # Request a completion from the OpenAI API based on the current board position and move.
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system",
             "content": "You are a chess assistant, skilled in analyzing chess games."},
            {"role": "user",
             "content": f"Given the board position {fen}, provide a short commentary on this move {move_san}"}
        ]
    )
    # Extract the commentary from the API's response.
    commentary = completion.choices[0].message.content
    return commentary

# Define a function to sanitize filenames to prevent invalid characters on Windows systems.
def sanitize_filename(name):
    # Replace characters not allowed in Windows filenames with underscores.
    return re.sub(r'[<>:"/\\|?*]', '_', name)

# Define the main function to analyze a chess game from a PGN file.
def analyze(pgn_file_path):
    # Open the PGN file and read the game.
    with open(pgn_file_path) as p:
        game = chess.pgn.read_game(p)

    # Check if player names are '?', absent, or empty, and replace with 'Unknown'.
    white_player = 'Unknown' if game.headers.get('White', 'Unknown') in ['?', ''] else game.headers['White']
    black_player = 'Unknown' if game.headers.get('Black', 'Unknown') in ['?', ''] else game.headers['Black']

    # Sanitize player names to prevent invalid characters in filenames.
    white_player_sanitized = sanitize_filename(white_player)
    black_player_sanitized = sanitize_filename(black_player)

    # Create 'Commentated_Games' directory if it doesn't exist.
    commentated_games_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Commentated_Games')
    if not os.path.exists(commentated_games_dir):
        os.makedirs(commentated_games_dir)

    # Construct a new filename for the output PGN file.
    new_filename = f"{white_player_sanitized}_vs_{black_player_sanitized}.pgn"
    new_file_path = os.path.join(commentated_games_dir, new_filename)

    # Create a new game object to store the game with commentary.
    game_with_commentary = chess.pgn.Game()

    # Copy the game headers from the original game.
    game_with_commentary.headers = game.headers

    # Initialize a node to keep track of the current move in the game commentary.
    node = game_with_commentary

    # Initialize a board object to represent the game state.
    board = game.board()

    # Iterate over all the moves in the game.
    for move in game.mainline_moves():
        move_san = board.san(move)
        fen = board.fen()
        board.push(move)

        # Get commentary for the current move.
        commentary = get_move_commentary(move_san, fen)
        # Add the move and its commentary to the game with commentary.
        node = node.add_variation(move)
        node.comment = commentary
        # Print the move, board state, and commentary to the console.
        print(f"Move: {move_san}")
        print(board)
        print("Commentary:", commentary)
        print("========")

    # Write the game with commentary to a new PGN file.
    with open(new_file_path, "w") as p:
        exporter = chess.pgn.FileExporter(p)
        game_with_commentary.accept(exporter)

    # Return 0 to indicate success.
    return 0

# Execute the analyze function with the PGN file path provided as an argument.
analyze(args.pgn_file_path)
