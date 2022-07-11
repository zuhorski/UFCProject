import pandas as pd


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
        if s[i] != 'UFC' and s[i] != 'Title'  and s[i] != 'Interim' and i == l:
            break
        elif s[i] not in ['UFC', 'Interim', 'Title']:
            i+= 1
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


if __name__ == "__main__":

    df = pd.read_csv('C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\MasterFightList.csv', index_col=0)
    df["FIGHTER_RED"] = df["FIGHTER_RED"].apply(lambda x: x.replace("'", ""))
    df["FIGHTER_BLUE"] = df["FIGHTER_BLUE"].apply(lambda x: x.replace("'", ""))
    df["EVENT"] = df["EVENT"].apply(lambda x: x.replace("vs.", "vs"))
    df["BOUT"] = df["BOUT"].apply(lambda x: x.replace("'", ""))

    title_Fight = []
    div = []
    for i in range(len(df)):
        wt = df["WeightClass"][i]
        titleFight = 'No'
        if ('UFC' in wt) and ('Interim' in wt) and ('Title' in wt):
            division = ufcINTERIMTitleDivisionSeperator(wt)
            titleFight = 'Yes'
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
        if titleFight != 'Yes':
            div.append(wt)

    df["WeightClass"] = div
    df["TitleFight"] = title_Fight
    df.to_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\CleanData.csv", header=True)



    n1 = df["FIGHTER_RED"].unique()
    n2 = df["FIGHTER_BLUE"].unique()

    fighter = list(n1)
    for ff in n2:
        fighter.append(ff)

    fighter = set(fighter)
    pd.DataFrame(fighter, columns=["Name"]).sort_values(by="Name").reset_index(drop=True).to_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\UFC_Fighters.csv", header=True)

