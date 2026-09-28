import pygame
import json
import os
from scripts.jogador import Jogador
from scripts.obstaculos import Triangulo, LinhaChegada, Bloco, Buraco, Plataforma
from scripts.interfaces import Texto, Botao, CaixaTexto

ARQUIVO_RANKING = "banco_ranking.json"

def carregar_dados():
    if os.path.exists(ARQUIVO_RANKING):
        with open(ARQUIVO_RANKING, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_dados_no_arquivo():
    with open(ARQUIVO_RANKING, "w", encoding="utf-8") as f:
        json.dump(dados_jogo["ranking"], f, indent=4)

dados_jogo = {
    "nome": "",
    "pontos": 0,
    "tempo_frames": 0,
    "mortes": 0,
    "fase_salva": 1,
    "jogo_em_andamento": False, 
    "ranking": carregar_dados() 
}

class Menu:
    def __init__(self, tela):
        self.tela = tela
        self.titulo = Texto(tela, "ESCAPE DOS TRIÂNGULOS", "centro", 60, (255, 20, 147), 40)
        
    def atualizar(self, eventos):
        self.titulo.desenhar()
        
        y_pos = 140
        botoes = []
        
        if dados_jogo["jogo_em_andamento"] and dados_jogo["nome"]:
            btn_retomar = Botao(self.tela, "RETOMAR", "centro", y_pos, 30, (20, 20, 20), (0, 255, 0))
            botoes.append(('partida', btn_retomar))
            y_pos += 60

        btn_jogar = Botao(self.tela, "NOVO JOGO", "centro", y_pos, 30, (20, 20, 20), (255, 20, 147))
        botoes.append(('nome_input', btn_jogar))
        y_pos += 60

        if dados_jogo["nome"]:
            btn_trocar = Botao(self.tela, f"JOGADOR: {dados_jogo['nome']} (TROCAR)", "centro", y_pos, 25, (20, 20, 20), (255, 165, 0))
            botoes.append(('nome_input', btn_trocar))
            y_pos += 60

        btn_ranking = Botao(self.tela, "RANKING", "centro", y_pos, 30, (20, 20, 20), (0, 255, 255))
        botoes.append(('ranking', btn_ranking))

        for proxima_cena, botao in botoes:
            botao.desenhar()
            if botao.get_click(eventos):
                if proxima_cena == 'nome_input':
                    dados_jogo["jogo_em_andamento"] = False
                return proxima_cena
            
        return 'menu'

class TelaNome:
    def __init__(self, tela):
        self.tela = tela
        self.instrucao = Texto(tela, "DIGITE SEU NOME:", "centro", 100, (255, 255, 255), 30)
        self.caixa_texto = CaixaTexto(tela, "centro", 150, 250, 40)
        self.botao_iniciar = Botao(tela, "INICIAR JOGO", "centro", 250, 30, (20, 20, 20), (255, 20, 147))
        self.botao_voltar = Botao(tela, "VOLTAR", "centro", 320, 20, (20, 20, 20), (200, 200, 200))

    def atualizar(self, eventos):
        self.instrucao.desenhar()
        self.caixa_texto.tratar_eventos(eventos)
        self.caixa_texto.desenhar()
        self.botao_iniciar.desenhar()
        self.botao_voltar.desenhar()

        if self.botao_iniciar.get_click(eventos) and len(self.caixa_texto.texto) > 0:
            dados_jogo["nome"] = self.caixa_texto.texto.upper()
            dados_jogo["pontos"] = 0
            dados_jogo["tempo_frames"] = 0
            dados_jogo["mortes"] = 0 
            dados_jogo["fase_salva"] = 1
            dados_jogo["jogo_em_andamento"] = True
            
            # Reseta os dados da partida diretamente aqui para evitar erros no main.py
            global instancia_partida_refeita
            return 'partida'
            
        if self.botao_voltar.get_click(eventos):
            return 'menu'
        return 'nome_input'

class Partida:
    def __init__(self, tela):
        self.tela = tela
        self.jogador = Jogador(tela, 100, 270)
        self.fase_atual = 1
        self.texto_hud = Texto(self.tela, "", 10, 10, (255, 255, 255), 20)
        self.texto_dicas = Texto(self.tela, "Atalhos: [R] Reiniciar  |  [M] Voltar ao Menu", 10, 35, (150, 150, 150), 16)
        self.reiniciar_fase()

    def reiniciar_fase(self, nova_partida=False):
        if nova_partida:
            self.fase_atual = dados_jogo["fase_salva"]
            
        self.jogador.posicao = [100, 270]
        self.jogador.velocidade_y = 0
        self.jogador.morto = False
        self.jogador.rotacao = 0
        self.obstaculos = []
        
        vel_fase = 8 + (self.fase_atual - 1)
        
        if self.fase_atual == 1:
            layout = [(Triangulo, x) for x in [800, 1400, 2000, 2600, 3100, 3600, 4100, 4600, 5200, 5800, 6400]]
            fim = 7000

        elif self.fase_atual == 2:
            layout = [(Triangulo, 800), (Triangulo, 1200), (Triangulo, 1230),
                      (Buraco, 1700, 80), (Triangulo, 2100), (Triangulo, 2130),
                      (Buraco, 2600, 90), (Bloco, 3000), (Triangulo, 3400),
                      (Triangulo, 3430), (Buraco, 3900, 100), (Bloco, 4400),
                      (Triangulo, 4430), (Triangulo, 4800), (Triangulo, 5200),
                      (Triangulo, 5230), (Buraco, 5700, 110), (Bloco, 6200)]
            fim = 6800

        elif self.fase_atual == 3:
            layout = [
                (Bloco, 800), (Plataforma, 1200, 240, 150), (Buraco, 1200, 150), 
                (Triangulo, 1800), (Triangulo, 1830), (Triangulo, 1860), 
                (Plataforma, 2400, 230, 200), (Buraco, 2400, 200),
                (Buraco, 2900, 120), (Bloco, 3400), (Plataforma, 3800, 240, 100), (Buraco, 3800, 100),
                (Triangulo, 4400), (Triangulo, 4430), (Triangulo, 4460), 
                (Plataforma, 5000, 240, 120), (Triangulo, 5030), (Triangulo, 5060),
                (Bloco, 5600), (Buraco, 6000, 140), (Bloco, 6200)
            ]
            fim = 6600

        elif self.fase_atual == 4:
            layout = [
                (Triangulo, 800), (Buraco, 1100, 130), (Plataforma, 1160, 240, 50),
                (Bloco, 1600), (Triangulo, 1630), (Triangulo, 2000), (Triangulo, 2030), (Triangulo, 2060), (Triangulo, 2090), 
                (Plataforma, 2600, 240, 300), (Triangulo, 2700, 240), (Triangulo, 2800, 240), 
                (Buraco, 2600, 300), 
                (Bloco, 3400), (Buraco, 3430, 80), (Bloco, 3510),
                (Plataforma, 3900, 230, 100), (Triangulo, 3930), (Triangulo, 3960),
                (Triangulo, 4500), (Triangulo, 4530), (Triangulo, 4560),
                (Buraco, 5000, 180), (Plataforma, 5080, 240, 50), (Bloco, 5600)
            ]
            fim = 6200

        elif self.fase_atual == 5:
            layout = [
                (Bloco, 800), (Buraco, 830, 150), (Plataforma, 920, 240, 60),
                (Triangulo, 1350), (Triangulo, 1380), (Triangulo, 1410),
                (Plataforma, 1800, 240, 250), (Triangulo, 1920, 240), 
                (Buraco, 1800, 250), 
                (Bloco, 2400), (Bloco, 2430), (Triangulo, 2460),
                (Buraco, 2900, 250), (Plataforma, 2950, 240, 50), (Plataforma, 3080, 240, 50), 
                (Triangulo, 3500), (Triangulo, 3530), (Triangulo, 3560), (Triangulo, 3590),
                (Bloco, 4000), 
                (Plataforma, 4300, 240, 400), (Triangulo, 4450, 240), (Triangulo, 4600, 240),
                (Buraco, 4300, 400),
                (Triangulo, 5100), (Triangulo, 5130), (Triangulo, 5160),
                (Plataforma, 5600, 230, 80), (Triangulo, 5620), (Triangulo, 5650),
                (Buraco, 6100, 200), (Plataforma, 6150, 240, 60),
                (Bloco, 6600), (Buraco, 6630, 160), (Triangulo, 6950) 
            ]
            fim = 7400
            
        for Tipo, x, *args in layout:
            if Tipo == Plataforma:
                self.obstaculos.append(Plataforma(self.tela, x, args[0], args[1], velocidade=vel_fase))
            elif Tipo == Buraco:
                self.obstaculos.append(Buraco(self.tela, x, 300, largura=args[0], velocidade=vel_fase))
            elif Tipo == Triangulo:
                y_pos = args[0] if args else 300
                self.obstaculos.append(Triangulo(self.tela, x, y_pos, velocidade=vel_fase))
            else:
                self.obstaculos.append(Bloco(self.tela, x, 300, velocidade=vel_fase))
                
        self.linha_chegada = LinhaChegada(self.tela, fim, 300, velocidade=vel_fase)

    def morrer(self):
        if not self.jogador.morto:
            self.salvar_ranking()
            self.jogador.morto = True
            self.jogador.velocidade_y = -8
            dados_jogo["mortes"] += 1
            dados_jogo["pontos"] = max(0, dados_jogo["pontos"] - 25)

    def salvar_ranking(self):
        nome = dados_jogo["nome"]
        if not nome:
            return
        pontos = dados_jogo["pontos"]
        tempo = dados_jogo["tempo_frames"] // 60
        mortes = dados_jogo["mortes"]
        
        if nome not in dados_jogo["ranking"] or pontos > dados_jogo["ranking"][nome]["pontos"]:
            dados_jogo["ranking"][nome] = {"pontos": pontos, "tempo": tempo, "mortes": mortes}
            salvar_dados_no_arquivo()

    def desenhar_cenario(self):
        pygame.draw.line(self.tela, (255, 20, 147), (0, 300), (800, 300), 4)

    def atualizar(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    self.reiniciar_fase()
                elif evento.key == pygame.K_m:
                    self.salvar_ranking()
                    dados_jogo["fase_salva"] = self.fase_atual
                    return 'menu'

        plataformas = [obs for obs in self.obstaculos if isinstance(obs, Plataforma)]
        self.jogador.atualizar(plataformas)
        
        dados_jogo["tempo_frames"] += 1
        tempo_segundos = dados_jogo["tempo_frames"] // 60
        
        self.desenhar_cenario()
        self.jogador.desenhar()
        
        hud = f"Fase: {self.fase_atual}/5 | {dados_jogo['nome']} | Pts: {dados_jogo['pontos']} | Mortes: {dados_jogo['mortes']} | Tempo: {tempo_segundos}s"
        self.texto_hud.atualizarTexto(hud)
        self.texto_hud.desenhar()
        self.texto_dicas.desenhar()

        for obs in self.obstaculos:
            if not self.jogador.morto:
                obs.atualizar()
            obs.desenhar()
            
            if not self.jogador.morto:
                limite_passou = getattr(obs, 'largura', getattr(obs, 'tamanho', 30))
                if obs.x + limite_passou < self.jogador.rect.x and not obs.passou:
                    dados_jogo["pontos"] += 10
                    obs.passou = True
                
                if obs.detectarColisao(self.jogador.getRect()):
                    self.morrer()
                    
        self.linha_chegada.atualizar()
        self.linha_chegada.desenhar()
        
        if self.jogador.morto:
            if self.jogador.posicao[1] > 500:
                self.reiniciar_fase()
            return 'partida'
        
        if self.linha_chegada.x < self.jogador.rect.x:
            dados_jogo["pontos"] += 100 
            if self.fase_atual < 5:
                self.salvar_ranking()
                self.fase_atual += 1
                self.reiniciar_fase()
            else:
                self.salvar_ranking()
                dados_jogo["jogo_em_andamento"] = False 
                self.fase_atual = 1
                return 'ranking'

        return 'partida'

class TelaRanking:
    def __init__(self, tela):
        self.tela = tela
        self.titulo = Texto(tela, "RANKING LOCAL", "centro", 50, (0, 255, 255), 40)
        self.botao_voltar = Botao(tela, "VOLTAR AO MENU", "centro", 320, 25, (20, 20, 20), (255, 20, 147))
        self.fonte_ranking = pygame.font.SysFont("Arial", 25)

    def atualizar(self, eventos):
        self.titulo.desenhar()
        self.botao_voltar.desenhar()
        
        lista_ranking = [(nome, d["pontos"], d["tempo"], d.get("mortes", 0)) for nome, d in dados_jogo["ranking"].items()]
        ranking_ordenado = sorted(lista_ranking, key=lambda x: (-x[1], x[3], x[2]))
        
        y = 120
        for i, (nome, pontos, tempo, mortes) in enumerate(ranking_ordenado[:5]): 
            texto = f"{i+1}º - {nome} | Pts: {pontos} | Mortes: {mortes} | Tempo: {tempo}s"
            txt_surface = self.fonte_ranking.render(texto, True, (255, 255, 255))
            pos_x = self.tela.get_width() // 2 - txt_surface.get_width() // 2
            self.tela.blit(txt_surface, (pos_x, y))
            y += 40

        if len(ranking_ordenado) == 0:
            txt_surface = self.fonte_ranking.render("Nenhum resultado ainda.", True, (150, 150, 150))
            self.tela.blit(txt_surface, (self.tela.get_width() // 2 - txt_surface.get_width() // 2, 150))

        if self.botao_voltar.get_click(eventos):
            return 'menu'
            
        return 'ranking'