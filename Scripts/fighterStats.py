import pandas as pd
import plotly.express as px
import numpy as np


def fighterStats(fighter, title=False):
    df = pd.read_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\CleanData.csv", index_col=0)
    df = df[df["BOUT"].str.contains(fighter)]
    if title and ('Yes' in list(df["TitleFight"])) | ('Interim' in list(df["TitleFight"])):
        df = df[(df['TitleFight'] == 'Yes') | (df['TitleFight'] == 'Interim')]
    redDF = df.filter(regex='RED$', axis=1)
    redDF["Fight_Time_(Min)"] = (df["Fight_Time_(sec)"] / 60).__round__(2)
    blueDF = df.filter(regex='BLUE$', axis=1)
    blueDF["Fight_Time_(Min)"] = (df["Fight_Time_(sec)"] / 60).__round__(2)

    redDF.columns = redDF.columns.str.replace('_RED', '')
    blueDF.columns = blueDF.columns.str.replace('_BLUE', '')

    redDF = (redDF[redDF["FIGHTER"] == fighter])
    blueDF = (blueDF[blueDF["FIGHTER"] == fighter])

    return pd.concat([redDF, blueDF]).sort_index()


def opponentStats(fighter, title=False):
    df = pd.read_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\CleanData.csv", index_col=0)
    df = df[df["BOUT"].str.contains(fighter)]
    if title and ('Yes' in list(df["TitleFight"])) | ('Interim' in list(df["TitleFight"])):
        df = df[(df['TitleFight'] == 'Yes') | (df['TitleFight'] == 'Interim')]

    redDF = df.filter(regex='RED$', axis=1)
    redDF["Fight_Time_(Min)"] = (df["Fight_Time_(sec)"] / 60).__round__(2)
    blueDF = df.filter(regex='BLUE$', axis=1)
    blueDF["Fight_Time_(Min)"] = (df["Fight_Time_(sec)"] / 60).__round__(2)

    redDF.columns = redDF.columns.str.replace('_RED', '')
    redDF = redDF[redDF["FIGHTER"] != fighter]
    blueDF.columns = blueDF.columns.str.replace('_BLUE', '')
    blueDF = blueDF[blueDF["FIGHTER"] != fighter]

    return pd.concat([redDF, blueDF]).sort_index()


def sideBySideStats(fighter, metric, title=False):
    if metric == "sum":
        f = pd.DataFrame(fighterStats(fighter, title).iloc[:, 1:].sum())
        o = pd.DataFrame(opponentStats(fighter, title).iloc[:, 1:].sum())
    else:
        f = pd.DataFrame(fighterStats(fighter, title).iloc[:, 1:].mean().round(2))
        o = pd.DataFrame(opponentStats(fighter, title).iloc[:, 1:].mean().round(2))
    combo = pd.merge(f, o, on=f.index)
    combo.rename(columns={'key_0': 'Fighter', '0_x': f'{fighter}', '0_y': 'Opponents'}, inplace=True)
    combo.set_index("Fighter", inplace=True)
    combo = combo.transpose()
    return combo


def individualFightStats(df):
    redDF = df.filter(regex='RED$', axis=1)
    redDF.insert(22, "CONTROL_TIME", df['CTRL_TIME_RED(sec)'])
    redDF["CONTROL_TIME"] = (df['CTRL_TIME_RED(sec)']).__round__(2)
    redDF["Fight_Time_(Min)"] = (df["Fight_Time_(sec)"] / 60).__round__(2)
    redDF["WeightClass"] = df["WeightClass"]
    blueDF = df.filter(regex='BLUE$', axis=1)
    blueDF.insert(22, "CONTROL_TIME", df['CTRL_TIME-BLUE(sec)'])
    blueDF["CONTROL_TIME"] = (df['CTRL_TIME-BLUE(sec)']).__round__(2)
    blueDF["Fight_Time_(Min)"] = (df["Fight_Time_(sec)"] / 60).__round__(2)
    blueDF["WeightClass"] = df["WeightClass"]
    redDF.columns = redDF.columns.str.replace('_RED', '')
    blueDF.columns = blueDF.columns.str.replace('_BLUE', '')
    ufc = pd.concat([redDF, blueDF]).sort_index()
    return ufc


if __name__ == "__main__":

    df = pd.read_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\CleanData.csv",
                     index_col=0)

    # ufc = individualFightStats(df)
    #
    # fightCount = ufc["WeightClass"].value_counts()
    # ufcSumStatsGrouped = (ufc.groupby("WeightClass").mean())
    # for i in ufcSumStatsGrouped.columns[:-1]:
    #     ufcSumStatsGrouped[i] = ((ufcSumStatsGrouped[i] / ufcSumStatsGrouped["Fight_Time_(Min)"])).__round__(2)
    #
    # attributes = "CONTROL_TIME"
    #
    # attDict = {"Total Strikes": ["TOTAL_STR_ATT", "TOTAL_STR_LAND"], "Head Strikes": ["HEAD_ATT", "HEAD_LAND"],
    #            "Body Strikes": ["BODY_ATT", "BODY_LAND"], "Leg Strikes": ["LEG_ATT", "LEG_LAND"],
    #            "Standing Strikes": ["STD_STR_ATT", "STD_STR_LAND"],
    #            "Clinch Strikes": ["CLINCH_STR_ATT", "CLINCH_STR_LAND"],
    #            "Ground Strikes": ['GRD_STR_ATT', 'GRD_STR_LAND'], "Takedowns": ["TD_ATT", "TD"]}
    #
    # attribute1 = attributes
    # ufcSumStatsGrouped = pd.DataFrame(ufcSumStatsGrouped)
    #
    # weightclass = ["Flyweight Bout", "Bantamweight Bout", "Featherweight Bout", "Lightweight Bout", "Welterweight Bout", "Middleweight Bout",
    #                             "Light Heavyweight Bout", "Heavyweight Bout", "Catch Weight Bout", "Women's Strawweight Bout", "Women's Flyweight Bout",
    #                             "Women's Bantamweight Bout", "Women's Featherweight Bout"]
    #
    #
    # ufcSumStatsGrouped.insert(0, "WeightClass", ufcSumStatsGrouped.index)
    # ufcSumStatsGrouped["WeightClass"] = pd.Categorical(ufcSumStatsGrouped['WeightClass'], weightclass)
    #
    # newind = list(range(len(ufcSumStatsGrouped)))
    # ufcSumStatsGrouped.insert(0, "index", newind)
    # ufcSumStatsGrouped.set_index('index', inplace=True)
    # ufcSumStatsGrouped.sort_values("WeightClass", inplace=True)
    # ufcSumStatsGrouped.reset_index(drop=True, inplace=True)
    # print(ufcSumStatsGrouped)
    # # ave1 = (np.mean(ufcSumStatsGrouped[attribute1]))
    # # ave2 = (np.mean(ufcSumStatsGrouped[attribute2]))
    #
    # fig = px.line(ufcSumStatsGrouped, "WeightClass", f"{attribute1}")
    # fig.show()


