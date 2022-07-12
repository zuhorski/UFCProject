import pandas as pd
from collections import defaultdict


def ufcTitleDivisionSeperator(division):
    s = division.split()
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


def ufcINTERIMTitleDivisionSeperator(division):
    s = division.split()
    i = 0
    l = len(s) - 1
    while True:
        if s[i] != 'UFC' and s[i] != 'Title' and s[i] != 'Interim' and i == l:
            break
        elif s[i] not in ['UFC', 'Interim', 'Title']:
            i += 1
        else:
            s.pop(i)
            i = 0
            l -= 1
    return " ".join(s)


def ultimateFighterDivisionSeperator(division):
    s = division.split()
    if "Women's" in s:
        ind = s.index("Women's")
        w = s[ind:]
        if 'Tournament' in w:
            ind = w.index('Tournament')
            w.pop(ind)
        if 'Title' in w:
            ind = w.index("Title")
            w.pop(ind)
    elif s[-5] == "Light":
        w = (s[-5:])
        w.pop(2)
        w.pop(2)
    else:
        w = s[-4:]
        w.pop(1)
        w.pop(1)

    return " ".join(w)


def tufDivisionSeperator(division):
    s = division.split()
    if 'TUF' in s:
        w = s[-4:]
        w.pop(1)
        w.pop(1)
    return " ".join(w)


def allFighters(df):
    n1 = df["FIGHTER_RED"].unique()
    n2 = df["FIGHTER_BLUE"].unique()
    fighter = list(n1)
    for ff in n2:
        fighter.append(ff)
    fighter = set(fighter)
    pd.DataFrame(fighter, columns=["Name"]).sort_values(by="Name").reset_index(drop=True).to_csv(
        "C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\UFC_Fighters.csv", header=True)


def df_by_totals():
    # This function returns columns as totals of a specific stat.
    # Columns that arent included are event, bout, winby, winner, weightclass, and title
    df = pd.read_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\CleanData.csv",
                     index_col=0)
    totals_dict = defaultdict(list)

    for i in range(len(df)):
        totals_dict["KD"].append(df["KD_RED"][i] + df["KD_BLUE"][i])
        totals_dict["SIG_STR_LAND"].append(df["SIG_STR_LAND_RED"][i] + df["SIG_STR_LAND_BLUE"][i])
        totals_dict["SIG_STR_ATT"].append(df["SIG_STR_ATT_RED"][i] + df["SIG_STR_ATT_BLUE"][i])
        totals_dict["TOTAL_STR_LAND"].append(df["TOTAL_STR_LAND_RED"][i] + df["TOTAL_STR_LAND_BLUE"][i])
        totals_dict["TOTAL_STR_ATT"].append(df["TOTAL_STR_ATT_RED"][i] + df["TOTAL_STR_ATT_BLUE"][i])
        totals_dict["TD"].append(df["TD_RED"][i] + df["TD_BLUE"][i])
        totals_dict["TD_ATT"].append(df["TD_ATT_RED"][i] + df["TD_ATT_BLUE"][i])
        totals_dict["SUB_ATT"].append(df["SUB_ATT_RED"][i] + df["SUB_ATT_BLUE"][i])
        totals_dict["REV"].append(df["REV_RED"][i] + df["REV_BLUE"][i])
        totals_dict["CTRL_TIME(sec)"].append(df["CTRL_TIME_RED(sec)"][i] + df["CTRL_TIME-BLUE(sec)"][i])
        totals_dict["HEAD_LAND"].append(df["HEAD_LAND_RED"][i] + df["HEAD_LAND_BLUE"][i])
        totals_dict["HEAD_ATT"].append(df["HEAD_ATT_RED"][i] + df["HEAD_ATT_BLUE"][i])
        totals_dict["BODY_LAND"].append(df["BODY_LAND_RED"][i] + df["BODY_LAND_BLUE"][i])
        totals_dict["BODY_ATT"].append(df["BODY_ATT_RED"][i] + df["BODY_ATT_BLUE"][i])
        totals_dict["LEG_LAND"].append(df["LEG_LAND_RED"][i] + df["LEG_LAND_BLUE"][i])
        totals_dict["LEG_ATT"].append(df["LEG_ATT_RED"][i] + df["LEG_ATT_BLUE"][i])
        totals_dict["STD_STR_LAND"].append(df["STD_STR_LAND_RED"][i] + df["STD_STR_LAND_BLUE"][i])
        totals_dict["STD_STR_ATT"].append(df["STD_STR_ATT_RED"][i] + df["STD_STR_ATT_BLUE"][i])
        totals_dict["CLINCH_STR_LAND"].append(df["CLINCH_STR_LAND_RED"][i] + df["CLINCH_STR_LAND_BLUE"][i])
        totals_dict["CLINCH_STR_ATT"].append(df["CLINCH_STR_ATT_RED"][i] + df["CLINCH_STR_ATT_BLUE"][i])
        totals_dict["GRD_STR_LAND"].append(df["GRD_STR_LAND_RED"][i] + df["GRD_STR_LAND_BLUE"][i])
        totals_dict["GRD_STR_ATT"].append(df["GRD_STR_ATT_RED"][i] + df["GRD_STR_ATT_BLUE"][i])
        totals_dict["FIGHT_TIME"].append(df["Fight_Time_(sec)"][i])
        totals_dict["LAST_ROUND"].append(df["LAST_ROUND"][i])
        totals_dict["FORMAT"].append(df["FORMAT"][i])

    return pd.DataFrame.from_dict(totals_dict)


