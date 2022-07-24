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


@st.cache
def mostRecentEventDataframe(showWinner=False):
    if showWinner:
        return cleanDataDF[cleanDataDF["EVENT"] == cleanDataDF.iloc[0, 0]].iloc[:, [0, 1, -2, -3, -7]]
    else:
        return cleanDataDF[cleanDataDF["EVENT"] == cleanDataDF.iloc[0, 0]].iloc[:, [0, 1, -2, ]]


# @st.cache(suppress_st_warning=True)
def record(win, loss, draw, nc, text):
    st.subheader(text)
    col_1, col_2, col_3, col_4 = st.columns(4)
    col_1.metric("Win", win)
    col_2.metric("Loss", loss)
    col_3.metric("Draw", draw)
    col_4.metric("No Contest", nc)


def fighterGraph(x, y, stat):
    fig = px.bar(x, y, stat)
    st.plotly_chart(fig, use_container_width=True)


# sourcery no-metrics
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
        noWinner = mostRecentEventDataframe()
        noStreamlitIndex()
        st.table(noWinner)
    else:
        winner = mostRecentEventDataframe(True)
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
                    cleanDataDF[
                        (cleanDataDF["EVENT"] == eventSelection) & (cleanDataDF["BOUT"] == boutSelection)].index[0]
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
    fighters = pd.read_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\UFC_Fighters.csv", index_col=0)

    with st.form("MyForm"):
        # Choose a fighter
        fighterSelection = st.selectbox("Choose a Fighter", fighters)

        # Choose to look at fight history or fight totals
        interest = st.selectbox("Choose what to look at", ["Fight History", "Fighter Totals"])
        st.form_submit_button("Submit")
    noStreamlitIndex()

    # Get all the bouts that contain the selected fighter
    opponents = cleanDataDF[cleanDataDF["BOUT"].str.contains(fighterSelection)]

    if interest == "Fight History":
        # Spoiler prevention - check the box to see the winner
        spoiler4 = st.checkbox("Display Winner")

        fights = opponents[["EVENT", "BOUT", "WeightClass", "WIN_BY", "WINNER", "TitleFight"]]
        if spoiler4:  # if the box is checked
            finishes = opponents[((opponents["WIN_BY"].str.contains("KO/TKO")) |
                                  (opponents["WIN_BY"].str.contains("Submission"))) &
                                 (opponents["WINNER"].str.contains(fighterSelection))]["WIN_BY"].count()

            win = fights[fights['WINNER'] == fighterSelection]['WINNER'].count()
            draw = fights[fights['WINNER'] == "D"]['WINNER'].count()
            nc = fights[fights['WINNER'] == "NC"]['WINNER'].count()
            loss = len(fights) - win - draw - nc

            # Display UFC Record
            record(win, loss, draw, nc, "UFC Record")
            # Display Finish Percent
            st.metric("Finish Percent", f"{str(((finishes / len(opponents)) * 100).__round__(2))}%")

            # If the fighter has fought for the Title, display record and finish percent
            if ('Interim' in list(fights["TitleFight"])) or ('Yes' in list(fights["TitleFight"])):
                beltFight = fights[(fights["TitleFight"] == "Yes") | (fights["TitleFight"] == "Interim")]
                title_finishes = beltFight[((beltFight["WIN_BY"].str.contains("KO/TKO")) |
                                            (beltFight["WIN_BY"].str.contains("Submission"))) &
                                           (beltFight["WINNER"].str.contains(fighterSelection))]["WIN_BY"].count()

                w = beltFight[beltFight['WINNER'] == fighterSelection]['WINNER'].count()
                d = beltFight[beltFight['WINNER'] == "D"]['WINNER'].count()
                noContest = beltFight[beltFight['WINNER'] == "NC"]['WINNER'].count()
                l = len(beltFight) - w - d - noContest

                # Display UFC Title Fight Record
                record(w, l, d, noContest, "UFC Record in Title Fights")
                # Display Title Fight Finish Percent
                st.metric("Title Fight Finish Percent", f"{str(((title_finishes / len(beltFight)) * 100).__round__(2))}%")

            st.table(fights)

        else:
            finishes = opponents[((opponents["WIN_BY"].str.contains("KO/TKO")) |
                                  (opponents["WIN_BY"].str.contains("Submission"))) &
                                 (opponents["WINNER"].str.contains(fighterSelection))]["WIN_BY"].count()
            win = fights[fights['WINNER'] == fighterSelection]['WINNER'].count()
            draw = fights[fights['WINNER'] == "D"]['WINNER'].count()
            nc = fights[fights['WINNER'] == "NC"]['WINNER'].count()
            loss = len(fights) - win - draw - nc

            # Display UFC Record
            record(win, loss, draw, nc, "UFC Record")
            # Display Finish Percent
            st.metric("Finish Percent", f"{str(((finishes / len(opponents)) * 100).__round__(2))}%")

            # If the fighter has fought for the Title, display record and finish percent
            if ('Interim' in list(fights["TitleFight"])) or ('Yes' in list(fights["TitleFight"])):
                beltFight = fights[(fights["TitleFight"] == "Yes") | (fights["TitleFight"] == "Interim")]
                title_finishes = beltFight[((beltFight["WIN_BY"].str.contains("KO/TKO")) |
                                            (beltFight["WIN_BY"].str.contains("Submission"))) &
                                           (beltFight["WINNER"].str.contains(fighterSelection))]["WIN_BY"].count()
                w = beltFight[beltFight['WINNER'] == fighterSelection]['WINNER'].count()
                d = beltFight[beltFight['WINNER'] == "D"]['WINNER'].count()
                noContest = beltFight[beltFight['WINNER'] == "NC"]['WINNER'].count()
                l = len(beltFight) - w - d - noContest

                # Display UFC Title Fight Record
                record(w, l, d, noContest, "UFC Record in Title Fights")
                # Display Title Fight Finish Percent
                st.metric("Title Fight Finish Percent", f"{str(((title_finishes / len(beltFight)) * 100).__round__(2))}%")

            st.table(fights[["EVENT", "BOUT", "WeightClass", "TitleFight"]])

    elif interest == "Fighter Totals":
        container = st.container()
        col1, col2, col3 = container.columns(3)
        statMetric = col1.selectbox("Choose how to view fighter stats",
                                    ["Totals", "Average", "Per Minute"])
        titleFightChecker = cleanDataDF[cleanDataDF["BOUT"].str.contains(fighterSelection)]
        if ('Yes' in list(titleFightChecker["TitleFight"])) | ('Interim' in list(titleFightChecker["TitleFight"])):
            titlefightstats = col3.checkbox("Display Stats for Title Fights")
            fights = opponents[["EVENT", "BOUT", "WeightClass", "WIN_BY", "WINNER", "TitleFight"]]
            if titlefightstats:
                if ('Interim' in list(fights["TitleFight"])) or ('Yes' in list(fights["TitleFight"])):
                    beltFight = fights[(fights["TitleFight"] == "Yes") | (fights["TitleFight"] == "Interim")]
                    w = beltFight[beltFight['WINNER'] == fighterSelection]['WINNER'].count()
                    d = beltFight[beltFight['WINNER'] == "D"]['WINNER'].count()
                    noContest = beltFight[beltFight['WINNER'] == "NC"]['WINNER'].count()
                    l = len(beltFight) - w - d - noContest
                    record(w, l, d, noContest, "UFC Record in Championship Fights")

                    if statMetric == "Totals":
                        stats = sideBySideStats(fighterSelection, 'sum', True)
                    elif statMetric == "Average":
                        stats = sideBySideStats(fighterSelection, 'mean', True)
                    else:
                        stats = sideBySideStats(fighterSelection, "Per Minute", True)
            else:
                win = fights[fights['WINNER'] == fighterSelection]['WINNER'].count()
                draw = fights[fights['WINNER'] == "D"]['WINNER'].count()
                nc = fights[fights['WINNER'] == "NC"]['WINNER'].count()
                loss = len(fights) - win - draw - nc
                record(win, loss, draw, nc, "UFC Record")

                if statMetric == "Totals":
                    stats = sideBySideStats(fighterSelection, 'sum')
                elif statMetric == "Average":
                    stats = sideBySideStats(fighterSelection, 'mean')
                else:
                    stats = sideBySideStats(fighterSelection, "Per Minute")
        else:
            fights = opponents[["EVENT", "BOUT", "WeightClass", "WIN_BY", "WINNER", "TitleFight"]]
            win = fights[fights['WINNER'] == fighterSelection]['WINNER'].count()
            draw = fights[fights['WINNER'] == "D"]['WINNER'].count()
            nc = fights[fights['WINNER'] == "NC"]['WINNER'].count()
            loss = len(fights) - win - draw - nc
            record(win, loss, draw, nc, "UFC Record")

            if statMetric == "Totals":
                stats = sideBySideStats(fighterSelection, 'sum')
            elif statMetric == "Average":
                stats = sideBySideStats(fighterSelection, 'mean')
            else:
                stats = sideBySideStats(fighterSelection, "Per Minute")

        st.dataframe(stats.style.format("{:2}"))
        statSelection = col2.selectbox("Select a Stat", stats.columns.drop("Fight_Time_(Min)"))
        fighterGraph(stats, stats.index, statSelection)

