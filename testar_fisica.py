"""Validação matemática das oito configurações; não requer Pygame."""
from scripts.configuracao_fases import FASES
from scripts.fisica_pulo import (
    calcular_gap_seguro,
    tempo_descida_ate_altura,
    altura_maxima_salto,
)

CHAO_Y = 300
LARGURA_JOGADOR = 30

print(f"Altura máxima simulada: {altura_maxima_salto():.1f} px")
print("Fase | Velocidade | Plataformas | Vãos calculados")
print("-----|------------|-------------|----------------")

for numero, config in FASES.items():
    origem_y = CHAO_Y
    gaps = []

    for altura, largura in config["plataformas"]:
        destino_y = CHAO_Y - altura
        delta_y = destino_y - origem_y
        frames = tempo_descida_ate_altura(delta_y)
        assert frames is not None, (numero, delta_y)
        gap = calcular_gap_seguro(config["velocidade"], delta_y, largura)

        # Simula a posição horizontal da plataforma no frame de pouso.
        deslocamento = config["velocidade"] * frames
        plataforma_esquerda = gap - deslocamento
        plataforma_direita = plataforma_esquerda + largura
        sobreposicao = max(
            0,
            min(LARGURA_JOGADOR, plataforma_direita) - max(0, plataforma_esquerda),
        )
        assert sobreposicao >= 8, (numero, altura, largura, gap, sobreposicao)

        gaps.append(gap)
        origem_y = destino_y

    assert all(gap > 0 for gap in gaps)
    print(
        f"{numero:>4} | {config['velocidade']:>10.1f} |"
        f" {len(config['plataformas']):>11} | {gaps}"
    )

print("\nValidação concluída: todas as plataformas têm sobreposição horizontal")
print("no instante calculado de aterrissagem, com a margem mínima configurada.")
