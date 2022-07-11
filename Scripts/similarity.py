import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
from sklearn import preprocessing
from collections import defaultdict

def similarFights(fight_num, includeWinner=False, byTotals=False):
    df = pd.read_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\CleanData.csv", index_col=0)
    if not byTotals:
        pure_data1 = df[['KD_RED', 'KD_BLUE', 'SIG_STR_ATT_RED', 'SIG_STR_LAND_BLUE', 'SIG_STR_ATT_BLUE',
                         'TOTAL_STR_LAND_RED', 'TOTAL_STR_ATT_RED', 'TOTAL_STR_LAND_BLUE', 'TOTAL_STR_ATT_BLUE',
                         'TD_RED', 'TD_ATT_RED', 'TD_BLUE', 'TD_ATT_BLUE', 'SUB_ATT_RED', 'SUB_ATT_BLUE',
                         'REV_RED', 'REV_BLUE', 'CTRL_TIME_RED(sec)', 'CTRL_TIME-BLUE(sec)',
                         'HEAD_LAND_RED', 'HEAD_ATT_RED', 'HEAD_LAND_BLUE', 'HEAD_ATT_BLUE', 'BODY_LAND_RED',
                         'BODY_ATT_RED', 'BODY_LAND_BLUE', 'BODY_ATT_BLUE', 'LEG_LAND_RED',
                         'LEG_ATT_RED', 'LEG_LAND_BLUE', 'LEG_ATT_BLUE', 'STD_STR_LAND_RED',
                         'STD_STR_ATT_RED', 'STD_STR_LAND_BLUE', 'STD_STR_ATT_BLUE',
                         'CLINCH_STR_LAND_RED', 'CLINCH_STR_ATT_RED', 'CLINCH_STR_LAND_BLUE',
                         'CLINCH_STR_ATT_BLUE', 'GRD_STR_LAND_RED', 'GRD_STR_ATT_RED',
                         'GRD_STR_LAND_BLUE', 'GRD_STR_ATT_BLUE', 'Fight_Time_(sec)', 'LAST_ROUND', 'FORMAT']]
    else:
        pure_data1 = df_by_totals()

    dataset1_standardized = preprocessing.scale(pure_data1)
    dataset1_standardized = pd.DataFrame(dataset1_standardized)

    sim = (1 - euclidean_distances(dataset1_standardized, dataset1_standardized.to_numpy()[fight_num, None]))
    simdf = (pd.DataFrame(sim).sort_values(by=0, ascending=False))

    if includeWinner:
        return df.iloc[simdf.index[1:11], [0, 1, -3]]
    else:
        return df.iloc[simdf.index[1:11], [0, 1]]


def df_by_totals():
    df = pd.read_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\CleanData.csv", index_col=0)
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


def similarityAnalysis(fightNumber):
        t = (similarFights(fightNumber, byTotals=True))
        nt = (similarFights(fightNumber))

        tindex = t.index
        ntindex = nt.index

        df = pd.read_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\CleanData.csv", index_col=0)
        fight = (df.iloc[fightNumber:fightNumber + 1, :])

        tdf = (df.iloc[tindex, :])
        ntdf = (df.iloc[ntindex, :])

        df2 = df_by_totals()
        df2.insert(0, "EVENT", df["EVENT"])
        df2.insert(1, "BOUT", df["BOUT"])
        df2.insert(24, "WIN_BY", df["WIN_BY"])
        df2.insert(28, "WINNER", df["WINNER"])
        df2.insert(29, "WeightClass", df["WeightClass"])
        df2.insert(30, "TitleFight", df["TitleFight"])

        df2fight = df2.iloc[fightNumber:fightNumber + 1, :]
        df2 = df2.iloc[tindex, :]


        with pd.ExcelWriter("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\SimilarityAnalysis.xlsx") as writer:
            t.to_excel(writer, sheet_name="Home")
            nt.to_excel(writer, sheet_name="Home", startcol=4)

            fight.to_excel(writer, sheet_name="ByTotal")
            fight.to_excel(writer, sheet_name="NotByTotal")

            tdf.to_excel(writer, sheet_name="ByTotal", startrow=3, header=False)
            ntdf.to_excel(writer, sheet_name="NotByTotal", startrow=3, header=False)

            df2fight.to_excel(writer, sheet_name="ByTotal", startrow=17)
            df2.to_excel(writer, sheet_name="ByTotal", startrow=20, header=False)
            df2.describe().to_excel(writer, sheet_name="ByTotal", startrow=32, startcol=2)


if __name__ == "__main__":
    print(similarFights(119, byTotals=True))
    print(similarFights(119))
    # similarityAnalysis(119)



