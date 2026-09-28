import pygame
from scripts.cenas import Partida, Menu, TelaNome, TelaRanking

pygame.init()

tamanhoTela = [800, 400]
tela = pygame.display.set_mode(tamanhoTela)
pygame.display.set_caption("Escape dos Triângulos")
relogio = pygame.time.Clock()
corFundo = (15, 15, 20)

# Instanciando todas as cenas
listaCenas = {
    'menu': Menu(tela),
    'nome_input': TelaNome(tela),
    'partida': Partida(tela),
    'ranking': TelaRanking(tela)
}

cenaAtual = 'menu'

while True:
    # Captura a lista de eventos
    eventos = pygame.event.get()
    
    for e in eventos:
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()

    tela.fill(corFundo)

    # Passamos os eventos para a cena tratar cliques e digitação
    proxima_cena = listaCenas[cenaAtual].atualizar(eventos)
    
    # Se a cena mudou, atualiza a variável cenaAtual
    if proxima_cena != cenaAtual:
        # Se voltamos pro jogo, garantimos que a partida inicie limpa
        if proxima_cena == 'partida':
            listaCenas['partida'].reiniciar_fase() # Correção feita aqui!
        cenaAtual = proxima_cena

    relogio.tick(60)
    pygame.display.flip()