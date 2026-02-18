import requests
import pandas as pd
from io import StringIO
def load_elo_data(date:str):
    URL = f"http://api.clubelo.com/{date}"
    try:
        r = requests.get(url = URL)
        assert r.status_code == 200, f"Failed to fetch data: {r.status_code}"
        data = StringIO(r.text)
        data = pd.read_csv(data)
    except Exception as e:
        print(e)
        return []
    
    data = data[data["Country"] == "POL"][["Club", "Elo"]]
    return data.to_dict(orient="records")