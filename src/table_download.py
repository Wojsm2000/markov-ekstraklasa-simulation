import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

def return_match_table():
    page = requests.get("http://www.90minut.pl/liga/1/liga14072.html")
    soup = BeautifulSoup(page.content, features="html.parser")
    tr=soup.find_all("tr", {"align": "center"})
    tr=[row.text.strip() for row in tr]
    
    tr=tr[2:20]
    
    tr=[tr.split("\n")[:4] for tr in tr]
    
    tr=[[row[1][1:],row[3]] for row in tr]
  
    result_dict = {team: points for team, points in tr}
    return result_dict

if __name__ == "__main__":
    print(return_match_table())


