import pandas as pd
import numpy as np
import streamlit as st
from similarity import similarFights
from fighterStats import sideBySideStats, individualFightStats
import plotly.express as px


def noStreamlitIndex():
    # No index shown in streamlit dataframes or tables
    hide_table_row_index = """
                        <style>
                        tbody th {display:none}
                        .blank {display:none}
                        </style>
                        """
    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)


def record(win, loss, draw, nc, text):
    # Used to display the record of a fighter in streamlit
    if (draw == 0) & (nc == 0):
        st.write(f"{text}: {win}-{loss}")
    elif (draw != 0) & (nc == 0):
        st.write(f"{text}: {win}-{loss}-{draw}")
    elif (draw != 0) & (nc != 0):
        st.write(f"{text}: {win}-{loss}-{draw} ({nc} NC)")
    elif (draw == 0) & (nc != 0):
        st.write(f"{text}: {win}-{loss} ({nc} NC)")


cleanDataDF = pd.read_csv(
    "C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\CleanData.csv", index_col=0)

st.set_page_config(layout="wide")
with st.sidebar:
    rad = st.radio("Selection", ("Home", "Fighter", "Similar Fights", "UFC"))

if rad == "Home":
    # Shows the fights on the most recent event
    st.title("Most Recent UFC Event", anchor="Home_Page")
    spoiler1 = st.radio("Show the Winner?", options=["No", "Yes"])  # An option to see the winner or not
    if spoiler1 == "No":
        noWinner = cleanDataDF[cleanDataDF["EVENT"] == cleanDataDF.iloc[0, 0]].iloc[:, [0, 1, -2, ]]
        noStreamlitIndex()
        st.table(noWinner)
    else:
        winner = cleanDataDF[cleanDataDF["EVENT"] == cleanDataDF.iloc[0, 0]].iloc[:, [0, 1, -2, -3, -7]]
        noStreamlitIndex()
        st.table(winner)

if rad == "Similar Fights":
    searchBy = st.selectbox("Search By Fighter or Event", ["Fighter", "Event"])
    if searchBy == "Event":
        events = cleanDataDF["EVENT"].unique()
        eventSelection = st.selectbox("Choose the Event", events)
        with st.form("MyForm"):
            bouts = cleanDataDF[cleanDataDF["EVENT"] == eventSelection]
            boutSelection = st.selectbox("Choose the fight", bouts["BOUT"].unique())
            spoiler2 = st.checkbox("Display Winner")
            submit_button = st.form_submit_button(label='Submit')

            if submit_button:
                st.subheader("10 Most Similar Fights")
                index_id = \
                cleanDataDF[(cleanDataDF["EVENT"] == eventSelection) & (cleanDataDF["BOUT"] == boutSelection)].index[0]
                if spoiler2:
                    st.table(similarFights(index_id, byTotals=True, includeWinner=True))
                else:
                    st.table(similarFights(index_id, byTotals=True))

    else:
        fighters = pd.read_csv(
            "C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\UFC_Fighters.csv",
            index_col=0)
        fighterSelection = st.selectbox("Choose the Fighter", fighters)
        with st.form("MyForm"):
            bouts = cleanDataDF[cleanDataDF["BOUT"].str.contains(fighterSelection)]
            event_bout = bouts["BOUT"] + " --- " + bouts["EVENT"]
            fightSelection = st.selectbox("Choose the Fight", event_bout)
            fightSelection = fightSelection.split(" --- ")

            spoiler3 = st.checkbox("Display Winner")
            submit_button = st.form_submit_button(label='Submit')

            if submit_button:
                st.subheader("10 Most Similar Fights")
                index_id = cleanDataDF[
                    (cleanDataDF["EVENT"] == fightSelection[1]) & (cleanDataDF["BOUT"] == fightSelection[0])].index[0]
                noStreamlitIndex()
                if spoiler3:
                    st.table(similarFights(index_id, byTotals=True, includeWinner=True))
                else:
                    st.table(similarFights(index_id, byTotals=True))

