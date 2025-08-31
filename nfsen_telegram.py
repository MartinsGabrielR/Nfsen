#!/usr/bin/env python3
import os
import time
import subprocess
import socket
from datetime import datetime
import requests
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_destino = os.getenv("TELEGRAM_CHAT_ID")

# Configurações gerais
diretorio_base = "/opt/nfsen/profiles-data/live/Firewall"
intervalo_monitoramento = 600  # 10 minutos
tentativas_max = 3
atraso_tentativa = 60
bot_ativo = True

def conexao_internet():
    try:
        socket.create_connection(("api.telegram.org", 443), timeout=5)
        return True
    except OSError:
        return False

def enviar_mensagem(texto, destino=chat_destino):
    for _ in range(tentativas_max):
        try:
            if not conexao_internet():
                raise ConnectionError("Sem internet")
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            requests.post(url, json={'chat_id': destino, 'text': texto}, timeout=10)
            return
        except Exception:
            time.sleep(atraso_tentativa)

def enviar_imagem(caminho_img, legenda, destino=chat_destino):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        with open(caminho_img, 'rb') as foto:
            requests.post(url, files={'photo': foto}, data={'chat_id': destino, 'caption': legenda})
    except Exception:
        pass

def arquivo_mais_recente():
    arquivos = []
    for raiz, _, nomes in os.walk(diretorio_base):
        for nome in nomes:
            if nome.startswith('nfcapd.20'):
                caminho = os.path.join(raiz, nome)
                arquivos.append((os.path.getmtime(caminho), caminho))
    if arquivos:
        arquivos.sort()
        return arquivos[-1][1]
    return None

def gerar_relatorio(caminho_arq, destino=chat_destino):
    nome_arq = os.path.basename(caminho_arq)
    ano, mes, dia = nome_arq[7:11], nome_arq[11:13], nome_arq[13:15]
    entrada = f"{ano}/{mes}/{dia}/{nome_arq}"

    cmd = f"nfdump -M /opt/nfsen/profiles-data/live/Firewall:MaquinaPrincipal:VM -T -r {entrada} -n 10 -s ip/flows"
    tmp = "/tmp/nfsen_bot"
    os.makedirs(tmp, exist_ok=True)
    saida_txt = os.path.join(tmp, "saida.txt")
    saida_img = os.path.join(tmp, "saida.png")

    with open(saida_txt, 'w') as f:
        subprocess.run(cmd, shell=True, stdout=f, stderr=subprocess.STDOUT)

    with open(saida_txt, 'r') as f:
        conteudo = f.read()

    if conteudo.strip():
        font = ImageFont.load_default()
        linhas = conteudo.splitlines()
        largura, altura = 800, 20 * len(linhas) + 50
        imagem = Image.new('RGB', (largura, altura), color='black')
        draw = ImageDraw.Draw(imagem)
        y = 10
        for linha in linhas:
            draw.text((10, y), linha, fill='white', font=font)
            y += 20
        imagem.save(saida_img)

        legenda = f"📊 Relatório NfSen - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        enviar_imagem(saida_img, legenda, destino)

def ciclo_monitoramento():
    enviar_mensagem("🔔 Monitoramento NfSen ativo")
    while bot_ativo:
        ultimo = arquivo_mais_recente()
        if ultimo:
            gerar_relatorio(ultimo)
        time.sleep(intervalo_monitoramento)

if __name__ == "__main__":
    try:
        ciclo_monitoramento()
    except KeyboardInterrupt:
        enviar_mensagem("🔴 Monitor desligado")
