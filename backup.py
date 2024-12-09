import os
import shutil
import sys
from datetime import datetime
import argparse

# List of source folders
SOURCE_FOLDERS = [
    "PATH/TO/FOLDER",
    "PATH/TO/SECOND/FOLDER",
    "PATH/TO/...",
]

# Target folder (Drive mounted?)
TARGET_FOLDER = "PATH/TO/FOLDER"

def incremental_backup(source_dir, target_dir, verbose=False):
    """
    Perform an incremental backup from source_dir to target_dir.
    Synchronize files and directories by copying new/updated files and removing obsolete files in the target.
    Returns the count of copied, skipped, and deleted files.
    """
    copied_count = 0
    skipped_count = 0
    deleted_count = 0

    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return copied_count, skipped_count, deleted_count

    if not os.path.exists(target_dir):
        try:
            os.makedirs(target_dir)
        except OSError as e:
            print(f"Error: Could not create target directory '{target_dir}'. {e}")
            return copied_count, skipped_count, deleted_count

    # Copy new/updated files
    for root, dirs, files in os.walk(source_dir):
        relative_path = os.path.relpath(root, source_dir)
        target_root = os.path.join(target_dir, relative_path)

        # Ensure the target directory exists
        if not os.path.exists(target_root):
            try:
                os.makedirs(target_root)
            except OSError as e:
                print(f"Error: Could not create directory '{target_root}'. {e}")
                continue

        # Copy files
        for file in files:
            source_file = os.path.join(root, file)
            target_file = os.path.join(target_root, file)

            # Skip symbolic links
            if os.path.islink(source_file):
#                if verbose:        <- To show every skipped link in verbose, which can be a lot
#                    print(f"Skipped symbolic link: {source_file}")
                continue

            if not os.path.exists(target_file) or \
               os.path.getmtime(source_file) > os.path.getmtime(target_file):
                try:
                    shutil.copy2(source_file, target_file)
                    copied_count += 1
                    if verbose:
                        print(f"Copied: {source_file} -> {target_file}")
                except IOError as e:
                    print(f"Error: Could not copy '{source_file}' to '{target_file}'. {e}")
            else:
                skipped_count += 1
#                if verbose:        <- To show every skipped file in verbose, which is a lot
#                    print(f"Skipped: {source_file}")

    # Remove files/directories in target that do not exist in source
    for root, dirs, files in os.walk(target_dir, topdown=False):
        relative_path = os.path.relpath(root, target_dir)
        source_root = os.path.join(source_dir, relative_path)

        # Remove files
        for file in files:
            target_file = os.path.join(root, file)
            source_file = os.path.join(source_root, file)

            if not os.path.exists(source_file):
                try:
                    os.remove(target_file)
                    deleted_count += 1
                    if verbose:
                        print(f"Deleted: {target_file}")
                except OSError as e:
                    print(f"Error: Could not delete file '{target_file}'. {e}")

        # Remove empty directories
        for dir in dirs:
            target_dir_path = os.path.join(root, dir)
            source_dir_path = os.path.join(source_root, dir)
            if not os.path.exists(source_dir_path):
                try:
                    os.rmdir(target_dir_path)
                    deleted_count += 1
                    if verbose:
                        print(f"Deleted directory: {target_dir_path}")
                except OSError as e:
                    print(f"Error: Could not delete directory '{target_dir_path}'. {e}")

    return copied_count, skipped_count, deleted_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Incremental Backup Script",
        epilog="This script synchronizes source directories with a target backup directory. "
               "It copies new/updated files, skips unchanged files, and removes files in the target "
               "that no longer exist in the source."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed file actions (e.g., copied, skipped, deleted)."
    )
    args = parser.parse_args()

    verbose = args.verbose

    print(f"Starting backup at {datetime.now().strftime('%d-%m-%Y - %H:%M:%S')}")

    if not os.path.exists(TARGET_FOLDER):
        print(f"Error: Target folder '{TARGET_FOLDER}' does not exist. Backup aborted.")
        sys.exit(1)

    total_copied = 0
    total_skipped = 0
    total_deleted = 0

    for source_folder in SOURCE_FOLDERS:
        target_subfolder = os.path.join(TARGET_FOLDER, os.path.basename(source_folder))
        copied, skipped, deleted = incremental_backup(source_folder, target_subfolder, verbose)
        total_copied += copied
        total_skipped += skipped
        total_deleted += deleted

    print(f"Backup completed at {datetime.now().strftime('%d-%m-%Y - %H:%M:%S')}")
    print(f"Summary: {total_copied} files copied, {total_skipped} files skipped, {total_deleted} files/directories deleted.")
