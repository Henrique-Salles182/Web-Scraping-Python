import requests
import time
from pathlib import Path

def coletar_html_netimoveis():
    # URL EXATA que você validou no navegador
    url = "https://www.netimoveis.com/venda/minas-gerais/belo-horizonte/apartamento"
         #"https://www.netimoveis.com.br/venda/minas-gerais/belo-horizonte/apartamento"
    
    # Parâmetros que aparecem após a '?' na url do navegador
    params = {
        "tipo": "apartamento",
        "transacao": "venda",
        "localizacao": "BR-MG-belo-horizonte---",
        "pagina": "1"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
        "Referer": "https://www.netimoveis.com.br/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        print(f"🚀 Tentando acessar: {url}")
        # Usamos o params=params para que o requests monte a URL corretamente
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        response.raise_for_status()
        
        caminho_bronze = Path(__file__).parent.parent / "data" / "bronze"
        caminho_bronze.mkdir(parents=True, exist_ok=True)
        
        with open(caminho_bronze / "busca_bh.html", "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print(f"✅ Sucesso! Arquivo salvo em: {caminho_bronze}/busca_bh.html")

    except requests.exceptions.ConnectionError as e:
        print(f"❌ Erro de Conexão: O site bloqueou o script. Verifique se você consegue acessar o site pelo navegador da VM agora.")
    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    coletar_html_netimoveis()