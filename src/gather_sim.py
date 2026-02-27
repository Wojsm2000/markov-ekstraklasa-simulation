import pandas as pd
import json
import os
from collections import defaultdict
from datetime import datetime
from run_one_sim import one_season_simulation
from tqdm import tqdm
from help_functions import recursive_to_dict
NAMES_DICT={
    "Jagiellonia": "Jagiellonia Białystok",
    "Gornik": "Górnik Zabrze",
    "Plock": "Wisła Płock",
    "Lubin": "Zagłębie Lubin",
    "Cracovia": "Cracovia",
    "Lech": "Lech Poznań",
    "Rakow": "Raków Częstochowa",
    "Korona": "Korona Kielce",
    "Lechia": "Lechia Gdańsk",
    "Radomiak": "Radomiak Radom",
    "Katowice": "GKS Katowice",
    "Piast Gliwice": "Piast Gliwice",
    "Pogon": "Pogoń Szczecin",
    "Motor Lublin": "Motor Lublin",
    "Widzew": "Widzew Łódź",
    "Arka": "Arka Gdynia",
    "Legia": "Legia Warszawa",
    "Nieciecza": "Bruk-Bet Termalica Nieciecza"
}


def return_whole_sim(elo_filepath, schedule_filepath, table_filepath, number_of_simulations=1_000_000):
    elo_data = pd.read_json(elo_filepath)
    
    elo_data["Club"] = elo_data["Club"].map(NAMES_DICT)
    elo_data = elo_data.set_index("Club")["Elo"].to_dict()
    
    simulated_results = defaultdict(lambda: defaultdict(int))
   
    with open(table_filepath, "r", encoding="utf-8") as f:
        table_data = json.load(f)
    with open(schedule_filepath, "r", encoding="utf-8") as f:
        match_data = json.load(f)    
    match_data=pd.read_json(schedule_filepath)
    match_data=match_data[match_data["home_scores"]==-1]
   

   ### NOTE TO MYSELF: when downloading data convert points to ints and then delete this part of code
    table_data = {k: int(v) for k, v in table_data.items()}

    for _ in tqdm(range(number_of_simulations)):
        
        temporary_elo = elo_data.copy()
        temporary_table = table_data.copy()
        temporary_match_data = match_data.copy()
        one_season_results=one_season_simulation(temporary_elo, temporary_table, temporary_list_home_teams=temporary_match_data["home_teams"].tolist(),
                                                 temporary_list_away_teams=temporary_match_data["away_teams"].tolist())
        
        for team, position in one_season_results.items():
            simulated_results[team][position] += 1


    return simulated_results   
    

if __name__ == "__main__":
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    elo_filepath = os.path.join(script_dir, "data", "elo_data.json")
    schedule_filepath = os.path.join(script_dir, "data", "schedule_data.json")
    table_filepath = os.path.join(script_dir, "data", "table_data.json")
    sim_file_path = os.path.join(script_dir, "data", "simulated_results.json")
    results = return_whole_sim(elo_filepath, schedule_filepath, table_filepath)
    

    if isinstance(results, defaultdict):
        clean_dict = recursive_to_dict(results)
        with open(sim_file_path, "w",encoding="utf-8") as f:
            json.dump(clean_dict, f, indent=4, ensure_ascii=False)