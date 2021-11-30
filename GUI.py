import pygame
from math import pi
import pygame.freetype
from pygame.locals import *
import Cribbage

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

GAME_FONT = pygame.freetype.Font('Assets\COMIC.TTF', 24)
back_card_img = pygame.image.load('Assets\card_back.png')
back_card_img = pygame.transform.scale(back_card_img, (172, 232))
board_img = pygame.image.load('Assets\cribbage_board.png')
board_img = pygame.transform.scale(board_img, (250, 700))
empty_img = pygame.image.load('Assets\Empty.png')
empty_img = pygame.transform.scale(empty_img, (156, 156))

# Paints the default game screen

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
        screen.blit(img, (x, y))
        x+=100

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
current_player = -1
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
cards = cf.get_pile_list(player_1.get_name())
card_list = cards["piles"][player_1.get_name()]["cards"]
print(card_list)
first = second = third = fourth = fifth = sixth = crib_use =  True
print(player_1_cards)

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == MOUSEBUTTONDOWN:
            if event.type == MOUSEBUTTONDOWN: 
                mx, my = pygame.mouse.get_pos()
                loc = [mx, my]
                if event.button == 1: 
                    clicking == True 
                    print(loc) 
                    if mx > 10 and mx < 175 and my > 10 and my < 240:
                        pygame.draw.circle(screen, RED, (100, 250), 20)
                        # flip deck
                        # upcard_deck(img)
                        # update scoring
                    elif my > 475 and my < 702:
                        if  mx > 14 and mx < 114:

                            print("First card")
                        elif mx > 114 and mx < 214:
                            print("second card")
                        elif mx > 214 and mx < 310:
                            print("third card")
                        elif mx > 310 and mx < 410:
                            print("fourth card")
                        elif mx > 410 and mx < 508:
                            print("fifth card")
                        elif mx > 508 and mx < 680:
                            print("sixth card")
                        else:
                            pass
                else: 
                    pass 
        if current_player == 1:
            place_hand(player_1_cards)
        elif current_player == 2:
            place_hand(player_2_cards)
        elif current_player == 3:
            current_player = 0
        current_player += 1
    pygame.display.update()



pygame.quit()
quit()
