import os
import time
import json
import chardet
import sys
import argparse

# Function to recursively save the content of files in a folder
def save_file_content(folder_path, file_content, base_path, file_extensions, output_file):
    """
    Recursively traverse the folder and save the content of files with the specified extensions, excluding the output file.

    Parameters:
    folder_path (str): The path to the current folder being processed.
    file_content (dict): Dictionary to store the file paths and their content.
    base_path (str): The base path for calculating relative paths.
    file_extensions (tuple): Tuple of file extensions to filter the files.

    Returns:
    dict: Updated file_content dictionary containing the content of all eligible files.
    """
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return file_content

    try:
        items = os.listdir(folder_path)
    except PermissionError as e:
        print(f"Permission denied while accessing folder {folder_path}: {e}")
        return file_content
    except FileNotFoundError as e:
        print(f"Folder not found during processing: {folder_path}: {e}")
        return file_content
    except Exception as e:
        print(f"Unexpected error while listing folder {folder_path}: {e}")
        return file_content

    for item in items:
        item_path = os.path.join(folder_path, item)
        
        # Skip files marked as output JSON files if .json is included in file_extensions
        if '.json' in file_extensions and item.endswith('.json'):
            try:
                with open(item_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f).get('__metadata__', {})
                    # Check if all required metadata fields are present
                    if all(key in metadata for key in ['file_name', 'project_name', 'creation_time', 'version', 'description', 'file_size']):
                        continue
            # except json.JSONDecodeError as e:
            #     print(f"JSON decoding error while reading file {item_path}: {e}")
            #     continue
            except Exception as e:
                # print(f"Error reading metadata from file {item_path}: {e}")
                pass

        if os.path.isdir(item_path):
            # Recursively process subfolders
            file_content = save_file_content(item_path, file_content, base_path, file_extensions, output_file)
        elif item.endswith(file_extensions):
            relative_path = os.path.relpath(item_path, base_path)
            try:
                with open(item_path, 'rb') as f:
                    content = f.read()
                    encodings = ['utf-8', 'gb2312', 'gbk', 'gb18030', 'big5', 'iso-8859-1', 'windows-1252', 'ascii']
                    decoded = False
                    for encoding in encodings:
                        try:
                            file_content[relative_path] = content.decode(encoding)
                            decoded = True
                            break
                        except UnicodeDecodeError:
                            continue
                        except Exception as e:
                            print(f"Error while decoding file {item_path} with encoding {encoding}: {e}")
                            continue
                    
                    if not decoded:
                        print(f"Unable to decode file {item_path}, saving as binary format")
                        file_content[relative_path] = content.hex()
            except FileNotFoundError:
                print(f"File not found: {item_path}")
            except PermissionError:
                print(f"Permission denied while reading file: {item_path}")
            except Exception as e:
                print(f"Error reading file {item_path}: {e}")

    return file_content


def format_file_size(size):
    """
    Format the file size into a human-readable format.

    Parameters:
    size (int): Size in bytes.

    Returns:
    str: Formatted size string.
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


def main():
    """
    Main function to handle command line arguments and initiate file processing.

    This function parses command line arguments, checks folder validity, and saves the content
    of eligible files to a specified or automatically generated output JSON file.
    """
    parser = argparse.ArgumentParser(description="Save the content of files in a specified folder to a JSON file.")
    parser.add_argument('folder_path', type=str, help='The path to the folder containing the files to be saved.')
    parser.add_argument('file_extensions', nargs='*', default=['.py'], help='Optional. A list of file extensions to include. If not specified, defaults to ".py".')
    parser.add_argument('-o', '--output', type=str, help='Optional. The path to the output JSON file. If not specified, defaults to a timestamp-named file.')
    
    args = parser.parse_args()

    folder_path = args.folder_path
    file_extensions = tuple(ext.lower() for ext in args.file_extensions)  # Normalize file extensions to lowercase
    output_file = args.output

    # Determine the output file path
    if not output_file:
        timestamp = str(int(time.time()))
        folder_name = os.path.basename(os.path.abspath(folder_path))
        output_folder = os.path.abspath(folder_path)
        output_file = os.path.join(output_folder, f"{timestamp}_content.json")

    # Validate the folder path
    if not os.path.exists(folder_path):
        print("The entered folder does not exist!")
        return
    if not os.path.isdir(folder_path):
        print("The entered path is not a directory!")
        return

    # Process the files and gather their content
    try:
        file_content = save_file_content(folder_path, {}, folder_path, file_extensions, output_file)
    except Exception as e:
        print(f"Unexpected error during file processing: {e}")
        return

    # Add metadata to identify the output file
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    description = ""
    readme_file = None
    # Check for README.md or README file for description
    for readme_name in ['README.md', 'README']:
        possible_path = os.path.join(folder_path, readme_name)
        if os.path.exists(possible_path):
            readme_file = possible_path
            break

    if readme_file:
        try:
            with open(readme_file, 'r', encoding='utf-8') as f:
                while True:
                    first_line = f.readline()
                    if not first_line:  # End of file
                        break
                    first_line = first_line.strip()
                    if first_line:  # Stop at the first non-empty line
                        if first_line.startswith('#'):
                            description = first_line.lstrip('#').strip()
                        else:
                            description = first_line
                        break
        except FileNotFoundError:
            print(f"README file not found: {readme_file}")
        except PermissionError:
            print(f"Permission denied while reading README file: {readme_file}")
        except Exception as e:
            print(f"Error reading description from {readme_file}: {e}")

    file_content['__metadata__'] = {
        'file_name': os.path.basename(output_file),
        'project_name': os.path.basename(os.path.abspath(folder_path)),
        'creation_time': timestamp,
        'version': '1.0',
        'description': description
    }

    # Write the gathered content to the output JSON file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(file_content, f, ensure_ascii=False, indent=2)
        
        # Update the actual file size after the file has been written
        file_size = os.path.getsize(output_file)
        file_content['__metadata__']['file_size'] = format_file_size(file_size)
        # Write the updated metadata with file size
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(file_content, f, ensure_ascii=False, indent=2)
        
        # Gather output file information
        formatted_size = file_content['__metadata__']['file_size']
        print(f"File content has been saved to: {output_file} (Size: {formatted_size})")

        # Display the largest files
        sorted_files = sorted(file_content.items(), key=lambda x: len(x[1]) if isinstance(x[1], str) else 0, reverse=True)
        print("Largest files (by size):")
        for file, content in sorted_files[:5]:
            if isinstance(content, str):
                print(f"{file}: {format_file_size(len(content.encode('utf-8')))}")
    except PermissionError as e:
        print(f"Permission denied while writing to output file {output_file}: {e}")
    except FileNotFoundError as e:
        print(f"Output file path not found: {output_file}: {e}")
    except Exception as e:
        print(f"Unexpected error while writing to output file {output_file}: {e}")


if __name__ == "__main__":
    main()
