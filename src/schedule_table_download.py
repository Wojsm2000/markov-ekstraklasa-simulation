
import requests
from help_functions import extract_date_from_string
from bs4 import BeautifulSoup

def return_match_data():
    page = requests.get("http://www.90minut.pl/liga/1/liga14072.html")
    soup = BeautifulSoup(page.content, features="html.parser")
    tb=soup.find_all("table", {"class": "main"})
    home_teams=[]
    away_teams=[]
    
    dates=[]
    home_score=[]
    away_score=[]
    for i in tb:
        d=i.find_all("td", {"valign": "top"})
        if len(d)>0:
            for i in range(36):
                if i%4==0:
                    home_teams.append(d[i].text.strip())
                elif i%4==1:
                    j=(d[i].text.strip())
                    
                    if j!="-":
                                home_score.append(int(j.split("-")[0]))
                                away_score.append(int(j.split("-")[1]))
                    else:
                                home_score.append(-1)
                                away_score.append(-1)
                                            
                elif i%4==2:
                    away_teams.append(d[i].text.strip())
                else:
                    dates.append(extract_date_from_string(d[i].text.strip()))
    
    
    return {"home_teams": home_teams, "away_teams": away_teams, "home_scores": home_score, "away_scores": away_score, "dates": dates}


