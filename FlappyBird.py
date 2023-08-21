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
    pass


class Cano:
    pass


class Chao:
    pass
