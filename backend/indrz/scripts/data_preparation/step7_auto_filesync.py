import os
import time
from pathlib import Path, PurePath

from utils import get_dxf_files


def is_file_older_than(file_path: str, days: float):
    '''
    Check if a file was modified in the last n days.
    '''

    # Get the modification time of the file in seconds since the epoch
    modification_time = os.path.getctime(file_path)

    # Get the current time in seconds since the epoch
    # cronjob executes this at 23:44 every day see crontab -e on server
    current_time = time.time()

    # Calculate the time difference in seconds
    time_difference = current_time - modification_time

    # Calculate the time difference in days
    time_difference_days = time_difference / (24 * 3600)

    # Check if the file was modified in the last 1 days.
    if time_difference_days <= days:
        return True
    else:
        return False


def new_dxf_files(days: float):
    '''
    Returns a list of new dxf files in the DXF_ROOT_PATH_PROD folder.
    not older than 1 day as defined in function is_file_older_than

    '''

    dxf_files = []
    # dxf_dir_path = Path(os.getenv('DXF_ROOT_PATH'))

    for root, dirs, files in os.walk(os.getenv('DXF_ROOT_PATH'), topdown=False):
        for file in files:
            if PurePath(file).suffix == ".dxf":
                file_full_path = os.path.join(root, file)

                if is_file_older_than(file_full_path, days):
                    print(file_full_path)
                    dxf_files.append(file_full_path)

    return dxf_files
