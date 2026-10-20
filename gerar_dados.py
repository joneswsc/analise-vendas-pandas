"""Gera um CSV fictício de vendas."""

import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

PRODUTOS = {
    "Eletrônicos": {"Notebook": 3500.00, "Smartphone": 2200.00, "Fone de Ouvido": 250.00, "Monitor": 1100.00},
    "Livros": {"Romance": 45.00, "Ficção Científica": 55.00, "Biografia": 60.00},
    "Roupas": {"Camiseta": 59.90, "Calça Jeans": 149.90, "Tênis": 299.90},
    "Casa": {"Cafeteira": 189.90, "Liquidificador": 159.90, "Luminária": 89.90},
}


def gerar_vendas(n: int = 100, seed: int = 42) -> pd.DataFrame:
    """Retorna um DataFrame com `n` vendas aleatórias (reprodutíveis via `seed`)."""
    rng = random.Random(seed)
    inicio = date(2026, 1, 1)
    linhas = []
    for i in range(1, n + 1):
        categoria = rng.choice(list(PRODUTOS))
        produto = rng.choice(list(PRODUTOS[categoria]))
        linhas.append(
            {
                "id_venda": i,
                "data": (inicio + timedelta(days=rng.randint(0, 180))).isoformat(),
                "produto": produto,
                "categoria": categoria,
                "quantidade": rng.randint(1, 10),
                "preco_unitario": PRODUTOS[categoria][produto],
            }
        )
    return pd.DataFrame(linhas)


def salvar_csv(df: pd.DataFrame, caminho: str | Path = "vendas.csv") -> Path:
    caminho = Path(caminho)
    df.to_csv(caminho, index=False)
    return caminho


if __name__ == "__main__":
    arquivo = salvar_csv(gerar_vendas())
    print(f"CSV gerado: {arquivo}")
