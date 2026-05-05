from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.dialects.postgresql import insert  # Importe o insert específico do Postgres
from sqlalchemy.orm import declarative_base, sessionmaker
from pathlib import Path
import json

Base = declarative_base()

class ImovelGold(Base):
    __tablename__ = 'imoveis_bh'
    
    # Definimos o id_site como único para permitir o Upsert
    id_site = Column(Integer, primary_key=True) 
    tipo = Column(String)
    bairro = Column(String)
    cidade = Column(String)
    preco = Column(Float)
    area = Column(Float)
    quartos = Column(Integer)
    vagas = Column(Integer)
    banheiros = Column(Integer)
    url_relativa = Column(String)

# 2. Conexão com o Banco (Túnel Docker)
# formato: postgresql://usuario:senha@host:porta/banco
CONN_STR = "postgresql://admin:pythonic@localhost:5432/db_imoveis"
engine = create_engine(CONN_STR)
Session = sessionmaker(bind=engine)

def executar_upsert(session, lista_imoveis):
    for dados in lista_imoveis:
        # Preparamos a instrução de inserção
        stmt = insert(ImovelGold).values(
            id_site=dados['id'],
            tipo=dados['tipo'],
            bairro=dados['bairro'],
            cidade=dados['cidade'],
            preco=dados['preco'],
            area=dados['area'],
            quartos=dados['quartos'],
            vagas=dados['vagas'],
            banheiros=dados['banheiros'],
            url_relativa=dados['url_relativa']
        )

        # Definimos o que atualizar caso o id_site já exista
        stmt = stmt.on_conflict_do_update(
            index_elements=['id_site'], # Onde ocorre o conflito
            set_={
                'preco': stmt.excluded.preco,
                'area': stmt.excluded.area,
                'tipo': stmt.excluded.tipo,
                'url_relativa': stmt.excluded.url_relativa
                # Adicione outros campos que podem mudar com o tempo
            }
        )
        
        session.execute(stmt)
    session.commit()

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
        
        # Aqui acontece a mágica: delegamos a lógica de 'Update or Insert' 
        # para a nossa função especializada em PostgreSQL
        executar_upsert(session, dados_silver)

        print("✅ Dados sincronizados com sucesso via Docker!")
        
      
if __name__ == "__main__":
    carregar_gold()