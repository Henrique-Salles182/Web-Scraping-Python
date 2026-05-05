import json
import re #importao para expresses regulares, caso precise limpar strings mais complexas
from pathlib import Path

def limpar_numero(valor: any) -> float:
    """
    Esta função é o 'filtro de impurezas'. 
    Ela recebe qualquer 'sujeira' (ex: '80 m²', 'R$ 500.000,00') 
    e devolve apenas o valor numérico puro.
    """
    if valor is None:
        return 0.0
    
    # Converte para string e remove tudo que NÃO for número, vírgula ou ponto
    texto = str(valor).strip()
    apenas_numeros = re.sub(r'[^\d,.]', '', texto)
    
    if not apenas_numeros:
        return 0.0
    
    # Padronização: transforma a vírgula brasileira em ponto decimal (padrão float)
    if ',' in apenas_numeros and '.' in apenas_numeros:
        # Caso tenha ambos (ex: 1.250,50), remove o ponto de milhar
        apenas_numeros = apenas_numeros.replace('.', '').replace(',', '.')
    else:
        apenas_numeros = apenas_numeros.replace(',', '.')
        
    try:
        return float(apenas_numeros)
    except ValueError:
        return 0.0

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
            # Usamos .get() com um valor padrão para evitar 'null' visual no JSON
            "tipo": item.get("tipoImovel1", "Nao informado"),
            "bairro": item.get("nomeBairro"),
            "cidade": item.get("nomeCidade"),
            "preco": limpar_numero(item.get("valorImovel")),
            "area": limpar_numero(item.get("areaRealPrivativa")), # Ajustado para areaTotal, que parece ser mais consistente
            "quartos": int(item.get("quartos") or 0),
            "vagas": int(item.get("vagaGaragem") or 0),
            "banheiros": int(item.get("banho") or 0),
            "url_relativa": item.get("urlDetalheImovel")
        }
        dados_limpos.append(registro)

    # 3. Persistência na Silver
    arquivo_saida = caminho_silver / "imoveis_bh_limpos.json"
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        json.dump(dados_limpos, f, indent=4, ensure_ascii=False)

    print(f"✨ Sucesso! Dados limpos salvos em: {arquivo_saida}")

if __name__ == "__main__":
    processar_dados_silver()