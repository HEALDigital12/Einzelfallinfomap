#!/usr/bin/env python3
import argparse,hashlib,json,re,time,sys
from datetime import datetime,date
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE='https://www.presseportal.de'
LIST=BASE+'/blaulicht/d/polizei'
UA='HEALDIGITAL-EinzelfallInfoMap/1.0 healdigital12@gmail.com'
DATA=Path('public/data')
CACHE=DATA/'geocode_cache.json'
RULES=[
('To