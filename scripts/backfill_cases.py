#!/usr/bin/env python3
"""Historical backfill entrypoint for EinzelfallInfoMap."""
import argparse
import json
from datetime import datetime
from pathlib import Path

DATA = Path('public/data')
LOGS = DATA / 'logs'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--from', dest='date_from', required=True)
    parser.add_argument('--to', dest='date_to', required=True)
