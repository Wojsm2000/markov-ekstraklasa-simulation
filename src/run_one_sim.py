import pandas as pd
import os
from help_functions import calculate_score_probabilities, simulate_match, simulate_elo_update, update_table
import json
from collections import defaultdict

def one_season_simulation(elo_data, temporary_table, temporary_list_home_teams, temporary_list_away_teams):
    assert len(temporary_list_home_teams) == len(temporary_list_away_teams), "Home and away teams lists must be of the same length"
    for home_team, away_team in zip(temporary_list_home_teams, temporary_list_away_teams):
        home_elo = elo_data[home_team]
        away_elo = elo_data[away_team]
        
        home_win_prob, draw_prob, away_win_prob = calculate_score_probabilities(home_elo, away_elo)
        
        outcome = simulate_match(home_win_prob, draw_prob, away_win_prob)
        temporary_table=update_table(temporary_table, home_team, away_team, outcome)

        new_home_elo, new_away_elo = simulate_elo_update(home_elo, away_elo, outcome)
        
        elo_data[home_team] = new_home_elo
        elo_data[away_team] = new_away_elo
    sorted_teams = sorted(temporary_table.items(), key=lambda x: x[1], reverse=True)
    


    positions = {team: rank + 1 for rank, (team, _) in enumerate(sorted_teams)}

    return positions,sorted_teams[-3][1]+1


if __name__ == "__main__":
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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    elo_filepath = os.path.join(script_dir, "data", "elo_data.json")
    schedule_filepath = os.path.join(script_dir, "data", "schedule_data.json")
    table_filepath = os.path.join(script_dir, "data", "table_data.json")
    sim_file_path = os.path.join(script_dir, "data", "simulated_results.json")

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
    table_data = {k: int(v) for k, v in table_data.items()}
    temporary_elo = elo_data.copy()
    temporary_table = table_data.copy()
    temporary_match_data = match_data.copy()
    one_season_results,pnt=one_season_simulation(temporary_elo, temporary_table, temporary_list_home_teams=temporary_match_data["home_teams"].tolist(),
                                                 temporary_list_away_teams=temporary_match_data["away_teams"].tolist())
    print(pnt )