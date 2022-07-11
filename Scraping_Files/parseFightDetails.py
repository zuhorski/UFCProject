# imports
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

# parse one event for fight details

# define url to parse
url = 'http://ufcstats.com/event-details/509697e08673d2e5'
# get soup
soup = LIB.get_soup(url)

# parse fight links
fight_details_df = LIB.parse_fight_details(soup)

# show fight links
print(fight_details_df.head())