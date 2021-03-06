import datetime
import logging
import json
import os
import sys

import fitbit
import fitbit.exceptions
import yaml

import common


TOKEN_FILE = "fitbit.token.json"
CREDS_FILE = "creds.secret.yml"

creds = yaml.load(CREDS_FILE)
CODE = creds['CODE']
CLIENT_ID = creds['CLIENT_ID']
CLIENT_SECRET = creds['CLIENT_SECRET']

REDIRECT_URI="http://localhost"

# {
#     "token_type": "Bearer",
#     "user_id": "23EDC",
#     "refresh_token": "afa534c...",
#     "access_token": "deadb33f...",
#     "scope": ["social", "settings", "activity", "location", "weight", "nutrition", "profile", "heartrate", "sleep"],
#     "expires_in": 28800, "expires_at": 1502414481.556811
# }
SAVE_KEYS = {
    "token_type", "user_id", "refresh_token", "access_token",
    "scope", "expires_in", "expires_at",
}

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as infile:
            token = json.load(infile)
        logging.info("Loaded token: %s", token)
        return token

def get_new_token_from_code():
    f = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET)
    token = f.client.fetch_access_token(CODE, redirect_uri=REDIRECT_URI)
    logging.info("Retrieved token")
    return save(token)


def save(token):
    t = {}
    for k in SAVE_KEYS:
        t[k] = token[k]

    with open(TOKEN_FILE, 'w') as outfile:
        json.dump(t, outfile, indent=4, sort_keys=True)

    logging.info("Saved token: %s", t)
    return t


def get_sleep_log_filename(dt):
    return os.path.join(common.SLEEP_LOGS, str(dt) + ".json")


def save_sleep(dt, sleep):
    with open(get_sleep_log_filename(dt), 'w') as outfile:
        json.dump(sleep, outfile, indent=4, sort_keys=True)
        logging.info("Wrote sleep log for %s", str(dt))


common.setup_logging()
token = load_token()

if token is None and CODE:
    token = get_new_token_from_code()

if token is None:
    print("Unable to load token. Please follow the auth process to get a code and re-run")
    sys.exit(1)

# At this point we have a valid token
f = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET,
                  access_token=token["access_token"],
                  refresh_token=token["refresh_token"],
                  expires_at=token["expires_at"],
                  refresh_cb=save)

today = datetime.date.today()
stop_date = today - datetime.timedelta(days=730)
download_date = today

while download_date >= stop_date:
    try:
        if os.path.exists(get_sleep_log_filename(download_date)):
            logging.info("Sleep data for %s already exists" % download_date)
        else:
            logging.info("Downloading sleep data for %s" % download_date)
            sleep = f.get_sleep(download_date)
            save_sleep(download_date, sleep)

        download_date -= datetime.timedelta(days=1)
    except fitbit.exceptions.HTTPTooManyRequests as ex:
        t = (datetime.datetime.now() +
             datetime.timedelta(seconds=ex.retry_after_secs))
        logging.error("Too many requests. Try again after %s" % t)
        break

logging.info("Completed downloads")
