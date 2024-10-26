# File Content Saver Script

## Overview
This script is designed to recursively scan a specified folder, read the content of files with specific extensions, and save all the gathered data into a JSON file. This tool is particularly useful for archiving or backing up the content of scripts, project files, or any other types of text-based files.

The output file contains a JSON representation of the content of each eligible file, organized with metadata that provides details like project name, creation time, and description. The description can be sourced from a `README.md` or `README` file if present in the folder.

## Features
- **Recursive Folder Scanning**: The script can scan all subfolders of the specified directory.
- **Customizable File Types**: The user can specify which file extensions to include when collecting content.
- **Automatic Metadata Generation**: Metadata, including project name, description, creation time, and file size, is added to the output JSON file.
- **Efficient Encoding Handling**: Attempts multiple encodings to ensure correct decoding of file content, and saves binary content as hexadecimal if decoding is not possible.
- **Avoid Redundant Processing**: The script skips the output JSON file if it is present in the scanned directory.
- **Largest File Display**: Displays the largest files (by size) in the terminal after processing.

## Usage
The script can be executed from the command line using Python. It requires a folder path and optionally accepts file extensions and an output file path.

### Command Line Arguments
- **folder_path** (required): The path to the folder containing the files to be saved.
- **file_extensions** (optional): A list of file extensions to include. If not specified, defaults to `.py`. This argument can be a list of multiple extensions.
- **-o, --output** (optional): The path to the output JSON file. If not provided, the script will generate an output file in the target directory with a timestamp-based name.

### Example Commands
```sh
# Save content of all .py files in the current directory
python file_saver.py . .py

# Save content of .txt and .md files in the folder '/path/to/folder'
python file_saver.py /path/to/folder .txt .md

# Save content of .py files and specify an output file
python file_saver.py /path/to/folder .py -o /path/to/output/content.json
```

### Metadata Description
The output JSON file will contain a `__metadata__` section that includes the following:
- **file_name**: The name of the output JSON file.
- **project_name**: The name of the folder being processed.
- **creation_time**: The timestamp when the JSON file was created.
- **version**: The version of the script (default is `1.0`).
- **description**: Description of the project, sourced from `README.md` or `README` if available.
- **file_size**: Size of the output JSON file, formatted in a readable form (e.g., KB, MB).

## Error Handling
The script includes error handling for various potential issues:
- **Folder Not Found**: If the provided folder path does not exist, an error message will be displayed.
- **Permission Issues**: If the script lacks the necessary permissions to read files or directories, a descriptive error message will be printed.
- **Encoding Problems**: Files that cannot be decoded with common encodings will be saved in their hexadecimal representation to prevent data loss.
- **Empty Files**: If the README is empty or does not contain valid text, the `description` will be left blank.

## Requirements
- Python 3.x

The script does not require any additional libraries outside of the Python Standard Library. However, having Python 3.6 or newer is recommended for optimal compatibility.

## Notes
- The script will attempt to process files with different encodings (`utf-8`, `gb2312`, `gbk`, etc.). If none of these encodings work, the content is saved in hexadecimal to prevent data loss.
- The generated JSON file may contain large volumes of text if many or large files are processed. Be cautious with the target directory if disk space is a concern.

## License
This script is provided "as is" without warranty of any kind. Feel free to modify and distribute as needed.

## Author
Created by [Your Name], [Year].

