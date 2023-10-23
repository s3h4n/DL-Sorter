"""

Author: W.M.S.R. Weerasekara
About: This script organizes files from a Downloads directory into specified subdirectories based on file types.
GitHub: https://github.com/s3h4n/DL-Sorter

"""

import json
import logging
import os
import platform
import time
from pathlib import Path


# Logging configuration
logging.basicConfig(
    filename="dl_sorter.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# Define the Downloads directory based on OS
if platform.system() == "Linux":
    DOWNLOADS_DIR = f"{Path.home()}/Downloads"
elif platform.system() == "Windows":
    DOWNLOADS_DIR = os.path.expanduser("~\\Downloads")
else:
    print("Error: Unsupported operating system.")
    logging.error("Error: Unsupported operating system.")
    exit(1)


def get_format(filename: str):
    """
    Get the list of file formats and their destinations as from pre-defined JSON file.
    """
    try:
        with open(filename, "r") as fp:
            structure = json.load(fp)

        print(f"`{filename}` successfully loaded.")
        logging.info(f"`{filename}` successfully loaded.")

        return structure

    except Exception as e:
        print(f"Error: Failed to load `{filename}`: {e}")
        logging.error(f"Error: Failed to load `{filename}`: {e}")
        exit(1)


def get_unique_filename(
    filename: str,
    destination: str,
):
    """
    Generate a unique filename to avoid overwriting existing files in the destination directory.
    """

    try:
        base, ext = os.path.splitext(filename)
        count = 1
        new_filename = filename

        while Path(Path(destination).joinpath(new_filename)).exists():
            new_filename = f"{base}_{count}{ext}"
            count += 1

        return new_filename

    except Exception as e:
        print(f"Error: Failed to rename `{filename}`: {e}")
        logging.error(f"Error: Failed to rename `{filename}`: {e}")
        exit(1)


def move_single_file(
    filename: str,
    source: str,
    destination: str,
):
    """
    Move a single file from the source to the destination, ensuring it doesn't overwrite existing files.
    """

    try:
        if not Path(destination).exists():
            logging.info(f"`{destination}` not found. Attempting to create...")

            try:
                Path(destination).mkdir(parents=True, exist_ok=True)
                logging.info(f"`{destination}` created.")

            except Exception as e:
                print(f"Error while creating `{destination}`: {e}")
                logging.error(f"Error while creating `{destination}`: {e}")

                return False

        _source_file_path = Path(source).joinpath(filename)
        _destination_file_path = Path(destination).joinpath(filename)

        if Path(_destination_file_path).exists():
            _destination_file_path = Path(destination).joinpath(
                get_unique_filename(filename, destination)
            )

        Path(_source_file_path).rename(_destination_file_path)
        return True

    except Exception as e:
        print(f"Error: Couldn't move file `{filename}` : {e}")
        logging.error(f"Error: Couldn't move file `{filename}` : {e}")

        return False


def move_multiple_files(
    source: str,
    destination: str,
    files_list: list,
    file_types: list,
):
    """
    Move multiple files from the source to the destination based on file types.
    """

    successful_moves = 0

    try:
        if not files_list:
            print("No files to move.")
            return True

        for filename in files_list:
            for filetype in file_types:
                if filename.endswith(filetype):
                    if move_single_file(filename, source, destination):
                        successful_moves += 1

        return successful_moves

    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    """
    Entry point for the script.
    """
    __successful_moves = {}

    __structure = get_format(filename="structure.json")

    for file_type in __structure:
        # Update list every iteration.
        __file_list = os.listdir(DOWNLOADS_DIR)
        __sub_directory = __structure[file_type]["path"]

        __successful_moves[file_type] = move_multiple_files(
            source=DOWNLOADS_DIR,
            destination=f"{Path(DOWNLOADS_DIR).joinpath(__sub_directory)}",
            files_list=__file_list,
            file_types=__structure[file_type]["type"],
        )

    print(__successful_moves)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"Execution time: {end - start} seconds")
