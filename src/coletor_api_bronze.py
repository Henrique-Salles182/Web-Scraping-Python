import requests
import json
from pathlib import Path

def coletar_api_netimoveis():
    # URL base extraída do seu curl
    url = "https://www.netimoveis.com/pesquisa"
    
    # Parâmetros de busca (Query Params)
    params = {
        "tipo": "apartamento",
        "transacao": "venda",
        "localizacao": '[{"urlPais":"BR","urlEstado":"minas-gerais","urlCidade":"belo-horizonte","urlRegiao":"","urlBairro":"","urlLogradouro":"","idAgrupamento":"","tipo":"cidade","idLocalizacao":"BR-MG-belo-horizonte---"}]',
        "pagina": "1",
        "retornaPaginacao": "true",
        "outrasPags": "true"
    }

    # Cabeçalhos cruciais extraídos do seu print
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.netimoveis.com/venda/minas-gerais/belo-horizonte/apartamento",
        "Connection": "keep-alive",
        # COLOQUE AQUI O SEU COOKIE COMPLETO (AQUELE TEXTO GIGANTE QUE COMEÇA COM g_state...)
        "Cookie": 'g_state={"i_l":1,"i_ll":1777377655257,"i_b":"7yEluLKq/BMT+n1IIyuhnwQsjTAcBWPCgVswY8rIKvs","i_e":{"enable_itp_optimization":0},"i_et":1777374305487,"i_p":1777381509525}; _ga_65GSH2ZVEX=GS2.1.s1777374305$o1$g1$t1777377654$j60$l0$h0; _ga=GA1.1.328867375.1777374306; _gcl_au=1.1.362679546.1777374306; _fbp=fb.1.1777374306214.25315483232159764; _clck=18zy2l2%5E2%5Eg5l%5E0%5E2309; _clsk=6hotzk%5E1777377409044%5E12%5E1%5Ez.clarity.ms%2Fcollect; cookie_guidid=0f0d111f-4f51-4101-be92-a10885ac335f; _vstidss_=e592c077-60fd-4b68-bcf2-3198c529a5a2'
    }

    try:
        print("🚀 Fazendo a chamada oficial para a API...")
        response = requests.get(url, headers=headers, params=params, timeout=20)
        
        # Rigor técnico: mostrar o que está acontecendo se der erro
        if response.status_code != 200:
            print(f"⚠️ Erro {response.status_code}: {response.text[:200]}")
            return

        dados = response.json()
        
        caminho_bronze = Path(__file__).parent.parent / "data" / "bronze"
        caminho_bronze.mkdir(parents=True, exist_ok=True)

        with open(caminho_bronze / "dados_api_bh.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

        print(f"✅ SUCESSO! {len(dados.get('lista', []))} imóveis capturados na Bronze.")

    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    coletar_api_netimoveis()