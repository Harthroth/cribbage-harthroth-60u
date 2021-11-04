import requests 
import json

class Player:
    global score
    global name
    def __init__(self, n) -> None:
        global score
        global name
        name = n
        score = 0

    def increase_score(self, new_score):
        global score
        score += new_score
    
    def reset_score(self):
        global score
        score = 0

class Crib_Functions:
    global deck_ID
    def __init__(self) -> None:
        global deck_ID
        response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
        x = json.loads(response.text)
        deck_ID = str(x["deck_id"])

    def get_deck_ID(self):
        global deck_ID
        return deck_ID

    def deal_cards(self, player1name, player2name):
        global deck_ID
        response1 = requests.get("https://deckofcardsapi.com/api/deck/"+deck_ID+"/pile/"+player1name+"/add/?count=6")
        response2 = requests.get("https://deckofcardsapi.com/api/deck/"+deck_ID+"/pile/"+player2name+"/add/?count=6")
