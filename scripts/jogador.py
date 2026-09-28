import pygame

class Jogador:
    def __init__(self, tela, x, y):
        self.tela = tela
        self.tamanho = [30, 30]
        self.posicao = [x, y]
        self.rect = pygame.Rect(self.posicao, self.tamanho)
        self.velocidade_y = 0
        self.gravidade = 0.6
        self.forca_pulo = -10.5 # Levemente mais forte para alcançar as plataformas
        self.no_chao = False
        self.cor = (255, 20, 147)
        
        # Variáveis para animação de morte
        self.morto = False
        self.rotacao = 0

    def desenhar(self):
        if self.morto:
            # Cria uma superfície temporária para rotacionar o bloquinho
            sup = pygame.Surface(self.tamanho, pygame.SRCALPHA)
            pygame.draw.rect(sup, self.cor, (0, 0, self.tamanho[0], self.tamanho[1]))
            pygame.draw.rect(sup, (255, 255, 255), (0, 0, self.tamanho[0], self.tamanho[1]), 2)
            
            rotacionada = pygame.transform.rotate(sup, self.rotacao)
            rect_rot = rotacionada.get_rect(center=self.rect.center)
            self.tela.blit(rotacionada, rect_rot.topleft)
        else:
            pygame.draw.rect(self.tela, self.cor, self.rect)
            pygame.draw.rect(self.tela, (255, 255, 255), self.rect, 2)

    def atualizar(self, plataformas=[]):
        if self.morto:
            # Animação de giro caindo para trás
            self.velocidade_y += self.gravidade
            self.posicao[1] += self.velocidade_y
            self.posicao[0] -= 3 # Recuo dramático
            self.rotacao -= 15   # Gira rapidamente
            self.rect.topleft = self.posicao
            return

        # Aplica gravidade padrão
        self.velocidade_y += self.gravidade
        self.posicao[1] += self.velocidade_y
        self.rect.topleft = self.posicao
        self.no_chao = False

        # Verifica se pousou em alguma Plataforma
        for plat in plataformas:
            if self.rect.colliderect(plat.rect):
                # Só pousa se estiver caindo (velocidade positiva) e estiver na parte de cima
                if self.velocidade_y >= 0 and self.rect.bottom <= plat.rect.top + 15:
                    self.posicao[1] = plat.rect.top - self.tamanho[1]
                    self.velocidade_y = 0
                    self.no_chao = True
                    self.rect.topleft = self.posicao

        # Colisão com o chão padrão (linha rosa)
        chao_y = 300
        if self.posicao[1] + self.tamanho[1] >= chao_y:
            self.posicao[1] = chao_y - self.tamanho[1]
            self.velocidade_y = 0
            self.no_chao = True
            self.rect.topleft = self.posicao

        # Pulo (Espaço ou Seta pra Cima)
        teclas = pygame.key.get_pressed()
        if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP]) and self.no_chao:
            self.velocidade_y = self.forca_pulo
            self.no_chao = False

    def getRect(self):
        return pygame.Rect(self.posicao, self.tamanho)