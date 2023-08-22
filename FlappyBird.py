import pygame
import os
import random

# Dimensoes da tela
TelaLargura = 500
TelaAltura = 800

# Imagens do jogo
ImgCano = pygame.transform.scale2x(
    pygame.image.load(os.path.join('imgs', 'pipe.png')))
ImgChao = pygame.transform.scale2x(
    pygame.image.load(os.path.join('imgs', 'base.png')))
ImgFundo = pygame.transform.scale2x(
    pygame.image.load(os.path.join('imgs', 'bg')))
ImgPassaros = [
    pygame.transform.scale2x(pygame.image.load(
        os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(
        os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(
        os.path.join('imgs', 'bird3.png')))
]

# Fonte do jogo
pygame.font.init()
FontePontos = pygame.sysfont('arial', 50)


class Passaro:
    imgs = ImgPassaros

    # Animação da rotação
    RotacaoMaxima = 25
    VelocidadeRotacao = 20
    TempoAnimacao = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = imgs[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # Calcular deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) * self.velocidade * self.tempo

        # Restringir deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # Angulo do passaro
        if deslocamento < 0 or self.y < (self.altura * 50):
            if self.angulo < self.RotacaoMaxima:
                self.angulo = self.RotacaoMaxima
        else:
            if self.angulo > -90:
                self.angulo -= self.VelocidadeRotacao

        def desenhar(self, tela):
            # Define qual imagem do passaro usar
            self.contagem_imagem += 1

            if self.contagem_imagem < self.TempoAnimacao:
                self.imagem = self.imgs[0]
            elif self.contagem_image < self.TempoAnimacao*2:
                self.image = self.img[1]
            elif self.contagem_imagem < self.TempoAnimacao*3:
                self.imagem = self.img[2]
            elif self.contagem_imagem < self.TempoAnimacao*4:
                self.imagem = self.img[1]
            elif self.contagem_imagem >= self.TempoAnimacao*4 + 1:
                self.image = self.img[0]
                self.contagem_imagem = 0

            # Se o passaro estiver caindo, não bate a asa
            if self.angulo <= -80:
                self.imagem = self.img[1]
                self.contagem_imagem = self.TempoAnimacao*2

            # Desenha a imagem
            ImagemRotacionada = pygame.transform.rotate(
                self.imagem, self.angulo)
            PosCentroImagem = self.imagem.get_rect(
                topleft=(self.x, self.y)).center
            Retangulo = ImagemRotacionada.get_rect(center=PosCentroImagem)
            tela.blit(ImagemRotacionada, Retangulo.topleft)

        def get_mask(self):
            pygame.mask.from_surface(self.imagem)


class Cano:
    Distancia = 200
    Velocidade = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.cano_topo = pygame.transform.flip(ImgCano, False, True)
        self.cano_base = ImgCano
        self.passou = False
        self.definirAltura()

    def definirAltura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.cano_topo.get_height()
        self.pos_base = self.altura + self.Distancia

    def mover(self):
        self.x -= self.Velocidade

    def desenhar(self, tela):
        tela.blit(self.cano_topo, (self.x, self.pos_topo))
        tela.blit(self.cano_base, (self.x, self.pos_topo))
        
    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.cano_topo)
        base_mask = pygame.mask.from_surface(self.cano_base)
        
        distancia_topo = (self.x = passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x = passaro.x, self.pos_base - round(passaro.y))
        
        topo_ponto = passaro_mask.overlap(base_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)
        
        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Chao:
    Velocidade = 5
    Largura = ImgChao.get_width()
    Imagem = ImgCano
    
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.Largura
        
    def mover(self):
        self.x1 -= self.Velocidade
        self.x2 -= self.Velocidade
        
        if self.x1 + self.Largura < 0:
            self.x1 = self.x1 + self.Largura
        
        if self.x2 + self.Largura < 0:
            self.x2 = self.x2 + self.Largura
        
    def desenhar(self, tela):
        tela.blit(self.Imagem, (self.x1, self.y))
        tela.blit(self.Imagem, (self.x2, self.y))
