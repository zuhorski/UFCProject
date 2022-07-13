import pandas as pd
import plotly.express as px


def fighterStats(fighter):
    df = pd.read_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\CleanData.csv", index_col=0)

    redDF = df.filter(regex='RED$', axis=1)
    redDF["Fight_Time_(Min)"] = df["Fight_Time_(sec)"] / 60
    blueDF = df.filter(regex='BLUE$', axis=1)
    blueDF["Fight_Time_(Min)"] = df["Fight_Time_(sec)"] / 60

    redDF.columns = redDF.columns.str.replace('_RED', '')
    blueDF.columns = blueDF.columns.str.replace('_BLUE', '')

    redDF = (redDF[redDF["FIGHTER"] == fighter])
    blueDF = (blueDF[blueDF["FIGHTER"] == fighter])

    return pd.concat([redDF, blueDF]).sort_index()

def opponentStats(fighter):
    df = pd.read_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\CleanData.csv", index_col=0)
    df = df[df["BOUT"].str.contains(fighter)]

    redDF = df.filter(regex='RED$', axis=1)
    redDF["Fight_Time_(Min)"] = df["Fight_Time_(sec)"] / 60
    blueDF = df.filter(regex='BLUE$', axis=1)
    blueDF["Fight_Time_(Min)"] = df["Fight_Time_(sec)"] / 60

    redDF.columns = redDF.columns.str.replace('_RED', '')
    redDF = redDF[redDF["FIGHTER"] != fighter]
    blueDF.columns = blueDF.columns.str.replace('_BLUE', '')
    blueDF = blueDF[blueDF["FIGHTER"] != fighter]

    return pd.concat([redDF, blueDF]).sort_index()

def sideBySideStats(fighter):
    f = pd.DataFrame(fighterStats(fighter).iloc[:, 1:].sum())
    o = pd.DataFrame(opponentStats(fighter).iloc[:, 1:].sum())
    combo = pd.merge(f, o, on=f.index)
    combo.rename(columns={'key_0': 'Fighter', '0_x': f'{fighter}', '0_y': 'Opponents'}, inplace=True)
    combo.set_index("Fighter", inplace=True)
    combo = combo.transpose()
    return combo

if __name__ == "__main__":
    # print(merged_df.iloc[:, 1:].sum())
    f = pd.DataFrame(fighterStats("Conor McGregor").iloc[:, 1:].sum())

    # print(merged_df.iloc[:, 1:].sum() / merged_df["Fight_Time_(Min)"].sum())
    o = pd.DataFrame(opponentStats("Conor McGregor").iloc[:, 1:].sum())

    combo = pd.merge(f, o, on=f.index)
    combo.rename(columns={'key_0': 'Fighter', '0_x': f'{"Conor McGregor"}', '0_y': 'Opponents'}, inplace=True)
    combo.set_index("Fighter", inplace=True)
    combo = combo.transpose()
    # print(combo)
    print(sideBySideStats('Conor McGregor'))
    # fig = px.bar(combo, combo.index, "KD")
    # fig.show()