"""
File reader tool for reading local files.
"""

import os
from typing import Optional


class FileReaderTool:
    """
    File reader tool for reading file contents.
    """

    @staticmethod
    def read_file(filepath: str, lines: Optional[tuple] = None) -> str:
        """
        Read file contents.

        Args:
            filepath (str): Path to the file.
            lines (Optional[tuple]): (start, end) line numbers to read (1-indexed).

        Returns:
            str: File contents or error message.
        """
        try:
            # Security: only allow reading from current directory and subdirectories
            if filepath.startswith("/") or ".." in filepath:
                return "Error: Can only read files from current directory."

            if not os.path.exists(filepath):
                return f"Error: File '{filepath}' not found."

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if lines:
                start, end = lines
                file_lines = content.split('\n')
                content = '\n'.join(file_lines[start - 1:end])

            return content
        except Exception as e:
            return f"Error reading file: {str(e)}"

    @staticmethod
    def is_file_read_needed(user_input: str) -> bool:
        """Check if file reader tool is needed."""
        file_keywords = ["read", "file", "content", "show", "display", ".txt", ".py", ".json"]
        return any(keyword in user_input.lower() for keyword in file_keywords)

    @staticmethod
    def list_files(directory: str = ".") -> list:
        """List files in a directory."""
        try:
            return os.listdir(directory)
        except Exception as e:
            return f"Error: {str(e)}"
