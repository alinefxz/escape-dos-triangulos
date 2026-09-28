import pygame

class Texto:
    def __init__(self, tela, texto, x, y, cor, tamanho):
        self.tela = tela
        self.texto = texto
        self.cor = cor
        pygame.font.init()
        self.fonte = pygame.font.SysFont("Arial", tamanho, bold=True)
        self.imagemTexto = self.fonte.render(self.texto, True, self.cor)
        
        # Lógica de centralização automática
        pos_x = tela.get_width() // 2 - self.imagemTexto.get_width() // 2 if x == "centro" else x
        self.posicao = (pos_x, y)

    def desenhar(self):
        self.tela.blit(self.imagemTexto, self.posicao)

    def atualizarTexto(self, novoTexto):
        self.texto = novoTexto
        self.imagemTexto = self.fonte.render(self.texto, True, self.cor)

class Botao:
    def __init__(self, tela, texto, x, y, tamanho, corFundo, corTexto):
        self.tela = tela
        self.texto_obj = Texto(tela, texto, 0, y, corTexto, tamanho) # X temporário
        
        # Lógica de centralização automática
        pos_x = tela.get_width() // 2 - self.texto_obj.imagemTexto.get_width() // 2 if x == "centro" else x
        self.texto_obj.posicao = (pos_x, y)
        
        self.corFundo = corFundo
        self.rect = pygame.Rect(pos_x - 15, y - 5, self.texto_obj.imagemTexto.get_width() + 30, self.texto_obj.imagemTexto.get_height() + 10)

    def desenhar(self):
        pygame.draw.rect(self.tela, self.corFundo, self.rect, border_radius=5)
        pygame.draw.rect(self.tela, (255, 255, 255), self.rect, 2, border_radius=5) # Borda neon
        self.texto_obj.desenhar()

    def get_click(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.rect.collidepoint(evento.pos):
                    return True
        return False

class CaixaTexto:
    def __init__(self, tela, x, y, largura, altura):
        self.tela = tela
        # Centralizando a caixa de texto
        pos_x = tela.get_width() // 2 - largura // 2 if x == "centro" else x
        self.rect = pygame.Rect(pos_x, y, largura, altura)
        self.texto = ""
        self.ativo = False
        self.fonte = pygame.font.SysFont("Arial", 30, bold=True)

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                self.ativo = self.rect.collidepoint(evento.pos)
            if evento.type == pygame.KEYDOWN and self.ativo:
                if evento.key == pygame.K_BACKSPACE:
                    self.texto = self.texto[:-1]
                elif evento.key != pygame.K_RETURN:
                    if len(self.texto) < 12: 
                        self.texto += evento.unicode

    def desenhar(self):
        cor_borda = (255, 20, 147) if self.ativo else (100, 100, 100)
        pygame.draw.rect(self.tela, cor_borda, self.rect, 2, border_radius=5)
        txt_surface = self.fonte.render(self.texto, True, (255, 255, 255))
        self.tela.blit(txt_surface, (self.rect.x + 10, self.rect.y + 5))