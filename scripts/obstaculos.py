import pygame

class Triangulo:
    def __init__(self, tela, x, chao_y, velocidade=8):
        self.tela = tela
        self.x = x
        self.largura = 30
        self.altura = 30
        self.chao_y = chao_y
        self.velocidade = velocidade
        self.cor = (255, 0, 100)
        self.passou = False
        self.atualizar_pontos()

    def atualizar_pontos(self):
        self.p1 = (self.x + self.largura / 2, self.chao_y - self.altura)
        self.p2 = (self.x, self.chao_y)
        self.p3 = (self.x + self.largura, self.chao_y)
        self.rect = pygame.Rect(self.x + 5, self.chao_y - self.altura + 5, self.largura - 10, self.altura - 5)

    def atualizar(self):
        self.x -= self.velocidade
        self.atualizar_pontos()

    def desenhar(self):
        pygame.draw.polygon(self.tela, self.cor, [self.p1, self.p2, self.p3])
        pygame.draw.polygon(self.tela, (255, 255, 255), [self.p1, self.p2, self.p3], 2)

    def detectarColisao(self, rectJogador):
        return rectJogador.colliderect(self.rect)


class Bloco:
    def __init__(self, tela, x, chao_y, velocidade=8):
        self.tela = tela
        self.x = x
        self.tamanho = 30
        self.chao_y = chao_y
        self.velocidade = velocidade
        self.passou = False
        self.rect = pygame.Rect(self.x, self.chao_y - self.tamanho, self.tamanho, self.tamanho)

    def atualizar(self):
        self.x -= self.velocidade
        self.rect.x = self.x

    def desenhar(self):
        pygame.draw.rect(self.tela, (0, 255, 255), self.rect)
        pygame.draw.rect(self.tela, (255, 255, 255), self.rect, 2)

    def detectarColisao(self, rectJogador):
        if rectJogador.colliderect(self.rect):
            if rectJogador.bottom > self.rect.top + 15:
                return True
        return False


class Buraco:
    def __init__(self, tela, x, chao_y, largura=70, velocidade=8):
        self.tela = tela
        self.x = x
        self.chao_y = chao_y
        self.largura = largura
        self.velocidade = velocidade
        self.passou = False
        self.rect = pygame.Rect(self.x, self.chao_y, self.largura, 10)

    def atualizar(self):
        self.x -= self.velocidade
        self.rect.x = self.x

    def desenhar(self):
        pygame.draw.rect(self.tela, (15, 15, 20), (self.x, self.chao_y - 2, self.largura, 6))

    def detectarColisao(self, rectJogador):
        if rectJogador.bottom >= self.chao_y and self.x < rectJogador.centerx < self.x + self.largura:
            return True
        return False


class LinhaChegada:
    def __init__(self, tela, x, chao_y, velocidade=8):
        self.tela = tela
        self.x = x
        self.chao_y = chao_y
        self.velocidade = velocidade
        self.rect = pygame.Rect(self.x, self.chao_y - 100, 20, 100)

    def atualizar(self):
        self.x -= self.velocidade
        self.rect.x = self.x

    def desenhar(self):
        pygame.draw.rect(self.tela, (0, 255, 255), self.rect)
        pygame.draw.rect(self.tela, (255, 255, 255), self.rect, 2)


class Plataforma:
    def __init__(self, tela, x, y, largura, velocidade=8):
        self.tela = tela
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = 20
        self.velocidade = velocidade
        self.passou = False
        self.rect = pygame.Rect(self.x, self.y, self.largura, self.altura)

    def atualizar(self):
        self.x -= self.velocidade
        self.rect.x = self.x

    def desenhar(self):
        pygame.draw.rect(self.tela, (148, 0, 211), self.rect)
        pygame.draw.rect(self.tela, (255, 255, 255), self.rect, 2)

    def detectarColisao(self, rectJogador):
        if rectJogador.colliderect(self.rect):
            if rectJogador.bottom > self.rect.top + 15:
                return True
        return False