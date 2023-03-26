import pygame
import random

mina = 'm'
vuoto = ''

class Cella:
    def __init__(self, screen, width, height, posx, posy ,val='') -> None:
        self.screen = screen
        self.width = width
        self.height = height
        self.posx = posx
        self.posy = posy
        self.val = val
        # self.val_nodo = val_nodo
        # if arch == None:
        #     self.archi = []
        
        self.coperto = True

        self.segnato = False
            
        self.esplosa = False

        self.img_mina = pygame.image.load("img/Mina.png")
        self.img_mina = pygame.transform.scale(self.img_mina, (width, height))


        self.font = pygame.font.SysFont(pygame.font.get_default_font(), int(self.height), bold = True, italic = False)

    def scopri(self,celle,rig,col):
        if self.segnato:
            return False


        if self.val == mina:
            self.esplosa = True
            self.coperto = False

            return True
        elif not self.coperto:
                
            nsegnati = 0
            for i in range(-1, 2):
                for j in range(-1,2):
                    if (rig+i >= 0 and rig+i <10) and (col+j >= 0 and col+j <10):
                        if celle[rig+i][col+j].segnato == True:
                            nsegnati += 1
            # print(nsegnati, self.val)
            if self.val == vuoto:
                pass
            elif nsegnati == int(self.val):
                # print("!")
                for i in range(-1, 2):
                    for j in range(-1,2):
                        if (rig+i >= 0 and rig+i <10) and (col+j >= 0 and col+j <10):
                            if not celle[rig+i][col+j].segnato:
                                if celle[rig+i][col+j].val == mina:
                                    celle[rig+i][col+j].coperto = False
                                    celle[rig+i][col+j].esplosa = True
                                    
                                    return True
                                celle[rig+i][col+j].coperto = False
        self.coperto = False
            

    def segna(self,rightclick):
        if rightclick:
            return True
        self.segnato = not self.segnato
        
        

    def draw(self) -> None:

        if self.coperto:
            pygame.draw.rect(self.screen, (100, 250, 100),
                            (self.posx, self.posy, self.width, self.height))
            if self.segnato:
                
                self.bandiera = pygame.image.load("img/bandiera.png")
                self.bandiera = pygame.transform.scale(self.bandiera, (self.width,self.height))
                self.screen.blit(self.bandiera, (self.posx, self.posy))
        else:
            pygame.draw.rect(self.screen, (50, 125, 50),
                            (self.posx, self.posy, self.width, self.height))

        pygame.draw.rect(self.screen, (10, 100, 10),
                         (self.posx, self.posy, self.width, self.height), 2)
        # print(self.posx, self.posy)
        if self.val == vuoto or self.coperto:
            return
        elif self.val == mina:
            self.screen.blit(self.img_mina, (self.posx, self.posy))
            

            if self.esplosa:  
                self.img_exp = pygame.image.load("img/Exp.png")
                self.img_exp = pygame.transform.scale(self.img_exp, (self.width, self.height))
                self.screen.blit(self.img_exp, (self.posx, self.posy))
                      
        else:
            self.renderNumero = self.font.render(self.val, True, (230, 230, 230), None)
            x = self.posx + self.width / 2 - self.renderNumero.get_width() / 2
            y = self.posy + self.height / 2 - self.renderNumero.get_height() / 2
            self.screen.blit(self.renderNumero, (x, y))

        
        
