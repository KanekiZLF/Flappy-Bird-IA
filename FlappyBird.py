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

        def desenhar(self):
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


class Cano:
    pass


class Chao:
    pass
