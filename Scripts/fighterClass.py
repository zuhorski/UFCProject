import pandas as pd
import numpy as np

class fighter:
    def __init__(self):
        self._data = pd.read_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\CleanData.csv", index_col=0)

    def fighterStats(self, fighter, title=False, metric=None):
        df = self._data
        df = df[df["BOUT"].str.contains(fighter)]
        if title and ('Yes' in list(df["TitleFight"])) | ('Interim' in list(df["TitleFight"])):
            df = df[(df['TitleFight'] == 'Yes') | (df['TitleFight'] == 'Interim')]
        redDF = df.filter(regex='RED$', axis=1)
        redDF["Fight_Time_(Min)"] = (df["Fight_Time_(sec)"] / 60).__round__(2)
        blueDF = df.filter(regex='BLUE$', axis=1)
        blueDF["Fight_Time_(Min)"] = (df["Fight_Time_(sec)"] / 60).__round__(2)

        redDF.insert(0, "EVENT", df["EVENT"])
        redDF.insert(1, "BOUT", df["BOUT"])
        redDF.insert(12, "Control_Time", df["CTRL_TIME_RED(sec)"])

        blueDF.insert(0, "EVENT", df["EVENT"])
        blueDF.insert(1, "BOUT", df["BOUT"])
        blueDF.insert(12, "Control_Time", df["CTRL_TIME-BLUE(sec)"])

        redDF.columns = redDF.columns.str.replace('_RED', '')
        blueDF.columns = blueDF.columns.str.replace('_BLUE', '')

        redDF = (redDF[redDF["FIGHTER"] == fighter])
        blueDF = (blueDF[blueDF["FIGHTER"] == fighter])

        stat = pd.concat([redDF, blueDF]).sort_index()
        if metric is None:
            return stat
        elif metric == "Totals":
            return stat.iloc[:, 3:].sum()
        elif metric == "Average":
            return stat.iloc[:, 3:].mean()
        else:
            stat = pd.DataFrame(stat.sum()).transpose()
            stat.iloc[:, 3:-1] = stat.iloc[:, 3:-1].applymap(lambda x: x / stat.iloc[0, -1])
            return stat.iloc[0, 3:]

    def opponentStats(self, fighter, title=False, metric=None):
        df = self._data
        df = df[df["BOUT"].str.contains(fighter)]
        if title and ('Yes' in list(df["TitleFight"])) | ('Interim' in list(df["TitleFight"])):
            df = df[(df['TitleFight'] == 'Yes') | (df['TitleFight'] == 'Interim')]

        redDF = df.filter(regex='RED$', axis=1)
        redDF["Fight_Time_(Min)"] = (df["Fight_Time_(sec)"] / 60).__round__(2)
        blueDF = df.filter(regex='BLUE$', axis=1)
        blueDF["Fight_Time_(Min)"] = (df["Fight_Time_(sec)"] / 60).__round__(2)

        redDF.insert(0, "EVENT", df["EVENT"])
        redDF.insert(1, "BOUT", df["BOUT"])
        redDF.insert(12, "Control_Time", df["CTRL_TIME_RED(sec)"])

        blueDF.insert(0, "EVENT", df["EVENT"])
        blueDF.insert(1, "BOUT", df["BOUT"])
        blueDF.insert(12, "Control_Time", df["CTRL_TIME-BLUE(sec)"])

        redDF.columns = redDF.columns.str.replace('_RED', '')
        redDF = redDF[redDF["FIGHTER"] != fighter]
        blueDF.columns = blueDF.columns.str.replace('_BLUE', '')
        blueDF = blueDF[blueDF["FIGHTER"] != fighter]

        stat = pd.concat([redDF, blueDF]).sort_index()
        if metric is None:
            return stat
        elif metric == "Totals":
            return stat.iloc[:, 3:].sum()
        elif metric == "Average":
            return stat.iloc[:, 3:].mean()
        else:
            stat = pd.DataFrame(stat.sum()).transpose()
            stat.iloc[:, 3:-1] = stat.iloc[:, 3:-1].applymap(lambda x: x / stat.iloc[0, -1])
            return stat.iloc[0, 3:]

    def individualFightStats(self, includeWinner=False):
        df = self._data
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
        if not includeWinner:
            return pd.concat([redDF, blueDF]).sort_index()
        stats = pd.concat([redDF, blueDF]).sort_index()
        stats.insert(26, "WINNER", df["WINNER"])
        return stats

    def sideBySideStats(self, fighter, metric, title=False, xNumFights=None, recentBeginning=None):
        if (metric == "sum") | (metric != 'mean'):
            if xNumFights is None:
                f = pd.DataFrame(self.fighterStats(fighter, title).iloc[:, 1:].sum())
                o = pd.DataFrame(self.opponentStats(fighter, title).iloc[:, 1:].sum())
            elif recentBeginning == "Recent":
                f = pd.DataFrame(self.fighterStats(fighter, title).reset_index(drop=True).iloc[:xNumFights, 1:].sum())
                o = pd.DataFrame(self.opponentStats(fighter, title).reset_index(drop=True).iloc[:xNumFights, 1:].sum())
            else:
                f = pd.DataFrame(self.fighterStats(fighter, title).reset_index(drop=True).iloc[:, 1:].tail(xNumFights).sum())
                o = pd.DataFrame(self.opponentStats(fighter, title).reset_index(drop=True).iloc[:, 1:].tail(xNumFights).sum())

        elif metric == "mean":
            if xNumFights is None:
                f = pd.DataFrame(self.fighterStats(fighter, title).iloc[:, 1:].mean().round(2))
                o = pd.DataFrame(self.opponentStats(fighter, title).iloc[:, 1:].mean().round(2))
            elif recentBeginning == "Recent":
                f = pd.DataFrame(self.fighterStats(fighter, title).reset_index(drop=True).iloc[:xNumFights, 1:].mean())
                o = pd.DataFrame(self.opponentStats(fighter, title).reset_index(drop=True).iloc[:xNumFights, 1:].mean())
            else:
                f = pd.DataFrame(self.fighterStats(fighter, title).reset_index(drop=True).iloc[:, 1:].tail(xNumFights).mean())
                o = pd.DataFrame(self.opponentStats(fighter, title).reset_index(drop=True).iloc[:, 1:].tail(xNumFights).mean())

        combo = pd.merge(f, o, on=f.index)
        combo.rename(columns={'key_0': 'Fighter', '0_x': f'{fighter}', '0_y': 'Opponents'}, inplace=True)
        combo.set_index("Fighter", inplace=True)
        combo = combo.transpose()
        if (metric != 'sum') & (metric != 'mean'):
            combo.iloc[:, 2:-1] = combo.iloc[:, 2:-1].applymap(lambda x: x / combo.iloc[0, -1])
            return combo.iloc[:, 2:].round(2)
        elif metric == 'mean':
            return combo.iloc[:, :]
        else:
            return combo.iloc[:, 2:]

    def fighterPercentage(self, fighter):
        x = self.fighterStats(fighter=fighter)

        sig_str_percent = x["SIG_STR_LAND"] / x["SIG_STR_ATT"]
        average_sig_str_percent = (np.mean(sig_str_percent)).round(3)
        total_str_percent = x["TOTAL_STR_LAND"] / x["TOTAL_STR_ATT"]
        average_total_str_percent = np.mean(total_str_percent).round(3)
        td_percent = x["TD"] / x["TD_ATT"]
        average_td_percent = np.mean(td_percent).round(3)
        head_str_percent = x["HEAD_LAND"] / x["HEAD_ATT"]
        average_head_str_percent = np.mean(head_str_percent).round(3)
        body_str_percent = x["BODY_LAND"] / x["BODY_ATT"]
        average_body_str_percent = np.mean(body_str_percent).round(3)
        leg_str_percent = x["LEG_LAND"] / x["LEG_ATT"]
        average_leg_str_percent = np.mean(leg_str_percent).round(3)
        stnd_str_percent = x["STD_STR_LAND"] / x["STD_STR_ATT"]
        average_stnd_str_land_percent = (np.mean(stnd_str_percent)).round(3)
        clinch_str_percent = x["CLINCH_STR_LAND"] / x["CLINCH_STR_ATT"]
        average_clinch_str_land_percent = np.mean(clinch_str_percent).round(3)
        ground_str_percent = x["GRD_STR_LAND"] / x["GRD_STR_ATT"]
        average_ground_str_land_percent = np.mean(ground_str_percent).round(3)

        fdf = x[["EVENT", "BOUT"]]
        fdf.insert(2, "SIG_STR_PERCENT", sig_str_percent)
        fdf.insert(3, "TOTAL_STR_PERCENT", total_str_percent)
        fdf.insert(4, "TD_PERCENT", td_percent)
        fdf.insert(5, "HEAD_STR_PERCENT", head_str_percent)
        fdf.insert(6, "BODY_STR_PERCENT", body_str_percent)
        fdf.insert(7, "LEG_STR_PERCENT", leg_str_percent)
        fdf.insert(8, "STD_STR_PERCENT", stnd_str_percent)
        fdf.insert(9, "CLINCH_STR_PERCENT", clinch_str_percent)
        fdf.insert(10, "GRND_STR_LAND_PERCENT", ground_str_percent)
        return fdf

    def opponentPercentage(self, fighter):
        x = self.opponentStats(fighter=fighter)

        sig_str_percent = x["SIG_STR_LAND"] / x["SIG_STR_ATT"]
        average_sig_str_percent = (np.mean(sig_str_percent)).round(3)
        total_str_percent = x["TOTAL_STR_LAND"] / x["TOTAL_STR_ATT"]
        average_total_str_percent = np.mean(total_str_percent).round(3)
        td_percent = x["TD"] / x["TD_ATT"]
        average_td_percent = np.mean(td_percent).round(3)
        head_str_percent = x["HEAD_LAND"] / x["HEAD_ATT"]
        average_head_str_percent = np.mean(head_str_percent).round(3)
        body_str_percent = x["BODY_LAND"] / x["BODY_ATT"]
        average_body_str_percent = np.mean(body_str_percent).round(3)
        leg_str_percent = x["LEG_LAND"] / x["LEG_ATT"]
        average_leg_str_percent = np.mean(leg_str_percent).round(3)
        stnd_str_percent = x["STD_STR_LAND"] / x["STD_STR_ATT"]
        average_stnd_str_land_percent = (np.mean(stnd_str_percent)).round(3)
        clinch_str_percent = x["CLINCH_STR_LAND"] / x["CLINCH_STR_ATT"]
        average_clinch_str_land_percent = np.mean(clinch_str_percent).round(3)
        ground_str_percent = x["GRD_STR_LAND"] / x["GRD_STR_ATT"]
        average_ground_str_land_percent = np.mean(ground_str_percent).round(3)

        fdf = x[["EVENT", "BOUT"]]
        fdf.insert(2, "SIG_STR_PERCENT", sig_str_percent)
        fdf.insert(3, "TOTAL_STR_PERCENT", total_str_percent)
        fdf.insert(4, "TD_PERCENT", td_percent)
        fdf.insert(5, "HEAD_STR_PERCENT", head_str_percent)
        fdf.insert(6, "BODY_STR_PERCENT", body_str_percent)
        fdf.insert(7, "LEG_STR_PERCENT", leg_str_percent)
        fdf.insert(8, "STD_STR_PERCENT", stnd_str_percent)
        fdf.insert(9, "CLINCH_STR_PERCENT", clinch_str_percent)
        fdf.insert(10, "GRND_STR_LAND_PERCENT", ground_str_percent)
        return fdf

    def ufcPercentage(self):
        x = self.individualFightStats()

        sig_str_percent = x["SIG_STR_LAND"] / x["SIG_STR_ATT"]
        average_sig_str_percent = (np.mean(sig_str_percent)).round(3)
        total_str_percent = x["TOTAL_STR_LAND"] / x["TOTAL_STR_ATT"]
        average_total_str_percent = np.mean(total_str_percent).round(3)
        td_percent = x["TD"] / x["TD_ATT"]
        average_td_percent = np.mean(td_percent).round(3)
        head_str_percent = x["HEAD_LAND"] / x["HEAD_ATT"]
        average_head_str_percent = np.mean(head_str_percent).round(3)
        body_str_percent = x["BODY_LAND"] / x["BODY_ATT"]
        average_body_str_percent = np.mean(body_str_percent).round(3)
        leg_str_percent = x["LEG_LAND"] / x["LEG_ATT"]
        average_leg_str_percent = np.mean(leg_str_percent).round(3)
        stnd_str_percent = x["STD_STR_LAND"] / x["STD_STR_ATT"]
        average_stnd_str_land_percent = (np.mean(stnd_str_percent)).round(3)
        clinch_str_percent = x["CLINCH_STR_LAND"] / x["CLINCH_STR_ATT"]
        average_clinch_str_land_percent = np.mean(clinch_str_percent).round(3)
        ground_str_percent = x["GRD_STR_LAND"] / x["GRD_STR_ATT"]
        average_ground_str_land_percent = np.mean(ground_str_percent).round(3)

        fdf = x[["EVENT", "BOUT"]]
        fdf.insert(2, "SIG_STR_PERCENT", sig_str_percent)
        fdf.insert(3, "TOTAL_STR_PERCENT", total_str_percent)
        fdf.insert(4, "TD_PERCENT", td_percent)
        fdf.insert(5, "HEAD_STR_PERCENT", head_str_percent)
        fdf.insert(6, "BODY_STR_PERCENT", body_str_percent)
        fdf.insert(7, "LEG_STR_PERCENT", leg_str_percent)
        fdf.insert(8, "STD_STR_PERCENT", stnd_str_percent)
        fdf.insert(9, "CLINCH_STR_PERCENT", clinch_str_percent)
        fdf.insert(10, "GRND_STR_LAND_PERCENT", ground_str_percent)
        return fdf


if __name__ == "__main__":
    f = fighter()
    # print(f.fighterStats("Conor McGregor", metric = 'Average'))
    # print(f.fighterStats("Conor McGregor", True))
    # print(f.opponentStats("Conor McGregor"))
    # print(f.opponentStats("Conor McGregor", True))
    # print(f.individualFightStats())
    # print(f.sideBySideStats("Conor McGregor", 'p'))
    # print(f.sideBySideStats("Conor McGregor", 'sum',  xNumFights=13))
    # print(f.fighterStats('Conor McGregor'))
    # print(f.fighterPercentage('Israel Adesanya'))
    # print(f.opponentPercentage('Israel Adesanya'))
    print(f.ufcPercentage().groupby(["EVENT","BOUT"]).mean().mean())