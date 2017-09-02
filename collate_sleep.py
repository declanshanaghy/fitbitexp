import datetime
import json
import logging
import os

import common


today = datetime.date.today()
fout = os.path.join(common.SLEEP_COLLATED, str(today) + '.csv')

sleep_headers = (
    "dateOfSleep",
    "duration",
    "efficiency",
    "endTime",
    "infoCode",
    "isMainSleep",
    "logId",
    "minutesAfterWakeup",
    "minutesAsleep",
    "minutesAwake",
    "minutesToFallAsleep",
    "startTime",
    "timeInBed",
)
summary_headers = (
    "totalMinutesAsleep",
    "totalTimeInBed",
)
stage_headers = (
    "deep",
    "light",
    "rem",
    "wake"
)

common.setup_logging()

with open(os.path.join(common.SLEEP_LOGS, fout), "w") as outfile:
    outfile.write(",".join(sleep_headers + summary_headers + stage_headers))
    outfile.write("\n")

    for f in os.listdir(common.SLEEP_LOGS):
        thisf = os.path.join(common.SLEEP_LOGS, f)
        if not os.path.isfile(thisf) or thisf[-5:] != ".json":
            continue

        logging.info("Processing %s", f)
        with open(thisf) as infile:
            data = json.load(infile)

        summary = data['summary']
        if summary['totalSleepRecords'] > 0:
            for sleep in data['sleep']:
                if sleep['type'] == "stages":
                    values = []

                    for k in sleep_headers:
                        values.append(str(sleep[k]))

                    for k in summary_headers:
                        values.append(str(summary[k]))

                    stages = sleep['levels']['summary']
                    for k in stage_headers:
                        values.append(str(stages[k]['minutes']))

                    outfile.write(",".join(values) + "\n")
