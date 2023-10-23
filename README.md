# DL-Sorter 🗂️

The Download Sorter is a Python script designed to automatically organize files in your downloads directory based on
their types. It identifies files by their extensions and moves them to specific subdirectories for better organization.

---

## Features

- Automatically sorts files by type into dedicated folders.
- Handles common file types like images, documents, audio, video, and more.
- Avoids overwriting existing files with a unique filename generation.
- Customizable for additional file types and destinations.

---

## Getting Started

### Supported Operating Systems

- Linux
- Windows

### Prerequisites

- Python 3.x installed on your system.

### Installation

1. Clone this repository to your local machine.

```bash
git clone https://github.com/s3h4n/DL-Sorter.git
```

### Usage

1. Run the script by executing `python dl_sorter.py`.
2. The script will automatically organize your files into designated folders in your Downloads directory based on their
   types.

### Customization

You can customize the script by adding or modifying file types and their corresponding paths. Edit
Edit `structure.json` file to include your preferred file types and destinations.

```JSON
{
  "Category": {
    "type": [
      ".ext1",
      ".ext2"
    ],
    "path": "Directory/Sub-Directory"
  }
  // Add more custom file types and paths here
}
```

---

## Automation

### Instructions for Windows:

1. Open the Task Scheduler. You can search for it in the Start Menu.
2. Click on `Create Basic Task…`.
3. Name the task and add a description.
4. Choose the `Daily` or `Weekly` or `Monthly` option depending on your preference.
5. Set the start time and date for the task.
6. In the `Action` step, choose `Start a program`.
7. Browse and select your Python executable file (python.exe, which is usually located in the Python directory).
8. In the `Add arguments` field, type the path of the `dl_sorter.py`.
9. Click `Finish`.

### Instructions for Linux:

1. Open Terminal.
2. Type crontab -e to edit the cron table.
3. Add a new line in the following format to run this script:

``` bash
  * * * * * /usr/bin/python3 /path/to/your/dl_sorter.py
```

4. The five asterisks can be replaced with:

- Minute (0 - 59)
- Hour (0 - 23)
- Day of month (1 - 31)
- Month (1 - 12)
- Day of week (0 - 7) (Sunday = 0 or 7)


- For example, if you want to run your script every hour, you would write:

``` bash
0 * * * * /usr/bin/python3 /path/to/your/dl_sorter.py
```

5. Save and exit.

---

## Logging

The script generates a log file named `dl_sorter.log` to track its activity and errors. You can find this log file in
the same directory as the script.

---

## Contributing

This script is open for contributions. If you have any improvements or bug fixes, feel free to submit a pull request.

---

## License

This project is licensed under the Apache v2 License. See the LICENSE file for details.

---

## Acknowledgments

Inspired by the need for better organization in our downloads folder.
