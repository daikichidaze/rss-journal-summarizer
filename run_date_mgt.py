import json
from datetime import datetime
import os
import pytz

# Set timezone to Indochina Time (ICT)
ICT = pytz.timezone('Asia/Bangkok')


def get_current_datetime() -> datetime:
    """Get the current datetime with ICT timezone."""
    return datetime.now(tz=ICT)


def read_last_run_date(file_path):
    """Read the last run date from a JSON file.

    If the file exists but does not contain the 'last_run_date' key,
    or if the file does not exist, return a default date.
    """
    # Default minimum date with timezone
    default_date = datetime(1900, 1, 1).replace(tzinfo=ICT)
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                last_run_date = datetime.strptime(
                    data['last_run_date'], '%Y-%m-%d').replace(tzinfo=ICT)
        except:
            # Return the default date if the key is not found
            last_run_date = default_date
    else:
        # Return the default date if the file does not exist
        last_run_date = default_date
    return last_run_date


def update_last_run_date(file_path, new_date):
    """Update the last run date in a JSON file."""
    with open(file_path, 'w') as file:
        data = {'last_run_date': new_date.strftime('%Y-%m-%d')}
        json.dump(data, file, indent=4)
