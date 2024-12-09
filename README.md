# Incremental Backup Script

## Overview
This is a simple Python script designed for incremental backups on Linux systems. It synchronizes source directories with a target backup directory, ensuring that new or updated files are copied while unchanged files are skipped. It also removes files in the target directory that no longer exist in the source.

## Features
- Incremental backups: Only new or updated files are copied.
- Synchronization: Files and directories in the target that are obsolete are removed.
- Verbose mode: Provides detailed information about file actions (copied, skipped, or deleted).
- Lightweight and customizable: Edit the source and target directories directly in the script.

## Prerequisites
- Python 3.x
- Linux-based system (script may work on other platforms but is not tested outside Linux).

## Installation
1. Clone this repository or download the script.
2. Ensure the script has execution permissions:
   ```bash
   chmod +x backup.py
   ```

## Usage
1. Open the script in a text editor and configure the `SOURCE_FOLDERS` and `TARGET_FOLDER` variables to your desired directories.
   - `SOURCE_FOLDERS`: List of directories to back up.
   - `TARGET_FOLDER`: Directory where backups will be stored.

2. Run the script:
   ```bash
   python3 backup.py
   ```
   Use the `-v` or `--verbose` option for detailed logging:
   ```bash
   python3 backup.py -v
   ```

## Example
### Configuration:
```python
SOURCE_FOLDERS = [
    "/home/user/documents",
    "/home/user/photos",
]

TARGET_FOLDER = "/mnt/backup_drive"
```

### Running the script:
```bash
python3 backup.py -v
```

### Output:
```
Starting backup at 09-12-2024 - 12:00:00
Copied: /home/user/documents/file1.txt -> /mnt/backup_drive/documents/file1.txt
Skipped: /home/user/photos/photo1.jpg
Deleted: /mnt/backup_drive/documents/old_file.txt
Backup completed at 09-12-2024 - 12:05:00
Summary: 10 files copied, 20 files skipped, 5 files/directories deleted.
```

## Script Details
- **Incremental Logic**:
  - Compares the last modified time of files in the source and target directories.
  - Copies files if they are new or updated.
  - Removes files and directories in the target that no longer exist in the source.

- **Error Handling**:
  - Checks for the existence of source and target directories.
  - Creates missing directories in the target as needed.

## Limitations
- Symbolic links in the source directories are ignored.
- Requires manual editing of the script for source and target directory paths.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