if rad == "Fighter":
    fighters = pd.read_csv(
        "C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\UFC_Fighters.csv", index_col=0)
    with st.form("MyForm"):
        fighterSelection = st.selectbox("Choose a Fighter", fighters)
        interest = st.selectbox("Choose what to look at", ["Fight History", "Fighter Totals"])
        st.form_submit_button("Submit")
    noStreamlitIndex()
    opponents = cleanDataDF[cleanDataDF["BOUT"].str.contains(fighterSelection)]

    if interest == "Fight History":
        spoiler4 = st.checkbox("Display Winner")
        if spoiler4:
            fights = opponents[["EVENT", "BOUT", "WeightClass", "WIN_BY", "WINNER", "TitleFight"]]
            win = fights[fights['WINNER'] == fighterSelection]['WINNER'].count()
            draw = fights[fights['WINNER'] == "D"]['WINNER'].count()
            nc = fights[fights['WINNER'] == "NC"]['WINNER'].count()
            loss = len(fights) - win - draw - nc

            record(win, loss, draw, nc, "UFC Record")

            if ('Interim' in list(fights["TitleFight"])) or ('Yes' in list(fights["TitleFight"])):
                beltFight = fights[(fights["TitleFight"] == "Yes") | (fights["TitleFight"] == "Interim")]
                w = beltFight[beltFight['WINNER'] == fighterSelection]['WINNER'].count()
                d = beltFight[beltFight['WINNER'] == "D"]['WINNER'].count()
                noContest = beltFight[beltFight['WINNER'] == "NC"]['WINNER'].count()
                l = len(beltFight) - w - d - noContest

                record(w, l, d, noContest, "UFC Record in Championship Fights")

            st.table(fights)
        else:
            fights = opponents[["EVENT", "BOUT", "WeightClass", "WIN_BY", "WINNER", "TitleFight"]]
            win = fights[fights['WINNER'] == fighterSelection]['WINNER'].count()
            draw = fights[fights['WINNER'] == "D"]['WINNER'].count()
            nc = fights[fights['WINNER'] == "NC"]['WINNER'].count()
            loss = len(fights) - win - draw - nc

            record(win, loss, draw, nc, "UFC Record")

            if ('Interim' in list(fights["TitleFight"])) or ('Yes' in list(fights["TitleFight"])):
                beltFight = fights[(fights["TitleFight"] == "Yes") | (fights["TitleFight"] == "Interim")]
                w = beltFight[beltFight['WINNER'] == fighterSelection]['WINNER'].count()
                d = beltFight[beltFight['WINNER'] == "D"]['WINNER'].count()
                noContest = beltFight[beltFight['WINNER'] == "NC"]['WINNER'].count()
                l = len(beltFight) - w - d - noContest

                record(w, l, d, noContest, "UFC Record in Championship Fights")

            st.table(fights[["EVENT", "BOUT", "WeightClass", "TitleFight"]])

    elif interest == "Fighter Totals":
        titleFightChecker = cleanDataDF[cleanDataDF["BOUT"].str.contains(fighterSelection)]
        if ('Yes' in list(titleFightChecker["TitleFight"])) | ('Interim' in list(titleFightChecker["TitleFight"])):
            titlefightstats = st.selectbox("Stats for Title Fights", ["No", "Yes"])
            if titlefightstats == 'Yes':
                stats = sideBySideStats(fighterSelection, True)
            else:
                stats = sideBySideStats(fighterSelection)
        else:
            stats = sideBySideStats(fighterSelection)
        st.dataframe(stats.style.format("{:2}"))
        statSelection = st.selectbox("Select a Stat", stats.columns.drop("Fight_Time_(Min)"))
        fig = px.bar(stats, stats.index, statSelection)
        st.plotly_chart(fig, use_container_width=True)

