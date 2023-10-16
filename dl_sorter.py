from pathlib import Path as path
import platform
import logging
import os

logging.basicConfig(
    filename="dl_sorter.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Define the Downloads directory
if platform.system() == "Linux":
    DOWNLOADS_DIR = f"{path.home()}/Downloads"
elif platform.system() == "Windows":
    DOWNLOADS_DIR = os.path.expanduser("~\\Downloads")
else:
    print("Unsupported operating system.")
    exit(1)

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
    destination_directory: str,
    filename: str,
):
    """
    Generate a unique filename to avoid overwriting existing files in the destination directory.

    Arguments:
        destination_directory (str): The directory where the file is to be moved.
        filename (str): The original filename.

    Returns:
        str: A unique filename that doesn't exist in the destination directory.
    """

    base, ext = os.path.splitext(filename)
    count = 1
    new_filename = filename

    while os.path.exists(os.path.join(destination_directory, new_filename)):
        new_filename = f"{base}_{count}{ext}"
        count += 1

    return new_filename


def move_single_file(
    source: str,
    destination: str,
    destination_directory: str,
):
    """
    Move a single file from the source to the destination, ensuring it doesn't overwrite existing files.

    Arguments:
        source (str): The path to the source file.
        destination (str): The desired path of the file in the destination directory.
        destination_directory (str): The directory where the file should be moved.

    Returns:
        bool: True if the file is successfully moved, False otherwise.
    """
    try:
        if path(destination).exists():
            destination = get_unique_filename(destination_directory, destination)

        path(source).rename(destination)
        return True

    except FileNotFoundError:
        print("Error: File Not Found. Attempting to create destination...")
        logging.error(msg="File Not Found. Attempting to create destination...")

        try:
            path(destination_directory).mkdir(parents=True, exist_ok=True)

            print("Destination directory created.")
            logging.info("Destination directory created.")

            path(source).rename(destination)

            # print("File moved successfully.")
            # logging.info("File moved successfully.")

            return True

        except Exception as e:
            print(f"Error while creating destination: {e}")
            logging.error(f"Error while creating destination: {e}")

            return False

    except FileExistsError:
        # TODO: Fix this with auto renaming feature.
        print("Error: File Already exists.")
        logging.error("Error: File Already exists.")

        return False


def move_multiple_files(
    source: str,
    files_list: str,
    destination: str,
    file_types: list,
):
    """
    Move multiple files from the source to the destination based on file types.

    Arguments:
        source (str): The source directory containing the files to be moved.
        files_list (str): A list of filenames to be moved.
        destination (str): The destination directory where the files should be moved.
        file_types (list): A list of file extensions to filter the files to be moved.

    Returns:
        int: The number of files successfully moved.
    """

    successful_moves = 0

    try:
        if not files_list:
            print("No files to move.")
            return True

        for item in files_list:
            for ft in file_types:
                if item.endswith(ft):
                    source_path = f"{source}/{item}"
                    destination_path = f"{destination}/{item}"

                    # print(f"Moving: {source}/{item}")
                    # logging.info(f"Moving: {source}/{item}")

                    if move_single_file(
                        source=source_path,
                        destination=destination_path,
                        destination_directory=destination,
                    ):
                        successful_moves += 1

        return successful_moves

    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    s_moves = {}

    for file_type in FILE_TYPES_AND_PATHS:
        s_moves[file_type] = move_multiple_files(
            source=DOWNLOADS_DIR,
            files_list=os.listdir(DOWNLOADS_DIR),
            destination=FILE_TYPES_AND_PATHS[file_type]["path"],
            file_types=FILE_TYPES_AND_PATHS[file_type]["type"],
        )

    print(s_moves)


main()
