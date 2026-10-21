# Análise de Vendas com pandas

Sistema simples de análise de vendas em Python: gera dados fictícios, calcula o faturamento e produz um relatório em Markdown.

## Funcionalidades

- Gera um CSV com 100 vendas fictícias (reprodutível, via semente fixa)
- Calcula o faturamento total e por categoria
- Identifica os 5 produtos mais vendidos (empates em ordem alfabética)
- Gera um relatório em Markdown com valores no formato brasileiro (`R$ 1.234,56`, `12,3%`)

## Estrutura

```
├── gerar_dados.py        # gera vendas.csv
├── analise.py            # lê vendas.csv, calcula e gera relatorio.md
├── tests/
│   └── test_analise.py   # testes com pytest
├── vendas.csv            # dados de exemplo gerados
├── relatorio.md          # relatório de exemplo gerado
├── requirements.txt
└── pytest.ini
```

## Instalação

Requer Python 3.10 ou superior.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> No Ubuntu/Debian, se o `venv` falhar com erro sobre `ensurepip`, instale antes: `sudo apt install python3-venv`.

## Uso

```bash
python gerar_dados.py   # cria vendas.csv
python analise.py       # cria relatorio.md
```

O `analise.py` funciona com qualquer CSV que tenha as colunas `produto`, `categoria`, `quantidade` e `preco_unitario`.

## Testes

```bash
pytest -v
```

## Exemplo de resultado

Com os dados de exemplo (100 vendas, 565 itens), o faturamento total é **R$ 369.485,90**, sendo 88,7% em Eletrônicos. Veja o relatório completo em [relatorio.md](relatorio.md).
