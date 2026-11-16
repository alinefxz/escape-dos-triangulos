"""Cálculos da física vertical e do alcance horizontal entre plataformas.

A simulação reproduz a ordem usada em Jogador.atualizar():
primeiro soma a gravidade à velocidade e depois atualiza a posição.
"""
from math import ceil, floor

GRAVIDADE = 0.6
FORCA_PULO = -10.5
LARGURA_JOGADOR = 30
MARGEM_COLISAO = 8


def tempo_descida_ate_altura(
    delta_y,
    gravidade=GRAVIDADE,
    forca_pulo=FORCA_PULO,
    max_frames=180,
):
    """Retorna os frames até cruzar uma altura durante a descida.

    delta_y é a diferença entre a altura de destino e a altura inicial do
    fundo do jogador. Valor negativo significa uma plataforma mais alta.
    Retorna None quando a plataforma está acima do alcance do salto.
    """
    deslocamento = 0.0
    velocidade_y = float(forca_pulo)
    tolerancia = 1e-7

    for frame in range(1, max_frames + 1):
        velocidade_y += gravidade
        deslocamento += velocidade_y

        if velocidade_y >= 0 and deslocamento >= delta_y - tolerancia:
            return frame

    return None


def altura_maxima_salto(
    gravidade=GRAVIDADE,
    forca_pulo=FORCA_PULO,
    max_frames=180,
):
    """Calcula a altura máxima real da simulação discreta, em pixels."""
    deslocamento = 0.0
    velocidade_y = float(forca_pulo)
    menor_deslocamento = 0.0

    for _ in range(max_frames):
        velocidade_y += gravidade
        deslocamento += velocidade_y
        menor_deslocamento = min(menor_deslocamento, deslocamento)
        if velocidade_y >= 0:
            break

    return abs(menor_deslocamento)


def calcular_gap_seguro(
    velocidade_cenario,
    delta_y,
    largura_plataforma,
    largura_jogador=LARGURA_JOGADOR,
    margem=MARGEM_COLISAO,
):
    """Calcula o vão entre bordas para a plataforma chegar alinhada ao pouso.

    Considera a velocidade horizontal, os frames reais até a altura de
    destino e a largura da plataforma seguinte. O vão ideal centraliza a
    plataforma sob o jogador no frame de aterrissagem.

    A margem garante que exista uma faixa de sobreposição mesmo com pequenas
    diferenças de arredondamento do pygame.Rect.
    """
    if velocidade_cenario <= 0:
        raise ValueError("A velocidade do cenário precisa ser positiva.")
    if largura_plataforma <= margem or largura_jogador <= margem:
        raise ValueError("A plataforma e o jogador precisam ser largos o bastante para a margem.")

    frames = tempo_descida_ate_altura(delta_y)
    if frames is None:
        raise ValueError(
            f"A plataforma está fora do alcance vertical do salto: delta_y={delta_y}."
        )

    deslocamento_horizontal = velocidade_cenario * frames

    # No pouso, alinha os centros horizontalmente:
    # jogador: [0, largura_jogador]; plataforma: [gap - deslocamento, ...]
    gap_ideal = deslocamento_horizontal + (largura_jogador - largura_plataforma) / 2

    # Limites em que ainda existe sobreposição mínima entre os retângulos.
    gap_minimo = deslocamento_horizontal - largura_plataforma + margem
    gap_maximo = deslocamento_horizontal + largura_jogador - margem

    gap_ajustado = min(max(gap_ideal, gap_minimo), gap_maximo)
    return max(0, round(gap_ajustado))
