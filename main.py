import pygame

from scripts.cenas import (
    Partida,
    Menu,
    TelaNome,
    TelaRanking,
    TelaPausa,
    TelaVitoria,
    dados_jogo,
)
from scripts.configuracao_fases import TOTAL_FASES


pygame.init()

tamanhoTela = [800, 400]
tela = pygame.display.set_mode(tamanhoTela)
pygame.display.set_caption("Escape dos Triângulos")
relogio = pygame.time.Clock()
corFundo = (15, 15, 20)

listaCenas = {
    "menu": Menu(tela),
    "nome_input": TelaNome(tela),
    "partida": Partida(tela),
    "ranking": TelaRanking(tela),
    "pausa": TelaPausa(tela),
    "vitoria": TelaVitoria(tela),
}

cenaAtual = "menu"
rodando = True


def iniciar_fase_direta(numero_fase):
    """Permite abrir qualquer fase pelo retorno fase_N_direto da cena."""
    if not 1 <= numero_fase <= TOTAL_FASES:
        return False

    dados_jogo["nome"] = "TESTE"
    dados_jogo["fase_salva"] = numero_fase
    dados_jogo["jogo_em_andamento"] = True

    partida = listaCenas["partida"]
    partida.fase_atual = numero_fase
    partida.reiniciar_fase()
    return True


while rodando:
    eventos = pygame.event.get()

    for evento in eventos:
        if evento.type == pygame.QUIT:
            rodando = False

    tela.fill(corFundo)
    proxima_cena = listaCenas[cenaAtual].atualizar(eventos)

    # Mantém fase_5_direto e aceita também fase_6_direto, ... fase_8_direto.
    if isinstance(proxima_cena, str) and proxima_cena.startswith("fase_") and proxima_cena.endswith("_direto"):
        parte_numero = proxima_cena[len("fase_") : -len("_direto")]
        if parte_numero.isdigit() and iniciar_fase_direta(int(parte_numero)):
            cenaAtual = "partida"
    elif proxima_cena == "partida_reiniciar":
        listaCenas["partida"].reiniciar_fase(nova_partida=True)
        cenaAtual = "partida"
    elif proxima_cena == "partida_resumir":
        cenaAtual = "partida"
    elif proxima_cena != cenaAtual and proxima_cena in listaCenas:
        if proxima_cena == "partida":
            listaCenas["partida"].reiniciar_fase()
        cenaAtual = proxima_cena

    relogio.tick(60)
    pygame.display.flip()

pygame.quit()
