"""
Conversor PNG/JPG -> WebP para a pasta da Fenix.

Uso (a partir da raiz do projeto):
    python tools/converter-imagens.py

Le arquivos .png/.jpg/.jpeg que voce dropar na raiz do projeto
e grava versoes otimizadas em .webp dentro de assets/img/.

Mapeamento esperado dos nomes (renomeie os arquivos antes de rodar
para que o nome do .webp gerado bata com o que o index.html espera):

    logo.png              -> assets/img/logo.webp
    favicon.png           -> assets/img/favicon.webp
    hero-bg.jpg           -> assets/img/hero-bg.webp
    engenheiro-fenix.jpg  -> assets/img/engenheiro-fenix.webp
    exemplo-01.jpg ... 03 -> assets/img/exemplo-0X.webp
    obra-01.jpg ... 06    -> assets/img/obra-0X.webp

Apos a conversao, o arquivo original e movido para assets/img/_originais/
(criada automaticamente) para nao ficar lixo na raiz.
"""
from PIL import Image
from pathlib import Path
import shutil

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / 'assets' / 'img'
BACKUP  = DESTINO / '_originais'
EXTENSOES = {'.png', '.jpg', '.jpeg'}
MAX_W = 1200
QUALIDADE = 86  # 0-100; 86 e equilibrio ideal para fotos

DESTINO.mkdir(parents=True, exist_ok=True)
BACKUP.mkdir(parents=True, exist_ok=True)

convertidos = 0

for arq in sorted(RAIZ.iterdir()):
    if not arq.is_file() or arq.suffix.lower() not in EXTENSOES:
        continue

    destino = DESTINO / (arq.stem + '.webp')
    try:
        img = Image.open(arq)
        if img.width > MAX_W:
            ratio = MAX_W / img.width
            img = img.resize((MAX_W, int(img.height * ratio)), Image.LANCZOS)
        # PNGs com transparencia (logo, favicon) preservam o canal alfa
        if img.mode in ('RGBA', 'LA', 'P') and arq.suffix.lower() == '.png':
            img = img.convert('RGBA')
            params = {'quality': 92, 'method': 6}
        else:
            img = img.convert('RGB')
            params = {'quality': QUALIDADE, 'method': 6}

        img.save(destino, 'WEBP', **params)

        antes = arq.stat().st_size
        depois = destino.stat().st_size
        reducao = (1 - depois / antes) * 100 if antes else 0
        print(f'OK  {arq.name:32s} -> {destino.name:28s} '
              f'{antes/1024:7.1f} KB -> {depois/1024:7.1f} KB '
              f'(-{reducao:.0f}%)')

        # Move o original para backup
        shutil.move(str(arq), str(BACKUP / arq.name))
        convertidos += 1
    except Exception as e:
        print(f'ERRO {arq.name}: {e}')

if convertidos:
    print(f'\nConcluido: {convertidos} convertidas. Originais em assets/img/_originais/')
else:
    print('\nNenhum arquivo .png/.jpg/.jpeg encontrado na raiz.')
    print(f'Largue os arquivos em {RAIZ} e rode novamente.')
