import os
import shutil
import logging


# Define directories
old_version_directory = 'old_textures'
new_version_directory = 'new_textures'
diff_directory = 'diff_textures'

if not os.path.exists(diff_directory):
    os.makedirs('diff_textures')

# Set up logging
logging.basicConfig(filename=os.path.join(diff_directory, 'file_changes.log'), level=logging.INFO)

# Get list of files in each directory
old_version_files = {os.path.relpath(os.path.join(root, name), old_version_directory)
                     for root, dirs, files in os.walk(old_version_directory) for name in files}
new_version_files = {os.path.relpath(os.path.join(root, name), new_version_directory)
                     for root, dirs, files in os.walk(new_version_directory) for name in files}

# Find new or moved files
new_or_moved_files = new_version_files - old_version_files
for file in new_or_moved_files:
    source = os.path.join(new_version_directory, file)
    destination = os.path.join(diff_directory, file)
    
    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    
    # Copy the file
    shutil.copy2(source, destination)
    logging.info('Added or moved file: %s', file)

# Find removed files and log them
removed_files = old_version_files - new_version_files
for file in removed_files:
    logging.info('Removed file: %s', file)
