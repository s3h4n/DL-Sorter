# DL-Sorter 🗂️

The Download Sorter is a Python script designed to automatically organize files in your downloads directory based on their types. It identifies files by their extensions and moves them to specific subdirectories for better organization.

## Features

- Automatically sorts files by type into dedicated folders.
- Handles common file types like images, documents, audio, video, and more.
- Avoids overwriting existing files with a unique filename generation.
- Customizable for additional file types and destinations.

## Getting Started

### Prerequisites

- Python 3.x installed on your system.

### Installation

1. Clone this repository or download the `dl_sorter.py` script to your local machine.

### Usage

1. Run the script by executing `python dl_sorter.py`.
2. The script will automatically organize your files into designated folders in your Downloads directory based on their types.

### Customization

You can customize the script by adding or modifying file types and their corresponding paths. Edit the `FILE_TYPES_AND_PATHS` dictionary in the script to include your preferred file types and destinations.

```python
FILE_TYPES_AND_PATHS = {
    "CustomType": {
        "type": [".ext1", ".ext2"],
        "path": f"{DOWNLOADS_DIR}/CustomDirectory",
    },
    # Add more custom file types and paths here
}
```

### Supported Operating Systems

- Linux
- Windows

### Logging

The script generates a log file named dl_sorter.log to track its activity and errors. You can find this log file in the same directory as the script.

## Contributing

This script is open for contributions. If you have any improvements or bug fixes, feel free to submit a pull request.

## License

This project is licensed under the Apache v2 License. See the LICENSE file for details.

## Acknowledgments

Inspired by the need for better organization in our downloads folder.
