import requests 
import json

def pile_value_change(pile):
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

class Player:
    score = 0
    name = ""
    def __init__(self, n) -> None:
        self.name = n.replace(' ', '_')
        self.score = 0

    def increase_score(self, new_score):
        self.score += new_score
    
    def reset_score(self):
        self.score = 0

    def get_score(self):
        return self.score
    
    def get_name(self):
        return self.name


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
        response = requests.get("https://deckofcardsapi.com/api/deck/"+self.get_deck_ID()+"/draw/?count=12")
        card_list = []
        card1 = ''
        card2 = ''
        for x in response.json()['cards']:
            card_list.append(x['code'])
        for x in range(0,12):
            if x < 6:
                card1+=str(card_list[x])+','
            else: 
                card2+=str(card_list[x])+','
        response1 = requests.get("https://deckofcardsapi.com/api/deck/"+deck_ID+"/pile/"+player1name+"/add/?cards="+str(card1))
        response2 = requests.get("https://deckofcardsapi.com/api/deck/"+deck_ID+"/pile/"+player2name+"/add/?cards="+str(card2))
        return response1.json(), response2.json()

# Creates the crib pile out of 4 cards contributed by the players
    def make_crib(self, list_of_cards):
        response = requests.get("https://deckofcardsapi.com/api/deck/"+self.get_deck_ID()+"/pile/crib/add/?cards="+list_of_cards)
        return response.json()
    
# Draws a card from a specific pile
    def draw_card_from_pile(self, pile_name):
        response = requests.get("https://deckofcardsapi.com/api/deck/"+self.get_deck_ID()+"/pile/"+pile_name+"/draw/?count=1")
        return response.json()

# Draws a specific card from a specific pile
    def draw_specific_card_from_pile(self, pile_name, card_name):
        response = requests.get("https://deckofcardsapi.com/api/deck/"+self.get_deck_ID()+"/pile/"+pile_name+"/draw/?cards="+card_name)
        return response.json()

# Draws a card from the deck (for top card or turn determination at beginning)
    def draw_card_from_deck(self):
        response = requests.get("https://deckofcardsapi.com/api/deck/"+self.get_deck_ID()+"/draw/?count=1")
        return response.json()

# For round play, placing cards in play pile - pile_nameplay
    def add_card_to_play_piles(self, pile_name, card_name):
        response = requests.get("https://deckofcardsapi.com/api/deck/"+deck_ID+"/pile/"+pile_name+"play/add/?cards="+card_name)
        return response.json()

# End of play, put cards in new deck - pile_namescore
    def add_cards_to_score_pile(self, pile_name):
        response1 = requests.get("https://deckofcardsapi.com/api/deck/"+deck_ID+"/pile/"+pile_name+"play/list")
        x = response1.json()
        card_list = ""
        for cards in x["piles"][pile_name+'play']["cards"]:
            card_list += cards["code"]+","
        card_list = card_list[:len(card_list)-1]
        response2 = requests.get("https://deckofcardsapi.com/api/deck/"+deck_ID+"/pile/"+pile_name+"score/add/?cards="+card_list)
        return response2.json()
    
    def get_pile_list(self, pile_name):
        response = requests.get("https://deckofcardsapi.com/api/deck/"+self.get_deck_ID()+"/pile/"+pile_name+"/list/")
        return response.json()

    def get_sum_of_cards(self, pile_name):
        cards = self.get_pile_list(pile_name)
        card_list = cards["piles"][pile_name]["cards"]
        fixed_card_list = pile_value_change(card_list)
        sum = 0
        for x in fixed_card_list:
            sum += int(x["value"])
        return sum

    def reset_deck(self):
        global deck_ID
        response = requests.get("https://deckofcardsapi.com/api/deck/"+deck_ID+"/return/")
        return response.json()

