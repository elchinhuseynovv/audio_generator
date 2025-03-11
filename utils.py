"""
Utility functions for the Voice-to-Music Generator
"""

import os
import time
from datetime import datetime

def generate_filename(prefix, extension):
    """
    Generate a unique filename with timestamp
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"

def get_file_path(directory, filename):
    """
    Get the full path for a file in a specific directory
    """
    return os.path.join(directory, filename)

def log_error(error, context=""):
    """
    Log error messages with timestamp and context
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_msg = f"[{timestamp}] ERROR: {str(error)}"
    if context:
        error_msg += f" (Context: {context})"
    print(error_msg)
    return error_msg

class Timer:
    """
    Context manager for timing operations
    """
    def __init__(self, operation_name):
        self.operation_name = operation_name

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        print(f"{self.operation_name} took {self.duration:.2f} seconds")