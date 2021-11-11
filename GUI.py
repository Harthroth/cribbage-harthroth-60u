import pygame
from math import pi
import pygame.freetype

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
TEST_COLOR = (199,36,177)

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
    multiplier = 1
    if player == 1:
        multiplier = 0.75
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
    return x, y

def board_scoring(player_number, points):
    y = 597
    if player_number == 1:
        x = 1024
        if points == 0:
            pygame.draw.circle(screen, WHITE, (1024, 638), 5)          
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
            print("ill do this one later")
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
            pygame.draw.circle(screen, WHITE, (1024, 638), 5)            
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
            print("ill do this one later")
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

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

     #  Testing
    
    image_array = [back_card_img, back_card_img, back_card_img, back_card_img, back_card_img, back_card_img]
    
    default_screen() 

    board_scoring(1, 45)
    board_scoring(1, 44)
    board_scoring(1, 43)
    board_scoring(1, 42)
    board_scoring(1, 41)
    board_scoring(1, 40)
    board_scoring(1, 39)
    board_scoring(1, 38)
    # + 6, - 16
    # + 10, -14
    # + 14, -9
    '''
    sum_text, rect = GAME_FONT.render("Sum: ", WHITE)    
    screen.blit(sum_text, (550, 30))

    # Player 1
    player_1_text, rect = GAME_FONT.render("Player 1:", WHITE)    
    screen.blit(player_1_text, (760, 30))

    # Player 2
    player2_text, rect2 = GAME_FONT.render("Player 2:", WHITE)
    screen.blit(player2_text, (760, 60))

    place_hand(image_array)
    place_player_one(back_card_img)
    place_player_two(back_card_img)
    empty_crib()
    player_turn(1)
    player_turn(2)
    board_scoring(0,0)
    '''
    pygame.display.update()

pygame.quit()
quit()
