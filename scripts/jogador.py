import pygame

from .fisica_pulo import GRAVIDADE, FORCA_PULO


class Jogador:
    def __init__(self, tela, x, y):
        self.tela = tela
        self.tamanho = [30, 30]
        self.posicao = [float(x), float(y)]
        self.rect = pygame.Rect(round(x), round(y), *self.tamanho)
        self.velocidade_y = 0.0
        self.gravidade = GRAVIDADE
        self.forca_pulo = FORCA_PULO
        self.no_chao = False
        self.cor = (255, 20, 147)

        self.morto = False
        self.rotacao = 0

    def desenhar(self):
        if self.morto:
            superficie = pygame.Surface(self.tamanho, pygame.SRCALPHA)
            pygame.draw.rect(
                superficie,
                self.cor,
                (0, 0, self.tamanho[0], self.tamanho[1]),
            )
            pygame.draw.rect(
                superficie,
                (255, 255, 255),
                (0, 0, self.tamanho[0], self.tamanho[1]),
                2,
            )
            rotacionada = pygame.transform.rotate(superficie, self.rotacao)
            rect_rotacionado = rotacionada.get_rect(center=self.rect.center)
            self.tela.blit(rotacionada, rect_rotacionado.topleft)
        else:
            pygame.draw.rect(self.tela, self.cor, self.rect)
            pygame.draw.rect(self.tela, (255, 255, 255), self.rect, 2)

    def atualizar(self, plataformas=None, chao_y=300):
        """Atualiza o salto e detecta pousos sem atravessar plataformas.

        A colisão usa a posição vertical anterior e a atual. Isso evita que o
        jogador atravesse uma plataforma quando a velocidade de queda aumenta.
        """
        if plataformas is None:
            plataformas = ()

        if self.morto:
            self.velocidade_y += self.gravidade
            self.posicao[1] += self.velocidade_y
            self.posicao[0] -= 3
            self.rotacao -= 15
            self.rect.topleft = (round(self.posicao[0]), round(self.posicao[1]))
            return

        rect_anterior = self.rect.copy()
        self.no_chao = False

        # Física vertical: mantém a mesma ordem usada no cálculo dos vãos.
        self.velocidade_y += self.gravidade
        self.posicao[1] += self.velocidade_y
        self.rect.topleft = (round(self.posicao[0]), round(self.posicao[1]))

        # Só pode pousar durante a descida e quando cruza o topo da plataforma.
        if self.velocidade_y >= 0:
            for plataforma in plataformas:
                sobreposicao_horizontal = (
                    self.rect.right > plataforma.rect.left
                    and self.rect.left < plataforma.rect.right
                )
                cruzou_o_topo = (
                    rect_anterior.bottom <= plataforma.rect.top
                    and self.rect.bottom >= plataforma.rect.top
                )

                if sobreposicao_horizontal and cruzou_o_topo:
                    self.posicao[1] = plataforma.rect.top - self.tamanho[1]
                    self.velocidade_y = 0.0
                    self.no_chao = True
                    self.rect.bottom = plataforma.rect.top
                    break

        # Chão principal do jogo.
        if self.posicao[1] + self.tamanho[1] >= chao_y:
            self.posicao[1] = chao_y - self.tamanho[1]
            self.velocidade_y = 0.0
            self.no_chao = True
            self.rect.bottom = chao_y

        # O pulo é iniciado somente depois de confirmar que está apoiado.
        teclas = pygame.key.get_pressed()
        if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP]) and self.no_chao:
            self.velocidade_y = self.forca_pulo
            self.no_chao = False

    def getRect(self):
        return pygame.Rect(self.posicao, self.tamanho)
