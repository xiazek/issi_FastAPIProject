"""
This module provides utility functions to ensure that the application database exists.
It initializes the database from a template if it is missing.
"""
import os
import shutil
import stat

DB_FILE = 'movies-extended.db'
DB_TEMPLATE = 'movies-extended.db.template'

def ensure_movies_db_exists():
    """
    Checks if the database file exists. If not, copies it from the template file
    and sets appropriate file permissions.
    """
    if not os.path.exists(DB_FILE):
        if os.path.exists(DB_TEMPLATE):
            print(f"Initializing {DB_FILE} from {DB_TEMPLATE}")
            shutil.copy2(DB_TEMPLATE, DB_FILE)
            # Ensure proper permissions: read/write for owner, read for others (0644)
            os.chmod(DB_FILE, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        else:
            print(f"Warning: {DB_TEMPLATE} not found. Database cannot be initialized.")
