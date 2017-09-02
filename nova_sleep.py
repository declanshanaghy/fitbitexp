import json
import logging
import os
import pprint

import common
import requests
import requests.auth


NOVA_URL = 'https://api-dshanaghy.splunknovadev.com/v1/events'
NOVA_CLIENT_ID = os.environ['NOVA_CLIENT_ID']
NOVA_CLIENT_SECRET = os.environ['NOVA_CLIENT_SECRET']
NOVA_AUTH = requests.auth.HTTPBasicAuth(NOVA_CLIENT_ID, NOVA_CLIENT_SECRET)

p = pprint.PrettyPrinter()
common.setup_logging()
pd = []


def postit():
    global pd
    if pd:
        r = requests.post(NOVA_URL + '/v1/events',
                          json=pd,
                          auth=NOVA_AUTH)
        if r.status_code == 200:
            c = json.loads(r.content)
            logging.info("Posted %s events", c['count'])
        else:
            raise StandardError(r.content)

    pd = []


for f in os.listdir(common.SLEEP_LOGS):
    thisf = os.path.join(common.SLEEP_LOGS, f)
    if not os.path.isfile(thisf) or thisf[-5:] != ".json":
        continue

    # logging.info("Processing %s", f)
    with open(thisf) as infile:
        data = json.load(infile)

    ev = {
        'entity': 'dek',
        'source': 'fitbit',
    }
    ev.update(data)
    pd.append(ev)

    postit()
