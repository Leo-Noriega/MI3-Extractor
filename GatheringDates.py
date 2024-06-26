import json
import os
from datetime import datetime

from DBConnection import client

db = client['sgen']
collection = db['data']

no_series = collection.distinct('no_serie')

for no_serie in no_series:
    results = collection.find({
        "no_serie": no_serie,
        "values.0": None,
        "values.1": None,
        "values.2": None,
        "values.3": None,
        "values.4": None,
        "values.5": None,
        "values.6": None
    }, {"date": 1, "device_id": 1})

    dates = {}

    for result in results:
        date_str = result['date'].strftime("%Y-%m-%d %H:%M:%S")
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        day_str = date_obj.strftime("%Y-%m-%d")

        if day_str not in dates:
            dates[day_str] = []

        dates[day_str].append({
            "device_id": result['device_id'],
            "no_serie": no_serie,
            "date_str": date_str
        })

    for day, day_dates in dates.items():
        os.makedirs(f'NullDates/{no_serie}/{day}/', exist_ok=True)

        with open(f'NullDates/{no_serie}/{day}/{day}.json', 'w') as f:
            json.dump(day_dates, f, indent=4)
