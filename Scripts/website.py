import pandas as pd
import streamlit as st
# from similarity import similarFights


def noStreamlitIndex():
    hide_table_row_index = """
                        <style>
                        tbody th {display:none}
                        .blank {display:none}
                        </style>
                        """
    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)


cleanDataDF = pd.read_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\CleanData.csv", index_col=0)

with st.sidebar:
    rad = st.radio("Selection", ("Home", "Similar Fights"))

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

# if rad == "Similar Fights":
#     searchBy = st.selectbox("Search By Fighter or Event", ["Fighter", "Event"])
#     if searchBy == "Event":
#         events = cleanDataDF["EVENT"].unique()
#         eventSelection = st.selectbox("Choose the Event", events)
#         with st.form("MyForm"):
#             bouts = cleanDataDF[cleanDataDF["EVENT"] == eventSelection]
#             boutSelection = st.selectbox("Choose the fight", bouts["BOUT"].unique())
#             spoiler2 = st.checkbox("Display Winner")
#             submit_button = st.form_submit_button(label='Submit')
#
#             if submit_button:
#                 st.subheader("10 Most Similar Fights")
#                 id = cleanDataDF[(cleanDataDF["EVENT"] == eventSelection) & (cleanDataDF["BOUT"] == boutSelection)].index[0]
#                 if spoiler2:
#                     st.table(similarFights(id, byTotals=True, includeWinner=True))
#                 else:
#                     st.table(similarFights(id, byTotals=True))
#
#     else:
#         fighters = pd.read_csv("C:\\Users\\sabzu\\Documents\\UFCRecommendationProject\\UFCProject\\DataFiles2\\UFC_Fighters.csv", index_col=0)
#         fighterSelection = st.selectbox("Choose the Fighter", fighters)
#         with st.form("MyForm"):
#             bouts = cleanDataDF[cleanDataDF["BOUT"].str.contains(fighterSelection)]
#             event_bout =  bouts["BOUT"] + " --- " + bouts["EVENT"]
#             fightSelection = st.selectbox("Choose the Fight", event_bout)
#             fightSelection = fightSelection.split(" --- ")
#
#             spoiler3 = st.checkbox("Display Winner")
#             submit_button = st.form_submit_button(label='Submit')
#
#             if submit_button:
#                 st.subheader("10 Most Similar Fights")
#                 id = cleanDataDF[(cleanDataDF["EVENT"] == fightSelection[1]) & (cleanDataDF["BOUT"] == fightSelection[0])].index[0]
#                 noStreamlitIndex()
#                 if spoiler3:
#                     st.table(similarFights(id, byTotals=True, includeWinner=True))
#                 else:
#                     st.table(similarFights(id, byTotals=True))

