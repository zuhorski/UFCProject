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
    if (metric == "sum") | (metric != 'mean'):
        f = pd.DataFrame(fighterStats(fighter, title).iloc[:, 1:].sum())
        o = pd.DataFrame(opponentStats(fighter, title).iloc[:, 1:].sum())
    elif metric == "mean":
        f = pd.DataFrame(fighterStats(fighter, title).iloc[:, 1:].mean().round(2))
        o = pd.DataFrame(opponentStats(fighter, title).iloc[:, 1:].mean().round(2))

    combo = pd.merge(f, o, on=f.index)
    combo.rename(columns={'key_0': 'Fighter', '0_x': f'{fighter}', '0_y': 'Opponents'}, inplace=True)
    combo.set_index("Fighter", inplace=True)
    combo = combo.transpose()
    if (metric != 'sum') & (metric != 'mean'):
        combo.iloc[:, :-1] = combo.iloc[:, :-1].applymap(lambda x: x / combo.iloc[0,-1])
    return combo.round(2)


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

    sideBySideStats("Conor McGregor", "noone")


