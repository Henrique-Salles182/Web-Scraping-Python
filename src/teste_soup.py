from bs4 import BeautifulSoup
from pathlib import Path
import json

caminho_bronze = Path(__file__).parent.parent / "data" / "bronze" / "busca_bh.html"
with open(caminho_bronze, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("🔍 Procurando dados estruturados escondidos...")

# Procuramos por scripts que possam conter o JSON dos imóveis
scripts = soup.find_all("script")

for i, s in enumerate(scripts):
    if s.string and "valorImovel" in s.string:
        print(f"✅ Achei dados potenciais no Script #{i}!")
        print(s.string[:500]) # Mostra os primeiros 500 caracteres