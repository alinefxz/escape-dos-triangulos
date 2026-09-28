import requests

def enviar_resultado_django(nome_jogador, pontuacao, mortes, fase):
    url = "http://127.0.0.1:8000/api/salvar_ranking/"
    dados = {
        "jogador": nome_jogador,
        "pontuacao": pontuacao,
        "mortes": mortes,
        "fase": fase
    }
    
    try:
        resposta = requests.post(url, json=dados)
        if resposta.status_code == 201:
            print("Resultado salvo com sucesso no ranking!")
    except requests.exceptions.RequestException as e:
        print("Erro ao conectar com o Django:", e)