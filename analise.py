"""Análise de vendas: faturamento, top produtos e relatório em Markdown."""

from pathlib import Path

import pandas as pd

COLUNAS_OBRIGATORIAS = {"produto", "categoria", "quantidade", "preco_unitario"}


def carregar_vendas(caminho: str | Path) -> pd.DataFrame:
    df = pd.read_csv(caminho)
    faltando = COLUNAS_OBRIGATORIAS - set(df.columns)
    if faltando:
        raise ValueError(f"Colunas ausentes no CSV: {sorted(faltando)}")
    df["faturamento"] = df["quantidade"] * df["preco_unitario"]
    return df


def faturamento_total(df: pd.DataFrame) -> float:
    return round(float(df["faturamento"].sum()), 2)


def faturamento_por_categoria(df: pd.DataFrame) -> pd.Series:
    """Faturamento por categoria, do maior para o menor."""
    return df.groupby("categoria")["faturamento"].sum().round(2).sort_values(ascending=False)


def top_produtos(df: pd.DataFrame, n: int = 5) -> pd.Series:
    """Os `n` produtos com maior quantidade vendida."""
    return df.groupby("produto")["quantidade"].sum().sort_values(ascending=False).head(n)


def formatar_moeda(valor: float) -> str:
    """Formata no padrão brasileiro: 1234.5 -> 'R$ 1.234,50'."""
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def gerar_relatorio(df: pd.DataFrame) -> str:
    total = faturamento_total(df)
    linhas = [
        "# Relatório de Vendas",
        "",
        f"- **Total de vendas:** {len(df)}",
        f"- **Itens vendidos:** {int(df['quantidade'].sum())}",
        f"- **Faturamento total:** {formatar_moeda(total)}",
        "",
        "## Faturamento por categoria",
        "",
        "| Categoria | Faturamento | % do total |",
        "|---|---:|---:|",
    ]
    for categoria, valor in faturamento_por_categoria(df).items():
        linhas.append(f"| {categoria} | {formatar_moeda(valor)} | {f'{valor / total:.1%}'.replace('.', ',')} |")

    linhas += [
        "",
        "## Top 5 produtos mais vendidos",
        "",
        "| # | Produto | Quantidade |",
        "|---:|---|---:|",
    ]
    for posicao, (produto, qtd) in enumerate(top_produtos(df).items(), start=1):
        linhas.append(f"| {posicao} | {produto} | {qtd} |")

    return "\n".join(linhas) + "\n"


def salvar_relatorio(conteudo: str, caminho: str | Path = "relatorio.md") -> Path:
    caminho = Path(caminho)
    caminho.write_text(conteudo, encoding="utf-8")
    return caminho


if __name__ == "__main__":
    vendas = carregar_vendas("vendas.csv")
    arquivo = salvar_relatorio(gerar_relatorio(vendas))
    print(f"Relatório gerado: {arquivo}")
