import dotenv
import requests
import os
from typing import List

BASE_URL = 'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/'
MATCH_HISTORY_URL = 'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/'
MATCH_DETAILS_URL = 'https://americas.api.riotgames.com/lol/match/v5/matches/'
valid_names = ['']

class Match:
    def __init__(self, match_id: str, game_mode: str, game_type: str, game_duration: int, participants: List['Participant']):
        self.match_id = match_id
        self.game_mode = game_mode
        self.game_type = game_type
        self.game_duration = game_duration
        self.participants = participants
    
    def __str__(self):
        return f"Match ID: {self.match_id}\nGame Mode: {self.game_mode}\nGame Type: {self.game_type}\nGame Duration: {self.game_duration}\nParticipants: {self.participants}\n\n"
    
class Participant:
    def __init__(self, puid: str, summoner_name: str, champion: str, team: int, position: str, win: bool, kills: int, deaths: int, assists: int, cs: int, q_pings: int, total_damage: int, damage_taken: int, total_heal: int, time_ccing_others: int, time_cc_dealt: int, time_dead: int, vision_score: int, gold_earned: int):
        self.puid = puid
        self.summoner_name = summoner_name
        self.champion = champion
        self.team = team
        self.position = position
        self.win = win
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.cs = cs
        self.q_pings = q_pings
        self.total_damage = total_damage
        self.damage_taken = damage_taken
        self.total_heal = total_heal
        self.time_ccing_others = time_ccing_others
        self.time_cc_dealt =  time_cc_dealt
        self.time_dead = time_dead
        self.vision_score = vision_score
        self.gold_earned = gold_earned
        #self.items = items
                
                
                
    def __str__(self):
        return f"Summoner Name: {self.summoner_name}\nChampion: {self.champion}\nTeam: {self.team}\nWin: {self.win}\nKills: {self.kills}\nDeaths: {self.deaths}\nAssists: {self.assists}\nCS: {self.cs}\nQuestion Pings: {self.q_pings}\nTime CC'ing Others: {self.time_ccing_others}\n"



def get_summoner_info(summoner_name: str, tag: str, api_key):
    # Construct the full URL
    url = f"{BASE_URL}{summoner_name}/{tag}?api_key={api_key}"
    
    # Replace <region> in the URL with the actual region

    # Make the GET request to the Riot API
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # Return the JSON response
    else:
        return None  # Handle the error accordingly
    
def get_match_details(match_id: str, api_key) -> Match:
    url = f"{MATCH_DETAILS_URL}{match_id}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code != 200: # Check if the request was successful
        return None
    responses = []
    response = response.json()
    for participant in response['info']['participants']:  
        responses.append(participant['riotIdGameName'])
                
    new_match: Match = Match(match_id, response['info']['gameMode'], response['info']['gameType'], response['info']['gameDuration'], responses)
    return new_match

    
def get_player_details():
    
    pass   

def get_last_match(pid: str, api_key: str):
    url = f"{MATCH_HISTORY_URL}{pid}/ids?start=0&count=1&api_key={api_key}"#Change count as needed
    response = requests.get(url)
    print(response.json()[0]) 
    url = f"{MATCH_DETAILS_URL}{response.json()[0]}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code != 200: return None
    responses = []
    response = response.json()
    for part in response['info']['participants']:  #Part short for participant
        player: Participant = Participant(part['puuid'], part['riotIdGameName'], part['championName'], part['teamId'], part['individualPosition'], part['win'], part['kills'], part['deaths'], part['assists'], part['totalMinionsKilled'] + part['neutralMinionsKilled'], part['enemyMissingPings'], part['totalDamageDealtToChampions'], part['totalDamageTaken'], part['totalHeal'], part['timeCCingOthers'], part['totalTimeCCDealt'], part['totalTimeSpentDead'], part['visionScore'], part['goldEarned'])
        responses.append(player)
    new_match: Match = Match(response, response['info']['gameMode'], response['info']['gameType'], response['info']['gameDuration'], responses)
    return new_match
    
       
    

def get_match_history(pid: str, api_key: str, count: int)-> list:
    url = f"{MATCH_HISTORY_URL}{pid}/ids?start=0&count={count}&api_key={api_key}"#Change count as needed
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    

def main() -> None:
    dotenv.load_dotenv()
    api = os.getenv('API_KEY')
    #Just put my account for testing purposes
    summoner_name = 'Porp80'
    tag = 'Na1'
    summoner_info = get_summoner_info(summoner_name, tag, api)
    puid = summoner_info['puuid']
    if not summoner_info: return None
    print("Summoner Information:")
    count = 10
    #match_history = get_match_history(puid, api, count)
    
    matches: list[Match] = []
    """for match in match_history:
        new_match = get_match_details(match, api)
        print(new_match)
        matches.append(new_match)"""
    get_last_match(puid, api)


if __name__ == "__main__":
    main()