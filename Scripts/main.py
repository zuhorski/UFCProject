import pandas as pd
import os
from UFCProject.Scraping_Files import scrape_ufc_stats_library as LIB
import importlib
importlib.reload(LIB)
import yaml


def divisonSeperator(division):
    s = division[0].split()
    i = 0
    l = len(s) - 1
    while True:
        if s[i] != 'UFC' and s[i] != 'Title' and i == l:
            break
        elif s[i] not in ['UFC', 'Title']:
            i += 1
        else:
            s.pop(i)
            i = 0
            l -= 1
    return " ".join(s)


def timeconvert(t):  # sourcery skip: assign-if-exp
    if t[0] == "nan":
        return 0
    else:
        minimum = int(t[0][0])

    if int(t[1][0]) == 0:
        sec = int(t[1][1])
    else:
        sec = int(t[1])

    return (minimum * 60) + sec


def total_fight_time(df):
    if df["ROUND"][0] == '1':
        return timeconvert((df["TIME"][0]).split(":"))
    elif df["TIME"][0] == "5:00":
        return int(df["ROUND"][0]) * timeconvert((df["TIME"][0]).split(":"))
    else:
        return ((int(df["ROUND"][0]) - 1) * 300) + timeconvert((df["TIME"][0]).split(":"))


def monthConversion(date):
    Months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5,
              'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10,
              'November': 11, 'December': 12}

    dateSplit = date.split(" ")
    dateSplit[0] = Months[dateSplit[0]]
    dateSplit[1] = dateSplit[1].strip(",")

    return f"{str(dateSplit[0])}-{str(dateSplit[1])}-{str(dateSplit[2])}"


def splittingBySpace(x):
    return x.split(" ")


def splitAndAppendToList(df, column, listname1, listname2):
    df[column] = df[column].apply(lambda x: splittingBySpace(x))
    df[column].apply(lambda y: listname1.append(int(y[0])))
    cleanDF.append(listname1)
    df[column].apply(lambda y: listname2.append(int(y[2])))
    cleanDF.append(listname2)


# sourcery no-metrics
config = yaml.safe_load(open('../Scraping_Files/scrape_ufc_stats_config.yaml'))


url = 'http://ufcstats.com/statistics/events/completed'  # first page
# url = 'http://ufcstats.com/statistics/events/completed?page=all' # all pages


# GET ALL THE FIGHT EVENTS URLS
soup = LIB.get_soup(url)    # get soup
event_details_df = LIB.parse_event_details(soup)    # parse event details
allfightsDF = pd.read_csv("../DataFiles2/MasterFightList.csv", index_col=0)
# allfightsDF = pd.DataFrame()


event_dictionary = {} # This will make the event lookup happen in O(1) rather than O(N) in a loop
with open("../Events2/event names.txt") as file:
    for line in file:
        event_dictionary[line] = []


