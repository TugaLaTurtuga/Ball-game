import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
save_time = 'saves/Ball_game_times/times_in_seconds.json'
save_high_score = 'saves/Ball_game_times/high_scores_in_seconds.json'

# Function to append the current time to the times JSON file
def ensure_directory(file_path):
    """Ensure that the directory for the given file path exists."""
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def load_json(file_path):
    """Load JSON data from a file, return an empty dictionary if file does not exist."""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except:
            return {}
    return {}


def save_json(file_path, data):
    """Save data to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def save_time_to_json(time, file_path, category):
    ensure_directory(file_path)

    data = load_json(file_path)

    if category not in data:
        data[category] = []

    data[category].append(time)

    save_json(file_path, data)


def update_high_score(time, file_path, category):
    ensure_directory(file_path)

    data = load_json(file_path)

    if category not in data:
        data[category] = float('inf')  # Initialize with a very high score

    if time < data[category]:
        data[category] = time

    save_json(file_path, data)

def get_high_score(row_and_cols):
    category = f"Rows: {row_and_cols[0]}, Cols: {row_and_cols[1]}"

    ensure_directory(save_high_score)

    data = load_json(save_high_score)

    if category not in data:
        data[category] = None

    return data[category]

def Finish_game(Finished, time, row_and_cols):
    if Finished:
        # Create a category string based on row_and_cols
        category = f"Rows: {row_and_cols[0]}, Cols: {row_and_cols[1]}"

        # Save the current time to the times JSON file under the category
        save_time_to_json(time, save_time, category)

        # Update the high score if the current time is better under the category
        update_high_score(time, save_high_score, category)