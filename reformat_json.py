import os
import json


LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
SLEEP_LOGS = os.path.join(LOGS_DIR, 'sleep')
REFORMAT_DIR = os.path.join(LOGS_DIR, 'sleep-reformatted')

if not os.path.exists(REFORMAT_DIR):
    os.makedirs(REFORMAT_DIR)

for f in os.listdir(SLEEP_LOGS):
    with open(os.path.join(SLEEP_LOGS, f)) as infile:
        data = json.load(infile)

    out = os.path.join(REFORMAT_DIR, f)
    with open(out, "w") as outfile:
        print("Wrote: " + out)
        json.dump(data, outfile, indent=4, sort_keys=True)

print("Done")
