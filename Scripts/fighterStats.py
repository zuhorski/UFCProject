import pandas as pd


df = pd.read_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\CleanData.csv", index_col=0)

redDF = df.filter(regex='RED$', axis=1)
blueDF = df.filter(regex='BLUE$', axis=1)


redDF.columns = redDF.columns.str.replace('_RED', '')
blueDF.columns = blueDF.columns.str.replace('_BLUE', '')

fighter = 'Conor McGregor'

redDF = (redDF[redDF["FIGHTER"] == fighter])
blueDF = (blueDF[blueDF["FIGHTER"] == fighter])

merged_df = pd.concat([redDF, blueDF]).sort_index()
print(merged_df.sum())