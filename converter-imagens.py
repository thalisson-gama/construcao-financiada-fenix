"""
Conversor PNG/JPG -> WebP para a pasta da Fenix.

Uso:
    python converter-imagens.py

Converte todas as imagens .png/.jpg/.jpeg do diretorio atual para .webp
mantendo qualidade visual alta (92) e transparencia (quando RGBA).
A logo nao e reprocessada (logo.webp ja foi gerada).

Mapeamento esperado (ajuste o nome do arquivo de origem para que o webp
gerado bata com o caminho usado no index.html):

    hero-bg.png            -> hero-bg.webp
    exemplo-01.jpg         -> exemplo-01.webp
    exemplo-02.jpg         -> exemplo-02.webp
    exemplo-03.jpg         -> exemplo-03.webp
    obra-01.jpg ... obra-10.jpg -> obra-01.webp ... obra-10.webp
    engenheiro-fenix.jpg   -> engenheiro-fenix.webp
"""
from PIL import Image
from pathlib import Path

AQUI = Path(__file__).resolve().parent
EXTENSOES = {'.png', '.jpg', '.jpeg'}
QUALIDADE = 92

convertidos = 0
ignorados = 0

for arq in sorted(AQUI.iterdir()):
    if arq.suffix.lower() not in EXTENSOES:
        continue
    if arq.stem.lower() == 'logo':
        ignorados += 1
        continue

    destino = arq.with_suffix('.webp')
    try:
        img = Image.open(arq)
        params = {'quality': QUALIDADE, 'method': 6}
        # Preserva transparencia em PNG RGBA
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGBA')
        else:
            img = img.convert('RGB')
        img.save(destino, 'WEBP', **params)
        antes = arq.stat().st_size
        depois = destino.stat().st_size
        reducao = (1 - depois / antes) * 100 if antes else 0
        print(f'OK  {arq.name:40s} -> {destino.name:30s} '
              f'{antes/1024:7.1f} KB -> {depois/1024:7.1f} KB '
              f'(-{reducao:.0f}%)')
        convertidos += 1
    except Exception as e:
        print(f'ERRO {arq.name}: {e}')

print(f'\nConcluido: {convertidos} convertidas, {ignorados} ignoradas (logo).')