if rad == "UFC":

    opt = st.selectbox("Category", options=["FIGHTER", "WeightClass", 'Title Fights'])

    if opt == "FIGHTER":
        container2 = st.container()
        col1, col2 = container2.columns(2)
        min_fights = col1.number_input("Choose the Minimum Amount of Fights (Average is 7)", min_value=1,
                                     max_value=41, step=1)

        ufc = individualFightStats(cleanDataDF)

        fightCount = ufc[opt].value_counts()
        ufcSumStatsGrouped = (ufc.groupby(opt).sum())

        for i in ufcSumStatsGrouped.columns[:-1]:
            ufcSumStatsGrouped[i] = (ufcSumStatsGrouped[i] / ufcSumStatsGrouped["Fight_Time_(Min)"]).__round__(2)

        attributes = col2.selectbox('Stat Selection',
                                  options=["Total Strikes", "Head Strikes", "Body Strikes", "Leg Strikes",
                                           "Standing Strikes", "Clinch Strikes", "Ground Strikes", "Takedowns"])

        attDict = {"Total Strikes": ["TOTAL_STR_ATT", "TOTAL_STR_LAND"], "Head Strikes": ["HEAD_ATT", "HEAD_LAND"],
                   "Body Strikes": ["BODY_ATT", "BODY_LAND"], "Leg Strikes": ["LEG_ATT", "LEG_LAND"],
                   "Standing Strikes": ["STD_STR_ATT", "STD_STR_LAND"],
                   "Clinch Strikes": ["CLINCH_STR_ATT", "CLINCH_STR_LAND"],
                   "Ground Strikes": ['GRD_STR_ATT', 'GRD_STR_LAND'], "Takedowns": ["TD_ATT", "TD"]}

        attribute1, attribute2 = attDict[attributes]
        ufcSumStatsGrouped = (ufcSumStatsGrouped[fightCount >= min_fights])
        ufcSumStatsGrouped = pd.DataFrame(ufcSumStatsGrouped)
        ufcSumStatsGrouped.insert(0, "FIGHTER", ufcSumStatsGrouped.index)
        newind = list(range(len(ufcSumStatsGrouped)))
        ufcSumStatsGrouped.insert(0, "index", newind)
        ufcSumStatsGrouped.set_index('index', inplace=True)
        ave1 = (np.mean(ufcSumStatsGrouped[attribute1]))
        ave2 = (np.mean(ufcSumStatsGrouped[attribute2]))

        name_labels = st.checkbox("Show Points With Name Labels")
        if not name_labels:
            fig = px.scatter(ufcSumStatsGrouped, f"{attribute1}", f"{attribute2}", hover_data=["FIGHTER"],
                             title=f'Ave {attribute1} vs Ave {attribute2} (Per Minute)',
                             labels={f"{attribute1}": f'Ave {attribute1} per Minute',
                                     f"{attribute2}": f'Ave {attribute2} per Minute'})
        else:
            fig = px.scatter(ufcSumStatsGrouped, f"{attribute1}", f"{attribute2}", text="FIGHTER",
                             title=f'Ave {attribute1} vs Ave {attribute2} (Per Minute)',
                             labels={f"{attribute1}": f'Ave {attribute1} per Minute',
                                     f"{attribute2}": f'Ave {attribute2} per Minute'})
            fig.update_traces(textposition="top center")

        fig.add_hline(ave1)
        fig.add_vline(ave2)

        st.plotly_chart(fig, use_container_width=True)

    if opt == "WeightClass":
        ufc = individualFightStats(cleanDataDF)
        fightCount = ufc["WeightClass"].value_counts()
        ufcSumStatsGrouped = (ufc.groupby("WeightClass").mean())
        for i in ufcSumStatsGrouped.columns[:-1]:
            ufcSumStatsGrouped[i] = (ufcSumStatsGrouped[i] / ufcSumStatsGrouped["Fight_Time_(Min)"]).__round__(2)

        attributes = st.selectbox(label='Select Stat', options=ufcSumStatsGrouped.columns[:-1])

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

        fig = px.bar(ufcSumStatsGrouped, "WeightClass", f"{attributes}",
                     labels={f"{attributes}": f'Ave {attributes} per Minute'})
        fig.add_hline(y=ave1)
        st.plotly_chart(fig, use_container_width=True)

    if opt == "Title Fights":
        st.write("Coming Soon")
