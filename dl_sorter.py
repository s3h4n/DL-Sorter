from pathlib import Path as path
import platform
import logging
import os

# Logging configuration
logging.basicConfig(
    filename="dl_sorter.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Define the Downloads directory based on OS
if platform.system() == "Linux":
    DOWNLOADS_DIR = f"{path.home()}/Downloads"
elif platform.system() == "Windows":
    DOWNLOADS_DIR = os.path.expanduser("~\\Downloads")
else:
    print("Unsupported operating system.")
    exit(1)

# Default file types and paths
FILE_TYPES_AND_PATHS = {
    "Images": {
        "type": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"],
        "path": f"{DOWNLOADS_DIR}/Images/Raster",
    },
    "Vector": {
        "type": [".eps", ".ai", ".svg"],
        "path": f"{DOWNLOADS_DIR}/Images/Vector",
    },
    "PSD": {
        "type": [".psd"],
        "path": f"{DOWNLOADS_DIR}/Images/PSD",
    },
    "GIF": {
        "type": [".gif"],
        "path": f"{DOWNLOADS_DIR}/Images/GIF",
    },
    "Audio": {
        "type": [".mp3", ".wav", ".flac"],
        "path": f"{DOWNLOADS_DIR}/Media/Audio",
    },
    "Video": {
        "type": [".mp4", ".avi", ".mkv", ".mov"],
        "path": f"{DOWNLOADS_DIR}/Media/Video",
    },
    "Text": {
        "type": [".txt", ".rtf", ".md"],
        "path": f"{DOWNLOADS_DIR}/Documents/Text",
    },
    "PDF": {
        "type": [".pdf"],
        "path": f"{DOWNLOADS_DIR}/Documents/PDF",
    },
    "Word": {
        "type": [".docx"],
        "path": f"{DOWNLOADS_DIR}/Documents/Word",
    },
    "Powerpoint": {
        "type": [".pptx", ".ppt", ".pps"],
        "path": f"{DOWNLOADS_DIR}/Documents/Powerpoint",
    },
    "Spreadsheets": {
        "type": [".xls", ".xlsx", ".ods"],
        "path": f"{DOWNLOADS_DIR}/Documents/Spreadsheets",
    },
    "Scripts": {
        "type": [".py", ".sh", ".bat", ".ps1"],
        "path": f"{DOWNLOADS_DIR}/Programs/Scripts",
    },
    "Packages": {
        "type": [".deb", ".rpm", ".pkg", ".msi", ".dmg", ".exe", ".sh"],
        "path": f"{DOWNLOADS_DIR}/Programs/Executables",
    },
    "Compressed": {
        "type": [".zip", ".rar", ".7z", ".gz", ".tar", ".bz2"],
        "path": f"{DOWNLOADS_DIR}/Archives/Compressed",
    },
    "ISO": {
        "type": [".iso"],
        "path": f"{DOWNLOADS_DIR}/Archives/ISO",
    },
    "Fonts": {
        "type": [".ttf", ".otf", ".woff", ".woff2"],
        "path": f"{DOWNLOADS_DIR}/Fonts",
    },
    "Database": {
        "type": [".sqlite", ".db", ".sql"],
        "path": f"{DOWNLOADS_DIR}/Databases",
    },
}


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

        while path(path(destination).joinpath(new_filename)).exists():
            new_filename = f"{base}_{count}{ext}"
            count += 1

        return new_filename

    except Exception as e:
        print(f"Error while renaming {filename}: {e}")
        logging.error(f"Error while renaming the file {filename}: {e}")

        logging.critical(f"Aborted.")

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
        if not path(destination).exists():
            # print(f"{destination} not found. Attempting to create...")
            logging.info(f"{destination} not found. Attempting to create...")

            try:
                path(destination).mkdir(parents=True, exist_ok=True)

                # print(f"{destination} created.")
                logging.info(f"{destination} created.")

            except Exception as e:
                print(f"Error while creating {destination}: {e}")
                logging.error(f"Error while creating {destination}: {e}")

                return False

        _source_file_path = path(source).joinpath(filename)
        _destination_file_path = path(destination).joinpath(filename)

        if path(_destination_file_path).exists():
            _destination_file_path = path(destination).joinpath(
                get_unique_filename(filename, destination)
            )

        path(_source_file_path).rename(_destination_file_path)
        return True

    except Exception as e:
        print(f"Error: {e}")
        logging.error(f"Error: {e}")

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
            for ftype in file_types:
                if filename.endswith(ftype):
                    # print(f"Moving: {source}/{item}")
                    # logging.info(f"Moving: {source}/{item}")

                    if move_single_file(filename, source, destination):
                        successful_moves += 1

        return successful_moves

    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    s_moves = {}

    for file_type in FILE_TYPES_AND_PATHS:
        # Update list every iteration.
        _file_list = os.listdir(DOWNLOADS_DIR)

        s_moves[file_type] = move_multiple_files(
            source=DOWNLOADS_DIR,
            destination=FILE_TYPES_AND_PATHS[file_type]["path"],
            files_list=_file_list,
            file_types=FILE_TYPES_AND_PATHS[file_type]["type"],
        )

    print(s_moves)


if __name__ == "__main__":
    main()
