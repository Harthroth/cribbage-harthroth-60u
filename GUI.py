import pygame
from math import pi
import pygame.freetype
from pygame.locals import *
import Cribbage
from urllib.request import urlopen
import io
import requests

pygame.init()

# Setting up screen variables

display_width = 1280
display_height = 720
crashed = False
screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('cribbage-harthroth-60u')

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (62, 126, 94)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

clicking = False

# Loading and editing assets

try:
    GAME_FONT = pygame.freetype.Font('cribbage-harthroth-60u-main\Assets\COMIC.TTF', 24)
    back_card_img = pygame.image.load('cribbage-harthroth-60u-main\Assets\card_back.png')
    board_img = pygame.image.load('cribbage-harthroth-60u-main\Assets\cribbage_board.png')
    empty_img = pygame.image.load('cribbage-harthroth-60u-main\Assets\Empty.png')
except:
    GAME_FONT = pygame.freetype.Font('Assets\COMIC.TTF', 24)
    back_card_img = pygame.image.load('Assets\card_back.png')
    board_img = pygame.image.load('Assets\cribbage_board.png')
    empty_img = pygame.image.load('Assets\Empty.png')

back_card_img = pygame.transform.scale(back_card_img, (172, 232))
board_img = pygame.transform.scale(board_img, (250, 700))
empty_img = pygame.transform.scale(empty_img, (156, 156))

# Paints the default game screen
def round_winner(name):
    screen.fill(BLACK)
    win_text, x = GAME_FONT.render("Round Winner: "+ name + "!", WHITE)    
    screen.blit(win_text, (display_width/2.5, display_height/2 - 50))

def default_screen():
    screen.fill(GREEN)
    screen.blit(board_img, (1000, 0))
    
    deck_text, rect = GAME_FONT.render("Deck", WHITE)    
    screen.blit(deck_text, (70, 250))
    screen.blit(back_card_img, (10, 10))

    crib_text, rect = GAME_FONT.render("Crib", WHITE)    
    screen.blit(crib_text, (250, 250))
    screen.blit(back_card_img, (190, 10))

def upcard_deck(img):
    screen.blit(img, (10, 10))

def place_hand(image_array):
    x, y = 10, 470
    for img in image_array:
        try:
            screen.blit(img, (x, y))
            x+=100
        except:
            pass

def place_player_one(card_img):
    screen.blit(card_img, (550,170))

def place_player_two(card_img):
    screen.blit(card_img, (760,170))

def empty_crib():
    screen.blit(empty_img, (198,48))

def cut_deck(img):
    screen.blit(img, (10, 10))

def player_turn(player_number):
    if player_number == 1:
        pygame.draw.circle(screen, RED, (745, 40), 5)
    elif player_number == 2:
        pygame.draw.circle(screen, RED, (745, 70), 5)
    else:
        print("Error: player_turn receives", player_number)

def top_curved_arc(player, points):
    if points <= 40:
        if points == 36:
            x, y = 1070, 138
        elif points == 37:
            x, y = 1076, 122
        elif points == 38:
            x, y =  1086, 108
        elif points == 39:
            x, y = 1100, 99
        elif points == 40:
            x, y = 1116, 95
        else:    
            print("Error: " + points) 
    else:
        temp_width = 1.76*display_width
        if points == 45:
            x, y = temp_width-1070, 138
        elif points == 44:
            x, y = temp_width-1076, 122
        elif points == 43:
            x, y = temp_width-1086, 108
        elif points == 42:
            x, y = temp_width-1100, 99
        elif points == 41:
            x, y = temp_width-1116, 95
        else:
            print("Error: " + points)
    if player == 1:
        return x, y
    return (x*1.75)-846, (y*1.75)-110

def bottom_curved_arc(player, points):
    x, y = 0, 0
    if points == 85:
        x, y = 1106, 625
    elif points == 84:
        x, y = 1129, 652
    elif points == 83:
        x, y = 1164, 662
    elif points == 82:
        x, y = 1199, 652
    elif points == 81:
        x, y = 1222, 625
    else:
        print('Error', points)
    if player == 2:
        return (x*0.25)+875, (y*0.25) + 456
    return x, y

def board_scoring(player_number, points):
    y = 597
    if player_number == 1:
        x = 1024
        if points == 0:
            y = 625     
        elif points <= 35:
            temp = points - 1
            y -= temp * 13
        elif points <= 45:
            xy_tuple = top_curved_arc(1, points)
            x, y = xy_tuple[0], xy_tuple[1]
        elif points <= 80:
            x = 1226
            temp = 35 - (points - 50)
            y -= temp * 13
        elif points <= 85:
            xy_tuple = bottom_curved_arc(1, points)
            x, y = xy_tuple[0], xy_tuple[1]
        elif points <= 120:
            x = 1102
            temp = points - 86
            y -= temp * 13
        else:
            x, y = 1126, 130
        pygame.draw.circle(screen, WHITE, (x, y), 5)                    
    elif player_number == 2:
        x = 1069
        if points == 0:
            y = 625            
        elif points <= 35:
            temp = points - 1
            y -= temp * 13
        elif points <= 45:
            xy_tuple = top_curved_arc(2, points)
            x, y = xy_tuple[0], xy_tuple[1]
        elif points <= 80:
            x = 1183
            temp = 35 - (points - 50)
            y -= temp * 13
        elif points <= 85:
            xy_tuple = bottom_curved_arc(2, points)
            x, y = xy_tuple[0], xy_tuple[1]
        elif points <= 120:
            x = 1148
            temp = points - 86
            y -= temp * 13
        else:
            x, y = 1126, 130
        pygame.draw.circle(screen, WHITE, (x, y), 5)   
    else:
        pygame.draw.circle(screen, WHITE, (1024, 625), 5)
        pygame.draw.circle(screen, WHITE, (1024, 638), 5)

        pygame.draw.circle(screen, WHITE, (1069, 625), 5)
        pygame.draw.circle(screen, WHITE, (1069, 638), 5)

