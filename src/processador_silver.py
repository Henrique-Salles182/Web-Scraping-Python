import json
from pathlib import Path

def processar_dados_silver():
    # Definição de caminhos
    caminho_raiz = Path(__file__).parent.parent
    caminho_bronze = caminho_raiz / "data" / "bronze" / "dados_api_bh.json"
    caminho_silver = caminho_raiz / "data" / "silver"
    
    caminho_silver.mkdir(parents=True, exist_ok=True)

    # 1. Leitura do dado bruto
    with open(caminho_bronze, "r", encoding="utf-8") as f:
        dados_brutos = json.load(f)

    # A API retorna os imóveis dentro da chave 'lista'
    imoveis_raw = dados_brutos.get("lista", [])
    dados_limpos = []

    print(f"🧹 Iniciando limpeza de {len(imoveis_raw)} imóveis...")

    # 2. Transformação e Limpeza (Coração da Camada Silver)
    for item in imoveis_raw:
        # Extraímos apenas o que é relevante para o negócio
        registro = {
            "id": item.get("imovelSan_Id"),
            "tipo": item.get("tipoImovel"),
            "bairro": item.get("nomeBairro"),
            "cidade": item.get("nomeCidade"),
            "preco": float(item.get("valorImovel", 0)),
            "area": item.get("metragem"),
            "quartos": int(item.get("quartos") or 0),
            "vagas": int(item.get("vagaGaragem") or 0),
            "banheiros": int(item.get("banho") or 0),
            "url_relativa": item.get("urlItem")
        }
        dados_limpos.append(registro)

    # 3. Persistência na Silver
    arquivo_saida = caminho_silver / "imoveis_bh_limpos.json"
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        json.dump(dados_limpos, f, indent=4, ensure_ascii=False)

    print(f"✨ Sucesso! Dados limpos salvos em: {arquivo_saida}")

if __name__ == "__main__":
    processar_dados_silver()