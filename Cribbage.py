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

    def get_score(self):
        global score
        return score
    
    def get_name(self):
        global name
        return name


class Crib_Functions:
    global deck_ID
    def __init__(self) -> None:
        global deck_ID
        response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
        x = json.loads(response.text)
        deck_ID = str(x["deck_id"])

# Returns the ID of the deck currently in use
    def get_deck_ID(self):
        global deck_ID
        return deck_ID

# Deals out 6 cards and creates 2 piles ID'd by the player's names
    def deal_cards(self, player1name, player2name):
        global deck_ID
        response1 = requests.get("https://deckofcardsapi.com/api/deck/"+deck_ID+"/pile/"+player1name+"/add/?count=6")
        response2 = requests.get("https://deckofcardsapi.com/api/deck/"+deck_ID+"/pile/"+player2name+"/add/?count=6")
        return json.loads(response1), json.loads(response2)

# Creates the crib pile out of 4 cards contributed by the players
    def make_crib(self, list_of_cards):
        response = requests.get("https://deckofcardsapi.com/api/deck/"+self.get_deck_ID+"/pile/crib/add/?cards="+list_of_cards)
        return json.loads(response)
    
# Draws a card from a specific pile
    def draw_card_from_pile(self, pile_name):
        response = requests.get("https://deckofcardsapi.com/api/deck/"+self.get_deck_ID+"/pile/"+pile_name+"/draw/?count=1")
        return json.loads(response)

# Draws a specific card from a specific pile
    def draw_specific_card_from_pile(self, pile_name, card_name):
        response = requests.get("https://deckofcardsapi.com/api/deck/"+self.get_deck_ID+"/pile/"+pile_name+"/draw/?cards="+card_name)
        return json.loads(response)

# Draws a card from the deck (for top card or turn determination at beginning)
    def draw_card_from_deck(self):
        response = requests.get("https://deckofcardsapi.com/api/deck/"+self.get_deck_ID+"/draw/?count=1")
        return json.loads(response)

# For round play, placing cards in play pile
    def add_card_to_play_piles(self, pile_name, card_name):
        response = requests.get("https://deckofcardsapi.com/api/deck/"+deck_ID+"/pile/"+pile_name+"play/add/?cards="+card_name)
        return json.loads(response)

    def add_cards_to_score_pile(self, pile_name):
        response1 = requests.get("https://deckofcardsapi.com/api/deck/"+deck_ID+"/pile/"+pile_name+"play/list")
        x = json.loads(response1)
        card_list = ""
        for cards in x["piles"][pile_name+'play']["cards"]:
            card_list += cards["code"]+","
        card_list = card_list[:len(card_list)-1]
        response2 = requests.get("https://deckofcardsapi.com/api/deck/"+deck_ID+"/pile/"+pile_name+"score/add/?cards="+card_list)
        return json.loads(response2)
