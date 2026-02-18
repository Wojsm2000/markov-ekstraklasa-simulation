import random
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



def calculate_score_probabilities(home_elo:float, away_elo:float) -> tuple:
    
    expected_home = 1 / (1 + 10 ** ((away_elo - home_elo) / 400))
    expected_away = 1 - expected_home
    
    
    draw_probability = 0.25
    
    
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