if rad == "UFC":

    opt = st.selectbox("Choose", options=["FIGHTER", "WeightClass"])
    if opt == "FIGHTER":

        # with st.form("MyForm"):
        min_fights = st.number_input("Choose the Minimum Amount of Fights (Average is 7)", min_value=1,
            max_value=41, step=1)

        # opt = st.selectbox("Choose", options=["FIGHTER", "WeightClass"])
        ufc = individualFightStats(cleanDataDF)

        fightCount = ufc[opt].value_counts()
        ufcSumStatsGrouped = (ufc.groupby(opt).sum())
        for i in ufcSumStatsGrouped.columns[:-1]:
            ufcSumStatsGrouped[i] = ((ufcSumStatsGrouped[i] / ufcSumStatsGrouped["Fight_Time_(Min)"])).__round__(2)

        attributes = st.selectbox('Stat Selection',
                                    options=["Total Strikes", "Head Strikes", "Body Strikes", "Leg Strikes",
                                             "Standing Strikes", "Clinch Strikes", "Ground Strikes", "Takedowns"])


        attDict = {"Total Strikes": ["TOTAL_STR_ATT", "TOTAL_STR_LAND"], "Head Strikes": ["HEAD_ATT", "HEAD_LAND"],
                   "Body Strikes": ["BODY_ATT", "BODY_LAND"], "Leg Strikes": ["LEG_ATT", "LEG_LAND"],
                   "Standing Strikes": ["STD_STR_ATT", "STD_STR_LAND"], "Clinch Strikes": ["CLINCH_STR_ATT", "CLINCH_STR_LAND"],
                   "Ground Strikes": ['GRD_STR_ATT', 'GRD_STR_LAND'], "Takedowns": ["TD_ATT", "TD"]}
            # subButton = st.form_submit_button("Submit")

        # if subButton:
        attribute1, attribute2 = attDict[attributes]
        ufcSumStatsGrouped = (ufcSumStatsGrouped[fightCount >= min_fights])
        ufcSumStatsGrouped = pd.DataFrame(ufcSumStatsGrouped)
        ufcSumStatsGrouped.insert(0, "FIGHTER", ufcSumStatsGrouped.index)
        newind = [x for x in range(len(ufcSumStatsGrouped))]
        ufcSumStatsGrouped.insert(0, "index", newind)
        ufcSumStatsGrouped.set_index('index', inplace=True)
        ave1 = (np.mean(ufcSumStatsGrouped[attribute1]))
        ave2 = (np.mean(ufcSumStatsGrouped[attribute2]))


        fig = px.scatter(ufcSumStatsGrouped, f"{attribute1}", f"{attribute2}", hover_data=["FIGHTER"],
                         title=f'Ave {attribute1} vs Ave {attribute2} (Per Minute)',
                         labels={f"{attribute1}": f'Ave {attribute1} per Minute',
                                 f"{attribute2}": f'Ave {attribute2} per Minute'})
        fig.add_hline(ave1)
        fig.add_vline(ave2)

        st.plotly_chart(fig, use_container_width=True)

    if opt == "WeightClass":
        ufc = individualFightStats(cleanDataDF)
        fightCount = ufc["WeightClass"].value_counts()
        ufcSumStatsGrouped = (ufc.groupby("WeightClass").mean())
        for i in ufcSumStatsGrouped.columns[:-2]:
            ufcSumStatsGrouped[i] = ((ufcSumStatsGrouped[i] / ufcSumStatsGrouped["Fight_Time_(Min)"])).__round__(2)

        attributes = st.selectbox(label='Select Stat',options=ufcSumStatsGrouped.columns[:-1])

        ufcSumStatsGrouped = pd.DataFrame(ufcSumStatsGrouped)

        weightclass = ["Flyweight Bout", "Bantamweight Bout", "Featherweight Bout", "Lightweight Bout",
                       "Welterweight Bout", "Middleweight Bout",
                       "Light Heavyweight Bout", "Heavyweight Bout", "Catch Weight Bout", "Women's Strawweight Bout",
                       "Women's Flyweight Bout",
                       "Women's Bantamweight Bout", "Women's Featherweight Bout"]

        ufcSumStatsGrouped.insert(0, "WeightClass", ufcSumStatsGrouped.index)
        ufcSumStatsGrouped["WeightClass"] = pd.Categorical(ufcSumStatsGrouped['WeightClass'], weightclass)

        newind = list(range(len(ufcSumStatsGrouped)))
        ufcSumStatsGrouped.insert(0, "index", newind)
        ufcSumStatsGrouped.set_index('index', inplace=True)
        ufcSumStatsGrouped.sort_values("WeightClass", inplace=True)
        ufcSumStatsGrouped.reset_index(drop=True, inplace=True)
        ave1 = (np.mean(ufcSumStatsGrouped[attributes]))

        fig = px.bar(ufcSumStatsGrouped, "WeightClass", f"{attributes}", labels={f"{attributes}": f'Ave {attributes} per Minute'})
        fig.add_hline(y=ave1)
        st.plotly_chart(fig, use_container_width=True)
