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
FLAGS_COUNTER = (150,75)
COUNTER_COORDINATES = ((WINDOW_SIZE[0] - FLAGS_COUNTER[0]) - 40, 
                       (WINDOW_SIZE[1] - GRIGLIA_SIZE[1])/2 - FLAGS_COUNTER[1]/2)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

pygame.display.set_caption('Campo Minato')
# pygame.display.toggle_fullscreen()

blocca = False
riavvio = False
fine = False


pygame.init()
g = Griglia(screen, GRIGLIA_SIZE[0], GRIGLIA_SIZE[1], (0, (WINDOW_SIZE[1]-GRIGLIA_SIZE[1])))
g.draw()

pressed = False
opaco = False


def click_down(posx,posy,su_griglia,button):
    global blocca
            
    if su_griglia:
        if button == 3:
            posx -= g.offset[0]
            posy -= g.offset[1]
            col = (posx*g.ncol) // g.width
            rig = (posy*g.nrig) // g.height
            if g.celle[rig][col].coperto == True:
                g.celle[rig][col].segna(stato_tasti[2])
                if not g.celle[rig][col].segnato:
                    g.nbandiere +=1
                else:
                    g.nbandiere -= 1
            
        elif g.click(posx, posy):
            explsound = pygame.mixer.Sound("audio/explosionmusic.wav")
            explsound.play(0,0,0)
            musica.stop()
            blocca = True
        else:
            posx -= g.offset[0]
            posy -= g.offset[1]
            col = (posx*g.ncol) // g.width
            rig = (posy*g.nrig) // g.height
            if g.celle[rig][col].segnato == False:
                if g.celle[rig][col].val == "":
                    g.scopritutto(g.celle[rig][col], rig,col)
            else:
                g.celle[rig][col].scopri(g.celle,rig,col)

            # elif g.celle[rig][col].segnato == True:
            #     g.celle[rig][col].segnato = False
            #     g.nbandiere+=1
    else: #click sulla barra nera
        pass
            
#inizializzo pygame.mixer

pygame.mixer.pre_init(44100,-16,2,2048)
pygame.mixer.init(44100,-16,2,2048)
musica = pygame.mixer.Sound("audio/mainmusic.mp3")
musica.play(-1,0,0)

# zona tempo
fps = 60
clock = pygame.time.Clock()
tempo = clock.tick(fps)
font = pygame.font.SysFont(pygame.font.get_default_font(),int(WINDOW_SIZE[1]), bold = True, italic = False)
render_cronometro = font.render(str(tempo), True, (230, 120, 90), None)
render_cronometro = pygame.transform.scale(render_cronometro,(CRONOMETRE_SIZE[0],CRONOMETRE_SIZE[1]))
screen.blit(render_cronometro,
            ((CRONOMETRE_COORDINATES[0] + CRONOMETRE_SIZE[0]/2 - render_cronometro.get_width()/2),
            (CRONOMETRE_COORDINATES[1] + CRONOMETRE_SIZE[1]/2 - render_cronometro.get_height()/2)))

