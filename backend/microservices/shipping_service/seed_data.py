# Script para popular banco de dados com dados de teste
# Útil para desenvolvimento e testes

import sys
from database import SessionLocal, create_tables
from models import Endereco, Frete, TipoFrete, StatusFrete
from decimal import Decimal


def seed_database():
    """Popula banco de dados com dados de teste"""
    
    print("🌱 Iniciando seed do banco de dados...")
    
    # Cria tabelas
    create_tables()
    
    # Cria sessão
    db = SessionLocal()
    
    try:
        # Verifica se já existem dados
        existing_enderecos = db.query(Endereco).count()
        if existing_enderecos > 0:
            print(f"⚠️  Banco já possui {existing_enderecos} endereços. Limpando...")
            db.query(Frete).delete()
            db.query(Endereco).delete()
            db.commit()
        
        # ==========================================
        # ENDEREÇOS
        # ==========================================
        
        print("\n📍 Criando endereços de exemplo...")
        
        enderecos = [
            # Usuário 1
            Endereco(
                usuario_id=1,
                cep="01310100",
                logradouro="Avenida Paulista",
                numero="1578",
                bairro="Bela Vista",
                cidade="São Paulo",
                estado="SP",
                apelido="Casa",
                principal=True
            ),
            Endereco(
                usuario_id=1,
                cep="01310200",
                logradouro="Rua Augusta",
                numero="2690",
                complemento="Apto 501",
                bairro="Consolação",
                cidade="São Paulo",
                estado="SP",
                apelido="Trabalho",
                principal=False
            ),
            # Usuário 2
            Endereco(
                usuario_id=2,
                cep="20040020",
                logradouro="Praça Mahatma Gandhi",
                numero="2",
                bairro="Cinelândia",
                cidade="Rio de Janeiro",
                estado="RJ",
                apelido="Casa",
                principal=True
            ),
            Endereco(
                usuario_id=2,
                cep="22250040",
                logradouro="Avenida Atlântica",
                numero="1702",
                complemento="Cobertura",
                bairro="Copacabana",
                cidade="Rio de Janeiro",
                estado="RJ",
                apelido="Praia",
                principal=False
            ),
            # Usuário 3
            Endereco(
                usuario_id=3,
                cep="30140071",
                logradouro="Avenida Afonso Pena",
                numero="1500",
                complemento="Apto 302",
                bairro="Centro",
                cidade="Belo Horizonte",
                estado="MG",
                apelido="Casa",
                principal=True
            ),
            # Usuário 4
            Endereco(
                usuario_id=4,
                cep="80010130",
                logradouro="Rua XV de Novembro",
                numero="555",
                bairro="Centro",
                cidade="Curitiba",
                estado="PR",
                apelido="Escritório",
                principal=True
            ),
            # Usuário 5
            Endereco(
                usuario_id=5,
                cep="40020000",
                logradouro="Praça da Sé",
                numero="385",
                bairro="Centro",
                cidade="Salvador",
                estado="BA",
                apelido="Casa",
                principal=True
            ),
        ]
        
        db.add_all(enderecos)
        db.commit()
        print(f"✅ Criados {len(enderecos)} endereços")
        
        # ==========================================
        # FRETES (Exemplos históricos)
        # ==========================================
        
        print("\n📦 Criando fretes de exemplo...")
        
        fretes = [
            Frete(
                pedido_id=1,
                endereco_destino_id=1,
                tipo_frete=TipoFrete.ECONOMICO,
                status=StatusFrete.ENTREGUE,
                valor=Decimal("15.00"),
                peso_total=Decimal("1.500"),
                transportadora="PAC",
                prazo_entrega=10,
                codigo_rastreamento="BR123456789SP"
            ),
            Frete(
                pedido_id=2,
                endereco_destino_id=3,
                tipo_frete=TipoFrete.PADRAO,
                status=StatusFrete.EM_TRANSITO,
                valor=Decimal("0.00"),
                peso_total=Decimal("0.800"),
                transportadora="Sedex",
                prazo_entrega=20,
                codigo_rastreamento="BR987654321RJ"
            ),
            Frete(
                pedido_id=3,
                endereco_destino_id=5,
                tipo_frete=TipoFrete.ECONOMICO,
                status=StatusFrete.PENDENTE,
                valor=Decimal("15.00"),
                peso_total=Decimal("2.100"),
                transportadora="PAC",
                prazo_entrega=10
            ),
        ]
        
        db.add_all(fretes)
        db.commit()
        print(f"✅ Criados {len(fretes)} fretes")
        
        # ==========================================
        # RESUMO
        # ==========================================
        
        print("\n" + "=" * 60)
        print("✅ Seed concluído com sucesso!")
        print("=" * 60)
        print(f"📍 Endereços criados: {len(enderecos)}")
        print(f"📦 Fretes criados: {len(fretes)}")
        print("=" * 60)
        
        # Exibe alguns exemplos
        print("\n📋 Exemplos de endereços criados:")
        for endereco in enderecos[:3]:
            print(f"  - ID {endereco.id}: {endereco.logradouro}, {endereco.numero} - {endereco.cidade}/{endereco.estado}")
        
        print("\n📋 Exemplos de fretes criados:")
        for frete in fretes:
            print(f"  - ID {frete.id}: Pedido #{frete.pedido_id} - {frete.status.value} - R$ {frete.valor}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro ao popular banco de dados: {str(e)}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