class Griglia:
    def __init__(self, screen, width, height, offset, nrig=10, ncol=10, nmine=16) -> None:
        self.screen = screen
        self.width = width
        self.height = height
        self.offset = offset
        self.nrig = nrig
        self.ncol = ncol
        self.nmine = nmine
        self.nbandiere = nmine
        self.bloccato = False
        self.sconfitta = False
        self.celle = None
        # self.celle = []
        # for i in range(nrig):
        #     riga = []
        #     for j in range(ncol):
        #         x = i * (width / ncol)
        #         y = j * (height / nrig)
        #         cella = Cella(screen, width/ncol, height/nrig, x, y)
        #         riga.append(cella)
        
        #creo celle vuote
        self.celle = [[Cella(self.screen, self.width/self.ncol, self.height/self.nrig, j * (self.width/self.ncol) + self.offset[0], i * (self.height/self.nrig) + self.offset[1]) for j in range(self.ncol)] for i in range(self.nrig)]
        # for riga in self.celle:
        #     for cella in riga:
        #         for valx in range(-1, +2):
        #             for valy in range(-1, +2):
        #                 if (cella.val_nodo[0]+valx >= 0 and cella.val_nodo[0]+valx <= 10) and (cella.val_nodo[1]+valy >= 0 and cella.val_nodo[1]+valy <= 0):
        #                     cella.archi.append((cella.val_nodo[0]+valx,cella.val_nodo[1] + valy))

        # metto le mine nella griglia
        for _ in range(nmine):
            i = random.randint(0, self.nrig-1)
            j = random.randint(0, self.ncol-1)

            while self.celle[i][j].val == mina:
                i = random.randint(0, self.nrig-1)
                j = random.randint(0, self.ncol-1)
            
            self.celle[i][j].val = mina
        
        print(len(self.celle), len(self.celle[0]))

        # metto i numerini intorno alle mine
        for i in range(self.nrig):
            for j in range(self.ncol):
                if self.celle[i][j].val == vuoto:
                    nmine = 0

                    for iad in range(-1, 2):
                        for jad in range(-1, 2):
                            if (iad, jad) != (0, 0) and i+iad >= 0 and i+iad < self.nrig and j+jad >= 0 and j+jad < self.ncol:
                                
                                if self.celle[i+iad][j+jad].val == mina:
                                    nmine += 1

                    if nmine != 0:
                        self.celle[i][j].val = str(nmine)

    def crea_celle(self):
        # creo le celle vuote
        self.celle = [[Cella(self.screen, self.width/self.ncol, self.height/self.nrig, j * (self.width/self.ncol) + self.offset[0], i * (self.height/self.nrig) + self.offset[1]) for j in range(self.ncol)] for i in range(self.nrig)]
        # for riga in self.celle:
        #     for cella in riga:
        #         for valx in range(-1, +2):
        #             for valy in range(-1, +2):
        #                 if (cella.val_nodo[0]+valx >= 0 and cella.val_nodo[0]+valx <= 10) and (cella.val_nodo[1]+valy >= 0 and cella.val_nodo[1]+valy <= 0):
        #                     cella.archi.append((cella.val_nodo[0]+valx,cella.val_nodo[1] + valy))

        # metto le mine nella griglia
        for _ in range(self.nmine):
            i = random.randint(0, self.nrig-1)
            j = random.randint(0, self.ncol-1)

            while self.celle[i][j].val == mina:
                i = random.randint(0, self.nrig-1)
                j = random.randint(0, self.ncol-1)
            
            self.celle[i][j].val = mina
        
        # print(len(self.celle), len(self.celle[0]))

        # metto i numerini intorno alle mine
        for i in range(self.nrig):
            for j in range(self.ncol):
                if self.celle[i][j].val == vuoto:
                    nmine = 0

                    for iad in range(-1, 2):
                        for jad in range(-1, 2):
                            if (iad, jad) != (0, 0) and i+iad >= 0 and i+iad < self.nrig and j+jad >= 0 and j+jad < self.ncol:
                                
                                if self.celle[i+iad][j+jad].val == mina:
                                    nmine += 1

                    if nmine != 0:
                        self.celle[i][j].val = str(nmine)

    def draw(self):
        pygame.font.init()
        font = pygame.font.SysFont(pygame.font.get_default_font(),int(self.height), bold = True, italic = False)
        for riga in self.celle:
            for cella in riga:
                cella.draw()
                if cella.esplosa:
                    self.bloccato = True
                    self.sconfitta = True

                    
                if self.nbandiere < -3:
                    self.bloccato = True
                    
        if self.controllatavolo()[0] == self.nmine and not self.sconfitta:
            img_vittoria = 'Hai vinto!!!'
            img_vittoria = font.render(img_vittoria, True, (250,250,250))
            img_vittoria = pygame.transform.scale(img_vittoria,
                                                        (self.width, self.width/4))
            self.screen.blit(img_vittoria,
                        ((self.width/2) - img_vittoria.get_width()/2, 
                        (self.height/2) - img_vittoria.get_height()/2))
            self.bloccato = True
        elif self.bloccato:
            img_sconfitta = 'Hai perso!!!'
            img_sconfitta = font.render(img_sconfitta, True, (250, 250, 250))
            img_sconfitta = pygame.transform.scale(img_sconfitta,
                                                    (self.width, self.width/4))
            self.screen.blit(img_sconfitta, 
                            ((self.width/2) - img_sconfitta.get_width()/2, 
                            (self.height/2) - img_sconfitta.get_height()/2))
            
    def reset(self):
        self.crea_celle()
        self.nbandiere = 16
        self.bloccato = False
        self.sconfitta = False

    def click(self, x, y):
        x -= self.offset[0]
        y -= self.offset[1]
        col = (x*self.ncol) // self.width
        rig = (y*self.nrig) // self.height
        # print(rig, col)

        #partita persa
        

        return self.celle[rig][col].scopri(self.celle,rig,col)
    
            
    def scopritutto(self,cella,rig,col, controllare = []):
        # grafo per scoprire tutte le celle connesse
        cella.coperto = False
        for i in range(-1,2):
            for j in range(-1,2):
                if (rig+i >= 0 and rig+i <self.nrig) and (col+j >= 0 and col+j <self.ncol):
                    if self.celle[rig+i][col+j].val ==  vuoto and self.celle[rig+i][col+j].coperto == True:
                        controllare.append([self.celle[rig+i][col+j], (rig+i,col+j)])
                    self.celle[rig+i][col+j].coperto = False
                
        if len(controllare) > 0:
            dati = [controllare[0][0], controllare[0][1]]
            controllare.pop(0)
            self.scopritutto(dati[0],dati[1][0],dati[1][1], controllare)
                
                
                
        # while len(controllare) > 0:
        #     controllo = controllare[0]
        #     controllo.coperto = False
        #     if controllo.segnato == True:
        #         controllo.segnato = False
        #         self.nbandiere +=1
                
        #     if controllo.val == vuoto:
        #         for (posx,posy) in controllo.archi:
        #             for riga in self.celle:
        #                 for celle in riga:
        #                     if celle.val_nodo[0] == posx and celle.val_nodo[1] == posy and celle not in controllati:
        #                         controllare.append(celle)
        #     controllare.pop(0)
        #     controllati.append(controllo)
        # trovato = False
        # for riga in range(-1,+2):
        #     for colonna in range(-1,+2):
        #         if ((rig+riga >=0 and rig+riga<len(self.celle)) and (col+colonna >= 0 and col+colonna<len(self.celle))):
        #             if self.celle[rig+riga][col+colonna].val == vuoto and self.celle[rig+riga][col+colonna].coperto:
        #                 self.celle[rig+riga][col+colonna].coperto = False
        #                 prossimo = [self.celle[rig+riga][col+colonna],rig+riga,col+colonna]
        #                 trovato = True
                        
        #             if self.celle[rig+riga][col+colonna].segnato == True:
        #                 self.celle[rig+riga][col+colonna].segnato = False
        #                 self.nbandiere +=1
        #             self.celle[rig+riga][col+colonna].coperto = False
                    
        # if trovato:
        #     self.scopritutto(prossimo[0], prossimo[1], prossimo[2])
    
    # controllo dello stato del Tavolo  
    def controllatavolo(self):
        coperte = 0
        segnate = 0
        for rig in self.celle:
            for celle in rig:
                if celle.coperto == True:
                    coperte +=1
                if celle.segnato == True:
                    segnate +=1
        
        return (coperte,segnate)