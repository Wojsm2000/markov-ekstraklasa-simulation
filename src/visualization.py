import streamlit as st
import json
import pandas as pd
from help_functions import sort_by_position_priority


with open(r"src/data/simulated_results.json", "r", encoding="utf-8") as f:
    simulated_results = json.load(f)

df = pd.DataFrame.from_dict(simulated_results, orient="index")

df=df.reindex(columns=[str(i) for i in range(1,19)])

df = df.fillna(0).astype(int)  



optimal_df = sort_by_position_priority(df)


def highlight_positions(row,df=optimal_df):
    total_rows = len(df)
    position = df.index.get_loc(row.name)+1

    if position in [1, 2]:
        color = "background-color: rgba(173, 216, 230, 0.4)"   # light blue
    elif position in [3, 4]:
        color = "background-color: rgba(144, 238, 144, 0.4)"   # light green
    elif position > total_rows - 3:
        color = "background-color: rgba(240, 128, 128, 0.4)"   # light red
    else:
        color = ""

    return [color] * len(row)



styled_df = optimal_df.style.apply(highlight_positions, axis=1)

st.dataframe(styled_df,width="stretch")
