# Sistema de Análise de Meteoritos — NASA Meteorite Landings

## Descrição do Projeto

Aplicação em Python para análise, organização e processamento da base de dados pública **NASA Meteorite Landings**, que contém registros de mais de 45.000 meteoritos catalogados ao redor do mundo.

## Objetivo da Solução

Permitir a exploração interativa dos dados de meteoritos: buscar por nome ou ano, ordenar por massa ou data, analisar padrões geográficos e temporais, e gerenciar lotes de análise — tudo demonstrando o uso prático das estruturas de dados e algoritmos estudados na disciplina.

## Tema Escolhido

**Meteoritos e padrões geográficos** — um dos temas da lista da economia espacial.

## Fonte dos Dados

- **NASA Meteorite Landings** — base pública disponível em [data.nasa.gov](https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh)
- Download automático na primeira execução via API aberta da NASA.
- Arquivo local salvo em `data/meteorites.csv`.

## Estruturas de Dados Implementadas

| Estrutura | Arquivo | Uso no Sistema |
|---|---|---|
| **Lista Duplamente Ligada** | `src/structures/linked_list.py` | Armazenamento principal de todos os meteoritos; permite navegação bidirecional |
| **Pilha (Stack)** | `src/structures/stack.py` | Histórico de visualizações (LIFO) — guarda os últimos meteoritos acessados |
| **Fila (Queue)** | `src/structures/queue_ds.py` | Fila de análise em lote (FIFO) — meteoritos enfileirados para exportação |

## Algoritmos Utilizados

| Algoritmo | Arquivo | Uso |
|---|---|---|
| **Busca Linear** | `src/algorithms/search.py` | Busca por nome ou classe (substring, case-insensitive) — O(n) |
| **Busca Binária** | `src/algorithms/search.py` | Busca por ano em lista pré-ordenada — O(log n) |
| **Quick Sort** | `src/algorithms/sorting.py` | Ordenação por massa (crescente ou decrescente) |
| **Merge Sort** | `src/algorithms/sorting.py` | Ordenação por ano (estável, usado na pré-ordenação para busca binária) |

## Tecnologias e Bibliotecas Utilizadas

- **Python 3.8+** (sem dependências externas obrigatórias)
- `csv` — leitura e escrita de arquivos CSV
- `urllib.request` — download da base de dados da NASA
- `collections.deque` — base interna da fila
- `datetime` — timestamps nos logs

## Explicação do Funcionamento

1. Ao iniciar, o usuário carrega os dados (baixados automaticamente da NASA se necessário).
2. Os meteoritos são armazenados em uma **lista duplamente ligada** como estrutura principal.
3. Busca por nome usa **busca linear** sobre a lista; busca por ano usa **busca binária** em lista pré-ordenada por **Merge Sort**.
4. A ordenação por massa usa **Quick Sort**.
5. Cada meteorito visualizado é empilhado na **pilha de histórico**.
6. O usuário pode enfileirar meteoritos para análise em lote na **fila**, exportando o resultado em CSV.
7. Todos os eventos são registrados em `data/app.log`.

## Estrutura de Arquivos

```
gs_meteorites/
├── main.py                        # Ponto de entrada / menu interativo
├── requirements.txt
├── README.md
├── data/
│   ├── meteorites.csv             # Gerado no primeiro uso
│   ├── app.log                    # Log de execução
│   ├── por_massa.csv              # Exportação Quick Sort
│   └── fila_exportada.csv         # Exportação fila em lote
└── src/
    ├── structures/
    │   ├── stack.py               # Pilha
    │   ├── queue_ds.py            # Fila
    │   └── linked_list.py         # Lista duplamente ligada
    ├── algorithms/
    │   ├── search.py              # Busca linear + binária
    │   └── sorting.py             # Quick Sort + Merge Sort
    ├── data_handler.py            # Carga e exportação CSV
    ├── analysis.py                # Análises estatísticas
    └── logger.py                  # Logging simples
```

## Instruções de Execução

```bash
# Clone ou entre na pasta do projeto
cd gs_meteorites

# Execute (Python 3.8+ sem instalação de pacotes)
python main.py
```

Na primeira execução, o sistema baixa automaticamente a base da NASA (~3 MB). As execuções seguintes usam o arquivo local.

## Nome dos Integrantes

| RM     | Nome              |
|--------|-------------------|
| 565585 | Enzo Dourado      |
| 561968 | Hugo Copatti      |
| 562200 | Lucas Villani     |
| 566447 | Matheus Victorio  |
| 564694 | Vinicius Lugli    |
