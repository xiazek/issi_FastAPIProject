"""
This module provides utility functions to ensure that the application database exists.
It initializes the database from a template if it is missing.
"""
import os
import shutil
import stat

def ensure_movies_db_exists(db_file: str):
    """
    Checks if the database file exists. If not, copies it from the template file
    and sets appropriate file permissions.
    """
    db_template = db_file + ".template"
    if not os.path.exists(db_file):
        if os.path.exists(db_template):
            print(f"Initializing {db_file} from {db_template}")
            shutil.copy2(db_template, db_file)
            # Ensure proper permissions: read/write for owner, read for others (0644)
            os.chmod(db_file, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        else:
            print(f"Warning: {db_template} not found. Database cannot be initialized.")
