import json
from datetime import datetime, timedelta
import os

import pytz

# Indochina Timezone
ICT = pytz.timezone('Asia/Bangkok')


def get_current_datetime() -> datetime:
    return datetime.now(tz=ICT)


def read_last_run_date(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            last_run_date = datetime.strptime(
                data['last_run_date'], '%Y-%m-%d')
    else:
        last_run_date = datetime.min
    return last_run_date


def update_last_run_date(file_path, new_date):
    with open(file_path, 'w') as file:
        data = {'last_run_date': new_date.strftime('%Y-%m-%d')}
        json.dump(data, file, indent=4)
    return


def get_new_data_since(last_run_date):
    today = datetime.now()
    if today > last_run_date + timedelta(days=1):
        return ["データ1", "データ2"]
    return []
