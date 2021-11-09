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

# For round play, placing cards in play pile - pile_nameplay
    def add_card_to_play_piles(self, pile_name, card_name):
        response = requests.get("https://deckofcardsapi.com/api/deck/"+deck_ID+"/pile/"+pile_name+"play/add/?cards="+card_name)
        return json.loads(response)

# End of play, put cards in new deck - pile_namescore
    def add_cards_to_score_pile(self, pile_name):
        response1 = requests.get("https://deckofcardsapi.com/api/deck/"+deck_ID+"/pile/"+pile_name+"play/list")
        x = json.loads(response1)
        card_list = ""
        for cards in x["piles"][pile_name+'play']["cards"]:
            card_list += cards["code"]+","
        card_list = card_list[:len(card_list)-1]
        response2 = requests.get("https://deckofcardsapi.com/api/deck/"+deck_ID+"/pile/"+pile_name+"score/add/?cards="+card_list)
        return json.loads(response2)

class final_scoring:
    def check_matching(self, pile):
        total = 0
        for x in pile:
            for y in pile:
                if x['value'] == y['value'] and x['code'] != y['code']:
                    total+=2
        return total

    def check_fifteen(self, pile):
        total = 0
        for x in pile:
            for y in pile:
                if x['value'] + y['value'] == 15 and x['code'] != y['code']:
                    total+=2
        return total

    def check_flush(self, pile):
        total = 0
        if len(pile) == 4:
            if pile[0]['suit'] == pile[1]['suit'] == pile[2]['suit'] == pile[3]['suit']:
                total+=4
        elif len(pile) == 5:
            if pile[0]['suit'] == pile[1]['suit'] == pile[2]['suit'] == pile[3]['suit'] == pile[4]['suit']:
                total += 5
        return total
            

    def check_runs(self, pile):
        pass

    def check_nubs(self, pile):
        if len(pile) == 2:
            if pile[0]['suit'] == pile[1]['suit']:
                return 2

    def check_all(self, pile):
        fifteen = self.check_fifteen(pile)
        flush = self.check_flush(pile)
        matching = self.check_matching(pile)
        nubs = self.check_nubs(pile)
        runs = self.check_runs(pile)
        return fifteen, flush, matching, nubs, runs
    
    def pile_value_change(self, pile):
        for x in range(0, len(pile)):
            if pile[x]['value'] == 'ACE':
                pile[x]['value'] = '1'
            elif pile[x]['value'] == 'JACK':
                pile[x]['value'] = '11'
            elif pile[x]['value'] == 'QUEEN':
                pile[x]['value'] = '12'
            elif pile[x]['value'] == 'KING':
                pile[x]['value'] = '13'
        return pile

class play_scoring:
    def check_fifteen(self, pile):
        pass
    def check_matching(self, pile):
        pass
    def check_runs(self, pile):
        pass
    def check_go(self, pile):
        pass
    def check_31(self, pile):
        pass
    def check_all(self, pile):
        pass
