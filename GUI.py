import pygame
from math import pi
import pygame.freetype  # Import the freetype module.

pygame.init()

display_width = 1280
display_height = 720

screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Cribbage')

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (62, 126, 94)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
TEST_COLOR = (199,36,177)

crashed = False

GAME_FONT = pygame.freetype.Font('Assets\COMIC.TTF', 24)

back_card_img = pygame.image.load('Assets\card_back.png')
back_card_img = pygame.transform.scale(back_card_img, (172, 232))
board_img = pygame.image.load('Assets\cribbage_board.png')
board_img = pygame.transform.scale(board_img, (250, 700))

def default_screen():
    screen.fill(GREEN)
    screen.blit(board_img, (1000, 0))
    # Some misc text
    deck_text, rect = GAME_FONT.render("Deck", BLACK)    
    screen.blit(deck_text, (55, 250))
    crib_text, rect = GAME_FONT.render("Crib", BLACK)    
    screen.blit(crib_text, (250, 250))
    
def back_card(x,y):
    screen.blit(back_card_img, (x,y))

x = 10
y = 10

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    default_screen()
    back_card(x,y)
    back_card(x,y+470)
    back_card(x+100,y+470)
    back_card(x+200,y+470)
    back_card(x+300,y+470)
    back_card(x+400,y+470)
    back_card(x+500,y+470)
    

    back_card(x+180,y)

    text_surface3, rect = GAME_FONT.render("Sum: 420", WHITE)    
    screen.blit(text_surface3, (650, 30))

    #placed down stack
    back_card(x+600,y+220)
    back_card(x+780,y+220)



    # Player 1
    text_surface, rect = GAME_FONT.render("Player 1 (20)", BLUE)    
    screen.blit(text_surface, (800, 30))
    pygame.draw.circle(screen, WHITE, (1024, 625), 5)
    pygame.draw.circle(screen, WHITE, (1024, 638), 5)

    # Player 2
    text_surface2, rect2 = GAME_FONT.render("Player 2 (60)", RED)
    screen.blit(text_surface2, (800, 60))
    pygame.draw.circle(screen, WHITE, (1069, 625), 5)
    pygame.draw.circle(screen, WHITE, (1069, 638), 5)

    pygame.display.update()

pygame.quit()
quit()
