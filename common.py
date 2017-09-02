import logging
import os
import sys


LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
SLEEP_LOGS = os.path.join(LOGS_DIR, 'sleep')
SLEEP_COLLATED = os.path.join(LOGS_DIR, 'sleep-collated')


if not os.path.exists(SLEEP_LOGS):
    os.makedirs(SLEEP_LOGS)

if not os.path.exists(SLEEP_COLLATED):
    os.makedirs(SLEEP_COLLATED)


def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s:%(threadName)s:%(name)s:"
                                  "%(levelname)s:%(message)s")
    ch.setFormatter(formatter)
    root.addHandler(ch)