def cleanup():
    df = pd.read_csv(
        'C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\MasterFightList.csv',
        index_col=0)
    df["FIGHTER_RED"] = df["FIGHTER_RED"].apply(lambda x: x.replace("'", ""))
    df["FIGHTER_BLUE"] = df["FIGHTER_BLUE"].apply(lambda x: x.replace("'", ""))
    df["EVENT"] = df["EVENT"].apply(lambda x: x.replace("vs.", "vs"))
    df["BOUT"] = df["BOUT"].apply(lambda x: x.replace("'", ""))
    df["WINNER"] = df["WINNER"].apply(lambda x: x.replace("'", ""))

    title_Fight = []
    div = []
    for i in range(len(df)):
        wt = df["WeightClass"][i]
        titleFight = 'No'
        if ('UFC' in wt) and ('Interim' in wt) and ('Title' in wt):
            division = ufcINTERIMTitleDivisionSeperator(wt)
            titleFight = 'Interim'
            div.append(division)
        elif ('UFC' in wt) and ('Title' in wt):
            division = ufcTitleDivisionSeperator(wt)
            titleFight = 'Yes'
            div.append(division)
        elif ('Ultimate' in wt) and ('Fighter' in wt):
            division = ultimateFighterDivisionSeperator(wt)
            titleFight = 'Yes'
            div.append(division)
        elif 'Nations' in wt:
            division = tufDivisionSeperator(wt)
            titleFight = 'Yes'
            div.append(division)
        title_Fight.append(titleFight)
        if (titleFight =="No"):
            div.append(wt)

    df["WeightClass"] = div
    df["TitleFight"] = title_Fight
    df.to_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\CleanData.csv",
              header=True)
    return df


def fullyCompletedTotalsDataframe(df):
    totals_df = df_by_totals()
    totals_df.insert(0, "EVENT", df["EVENT"])
    totals_df.insert(1, "BOUT", df["BOUT"])
    totals_df.insert(24, "WIN_BY", df["WIN_BY"])
    totals_df.insert(28, "WINNER", df["WINNER"])
    totals_df.insert(29, "WeightClass", df["WeightClass"])
    totals_df.insert(30, "TitleFight", df["TitleFight"])
    return totals_df


if __name__ == "__main__":
    df = cleanup()

    allFighters(df)

    totals_df = fullyCompletedTotalsDataframe(df)
    totals_df.to_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\FightTotals.csv", header=True)
