import pandas as pd
import numpy as np
import os
import re
import requests
from bs4 import BeautifulSoup
import itertools

# import library
import scrape_ufc_stats_library as LIB
import importlib
importlib.reload(LIB)

# import configs
import yaml
config = yaml.safe_load(open('scrape_ufc_stats_config.yaml'))

# define url to parse
# url = 'http://ufcstats.com/statistics/events/completed' # first page
url = 'http://ufcstats.com/statistics/events/completed?page=all' # all pages

# get soup
soup = LIB.get_soup(url)

# parse event details
event_details_df = LIB.parse_event_details(soup)

# show event details
print((event_details_df))