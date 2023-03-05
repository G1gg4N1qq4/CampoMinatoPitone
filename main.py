from tkinter.tix import WINDOW
from tavolo import Griglia

from os import system
system("cls")

import pygame
from pygame.locals import *

#impostazioni finestra
WINDOW_SIZE = (600, 750)
GRIGLIA_SIZE = (600, 600)
RESTART_SIZE = (75, 75)
CRONOMETRE_SIZE = (150,75)
CRONOMETRE_COORDINATES = ((WINDOW_SIZE[0] - RESTART_SIZE[0])/2 - 80 - CRONOMETRE_SIZE[0],
                          (WINDOW_SIZE[1] - GRIGLIA_SIZE[1])/2 - CRONOMETRE_SIZE[1]/2)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

pygame.display.set_caption('Campo Minato')

clock = pygame.time.Clock()
fps = 120

img_time = " 0"

blocca = False

riavvio = False

fine = False

tempo = 000

pygame.init()
font = pygame.font.SysFont(pygame.font.get_default_font(),int(WINDOW_SIZE[1]), bold = True, italic = False)
render_cronometro = font.render(str(tempo), True, (230, 120, 90), None)
render_cronometro = pygame.transform.scale(render_cronometro,(CRONOMETRE_SIZE[0],CRONOMETRE_SIZE[1]))
screen.blit(render_cronometro,
            ((CRONOMETRE_COORDINATES[0] + CRONOMETRE_SIZE[0]/2 - render_cronometro.get_width()/2),
            (CRONOMETRE_COORDINATES[1] + CRONOMETRE_SIZE[1]/2 - render_cronometro.get_height()/2)))
g = Griglia(screen, GRIGLIA_SIZE[0], GRIGLIA_SIZE[1], (0, (WINDOW_SIZE[1]-GRIGLIA_SIZE[1])))
g.draw()

#inizializzo pygame.mixer
pygame.mixer.pre_init(44100,-16,2,512)
pygame.mixer.init(44100,-16,2,512,)

# musica = pygame.mixer_music.load("mainmusic.mp3",)
musica = pygame.mixer.Sound("mainmusic.mp3")
pressed = False

def click_down(posx,posy,su_griglia):
    global blocca
    if su_griglia:
        
        if g.click(posx, posy):
            explsound = pygame.mixer.Sound("explosionmusic.wav")
            explsound.play(0,0,0)
            musica.stop()
            blocca = True
        else:
            posx -= g.offset[0]
            posy -= g.offset[1]
            col = (posx*g.ncol) // g.width
            rig = (posy*g.nrig) // g.height
            if g.celle[rig][col].val == "":
                g.scopritutto(g.celle[rig][col], rig,col)
            g.draw()
    else: #click sulla barra nera
        pass
            

musica.play(-1,0,0)
while True:
        
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    if event.type == pygame.MOUSEBUTTONDOWN and not pressed:
        pressed = True
        if not blocca:
            posx, posy = pygame.mouse.get_pos()
            # print("mousebuttondown:", posx, posy)
            # click_down(posx, posy)

    if event.type == pygame.MOUSEBUTTONUP and pressed:
        pressed = False

        posx, posy = pygame.mouse.get_pos()
        if not blocca:
            if posy > WINDOW_SIZE[1]-GRIGLIA_SIZE[1]:
                click_down(posx, posy, True)
            else:
                click_down(posx, posy, False)

            # print("mousebuttonup:", posx, posy)
        else: # preparazione al riavvio
            # print("Riavvio")
            if (posx > WINDOW_SIZE[0]/2-RESTART_SIZE[0]/2 and posx < WINDOW_SIZE[0]/2+RESTART_SIZE[0]/2 and 
                posy >(WINDOW_SIZE[1] - GRIGLIA_SIZE[1])/2 - RESTART_SIZE[1]/2 and 
                posy < (WINDOW_SIZE[1] - GRIGLIA_SIZE[1])/2 + RESTART_SIZE[1]/2):
                blocca = False
                riavvio = True
    # if t.vincitore != None:
    #     fine = True
    #     if t.vincitore == Tavolo.v:
    #         print('Partita finita in pareggio')
    #     else:
    #         print(f'Vince il giocatore {t.vincitore}')

    # chiamo le draw per tutti gli elementi
    g.draw()

    #draw restart
    pygame.draw.rect(screen, (255, 255, 255),
                    (WINDOW_SIZE[0]/2 - RESTART_SIZE[0]/2, 
                     (WINDOW_SIZE[1]-GRIGLIA_SIZE[1])/2 - RESTART_SIZE[1]/2, 
                     RESTART_SIZE[0], RESTART_SIZE[1]))
    
    #draw casella cronometro
    pygame.draw.rect(screen, (255, 255, 255), 
                    (CRONOMETRE_COORDINATES[0], 
                        CRONOMETRE_COORDINATES[1], 
                        CRONOMETRE_SIZE[0], CRONOMETRE_SIZE[1]))
    #stampo solo ad 1/60 delle volte in cui entra
    if tempo%120 == 0:
        img_time = f'{int(tempo/120):2}'
    render_cronometro = font.render(img_time, True, (230, 80, 110), None)
    render_cronometro = pygame.transform.scale(render_cronometro,(CRONOMETRE_SIZE[1],CRONOMETRE_SIZE[1]))
    screen.blit(render_cronometro,
                ((CRONOMETRE_COORDINATES[0] + CRONOMETRE_SIZE[0]/2 - render_cronometro.get_width()/2),
                (CRONOMETRE_COORDINATES[1] + CRONOMETRE_SIZE[1]/2 - render_cronometro.get_height()/2)))

    # draw della faccina sul tasto restart
    if not g.bloccato:
        faccina = pygame.image.load("faccina_felice.png")
        faccina = pygame.transform.scale(faccina, ((RESTART_SIZE[0]), (RESTART_SIZE[1])))
        g.screen.blit(faccina,
                      ((WINDOW_SIZE[0] - RESTART_SIZE[0])/2,
                       (WINDOW_SIZE[1] - GRIGLIA_SIZE[1])/2 - RESTART_SIZE[1]/2)) 
    else:
        faccina = pygame.image.load("faccina_triste.png")
        faccina = pygame.transform.scale(faccina, (RESTART_SIZE[0], RESTART_SIZE[1]))
        
        g.screen.blit(faccina,
                      ((WINDOW_SIZE[0] - RESTART_SIZE[0])/2,
                               (WINDOW_SIZE[1] - GRIGLIA_SIZE[1])/2 - RESTART_SIZE[1]/2))
        
    if riavvio: # riavvio vero e proprio
       
        tempo = 000
        g = Griglia(screen, GRIGLIA_SIZE[0], GRIGLIA_SIZE[1], (0, (WINDOW_SIZE[1]-GRIGLIA_SIZE[1])))
        g.draw()
        print("Riavvio")
        riavvio = False
        musica.play()
        
    pygame.display.flip()
    
    tempo +=1
    clock.tick(fps)