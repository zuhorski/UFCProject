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

# define url to parse
# various types of fights
# url = 'http://ufcstats.com/fight-details/4b7ec02b39fc6f70' # one round finish
# url = 'http://ufcstats.com/fight-details/8b3b38167060b1d7' # three rounds decision
# url = 'http://ufcstats.com/fight-details/b22eab3aa1522f40' # three rounds finish
# url = 'http://ufcstats.com/fight-details/3109d1151f149aaf' # five rounds decision
# url = 'http://ufcstats.com/fight-details/d93c8c77e1091a16' # no stats
# url = 'http://ufcstats.com/fight-details/c63edd25d2201a46' # draw
url = 'http://ufcstats.com/fight-details/37cb7ce0f0b70640' # point deduction

# get soup
soup = LIB.get_soup(url)

# parse fight results from soup
fight_results = LIB.parse_fight_results(soup)
# append fight url
fight_results.append('URL:'+url)

# show fight results
print(fight_results)


# organise fight results
fight_results_df = LIB.organise_fight_results(fight_results, config['fight_results_column_names'])

# show fight results
# print(fight_results_df.head())
# print(fight_results_df.columns)

# PARSE FIGHT STATS

# parse full fight stats for both fighters
fighter_a_stats, fighter_b_stats = LIB.parse_fight_stats(soup)

# show fighter stats
print(fighter_a_stats[:20])
print(fighter_b_stats[:20])

# organise stats extracted from soup
fighter_a_stats_clean = LIB.organise_fight_stats(fighter_a_stats)
fighter_b_stats_clean = LIB.organise_fight_stats(fighter_b_stats)

# show organised stats
print(fighter_a_stats_clean[:2])
print(fighter_b_stats_clean[:2])

# convert list of fighter stats into a structured dataframe
fighter_a_stats_df = LIB.convert_fight_stats_to_df(fighter_a_stats_clean, config['totals_column_names'], config['significant_strikes_column_names'])
fighter_b_stats_df = LIB.convert_fight_stats_to_df(fighter_b_stats_clean, config['totals_column_names'], config['significant_strikes_column_names'])

# show stats df
print(fighter_a_stats_df)
print(fighter_b_stats_df)

# combine fighter stats into one
fight_stats = LIB.combine_fighter_stats_dfs(fighter_a_stats_df, fighter_b_stats_df, soup)

# show fight stats
print(fight_stats)