#!/usr/bin/env python3
import os
import tarfile
import time
from datetime import datetime

base_dir = "/caminho/do/profiles-data"
backup_dir = "/Área de trabalho/Backup_nfsen"

def compactar_diretorio(caminho, destino):
    nome = os.path.basename(caminho.rstrip('/'))
    arquivo_saida = os.path.join(destino, f"{nome}.tar.gz")
    with tarfile.open(arquivo_saida, "w:gz") as tar:
        tar.add(caminho, arcname=nome)
    return arquivo_saida

def executar_backup():
    os.makedirs(backup_dir, exist_ok=True)
    hoje = datetime.now().strftime("%Y/%m/%d")

    for raiz, dirs, _ in os.walk(base_dir):
        for d in dirs:
            if d.count("-") == 0:
                caminho = os.path.join(raiz, d)
                if hoje not in caminho:
                    destino = os.path.join(backup_dir, datetime.now().strftime("%Y-%m-%d"))
                    os.makedirs(destino, exist_ok=True)
                    arquivo = compactar_diretorio(caminho, destino)
                    for raiz2, _, arquivos in os.walk(caminho):
                        for arquivo in arquivos:
                            os.remove(os.path.join(raiz2, arquivo))
                    print(f"Backup concluído: {arquivo}")

if __name__ == "__main__":
    while True:
        executar_backup()
        time.sleep(86400)
