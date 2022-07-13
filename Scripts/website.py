import pandas as pd
import streamlit as st
from similarity import similarFights
from fighterStats import sideBySideStats
import plotly.express as px


def noStreamlitIndex():
    hide_table_row_index = """
                        <style>
                        tbody th {display:none}
                        .blank {display:none}
                        </style>
                        """
    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)


def record(win, loss, draw, nc, text):
    if (draw == 0) & (nc == 0):
        st.write(f"{text}: {win}-{loss}")
    elif (draw != 0) & (nc == 0):
        st.write(f"{text}: {win}-{loss}-{draw}")
    elif (draw != 0) & (nc != 0):
        st.write(f"{text}: {win}-{loss}-{draw} ({nc} NC)")
    elif (draw == 0) & (nc != 0):
        st.write(f"{text}: {win}-{loss} ({nc} NC)")


cleanDataDF = pd.read_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\CleanData.csv", index_col=0)

with st.sidebar:
    rad = st.radio("Selection", ("Home", "Fighter", "Similar Fights"))

if rad == "Home":
    st.title("Most Recent UFC Event", anchor="Home_Page")
    spoiler1 = st.radio("Show the Winner?", options=["No", "Yes"])
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
                id = cleanDataDF[(cleanDataDF["EVENT"] == eventSelection) & (cleanDataDF["BOUT"] == boutSelection)].index[0]
                if spoiler2:
                    st.table(similarFights(id, byTotals=True, includeWinner=True))
                else:
                    st.table(similarFights(id, byTotals=True))

    else:
        fighters = pd.read_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\UFC_Fighters.csv", index_col=0)
        fighterSelection = st.selectbox("Choose the Fighter", fighters)
        with st.form("MyForm"):
            bouts = cleanDataDF[cleanDataDF["BOUT"].str.contains(fighterSelection)]
            event_bout =  bouts["BOUT"] + " --- " + bouts["EVENT"]
            fightSelection = st.selectbox("Choose the Fight", event_bout)
            fightSelection = fightSelection.split(" --- ")

            spoiler3 = st.checkbox("Display Winner")
            submit_button = st.form_submit_button(label='Submit')

            if submit_button:
                st.subheader("10 Most Similar Fights")
                id = cleanDataDF[(cleanDataDF["EVENT"] == fightSelection[1]) & (cleanDataDF["BOUT"] == fightSelection[0])].index[0]
                noStreamlitIndex()
                if spoiler3:
                    st.table(similarFights(id, byTotals=True, includeWinner=True))
                else:
                    st.table(similarFights(id, byTotals=True))


if rad == "Fighter":
    fighters = pd.read_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\UFC_Fighters.csv", index_col=0)
    fighterSelection = st.selectbox("Choose a Fighter", fighters)
    noStreamlitIndex()
    opponents = cleanDataDF[cleanDataDF["BOUT"].str.contains(fighterSelection)]
    with st.form("MyForm"):
        interest = st.selectbox("Choose what to look at", ["Fight History", "Fighter Totals"])

        if interest == "Fight History":
            spoiler4 = st.checkbox("Display Winner")
            st.form_submit_button("Submit")
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
            # stats = sideBySideStats(fighterSelection)
            # st.dataframe(stats)
            titleFightChecker = cleanDataDF[cleanDataDF["BOUT"].str.contains(fighterSelection)]
            if ('Yes' in list(titleFightChecker["TitleFight"])) | ('Interim' in list(titleFightChecker["TitleFight"])):
                titlefightstats = st.selectbox("Stats for Title Fights", ["No", "Yes"])
                if titlefightstats == 'Yes':
                    stats = sideBySideStats(fighterSelection, True)
                    st.dataframe(stats)
                else:
                    stats = sideBySideStats(fighterSelection)
                    st.dataframe(stats)
            else:
                stats = sideBySideStats(fighterSelection)
                st.dataframe(stats)
            statSelection = st.selectbox("Select a Stat", stats.columns.drop("Fight_Time_(Min)"))
            st.form_submit_button("Submit")
            fig = px.bar(stats, stats.index, statSelection)
            st.plotly_chart(fig, use_container_width=True)
