import pygame
import random

class Mato:
    def __init__(self):
        pygame.init()
        self.uusi_peli()
        self.naytto_leveys=20*self.skaala
        self.naytto_korkeus=15*self.skaala
        self.naytto = pygame.display.set_mode((self.naytto_leveys, self.naytto_korkeus))  
        self.kello=pygame.time.Clock()
        self.hiscore=0
        self.fontti = pygame.font.SysFont("Arial", 2*self.skaala)
        self.fontti2 = pygame.font.SysFont("Arial", 1*self.skaala)    
        self.silmukka()

        
        
    def uusi_peli(self):
        pygame.display.set_caption("Kärmes") 
        self.skaala=30
        self.suu = [3*self.skaala, 3*self.skaala]
        self.suunta = "alas"
        self.nopeus=15
        self.syoty=False
        self.game_over=False
        self.mato = [[3*self.skaala, 3*self.skaala], [3*self.skaala, 2*self.skaala], [3*self.skaala, self.skaala]]
        self.ruoka=[random.randint(0, 19) * self.skaala, random.randint(0, 14) * self.skaala]
        self.uusisuunta="alas"
        self.hiiri_painikkeella=False
        self.score=0

    def silmukka(self):
        while True:
            self.tutki_tapahtumat()
            self.liike()
            self.piirra_ruutu()
 
    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                exit()
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT and self.suunta!="oikea":
                    self.uusisuunta="vasen"
                if tapahtuma.key == pygame.K_RIGHT and self.suunta!="vasen":
                    self.uusisuunta="oikea"
                if tapahtuma.key == pygame.K_UP and self.suunta!="alas":
                    self.uusisuunta="ylos"
                if tapahtuma.key == pygame.K_DOWN and self.suunta!="ylos":
                    self.uusisuunta="alas"
            if self.game_over:
                if tapahtuma.type == pygame.MOUSEBUTTONDOWN:
                    if 2*self.skaala<tapahtuma.pos[0]<int(7.2*self.skaala) and 8*self.skaala<tapahtuma.pos[1]<int(9.5*self.skaala):
                        self.uusi_peli()
                if tapahtuma.type == pygame.MOUSEMOTION:
                    if 2*self.skaala<tapahtuma.pos[0]<int(7.2*self.skaala) and 8*self.skaala<tapahtuma.pos[1]<int(9.5*self.skaala):
                        self.hiiri_painikkeella=True
                    else:
                        self.hiiri_painikkeella=False
                    

    def syonti(self):
        self.ruoka=[random.randint(0, 19) * self.skaala, random.randint(0, 14) * self.skaala]
        while self.ruoka in self.mato:
            self.ruoka=[random.randint(0, 19) * self.skaala, random.randint(0, 14) * self.skaala]
        self.score+=5
        print(self.ruoka)
        self.syoty=True
        pygame.display.set_caption(f"Score: {self.score}") 

    def liike(self):
        if self.game_over:
            return
        self.suunta=self.uusisuunta
        if self.suunta=="vasen":
            if self.suu[0]==0:
                self.suu[0]+=self.skaala*20
            self.suu[0]-=self.skaala

        if self.suunta=="oikea":
            if self.suu[0]==self.skaala*19:
                self.suu[0]-=self.skaala*20
            self.suu[0]+=self.skaala

        if self.suunta=="ylos":
            if self.suu[1]==0:
                self.suu[1]+=self.skaala*15
            self.suu[1]-=self.skaala    

        if self.suunta=="alas":
            if self.suu[1]==self.skaala*14:
                self.suu[1]-=self.skaala*15            
            self.suu[1]+=self.skaala
        #itseen törmäys
        if self.suu in self.mato:
            self.gameover()
            return
        #syönti
        if self.suu == self.ruoka:
            self.syonti()
        self.mato.insert (0, self.suu.copy())
        if not self.syoty:
            self.mato.pop()
        self.syoty=False
        self.kello.tick(self.nopeus)

    def gameover(self):
        self.game_over=True
        self.score=(len(self.mato)-3)*5
        if self.score>self.hiscore:
            self.hiscore=self.score
        pygame.display.set_caption(f"Score: {self.score} HS: {self.hiscore}")

    def piirra_ruutu(self):
        self.naytto.fill((0, 0, 0))
        for patka in self.mato:
            pygame.draw.circle(self.naytto, (0, 255, 0), (patka[0] + self.skaala/2, patka[1] + self.skaala/2), self.skaala/2)
            pygame.draw.rect(self.naytto, (255, 0, 0), pygame.Rect(self.ruoka[0], self.ruoka[1], self.skaala, self.skaala))
        if self.game_over:
            teksti = self.fontti.render("Kärmes menehtyi.", True, (255, 100, 0))
            self.naytto.blit(teksti, (2*self.skaala, 4*self.skaala))
            if self.hiiri_painikkeella:
                pygame.draw.rect(self.naytto, (150, 0, 0), pygame.Rect(self.skaala*2, self.skaala*8, int(self.skaala*5.3), int(self.skaala*1.4)))
            teksti = self.fontti2.render("Uudestaan?", True, (255, 0, 0))
            self.naytto.blit(teksti, (2*self.skaala, 8*self.skaala))
            
        pygame.display.flip()

Mato()