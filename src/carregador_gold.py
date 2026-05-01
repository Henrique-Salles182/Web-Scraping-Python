from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import declarative_base, sessionmaker
from pathlib import Path
import json

# 1. Configuração do Modelo (O esquema da Tabela)
Base = declarative_base()

class ImovelGold(Base):
    __tablename__ = 'imoveis_bh'
    
    id_unico = Column(Integer, primary_key=True)
    id_site = Column(Integer)
    bairro = Column(String)
    preco = Column(Float)
    area = Column(Float)
    quartos = Column(Integer)

# 2. Conexão com o Banco (Túnel Docker)
# formato: postgresql://usuario:senha@host:porta/banco
CONN_STR = "postgresql://admin:pythonic@localhost:5432/db_imoveis"
engine = create_engine(CONN_STR)
Session = sessionmaker(bind=engine)

def carregar_gold():
    # Caminho da Silver
    caminho_silver = Path(__file__).parent.parent / "data" / "silver" / "imoveis_bh_limpos.json"
    
    if not caminho_silver.exists():
        print("❌ Dados da Silver não encontrados!")
        return

    # Criar a tabela se não existir
    Base.metadata.create_all(engine)

    with open(caminho_silver, "r", encoding="utf-8") as f:
        dados_silver = json.load(f)

    with Session() as session:
        print(f"🚀 Carregando {len(dados_silver)} registros na Camada Gold...")
        
        for item in dados_silver:
            imovel = ImovelGold(
                id_site=item.get("id"),
                bairro=item.get("bairro"),
                preco=item.get("preco"),
                area=item.get("area"),
                quartos=item.get("quartos")
            )
            session.add(imovel)
        
        session.commit() # Salva tudo de uma vez
        print("✅ Dados persistidos com sucesso no PostgreSQL via Docker!")

if __name__ == "__main__":
    carregar_gold()