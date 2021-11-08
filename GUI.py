import pygame


pygame.init()


display_width = 1280
display_height = 720

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Cribbage')

black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()
crashed = False
back_card_img = pygame.image.load('Images\card_back.png')
back_card_img = pygame.transform.scale(back_card_img, (172, 232))

def back_card(x,y):
    gameDisplay.blit(back_card_img, (x,y))

x = 10
y = 10

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.fill(white)
    back_card(x,y)
    back_card(x,y+450)
    back_card(x+100,y+450)
    back_card(x+200,y+450)
    back_card(x+300,y+450)
    back_card(x+400,y+450)
    back_card(x+500,y+450)
    pygame.draw.rect(gameDisplay,black,(x+700,0,display_width,display_height))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()