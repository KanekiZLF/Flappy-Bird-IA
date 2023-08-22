import pygame
import os
import random
import neat

ai_jogando = True
geracao = 0

# Dimensoes da tela
TelaLargura = 500
TelaAltura = 650

# Imagens do jogo
ImgCano = pygame.transform.scale2x(
    pygame.image.load(os.path.join('imgs', 'pipe.png')))
ImgChao = pygame.transform.scale2x(
    pygame.image.load(os.path.join('imgs', 'base.png')))
ImgFundo = pygame.transform.scale2x(
    pygame.image.load(os.path.join('imgs', 'bg.png')))
ImgPassaros = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
               pygame.transform.scale2x(pygame.image.load(
                   os.path.join('imgs', 'bird2.png'))),
               pygame.transform.scale2x(pygame.image.load(
                   os.path.join('imgs', 'bird3.png'))),
               ]

# Fonte do jogo
pygame.font.init()
FontePontos = pygame.font.SysFont('arial', 50)


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
        self.imagem = self.imgs[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # Calcular deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        # Restringir deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # Angulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50):
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
        elif self.contagem_imagem < self.TempoAnimacao*2:
            self.imagem = self.imgs[1]
        elif self.contagem_imagem < self.TempoAnimacao*3:
            self.imagem = self.imgs[2]
        elif self.contagem_imagem < self.TempoAnimacao*4:
            self.imagem = self.imgs[1]
        elif self.contagem_imagem >= self.TempoAnimacao*4 + 1:
            self.imagem = self.imgs[0]
            self.contagem_imagem = 0

        # Se o passaro estiver caindo, não bate a asa
        if self.angulo <= -80:
            self.imagem = self.imgs[1]
            self.contagem_imagem = self.TempoAnimacao*2

        # Desenha a imagem
        ImagemRotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        PosCentroImagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        Retangulo = ImagemRotacionada.get_rect(center=PosCentroImagem)
        tela.blit(ImagemRotacionada, Retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


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
        tela.blit(self.cano_base, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.cano_topo)
        base_mask = pygame.mask.from_surface(self.cano_base)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Chao:
    Velocidade = 5
    Largura = ImgChao.get_width()
    Imagem = ImgChao

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.Largura

    def mover(self):
        self.x1 -= self.Velocidade
        self.x2 -= self.Velocidade

        if self.x1 + self.Largura < 0:
            self.x1 = self.x2 + self.Largura
        if self.x2 + self.Largura < 0:
            self.x2 = self.x1 + self.Largura

    def desenhar(self, tela):
        tela.blit(self.Imagem, (self.x1, self.y))
        tela.blit(self.Imagem, (self.x2, self.y))

    # Desenha a tela do Jogo


def desenharTela(tela, passaros, canos, chao, pontos):
    tela.blit(ImgFundo, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = FontePontos.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TelaLargura - 10 - texto.get_width(), 10))

    if ai_jogando:
        texto = FontePontos.render(f"Geração: {geracao}", 1, (255, 255, 255))
        tela.blit(texto, (10, 10))

    chao.desenhar(tela)
    pygame.display.update()


def main(genomas, config):  # Fitness Function
    global geracao
    geracao += 1

    if ai_jogando:
        # Criar os passaros
        redes = []
        lista_genomas = []
        passaros = []
        for _, genoma in genomas:
            rede = neat.nn.FeedForwardNetwork.create(genoma, config)
            redes.append(rede)
            genoma.fitness = 0
            lista_genomas.append(genoma)
            passaros.append(Passaro(230, 350))
    else:
        passaros = [Passaro(230, 350)]
    chao = Chao(600)
    canos = [Cano(550)]
    tela = pygame.display.set_mode((TelaLargura, TelaAltura))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)
        # Interação
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if not ai_jogando:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        for passaro in passaros:
                            passaro.pular()

        indice_cano = 0
        if len(passaros) > 0:
            # Descobrir qual cano olhar
            if len(canos) > 1 and passaros[0].x > canos[0].x + canos[0].cano_topo.get_width():
                indice_cano = 1
        else:
            rodando = False
            break
        # Mover
        for i, passaro in enumerate(passaros):
            passaro.mover()
            # Aumentar a Fitness do passaro
            lista_genomas[i].fitness += 0.1
            output = redes[i].activate((passaro.y,
                                        abs(passaro.y -
                                            canos[indice_cano].altura),
                                        abs(passaro.y - canos[indice_cano].pos_base)))
            # Se o output for superior a 0.5 ele pula
            if output[0] > 0.5:
                passaro.pular()

        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                    if ai_jogando:
                        lista_genomas[i].fitness -= 1
                        lista_genomas.pop(i)
                        redes.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + cano.cano_topo.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
            for genoma in lista_genomas:
                genoma.fitness += 5
        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)
                if ai_jogando:
                    lista_genomas.pop(i)
                    redes.pop(i)

        desenharTela(tela, passaros, canos, chao, pontos)


def rodar(arqvConfig):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                arqvConfig)
    populacao = neat.Population(config)
    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.StatisticsReporter())

    if ai_jogando:
        populacao.run(main, 50)
    else:
        main(None, None)


if __name__ == '__main__':
    caminho = os.path.dirname(__file__)
    arqvConfig = os.path.join(caminho, 'config.txt')
    rodar(arqvConfig)