def update_text(player_number, points):
    # Player 1
    str_player = "Player " + str(player_number) + ": " + str(points)
    if player_number == 1:
        x, y = 760, 30
    elif player_number == 2:
        x, y = 760, 60
    else:
        pass
    player_text, rect = GAME_FONT.render(str_player, WHITE)    
    screen.blit(player_text, (x, y))

def update_sum(sum):
    str_sum = "Sum: " + str(sum)
    sum_text, rect = GAME_FONT.render(str_sum, WHITE)    
    screen.blit(sum_text, (550, 30))

# Default Game

image_array = [back_card_img, back_card_img, back_card_img, back_card_img, back_card_img, back_card_img]    
cf = Cribbage.Crib_Functions()
player_1 = Cribbage.Player("Player 1")
player_2 = Cribbage.Player("Player 2")

default_screen() 
board_scoring(0,0)
empty_crib()
player_turn(1)
update_text(1, player_1.get_score())
update_text(2, player_2.get_score())
update_sum(0)
place_hand(image_array)
player_1_cards, player_2_cards = cf.deal_cards(player_1.get_name(), player_2.get_name())

count = 0

def get_player_images(player_number):
    image_array = []
    value_array = []
    if player_number == 1:
        cards = cf.get_pile_list(player_1.get_name())
        card_list = cards["piles"][player_1.get_name()]["cards"]
    else:
        cards = cf.get_pile_list(player_2.get_name())
        card_list = cards["piles"][player_2.get_name()]["cards"]


    for val in card_list:
        number = str(val['value'])
        url = str(val['images']['png'])
        r = requests.get(url)
        image_file = io.BytesIO(r.content)
        image_hand = pygame.image.load(image_file)
        image_hand = pygame.transform.scale(image_hand, (172, 232))
        image_array.append(image_hand)
        try: 
            value_array.append(int(number))
        except:
            value_array.append(10)
    return image_array, value_array


first = second = third = fourth = fifth = sixth = crib_use =  True
array_one, one_val = get_player_images(1)
array_two, two_val = get_player_images(2)


current_player = 0
crib_img = []
total_sum = 0

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            loc = [mx, my]
            default_screen()
            board_scoring(1, player_1.get_score())
            board_scoring(2, player_2.get_score())
            place_hand(array_one)
            update_text(1, player_1.get_score())
            update_text(2, player_2.get_score())
            print(player_1.get_score())
            # board_scoring(1, player_1.get_score())
            # board_scoring(2, player_2.get_score())
            if current_player == 0:
                player_turn(1)
                empty_crib() 
                cut_deck(array_one[2])
                current_player+=1
            elif current_player > 0 and total_sum <= 31:
                if my > 475 and my < 702 and first:
                    if  mx > 14 and mx < 114:
                        number = 0
                    elif mx > 114 and mx < 214 and second:
                        number = 1
                    elif mx > 214 and mx < 310 and third:
                        number = 2
                    elif mx > 310 and mx < 410 and fourth:
                        number = 3
                    elif mx > 410 and mx < 508 and fifth:
                        number = 4
                    elif mx > 508 and mx < 680 and sixth:
                        number = 5
                    # crib play
                    if current_player <= 4:
                        empty_crib() 
                        if current_player >= 2:
                            place_player_two(back_card_img)
                            place_player_one(back_card_img)
                        if current_player % 2 == 0:
                            player_turn(2)
                            crib_img.append(array_two[number])
                            array_two[number] = ''
                            array_two.remove('')
                        else:
                            player_turn(1)
                            crib_img.append(array_one[number])
                            place_player_one(back_card_img)
                            array_one[number] = ''
                            array_one.remove('')
                    else:
                        if current_player % 2 == 0:
                            player_turn(2)
                            place_player_two(array_two[number])
                            array_two[number] = ''
                            array_two.remove('')
                            player_2.increase_score(player_2.get_score() + int((two_val[number]/3)))
                            total_sum+=two_val[number]
                            try:
                                two_val.remove(number)
                            except:
                                pass
                        else:
                            player_turn(1)
                            place_player_one(array_one[number])
                            array_one[number] = ''
                            array_one.remove('')
                            player_1.increase_score(player_1.get_score() + int((one_val[number]/3)))
                            total_sum+=one_val[number]
                            try:
                                one_val.remove(number)
                            except:
                                pass
                    update_sum(total_sum)
                    current_player+=1
            else:
                if player_1.get_score() > player_2.get_score():
                    round_winner("Player 1")
                elif player_1.get_score() < player_2.get_score():
                    round_winner("Player 2")
                else:
                    round_winner("Player 1 & 2")
    pygame.display.update()



pygame.quit()
quit()
