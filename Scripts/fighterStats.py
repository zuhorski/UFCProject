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

    redDF.insert(0, "EVENT", df["EVENT"])
    redDF.insert(1, "BOUT", df["BOUT"])

    blueDF.insert(0, "EVENT", df["EVENT"])
    blueDF.insert(1, "BOUT", df["BOUT"])

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

    redDF.insert(0, "EVENT", df["EVENT"])
    redDF.insert(1, "BOUT", df["BOUT"])

    blueDF.insert(0, "EVENT", df["EVENT"])
    blueDF.insert(1, "BOUT", df["BOUT"])

    redDF.columns = redDF.columns.str.replace('_RED', '')
    redDF = redDF[redDF["FIGHTER"] != fighter]
    blueDF.columns = blueDF.columns.str.replace('_BLUE', '')
    blueDF = blueDF[blueDF["FIGHTER"] != fighter]

    return pd.concat([redDF, blueDF]).sort_index()


def sideBySideStats(fighter, metric, title=False):
    if (metric == "sum") | (metric != 'mean'):
        f = pd.DataFrame(fighterStats(fighter, title).iloc[:, 3:].sum())
        o = pd.DataFrame(opponentStats(fighter, title).iloc[:, 3:].sum())
    elif metric == "mean":
        f = pd.DataFrame(fighterStats(fighter, title).iloc[:, 3:].mean().round(2))
        o = pd.DataFrame(opponentStats(fighter, title).iloc[:, 3:].mean().round(2))

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
    redDF.insert(0, "EVENT", df["EVENT"])
    redDF.insert(1, "BOUT", df["BOUT"])
    blueDF = df.filter(regex='BLUE$', axis=1)
    blueDF.insert(22, "CONTROL_TIME", df['CTRL_TIME-BLUE(sec)'])
    blueDF["CONTROL_TIME"] = (df['CTRL_TIME-BLUE(sec)']).__round__(2)
    blueDF["Fight_Time_(Min)"] = (df["Fight_Time_(sec)"] / 60).__round__(2)
    blueDF["WeightClass"] = df["WeightClass"]
    blueDF.insert(0, "EVENT", df["EVENT"])
    blueDF.insert(1, "BOUT", df["BOUT"])
    redDF.columns = redDF.columns.str.replace('_RED', '')
    blueDF.columns = blueDF.columns.str.replace('_BLUE', '')
    return pd.concat([redDF, blueDF]).sort_index()


if __name__ == "__main__":

    df = pd.read_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\CleanData.csv",
                     index_col=0)

    # print(individualFightStats(df).columns)

    # print(sideBySideStats("Conor McGregor", 'sum'))
    # print(sideBySideStats("Conor McGregor", 'sum', title=True))
    # print(sideBySideStats("Conor McGregor", 'mean'))
    # print(sideBySideStats("Conor McGregor", 'mean', True))
    # print(sideBySideStats("Conor McGregor", 'Per Minute'))
    # print(sideBySideStats("Conor McGregor", 'Per Minute', True))

    # print(fighterStats("Conor McGregor"))
    print(fighterStats("Conor McGregor", True))


