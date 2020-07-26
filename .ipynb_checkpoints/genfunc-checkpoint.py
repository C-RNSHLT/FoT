import json
import requests

#find team results
def find_results(team, competition):
    for match in competition:
        home_team = match["home_team"]["home_team_name"]
        away_team = match["away_team"]["away_team_name"]
        if home_team == team or away_team == team:
            print(home_team + " : " + away_team + "\n"
                  + str(match["home_score"]) + " : " + str(match["away_score"]))

#find match id
def find_id(home_team, away_team, comp_id, season_id):
    match_url = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/{}/{}.json"
    match = requests.get(url=match_url.format(comp_id, season_id)).json()
    for m in match:
        home_team_name = m["home_team"]["home_team_name"]
        away_team_name = m["away_team"]["away_team_name"]
        if (home_team_name == home_team) and (away_team_name == away_team):
            return((m["match_id"]))

#find path to matches data
def path_to_matches(league, season):
    with open("statsBomb_data/data/competitions.json") as file:
            competitions = json.load(file)
    for competition in competitions:
        competition_name = competition["competition_name"]
        season_name = competition["season_name"]
        if competition_name == league and season_name == season:
            return "statsBomb_data/data/matches/" + str(competition["competition_id"]) + "/" + str(competition["season_id"]) + ".json"
    print("Error")

#transform StatsBomb from GitHub into Pandas DataFrame
#import pandas as pd
#import requests
def parse_data(competition_id, season_id):
    matches = requests.get(url = comp_url.format(competition_id, season_id)).json()
    match_ids = [match["match_id"] for match in matches]
    
    all_events = []
    for match_id in match_ids:
        
        events = requests.get(url = match_url.format(match_id)).json()
        
        shots = [x for x in events if x["type"]["name"] == "Shot"]
        for shot in shots:
            attributes = {
                "match_id": match_id,
                "team": shot["possession_team"]["name"],
                "player": shot["player"]["name"],
                "x": shot["location"][0],
                "y": shot["location"][1],
                "outcome": shot["shot"]["outcome"]["name"],
            }
            all_events.append(attributes)
    return pd.DataFrame(all_events)


def main():
    pass

if __name__ == "__main__":
    main()