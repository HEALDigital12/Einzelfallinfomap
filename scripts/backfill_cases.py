#!/usr/bin/env python3
import argparse, hashlib, json, re, time
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE = 'https://www.presseportal.de'
LIST_URL = BASE + '/blaulicht/d/polizei'
UA = 'HEALDIGITAL-EinzelfallInfoMap/1.0'
DATA = Path('public/data')
LOGS = DATA / 'logs'

RULES = [
    ('Toetungsdelikt', ['mord', 'totschlag', 'tötungsdelikt', 'toetungsdel