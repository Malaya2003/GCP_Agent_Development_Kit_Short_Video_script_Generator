# youtube_short_assistance/util.py
import os

def load_instruction_from_file(file_path):
    """Loads instructions from a text file."""
    try:
        # It's often better to construct the path relative to this file
        # or use absolute paths, but for simplicity, we assume the path
        # is relative to where the main script is run.
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Error: Instruction file not found at '{file_path}'")
        # Decide how to handle: return None, return default string, or raise error
        raise  # Re-raise the exception to stop execution if file is critical
    except Exception as e:
        print(f"Error loading instructions from {file_path}: {e}")
        raise # Re-raise for clarity


# You might add other utility functions here later