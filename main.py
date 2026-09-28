import pygame
from scripts.cenas import Partida, Menu, TelaNome, TelaRanking, TelaPausa, TelaVitoria

pygame.init()

tamanhoTela = [800, 400]
tela = pygame.display.set_mode(tamanhoTela)
pygame.display.set_caption("Escape dos Triângulos")
relogio = pygame.time.Clock()
corFundo = (15, 15, 20)

# Telas novas adicionadas no dicionário
listaCenas = {
    'menu': Menu(tela),
    'nome_input': TelaNome(tela),
    'partida': Partida(tela),
    'ranking': TelaRanking(tela),
    'pausa': TelaPausa(tela),
    'vitoria': TelaVitoria(tela)
}

cenaAtual = 'menu'

while True:
    eventos = pygame.event.get()
    
    for e in eventos:
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()

    tela.fill(corFundo)

    proxima_cena = listaCenas[cenaAtual].atualizar(eventos)
    
    # Adicionada a regra 'partida_resumir' para tirar do pause sem reiniciar a fase
    if proxima_cena == 'partida_reiniciar':
        listaCenas['partida'].reiniciar_fase(nova_partida=True)
        cenaAtual = 'partida'
    elif proxima_cena == 'partida_resumir':
        cenaAtual = 'partida'
    elif proxima_cena != cenaAtual:
        if proxima_cena == 'partida':
            listaCenas['partida'].reiniciar_fase()
        cenaAtual = proxima_cena

    relogio.tick(60)
    pygame.display.flip()