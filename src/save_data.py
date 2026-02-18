from elo_download import load_elo_data
from schedule_table_download import return_match_data
from table_download import return_match_table
import json

def save_table(filepath):
    data=return_match_table()
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def save_schedule(filepath):
    data=return_match_data()
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def save_elo(filepath,date):
    data=load_elo_data(date)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    save_table("src\\data\\table_data.json")
    save_schedule("src\\data\\schedule_data.json")
    save_elo("src\\data\\elo_data.json","18-02-2026")