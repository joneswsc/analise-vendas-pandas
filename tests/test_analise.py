import pandas as pd
import pytest

from analise import (
    carregar_vendas,
    faturamento_por_categoria,
    faturamento_total,
    formatar_moeda,
    gerar_relatorio,
    salvar_relatorio,
    top_produtos,
)
from gerar_dados import gerar_vendas, salvar_csv


@pytest.fixture
def csv_simples(tmp_path):
    """CSV pequeno com valores conhecidos para conferir os cálculos."""
    df = pd.DataFrame(
        {
            "produto": ["A", "B", "A", "C", "D", "E", "F"],
            "categoria": ["X", "Y", "X", "Y", "Z", "Z", "Z"],
            "quantidade": [2, 1, 3, 4, 1, 6, 2],
            "preco_unitario": [10.0, 100.0, 10.0, 5.0, 50.0, 1.0, 2.5],
        }
    )
    caminho = tmp_path / "vendas.csv"
    df.to_csv(caminho, index=False)
    return caminho


@pytest.fixture
def vendas(csv_simples):
    return carregar_vendas(csv_simples)


# --- gerar_dados ---

def test_gera_100_vendas_com_colunas_esperadas():
    df = gerar_vendas()
    assert len(df) == 100
    assert {"id_venda", "data", "produto", "categoria", "quantidade", "preco_unitario"} <= set(df.columns)
    assert (df["quantidade"] > 0).all()
    assert (df["preco_unitario"] > 0).all()


def test_geracao_e_reprodutivel():
    pd.testing.assert_frame_equal(gerar_vendas(seed=1), gerar_vendas(seed=1))


def test_salvar_csv(tmp_path):
    caminho = salvar_csv(gerar_vendas(10), tmp_path / "v.csv")
    assert len(pd.read_csv(caminho)) == 10


# --- análise ---

def test_carregar_calcula_faturamento(vendas):
    assert vendas["faturamento"].tolist() == [20.0, 100.0, 30.0, 20.0, 50.0, 6.0, 5.0]


def test_carregar_rejeita_csv_sem_colunas(tmp_path):
    caminho = tmp_path / "ruim.csv"
    pd.DataFrame({"produto": ["A"]}).to_csv(caminho, index=False)
    with pytest.raises(ValueError, match="Colunas ausentes"):
        carregar_vendas(caminho)


def test_faturamento_total(vendas):
    assert faturamento_total(vendas) == 231.0


def test_faturamento_por_categoria(vendas):
    resultado = faturamento_por_categoria(vendas)
    assert resultado.to_dict() == {"Y": 120.0, "Z": 61.0, "X": 50.0}
    assert list(resultado.index) == ["Y", "Z", "X"]  # ordenado do maior para o menor


def test_soma_das_categorias_igual_ao_total(vendas):
    assert faturamento_por_categoria(vendas).sum() == pytest.approx(faturamento_total(vendas))


def test_top_produtos(vendas):
    top = top_produtos(vendas)
    assert len(top) == 5
    assert top.index[0] == "E"  # 6 unidades
    assert top["A"] == 5  # 2 + 3 somados
    assert list(top.values) == sorted(top.values, reverse=True)


def test_top_produtos_desempata_em_ordem_alfabetica(vendas):
    # B e D empatam com 1 unidade na 5ª posição; B vem antes por ordem alfabética.
    assert list(top_produtos(vendas).index) == ["E", "A", "C", "F", "B"]


def test_formatar_moeda():
    assert formatar_moeda(1234567.891) == "R$ 1.234.567,89"
    assert formatar_moeda(0) == "R$ 0,00"


# --- relatório ---

def test_relatorio_markdown(vendas):
    md = gerar_relatorio(vendas)
    assert md.startswith("# Relatório de Vendas")
    assert "## Faturamento por categoria" in md
    assert "## Top 5 produtos mais vendidos" in md
    assert "R$ 231,00" in md


def test_relatorio_porcentagem_no_formato_brasileiro(vendas):
    md = gerar_relatorio(vendas)
    assert "| Y | R$ 120,00 | 51,9% |" in md  # 120 / 231
    assert "| X | R$ 50,00 | 21,6% |" in md  # 50 / 231


def test_salvar_relatorio(tmp_path):
    caminho = salvar_relatorio("# Teste\n", tmp_path / "r.md")
    assert caminho.read_text(encoding="utf-8") == "# Teste\n"
