import os
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()

API_HOST = "api-football-v1.p.rapidapi.com"
API_BASE_URL = "https://api-football-v1.p.rapidapi.com/v3"

API_KEY = os.getenv("API_FOOTBALL_KEY", "YOUR_API_KEY_HERE")

HEADERS = {
    "x-rapidapi-host": API_HOST,
    "x-rapidapi-key": API_KEY
}

def get_team_id_by_name(team_name):
    """
    Lekéri egy csapat ID-ját név alapján. Pontos egyezést keres!
    """
    url = f"{API_BASE_URL}/teams?search={team_name}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        data = resp.json()
        teams = data.get('response', [])
        if teams:
            return teams[0]['team']['id']
    return None

def get_fixtures_by_date(match_date):
    """
    Lekérdezi az összes elérhető mérkőzést (fixture-t) egy adott napon.
    Visszaadja a meccsek listáját (hazai csapat, vendég csapat, liga, időpont, fixture_id).
    Egyetlen API-hívás!
    """
    date_str = match_date.strftime('%Y-%m-%d')
    url = f"{API_BASE_URL}/fixtures?date={date_str}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        data = resp.json()
        fixtures = data.get('response', [])
        results = []
        for fixture in fixtures:
            results.append({
                'home_team': fixture['teams']['home']['name'],
                'away_team': fixture['teams']['away']['name'],
                'league': fixture['league']['name'],
                'country': fixture['league']['country'],
                'time': fixture['fixture']['date'],
                'fixture_id': fixture['fixture']['id']
            })
        return results
    return []

def find_fixture_id(home_team_id, away_team_id, match_date):
    """
    Lekéri a fixture_id-t két csapat ID és dátum alapján.
    """
    date_str = match_date.strftime('%Y-%m-%d')
    url = f"{API_BASE_URL}/fixtures?date={date_str}&team={home_team_id}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        data = resp.json()
        fixtures = data.get('response', [])
        for fixture in fixtures:
            h_id = fixture['teams']['home']['id']
            a_id = fixture['teams']['away']['id']
            if (h_id == home_team_id and a_id == away_team_id):
                return fixture['fixture']['id']
    return None

def get_prediction_by_fixture_id(fixture_id):
    """
    Visszaadja a predikciókat egy adott fixture_id-re az API-Football-ból.
    """
    url = f"{API_BASE_URL}/predictions?fixture={fixture_id}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json()
    return None
