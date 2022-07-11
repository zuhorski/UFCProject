from similarity import df_by_totals
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == "__main__":
    totalDF = (df_by_totals())
    df = pd.read_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\CleanData.csv", index_col=0)

    # Finding the percent of total strikes landed that are from Standing Position
    # Finding the average percent of total strikes landed that are from the Standing Position
    stnd_str_land_percent = totalDF["STD_STR_LAND"] / totalDF["TOTAL_STR_LAND"]
    average_stnd_str_land_percent = (np.mean(stnd_str_land_percent)).round(3)
    print("Average Stand Strike Land %:", average_stnd_str_land_percent)

    # Finding the percent of total strikes attempted that are from Standing Position
    # Finding the average percent of total strikes attempted that are from the Standing Position
    stnd_str_att_percent = totalDF["STD_STR_ATT"] / totalDF["TOTAL_STR_ATT"]
    average_stnd_str_att_percent = np.mean(stnd_str_att_percent).round(3)
    print("Average Stand Strike Attempt %:", average_stnd_str_att_percent)

    # Finding the percent of total strikes landed that are from Clinch Position
    # Finding the average percent of total strikes landed that are from the Clinch Position
    clinch_str_land_percent = totalDF["CLINCH_STR_LAND"] / totalDF["TOTAL_STR_LAND"]
    average_clinch_str_land_percent = np.mean(clinch_str_land_percent).round(3)
    print("Average Clinch Strike Land %:", average_clinch_str_land_percent)

    # Finding the percent of total strikes attempted that are from Clinch Position
    # Finding the average percent of total strikes attempted that are from the Clinch Position
    clinch_str_att_percent = totalDF["CLINCH_STR_ATT"] / totalDF["TOTAL_STR_ATT"]
    average_clinch_str_att_percent = np.mean(clinch_str_att_percent).round(3)
    print("Average Clinch Strike Attempt %:", average_clinch_str_att_percent)

    # Finding the percent of total strikes landed that are from Ground Position
    # Finding the average percent of total strikes landed that are from the Ground Position
    ground_str_land_percent = totalDF["GRD_STR_LAND"] / totalDF["TOTAL_STR_LAND"]
    average_ground_str_land_percent = np.mean(ground_str_land_percent).round(3)
    print("Average Ground Strike Land %:", average_ground_str_land_percent)

    # Finding the percent of total strikes attempted that are from Ground Position
    # Finding the average percent of total strikes attempted that are from the Ground Position
    ground_str_att_percent = totalDF["GRD_STR_ATT"] / totalDF["TOTAL_STR_ATT"]
    average_ground_str_att_percent = np.mean(ground_str_att_percent).round(3)
    print("Average Ground Strike Attempt %:", average_ground_str_att_percent)

    # Finding the percent of the fight duration that is spent in a fighters control
    # Finding the average percent of the fight duration spent in a fighters control
    ctrl_time_percent = totalDF["CTRL_TIME(sec)"] / totalDF["FIGHT_TIME"]
    average_ctrl_time_percent = np.mean(ctrl_time_percent).round(3)
    print("Average Control Time %", average_ctrl_time_percent)


    ndf = df[["EVENT", "BOUT"]]
    ndf.insert(2, "STD_STR_LAND_PERCENT", stnd_str_land_percent)
    ndf.insert(3, "STD_STR_ATT_PERCENT", stnd_str_att_percent)
    ndf.insert(4, "CLINCH_STR_LAND_PERCENT", clinch_str_land_percent)
    ndf.insert(5, "CLINCH_STR_ATT_PERCENT", clinch_str_att_percent)
    ndf.insert(6, "GRND_STR_LAND_PERCENT", ground_str_land_percent)
    ndf.insert(7, "GRND_STR_ATT_PERCENT", ground_str_att_percent)
    ndf.insert(8, "CTRL_TIME_PERCENT", ctrl_time_percent)




    # Not the same count in every column
    # print(ndf.info())
    # The rows in these are all the same. Need to investigate this
    # print(ndf[ndf["STD_STR_LAND_PERCENT"].isnull() == True])
    # print(ndf[ndf["CLINCH_STR_LAND_PERCENT"].isnull() == True])
    # print(ndf[ndf["GRND_STR_LAND_PERCENT"].isnull() == True])