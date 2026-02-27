import random
import math
from collections import defaultdict
import pandas as pd
def extract_date_from_string(string: str) -> str:
    #
    
    if ',' not in string:
        return ""
    months = {
    "stycznia": "01",
    "lutego": "02",
    "marca": "03",
    "kwietnia": "04",
    "maja": "05",
    "czerwca": "06",
    "lipca": "07",
    "sierpnia": "08",
    "września": "09",
    "października": "10",
    "listopada": "11",
    "grudnia": "12"
}
    string=string.split(',')[0].strip()
    day,month=string.split(' ')
    month=months[month]
    day=day.zfill(2)
    year='2026' if month in ['01','02','03','04','05','06'] else '2025'
    date=f"{day}-{month}-{year}"
    return date



def calculate_score_probabilities(home_elo: float, away_elo: float, home_advantage: float = 75) -> tuple:
    
   
    adjusted_home_elo = home_elo + home_advantage
    
    expected_home = 1 / (1 + 10 ** ((away_elo - adjusted_home_elo) / 400))
    expected_away = 1 - expected_home
    
    draw_probability = 0.30 * math.exp(-0.0027 * abs(adjusted_home_elo - away_elo))
    
    home_win_probability = expected_home * (1 - draw_probability)
    away_win_probability = expected_away * (1 - draw_probability)
    
    return home_win_probability, draw_probability, away_win_probability

def simulate_match(home_win_prob: float, draw_prob: float, away_win_prob: float) -> str:
    outcome = random.choices(
        population=["1", "X", "2"],
        weights=[home_win_prob, draw_prob, away_win_prob],
        k=1
    )[0]
    return outcome

def simulate_elo_update(home_elo: float, away_elo: float, outcome: str, k: int = 20) -> tuple:
    expected_home = 1 / (1 + 10 ** ((away_elo - home_elo) / 400))
    expected_away = 1 - expected_home
    
    if outcome == "1":
        home_score, away_score = 1, 0
    elif outcome == "X":
        home_score, away_score = 0.5, 0.5
    else:
        home_score, away_score = 0, 1
    
    new_home_elo = home_elo + k * (home_score - expected_home)
    new_away_elo = away_elo + k * (away_score - expected_away)
    
    return new_home_elo, new_away_elo


def update_table(temporary_table, home_team, away_team, outcome):
    if outcome == "1":
        temporary_table[home_team]+= 3
        
    elif outcome == "X":
        temporary_table[home_team]+= 1
        temporary_table[away_team]+= 1
    else:
        temporary_table[away_team]+= 3
        
    return temporary_table

def recursive_to_dict(d)-> dict:
    if isinstance(d, defaultdict):
        d = {k: recursive_to_dict(v) for k, v in d.items()}
    return d




def sort_by_position_priority(df):
    df_copy = df.copy()
    ordered_teams = []

    df_copy=df_copy.cumsum(axis=1)
    for position in df.columns:
        if df_copy.empty:
            break

        
        best_team = df_copy[position].idxmax()
        ordered_teams.append(best_team)

       
        df_copy = df_copy.drop(index=best_team)
    
    return df.loc[ordered_teams]


    









if __name__ == "__main__":
    print(extract_date_from_string('30 stycznia, 18:00 (3745)'))
    print(calculate_score_probabilities(1534, 1345))
    print(simulate_match(0.4, 0.3, 0.3))
    print(simulate_elo_update(1500, 1600, "2"))