# FROM EVENT URL GET THE INDIVIDUAL FIGHTS URLS
for id in range(5, -1, -1): # 575 len(event_details_df.iloc[:576, :2])
    event_url = event_details_df.iloc[:, :2]
    event_url = event_url["URL"][id]
    soup = LIB.get_soup(event_url)  # get soup
    fight_details_df = LIB.parse_fight_details(soup)    # parse fight links
    fight_details_df["BOUT"] = fight_details_df["BOUT"].apply(lambda x: x.replace(".", ""))
    fight_details_df["EVENT"] = fight_details_df["EVENT"].apply(lambda x: x.replace("vs.", "vs"))

    with open("../Events2/event names.txt", "r+") as en:
        event = en.readlines()
        infile = False
        # for e in event:
        if f"{fight_details_df['EVENT'][0]}\n" in event_dictionary:
            infile = True
            continue
        if not infile:
            event.insert(0, f"{fight_details_df['EVENT'][0]}\n")
            en.seek(0)
            en.writelines(event)
    if infile:
        continue

    # GET INDIVIDUAL FIGHT DETAILS
    for f in range(len(fight_details_df)):

        event_fight_url = fight_details_df.loc[f, "URL"]
        soup = LIB.get_soup(event_fight_url)    # get soup
        fight_results = LIB.parse_fight_results(soup)   # parse fight results from soup
        fight_results.append('URL:' + event_fight_url)  # append fight url

        # ORGANIZE FIGHT RESULTS
        fight_results_df = LIB.organise_fight_results(fight_results, config['fight_results_column_names'])
        eventName = fight_details_df["EVENT"]
        bout = fight_details_df["BOUT"][f]
        win_by = fight_results_df["METHOD"]
        last_round = fight_results_df["ROUND"]
        rounds = fight_results_df['TIME FORMAT'][0][0]
        division = list(fight_results_df['WEIGHTCLASS'])
        fight_time = total_fight_time(fight_results_df)

        # show fight results
        results = (fight_results_df.iloc[0, 2].split("/"))
        red_result = results[0]
        blue_results = results[1]

        # GET STATS FOR THE FIGHTERS
        fighter_a_stats, fighter_b_stats = LIB.parse_fight_stats(soup)  # parse full fight stats for both fighters

        fighter_a_stats_clean = LIB.organise_fight_stats(fighter_a_stats)   # organise stats extracted from soup
        fighter_b_stats_clean = LIB.organise_fight_stats(fighter_b_stats)   # organise stats extracted from soup

        # convert list of fighter stats into a structured dataframe
        fighter_a_stats_df = LIB.convert_fight_stats_to_df(fighter_a_stats_clean, config['totals_column_names'],
                                                           config['significant_strikes_column_names'])
        fighter_b_stats_df = LIB.convert_fight_stats_to_df(fighter_b_stats_clean, config['totals_column_names'],
                                                           config['significant_strikes_column_names'])

        combined_fighter_df = pd.merge(fighter_a_stats_df, fighter_b_stats_df, how="outer", on="ROUND",
                                       suffixes=("_RED", "_BLUE"))

        cleanDF = pd.DataFrame()
        cleanDF[combined_fighter_df.columns[0]] = combined_fighter_df[combined_fighter_df.columns[0]]   # Round
        cleanDF[combined_fighter_df.columns[1]] = combined_fighter_df[combined_fighter_df.columns[1]]   # Fighter_Red
        cleanDF[combined_fighter_df.columns[17]] = combined_fighter_df[combined_fighter_df.columns[17]] # Fighter_Blue
        cleanDF[combined_fighter_df.columns[2]] = combined_fighter_df[combined_fighter_df.columns[2]]   # KD_Red
        cleanDF[combined_fighter_df.columns[18]] = combined_fighter_df[combined_fighter_df.columns[18]] #   KD_Blue


        SIG_STR_LAND_RED = []
        SIG_STR_ATT_RED = []
        SIG_STR_LAND_BLUE = []
        SIG_STR_ATT_BLUE = []
        splitAndAppendToList(combined_fighter_df, "SIG.STR._RED", SIG_STR_LAND_RED, SIG_STR_ATT_RED)
        splitAndAppendToList(combined_fighter_df, "SIG.STR._BLUE", SIG_STR_LAND_BLUE, SIG_STR_ATT_BLUE)
        cleanDF["SIG_STR_LAND_RED"] = SIG_STR_LAND_RED
        cleanDF["SIG_STR_ATT_RED"] = SIG_STR_ATT_RED
        cleanDF["SIG_STR_LAND_BLUE"] = SIG_STR_LAND_BLUE
        cleanDF["SIG_STR_ATT_BLUE"] = SIG_STR_ATT_BLUE

        TOTAL_STR_LAND_RED = []
        TOTAL_STR_ATT_RED = []
        TOTAL_STR_LAND_BLUE = []
        TOTAL_STR_ATT_BLUE = []
        splitAndAppendToList(combined_fighter_df, "TOTAL STR._RED", TOTAL_STR_LAND_RED, TOTAL_STR_ATT_RED)
        splitAndAppendToList(combined_fighter_df, "TOTAL STR._BLUE", TOTAL_STR_LAND_BLUE, TOTAL_STR_ATT_BLUE)
        cleanDF["TOTAL_STR_LAND_RED"] = TOTAL_STR_LAND_RED
        cleanDF["TOTAL_STR_ATT_RED"] = TOTAL_STR_ATT_RED
        cleanDF["TOTAL_STR_LAND_BLUE"] = TOTAL_STR_LAND_BLUE
        cleanDF["TOTAL_STR_ATT_BLUE"] = TOTAL_STR_ATT_BLUE

        TD_RED = []
        TD_ATT_RED = []
        TD_BLUE = []
        TD_ATT_BLUE = []
        splitAndAppendToList(combined_fighter_df, "TD_RED", TD_RED, TD_ATT_RED)
        splitAndAppendToList(combined_fighter_df, "TD_BLUE", TD_BLUE, TD_ATT_BLUE)
        cleanDF["TD_RED"] = TD_RED
        cleanDF["TD_ATT_RED"] = TD_ATT_RED
        cleanDF["TD_BLUE"] = TD_BLUE
        cleanDF["TD_ATT_BLUE"] = TD_ATT_BLUE

        cleanDF["SUB_ATT_RED"] = combined_fighter_df[combined_fighter_df.columns[8]]   # SubAtt_Red
        cleanDF["SUB_ATT_BLUE"] = combined_fighter_df[combined_fighter_df.columns[24]] # SubAtt_Blue
        cleanDF["REV_RED"] = combined_fighter_df[combined_fighter_df.columns[9]]   # Rev_Red
        cleanDF["REV_BLUE"] = combined_fighter_df[combined_fighter_df.columns[25]] # Rev_Blue

        R_CTRL_TIME = []
        combined_fighter_df["CTRL_RED"] = combined_fighter_df["CTRL_RED"].apply(lambda x: str(x).split(":"))
        combined_fighter_df["CTRL_RED"].apply(lambda t: R_CTRL_TIME.append(timeconvert(t)))
        B_CTRL_TIME = []
        combined_fighter_df["CTRL_BLUE"] = combined_fighter_df["CTRL_BLUE"].apply(lambda x: str(x).split(":"))
        combined_fighter_df["CTRL_BLUE"].apply(lambda t: B_CTRL_TIME.append(timeconvert(t)))
        cleanDF["CTRL_TIME_RED(sec)"] = R_CTRL_TIME
        cleanDF["CTRL_TIME-BLUE(sec)"] = B_CTRL_TIME

        HEAD_LAND_RED = []
        HEAD_ATT_RED = []
        HEAD_LAND_BLUE = []
        HEAD_ATT_BLUE = []
        splitAndAppendToList(combined_fighter_df, "HEAD_RED", HEAD_LAND_RED, HEAD_ATT_RED)
        splitAndAppendToList(combined_fighter_df, "HEAD_BLUE", HEAD_LAND_BLUE, HEAD_ATT_BLUE)
        cleanDF["HEAD_LAND_RED"] = HEAD_LAND_RED
        cleanDF["HEAD_ATT_RED"] = HEAD_ATT_RED
        cleanDF["HEAD_LAND_BLUE"] = HEAD_LAND_BLUE
        cleanDF["HEAD_ATT_BLUE"] = HEAD_ATT_BLUE

        BODY_LAND_RED = []
        BODY_ATT_RED = []
        BODY_LAND_BLUE = []
        BODY_ATT_BLUE = []
        splitAndAppendToList(combined_fighter_df, "BODY_RED", BODY_LAND_RED, BODY_ATT_RED)
        splitAndAppendToList(combined_fighter_df, "BODY_BLUE", BODY_LAND_BLUE, BODY_ATT_BLUE)
        cleanDF["BODY_LAND_RED"] = BODY_LAND_RED
        cleanDF["BODY_ATT_RED"] = BODY_ATT_RED
        cleanDF["BODY_LAND_BLUE"] = BODY_LAND_BLUE
        cleanDF["BODY_ATT_BLUE"] = BODY_ATT_BLUE

        LEG_LAND_RED = []
        LEG_ATT_RED = []
        LEG_LAND_BLUE = []
        LEG_ATT_BLUE = []
        splitAndAppendToList(combined_fighter_df, "LEG_RED", LEG_LAND_RED, LEG_ATT_RED)
        splitAndAppendToList(combined_fighter_df, "LEG_BLUE", LEG_LAND_BLUE, LEG_ATT_BLUE)
        cleanDF["LEG_LAND_RED"] = LEG_LAND_RED
        cleanDF["LEG_ATT_RED"] = LEG_ATT_RED
        cleanDF["LEG_LAND_BLUE"] = LEG_LAND_BLUE
        cleanDF["LEG_ATT_BLUE"] = LEG_ATT_BLUE

        STD_STR_LAND_RED = []
        STD_STR_ATT_RED = []
        STD_STR_LAND_BLUE = []
        STD_STR_ATT_BLUE = []
        splitAndAppendToList(combined_fighter_df, "DISTANCE_RED", STD_STR_LAND_RED, STD_STR_ATT_RED)
        splitAndAppendToList(combined_fighter_df, "DISTANCE_BLUE", STD_STR_LAND_BLUE, STD_STR_ATT_BLUE)
        cleanDF["STD_STR_LAND_RED"] = STD_STR_LAND_RED
        cleanDF["STD_STR_ATT_RED"] = STD_STR_ATT_RED
        cleanDF["STD_STR_LAND_BLUE"] = STD_STR_LAND_BLUE
        cleanDF["STD_STR_ATT_BLUE"] = STD_STR_ATT_BLUE

        CLINCH_STR_LAND_RED = []
        CLINCH_STR_ATT_RED = []
        CLINCH_STR_LAND_BLUE = []
        CLINCH_STR_ATT_BLUE = []
        splitAndAppendToList(combined_fighter_df, "CLINCH_RED", CLINCH_STR_LAND_RED, CLINCH_STR_ATT_RED)
        splitAndAppendToList(combined_fighter_df, "CLINCH_BLUE", CLINCH_STR_LAND_BLUE, CLINCH_STR_ATT_BLUE)
        cleanDF["CLINCH_STR_LAND_RED"] = CLINCH_STR_LAND_RED
        cleanDF["CLINCH_STR_ATT_RED"] = CLINCH_STR_ATT_RED
        cleanDF["CLINCH_STR_LAND_BLUE"] = CLINCH_STR_LAND_BLUE
        cleanDF["CLINCH_STR_ATT_BLUE"] = CLINCH_STR_ATT_BLUE

        GRD_STR_LAND_RED = []
        GRD_STR_ATT_RED = []
        GRD_STR_LAND_BLUE = []
        GRD_STR_ATT_BLUE = []
        splitAndAppendToList(combined_fighter_df, "GROUND_RED", GRD_STR_LAND_RED, GRD_STR_ATT_RED)
        splitAndAppendToList(combined_fighter_df, "GROUND_BLUE", GRD_STR_LAND_BLUE, GRD_STR_ATT_BLUE)
        cleanDF["GRD_STR_LAND_RED"] = GRD_STR_LAND_RED
        cleanDF["GRD_STR_ATT_RED"] = GRD_STR_ATT_RED
        cleanDF["GRD_STR_LAND_BLUE"] = GRD_STR_LAND_BLUE
        cleanDF["GRD_STR_ATT_BLUE"] = GRD_STR_ATT_BLUE

        cleanDF["KD_RED"] = cleanDF["KD_RED"].astype(int)
        cleanDF["KD_BLUE"] = cleanDF["KD_BLUE"].astype(int)
        cleanDF["SUB_ATT_RED"] = cleanDF["SUB_ATT_RED"].astype(int)
        cleanDF["SUB_ATT_BLUE"] = cleanDF["SUB_ATT_BLUE"].astype(int)
        cleanDF["REV_RED"] = cleanDF["REV_RED"].astype(int)
        cleanDF["REV_BLUE"] = cleanDF["REV_BLUE"].astype(int)

        singleRowCleanDF = pd.DataFrame(columns=cleanDF.iloc[:, 1:].columns)
        singleRowCleanDF["FIGHTER_RED"] = [cleanDF["FIGHTER_RED"][0]]
        singleRowCleanDF["FIGHTER_BLUE"] = [cleanDF["FIGHTER_BLUE"][0]]
        for c in cleanDF.iloc[:, 3:].columns:
            singleRowCleanDF[c] = [cleanDF[c].sum()]

        singleRowCleanDF["WIN_BY"] = win_by
        singleRowCleanDF["LAST_ROUND"] = last_round
        singleRowCleanDF["FORMAT"] = rounds
        if red_result == "W":
            singleRowCleanDF["WINNER"] = [singleRowCleanDF["FIGHTER_RED"][0]]
        elif blue_results == "W":
            singleRowCleanDF["WINNER"] = [singleRowCleanDF["FIGHTER_BLUE"][0]]
        elif (red_result == 'NC') & (blue_results == 'NC'):
            singleRowCleanDF['WINNER'] = 'NC'
        elif (red_result == 'D') & (blue_results == 'D'):
            singleRowCleanDF['WINNER'] = 'D'

        else:
            singleRowCleanDF["WINNER"] = "nan"

        singleRowCleanDF["WeightClass"] = division
        # singleRowCleanDF["Title_fight"] = titleFight
        singleRowCleanDF.insert(47, "Fight_Time_(sec)", fight_time)

        singleRowCleanDF.insert(0, "EVENT", eventName)
        singleRowCleanDF.insert(1, "BOUT", bout)

        if allfightsDF.empty:
            allfightsDF = singleRowCleanDF
        else:
            allfightsDF = pd.concat([singleRowCleanDF, allfightsDF]).reset_index(drop=True)

    filenum = len(os.listdir(fr"../Events2")) - 1
    allfightsDF.to_csv(fr"C:\Users\sabzu\Documents\UFCRecommendationProject\UFCProject\Events2\MasterFightList_{filenum}.csv", header=True)
    allfightsDF.to_csv(fr"C:\Users\sabzu\Documents\UFCRecommendationProject\UFCProject\DataFiles2\MasterFightList.csv", header=True)

