import pygame
from math import pi
import pygame.freetype  # Import the freetype module.

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

    sum_text, rect = GAME_FONT.render("Sum: ", WHITE)    
    screen.blit(sum_text, (550, 30))

    # Player 1
    player_1_text, rect = GAME_FONT.render("Player 1:", WHITE)    
    screen.blit(player_1_text, (760, 30))

    # Player 2
    player2_text, rect2 = GAME_FONT.render("Player 2:", WHITE)
    screen.blit(player2_text, (760, 60))

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
        print("player_turn receives", player_number)

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

     #  Testing

    default_screen() 
    image_array = [back_card_img, back_card_img, back_card_img, back_card_img, back_card_img, back_card_img]
    place_hand(image_array)
    place_player_one(back_card_img)
    place_player_two(back_card_img)
    empty_crib()
    player_turn(1)
    player_turn(2)

    '''
    Player 1
    pygame.draw.circle(screen, WHITE, (1024, 625), 5)
    pygame.draw.circle(screen, WHITE, (1024, 638), 5)

    Player 2
    pygame.draw.circle(screen, WHITE, (1069, 625), 5)
    pygame.draw.circle(screen, WHITE, (1069, 638), 5)
    '''
    pygame.display.update()

pygame.quit()
quit()