class final_scoring:

    global already_paired
    """
    lists are in order of the methods here
    0 - matching
    1 - fifteen
    2 - flush
    3 - runs
    4 - nobs
    """
    already_paired = [[],[],[],[],[]]
    def check_matching(self, pile):
        global already_paired
        total_cards = 0
        length = len(pile)
        if length > 2:
            for x in range(length-1, 0):
                if pile[x]['value'] == pile[x-1]['value']:
                    total_cards += 1
                elif total_cards == 4:
                    break
                else:
                    break
        if total_cards == 2:
            if [pile[length-1]['code'], pile[length-2]['code']].sort() in already_paired[0]:
                return -1
            else:
                already_paired[0].append([pile[length-1]['code'], pile[length-2]['code']].sort())
                return 2
        elif total_cards == 3:
            if [pile[length-1]['code'], pile[length-2]['code'], pile[length-3]['code']].sort() in already_paired[0]:
                return -1
            else:
                already_paired[0].append([pile[length-1]['code'], pile[length-2]['code'], pile[length-3]['code']].sort())
                return 6
        elif total_cards == 4:
            if [pile[length-1]['code'], pile[length-2]['code'], pile[length-3]['code'], pile[length-4]['code']].sort() in already_paired[0]:
                return -1
            else:
                already_paired[0].append([pile[length-1]['code'], pile[length-2]['code'], pile[length-3]['code'], pile[length-4]['code']].sort())
                return 12
        else:
            return 0

    def check_fifteen(self, pile):
        global already_paired
        total = 0
        pile_switched = pile_value_change(pile)
        card_list = []
        for x in pile_switched:
            total += int(x['value'])
            card_list.append(x['code'])
        card_list.sort()
        if total == 15:
            if card_list in already_paired[1]:
                return -1
            else:
                already_paired[1].append(card_list)
                return 2
        else:
            return 0

    def check_flush(self, pile):
        global already_paired
        total = 0
        if len(pile) == 4:
            if pile[0]['suit'] == pile[1]['suit'] == pile[2]['suit'] == pile[3]['suit']:
                if [pile[0]['code'], pile[1]['code'], pile[2]['code'], pile[3]['code']].sort() in already_paired[2]:
                    return -1
                already_paired[2].append([pile[0]['code'], pile[1]['code'], pile[2]['code'], pile[3]['code']].sort())
                total+=4
        elif len(pile) == 5:
            if pile[0]['suit'] == pile[1]['suit'] == pile[2]['suit'] == pile[3]['suit'] == pile[4]['suit']:
                if [pile[0]['code'], pile[1]['code'], pile[2]['code'], pile[3]['code'], pile[4]['code']].sort() in already_paired[2]:
                    return -1
                already_paired[2].append([pile[0]['code'], pile[1]['code'], pile[2]['code'], pile[3]['code'], pile[4]['code']].sort())
                total += 5
        return total
            

    def check_runs(self, pile):
        global already_paired
        pile_switched = pile_value_change(pile)
        pile_list = []
        for x in pile_switched:
            pile_list.insert(int(x['value']))
        pile_list.sort()
        total = 0
        card_list = []
        for x in range(0,len(pile_list)-1):
            if pile_list[x] + 1 == pile_list[x+1]:
                total+=1
                card_list.append(pile_switched[x]['code'])
        card_list.sort()
        if total > 2:
            if card_list in already_paired[3]:
                return -1
            already_paired[3].append(card_list)
            return total
        else:
            return 0

    # make sure to require flipped card in input to this.
    def check_nobs(self, pile):
        global already_paired
        if len(pile) == 2:
            if pile[0]['suit'] == pile[1]['suit'] and (pile[0]['value'] == 'JACK' or pile[1]['value'] == 'JACK'):
                if [pile[0]['code'], pile[1]['code']].sort() in already_paired[4]:
                    return -1
                already_paired.append([pile[0]['code'], pile[1]['code']].sort())
                return 2

    def check_all(self, pile):
        fifteen = self.check_fifteen(pile)
        flush = self.check_flush(pile)
        matching = self.check_matching(pile)
        runs = self.check_runs(pile)
        return fifteen, flush, matching, runs

class play_scoring:
    def check_fifteen(self, pile):
        length = len(pile)
        pile_switched = self.pile_value_change(pile)
        if length > 2:
            if int(pile_switched[length-1]['value']) + int(pile_switched[length-2]['value']) == 15:
                return 2

    def check_matching(self, pile):
        total_cards = 0
        length = len(pile)
        if length > 2:
            for x in range(length-1, 0):
                if pile[x]['value'] == pile[x-1]['value']:
                    total_cards += 1
                elif total_cards == 4:
                    break
                else:
                    break
        if total_cards == 2:
            return 2
        elif total_cards == 3:
            return 6
        elif total_cards == 4:
            return 12
        else:
            return 0

    def check_runs(self, pile):
        pile_switched = pile_value_change(pile)
        if len(pile_switched) >= 5:
            pile_list = []
            for x in range(len(pile_switched)-1, len(pile_switched)-6):
                pile_list.insert(int(pile_switched['value']))
            pile_list.sort()
            if pile_list[0] == pile_list[1] - 1 == pile_list[2] - 2 == pile_list[3] - 3 == pile_list[4] - 4:
                return 5
        if len(pile_switched) >= 4:
            pile_list = []
            for x in range(len(pile_switched)-1, len(pile_switched)-5):
                pile_list.insert(int(pile_switched['value']))
            pile_list.sort()
            if pile_list[0] == pile_list[1] - 1 == pile_list[2] - 2 == pile_list[3] - 3:
                return 4
        if len(pile_switched) >= 3:
            pile_list = []
            for x in range(len(pile_switched)-1, len(pile_switched)-6):
                pile_list.insert(int(pile_switched['value']))
            pile_list.sort()
            if pile_list[0] == pile_list[1] - 1 == pile_list[2] - 2:
                return 3
        return 0 

    def check_31(self, pile):
        pile_switched = pile_value_change(pile)
        total = 0
        for x in pile_switched:
            total += int(pile_switched['value'])
        if total == 31:
            return 2
        else:
            return 0
            
    def check_all(self, pile):
        fifteen = self.check_fifteen(pile)
        matching = self.check_matching(pile)
        runs = self.check_runs(pile)
        thirtyone = self.check_31(pile)
        return fifteen, matching, runs, thirtyone

