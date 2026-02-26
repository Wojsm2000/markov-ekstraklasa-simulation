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
print(optimal_df)