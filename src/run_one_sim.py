import pandas as pd

from help_functions import calculate_score_probabilities, simulate_match, simulate_elo_update, update_table


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
    sorted_teams = sorted(elo_data.items(), key=lambda x: x[1], reverse=True)


    positions = {team: rank + 1 for rank, (team, _) in enumerate(sorted_teams)}

    return positions
