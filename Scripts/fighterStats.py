import pandas as pd
import plotly.express as px


def fighterStats(fighter, title=False):
    df = pd.read_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\CleanData.csv", index_col=0)
    df = df[df["BOUT"].str.contains(fighter)]
    if title and ('Yes' in list(df["TitleFight"])) | ('Interim' in list(df["TitleFight"])):
        df = df[(df['TitleFight'] == 'Yes') | (df['TitleFight'] == 'Interim')]
    redDF = df.filter(regex='RED$', axis=1)
    redDF["Fight_Time_(Min)"] = df["Fight_Time_(sec)"] / 60
    blueDF = df.filter(regex='BLUE$', axis=1)
    blueDF["Fight_Time_(Min)"] = df["Fight_Time_(sec)"] / 60

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
    redDF["Fight_Time_(Min)"] = df["Fight_Time_(sec)"] / 60
    blueDF = df.filter(regex='BLUE$', axis=1)
    blueDF["Fight_Time_(Min)"] = df["Fight_Time_(sec)"] / 60

    redDF.columns = redDF.columns.str.replace('_RED', '')
    redDF = redDF[redDF["FIGHTER"] != fighter]
    blueDF.columns = blueDF.columns.str.replace('_BLUE', '')
    blueDF = blueDF[blueDF["FIGHTER"] != fighter]

    return pd.concat([redDF, blueDF]).sort_index()


def sideBySideStats(fighter, title=False):
    f = pd.DataFrame(fighterStats(fighter, title).iloc[:, 1:].sum())
    o = pd.DataFrame(opponentStats(fighter, title).iloc[:, 1:].sum())
    combo = pd.merge(f, o, on=f.index)
    combo.rename(columns={'key_0': 'Fighter', '0_x': f'{fighter}', '0_y': 'Opponents'}, inplace=True)
    combo.set_index("Fighter", inplace=True)
    combo = combo.transpose()
    return combo


if __name__ == "__main__":
    # df = pd.read_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\CleanData.csv",
    #                  index_col=0)
    # title = False
    # df = df[df["BOUT"].str.contains('Conor McGregor')]
    # if title and ('Yes' in list(df["TitleFight"])) | ('Interim' in list(df["TitleFight"])):
    #     df = df[(df['TitleFight'] == 'Yes') | (df['TitleFight'] == 'Interim')]
    #
    # redDF = df.filter(regex='RED$', axis=1)
    # redDF["Fight_Time_(Min)"] = df["Fight_Time_(sec)"] / 60
    # blueDF = df.filter(regex='BLUE$', axis=1)
    # blueDF["Fight_Time_(Min)"] = df["Fight_Time_(sec)"] / 60
    #
    # redDF.columns = redDF.columns.str.replace('_RED', '')
    # blueDF.columns = blueDF.columns.str.replace('_BLUE', '')
    #
    # redDF = (redDF[redDF["FIGHTER"] == 'Conor McGregor'])
    # blueDF = (blueDF[blueDF["FIGHTER"] == 'Conor McGregor'])
    #
    # print(pd.concat([redDF, blueDF]).sort_index())
    print(sideBySideStats('Sean OMalley', True))