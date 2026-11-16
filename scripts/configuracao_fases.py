"""Configuração das oito fases e criação de uma sequência de plataformas.

As alturas são medidas em pixels acima do chão (chao_y). Cada item é
(altura_acima_do_chao, largura_da_plataforma).
Os vãos são calculados automaticamente pela física_pulo.py.
"""
from .fisica_pulo import calcular_gap_seguro

TOTAL_FASES = 8

# A progressão parte da velocidade original padrão (8) e acrescenta 0,5
# por fase. As fases 1 a 5 também passam a usar esta configuração uniforme.
FASES = {
    1: {
        "velocidade": 8.0,
        "plataformas": ((25, 160), (10, 155), (35, 150), (15, 150)),
        "obstaculos": {"triangulos": 2, "blocos": 0, "buracos": 0, "largura_buraco": 60},
    },
    2: {
        "velocidade": 8.5,
        "plataformas": ((30, 150), (55, 145), (20, 145), (50, 140), (15, 145)),
        "obstaculos": {"triangulos": 3, "blocos": 0, "buracos": 1, "largura_buraco": 65},
    },
    3: {
        "velocidade": 9.0,
        "plataformas": ((30, 145), (55, 140), (20, 135), (60, 135), (25, 140)),
        "obstaculos": {"triangulos": 3, "blocos": 1, "buracos": 1, "largura_buraco": 68},
    },
    4: {
        "velocidade": 9.5,
        "plataformas": ((35, 140), (60, 135), (25, 130), (55, 130), (15, 135)),
        "obstaculos": {"triangulos": 4, "blocos": 1, "buracos": 1, "largura_buraco": 70},
    },
    5: {
        "velocidade": 10.0,
        "plataformas": ((40, 135), (65, 130), (25, 125), (60, 125), (20, 130)),
        "obstaculos": {"triangulos": 4, "blocos": 1, "buracos": 2, "largura_buraco": 72},
    },
    6: {
        "velocidade": 10.5,
        "plataformas": ((40, 130), (65, 125), (25, 120), (60, 120), (20, 125), (55, 120)),
        "obstaculos": {"triangulos": 5, "blocos": 1, "buracos": 2, "largura_buraco": 75},
    },
    7: {
        "velocidade": 11.0,
        "plataformas": ((45, 125), (70, 120), (30, 115), (65, 115), (25, 120), (60, 115)),
        "obstaculos": {"triangulos": 5, "blocos": 2, "buracos": 2, "largura_buraco": 78},
    },
    8: {
        "velocidade": 11.5,
        "plataformas": ((50, 120), (70, 115), (30, 110), (65, 110), (25, 115), (60, 110)),
        "obstaculos": {"triangulos": 6, "blocos": 2, "buracos": 3, "largura_buraco": 80},
    },
}


def obter_configuracao_fase(numero_fase):
    """Obtém a configuração de uma fase, validando o intervalo de 1 a 8."""
    if numero_fase not in FASES:
        raise ValueError(f"Fase inválida: {numero_fase}. O jogo possui {TOTAL_FASES} fases.")
    return FASES[numero_fase]


def criar_plataformas(tela, borda_anterior, chao_y, numero_fase, classe_plataforma):
    """Cria as plataformas de uma fase com vãos calculados pela física.

    borda_anterior é a coordenada X da borda direita da superfície de onde
    o jogador parte (por exemplo, o fim do chão ou da plataforma anterior).
    A função retorna a lista de objetos Plataforma.
    """
    config = obter_configuracao_fase(numero_fase)
    velocidade = config["velocidade"]
    plataformas = []
    origem_y = chao_y
    borda_x = borda_anterior

    for altura, largura in config["plataformas"]:
        destino_y = chao_y - altura
        delta_y = destino_y - origem_y
        gap = calcular_gap_seguro(velocidade, delta_y, largura)
        x = borda_x + gap

        plataforma = classe_plataforma(
            tela,
            x,
            destino_y,
            largura,
            velocidade,
        )
        plataformas.append(plataforma)

        borda_x = x + largura
        origem_y = destino_y

    return plataformas
