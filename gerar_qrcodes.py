"""
gerar_qrcodes.py
----------------
Execute este script UMA VEZ para gerar os QR codes de cada livro.
Os QR codes são salvos como imagens PNG na pasta 'qrcodes/'.
Depois, você pode imprimi-los e colá-los nos livros físicos.

Como usar:
  1. Abra o terminal (Prompt de Comando) na pasta do projeto
  2. Execute:  python gerar_qrcodes.py
  3. Imprima as imagens da pasta 'qrcodes/'
"""

import os
import qrcode
import pandas as pd

# ── Configurações ─────────────────────────────────────────────────────────
# Cole aqui a URL pública do seu app no Streamlit Cloud:
URL_DO_APP = "https://SEU-APP.streamlit.app"

ARQUIVO_LIVROS = "livros.xlsx"
PASTA_SAIDA    = "qrcodes"

# ── Geração ───────────────────────────────────────────────────────────────
os.makedirs(PASTA_SAIDA, exist_ok=True)

if not os.path.exists(ARQUIVO_LIVROS):
    print(f"Arquivo '{ARQUIVO_LIVROS}' não encontrado. Rode o app.py primeiro.")
    exit()

df = pd.read_excel(ARQUIVO_LIVROS)

for _, livro in df.iterrows():
    titulo_busca = livro["titulo"].replace(" ", "+")
    url = f"{URL_DO_APP}?busca={titulo_busca}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#3b2a1a", back_color="white")

    # Nome do arquivo: ID + título (sem caracteres especiais)
    nome_arquivo = f"{int(livro['id']):03d}_{livro['titulo'][:40]}.png"
    nome_arquivo = "".join(c if c.isalnum() or c in "._- " else "_" for c in nome_arquivo)
    caminho = os.path.join(PASTA_SAIDA, nome_arquivo)

    img.save(caminho)
    print(f"✅ QR gerado: {caminho}  →  {url}")

print(f"\n🎉 {len(df)} QR codes salvos na pasta '{PASTA_SAIDA}/'")
print("Imprima, recorte e cole nos livros físicos!")
