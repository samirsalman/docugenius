import os
from pathlib import Path
from typing import List


def find_python_files(root_dir: str) -> List[str]:
    """
    Return a list of all the Python files in the specified directory and its subdirectories.

    Args:
        root_dir (str): The root directory to search for Python files.

    Returns:
        List[str]: A list of all the Python files in the specified directory and its subdirectories.

    Raises:
        FileNotFoundError: If the specified root directory does not exist.
        PermissionError: If there is a permission error accessing the directory.

    Examples:
        >>> find_python_files('/path/to/directory')
        ['/path/to/directory/file1.py', '/path/to/directory/subdir/file2.py']
    """

    file_list = []
    root_path = Path(root_dir)
    for root, _, files in root_path.walk():
        for file in files:
            if file.endswith(".py"):
                file_list.append(os.path.join(root, file))
    return file_list