# tempo iniziale in cui il tasto restart rimane opaco, cioè = 0
timeropaco = 0
g.screen.fill((50, 125, 50))
while True:
    
    if g.bloccato:
        blocca = True
    
    if not blocca:
        #draw casella cronometro
        pygame.draw.rect(screen, (255, 255, 255), 
                        (CRONOMETRE_COORDINATES[0], 
                            CRONOMETRE_COORDINATES[1], 
                            CRONOMETRE_SIZE[0], CRONOMETRE_SIZE[1]))

        # stampo il tempo del cronometro
        img_cronometro = pygame.image.load('img/cronometro.png')
        img_cronometro = pygame.transform.scale( img_cronometro, (CRONOMETRE_SIZE[0]/2, CRONOMETRE_SIZE[1]))
        screen.blit(img_cronometro,
                    ((CRONOMETRE_COORDINATES[0]),
                    (CRONOMETRE_COORDINATES[1])))
        
        img_time = f'{int((tempo//1000)):2}'
        render_cronometro = font.render(img_time, True, (230, 80, 110), None)
        render_cronometro = pygame.transform.scale(render_cronometro,(CRONOMETRE_SIZE[0]/2,CRONOMETRE_SIZE[1]))
        screen.blit(render_cronometro,
                    ((CRONOMETRE_COORDINATES[0] + img_cronometro.get_size()[0] ),
                    (CRONOMETRE_COORDINATES[1])))
        
        #draw contatore bandiere
        pygame.draw.rect(screen,(255,255,255), (COUNTER_COORDINATES[0],COUNTER_COORDINATES[1],
                                                FLAGS_COUNTER[0], FLAGS_COUNTER[1]))
        bandiera = pygame.image.load("img/bandiera.png")
        bandiera = pygame.transform.scale(bandiera, (FLAGS_COUNTER[0]/2,FLAGS_COUNTER[0]/2))
        screen.blit(bandiera, (COUNTER_COORDINATES[0], COUNTER_COORDINATES[1]))
        img_bandiere_counter = f'{g.nbandiere}'
        img_bandiere_counter = font.render(img_bandiere_counter, True, (50, 120, 250), None)
        img_bandiere_counter = pygame.transform.scale(img_bandiere_counter,(FLAGS_COUNTER[0]/2, FLAGS_COUNTER[1]))
        screen.blit(img_bandiere_counter,
                    ((COUNTER_COORDINATES[0] + FLAGS_COUNTER[0]/2 ), 
                    COUNTER_COORDINATES[1]))
        
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    # pre-impostazione effetto pressione
    if event.type == pygame.MOUSEBUTTONDOWN and not pressed:
        pressed = True
        # if not blocca:
        #     posx, posy = pygame.mouse.get_pos()
            # print("mousebuttondown:", posx, posy)
            # click_down(posx, posy)
    
    # impostazione effetto pressione del restart 
    stato_tasti = pygame.mouse.get_pressed(3)
    if( stato_tasti[0] or stato_tasti[1] or stato_tasti[2]):
        posx, posy = pygame.mouse.get_pos()
        if (posx > WINDOW_SIZE[0]/2-RESTART_SIZE[0]/2 and posx < WINDOW_SIZE[0]/2+RESTART_SIZE[0]/2 and 
                posy >(WINDOW_SIZE[1] - GRIGLIA_SIZE[1])/2 - RESTART_SIZE[1]/2 and 
                posy < (WINDOW_SIZE[1] - GRIGLIA_SIZE[1])/2 + RESTART_SIZE[1]/2):
            button_sound = pygame.mixer.Sound("audio/click.wav")
            button_sound.play()
            musica = pygame.mixer.Sound("audio/mainmusic.mp3")
            musica.play(-1)
            opaco = True
            timeropaco = 11
    timeropaco -=1


            
    if event.type == pygame.MOUSEBUTTONUP and pressed:
        pressed = False

        if not blocca:
            if posy > WINDOW_SIZE[1]-GRIGLIA_SIZE[1]:
                click_down(posx, posy, True, event.button)
            else:
                click_down(posx, posy, False, event.button)

            # print("mousebuttonup:", posx, posy)
        else: # preparazione al riavvio
            posx, posy = pygame.mouse.get_pos()
            # print("Riavvio")
            if (posx > WINDOW_SIZE[0]/2-RESTART_SIZE[0]/2 and posx < WINDOW_SIZE[0]/2+RESTART_SIZE[0]/2 and 
                posy >(WINDOW_SIZE[1] - GRIGLIA_SIZE[1])/2 - RESTART_SIZE[1]/2 and 
                posy < (WINDOW_SIZE[1] - GRIGLIA_SIZE[1])/2 + RESTART_SIZE[1]/2):
                print("!")
                blocca = False
                riavvio = True

    # chiamo le draw per tutti gli elementi

    g.draw()

    #draw restart
    pygame.draw.rect(screen, (255, 255, 255),
                    (WINDOW_SIZE[0]/2 - RESTART_SIZE[0]/2, 
                     (WINDOW_SIZE[1]-GRIGLIA_SIZE[1])/2 - RESTART_SIZE[1]/2, 
                     RESTART_SIZE[0], RESTART_SIZE[1]))
    
    # draw della faccina sul tasto restart
    if not blocca or g.controllatavolo()[0] == g.nmine:
        if opaco or timeropaco >=0:
            faccina = pygame.image.load("img/faccina_felice_opaca.png")
            faccina = pygame.transform.scale(faccina, ((RESTART_SIZE[0]), (RESTART_SIZE[1])))
            g.screen.blit(faccina,
                        ((WINDOW_SIZE[0] - RESTART_SIZE[0])/2,
                        (WINDOW_SIZE[1] - GRIGLIA_SIZE[1])/2 - RESTART_SIZE[1]/2)) 
            opaco = False
            musica.stop()


        else:
            faccina = pygame.image.load("img/faccina_felice.png")
            faccina = pygame.transform.scale(faccina, ((RESTART_SIZE[0]), (RESTART_SIZE[1])))
            g.screen.blit(faccina,
                        ((WINDOW_SIZE[0] - RESTART_SIZE[0])/2,
                        (WINDOW_SIZE[1] - GRIGLIA_SIZE[1])/2 - RESTART_SIZE[1]/2)) 
    else:   
        if opaco or timeropaco >=0:
            faccina = pygame.image.load("img/faccina_triste_opaca.png")
            faccina = pygame.transform.scale(faccina, ((RESTART_SIZE[0]), (RESTART_SIZE[1])))
            screen.blit(faccina,
                        ((WINDOW_SIZE[0] - RESTART_SIZE[0])/2,
                        (WINDOW_SIZE[1] - GRIGLIA_SIZE[1])/2 - RESTART_SIZE[1]/2))
            opaco = False
        else:
            faccina = pygame.image.load("img/faccina_triste.png")
            faccina = pygame.transform.scale(faccina, ((RESTART_SIZE[0]), (RESTART_SIZE[1])))
            
            g.screen.blit(faccina,
                        ((WINDOW_SIZE[0] - RESTART_SIZE[0])/2,
                        (WINDOW_SIZE[1] - GRIGLIA_SIZE[1])/2 - RESTART_SIZE[1]/2))        
        
    pygame.display.flip()
    
    if riavvio: # riavvio vero e proprio
       
        tempo = 000
        g.reset()
        g.draw()
        riavvio = False
        opaco = False
        blocca = False
        clock = pygame.time.Clock()
        tempo = 0
        musica.play(-1,0,0)
    
    if not blocca:
        tempo += clock.tick(fps)