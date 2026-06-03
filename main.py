"""
Sistema de Analise de Meteoritos (NASA Meteorite Landings)
Disciplina: Estruturas de Dados
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from src.structures.linked_list import DoublyLinkedList
from src.structures.stack import Stack
from src.structures.queue_ds import Queue
from src.algorithms.sorting import quick_sort, merge_sort
from src.algorithms.search import linear_search, binary_search_by_year
from src.data_handler import load_data, export_to_csv
from src.analysis import (
    general_stats, geographic_distribution,
    temporal_distribution, fell_vs_found,
)
from src.logger import log

SEPARATOR = "=" * 60
_meteorites_ll = DoublyLinkedList()
_history_stack = Stack(max_size=20)
_analysis_queue = Queue()
_sorted_by_year = []
_loaded = False


# ─────────────────────────────────────────────
# Helpers de exibição
# ─────────────────────────────────────────────

def _header(title):
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR)


def _fmt_meteorite(m, index=None):
    prefix = f"[{index}] " if index is not None else ""
    mass = f"{m['mass']:,.1f} g" if m['mass'] else "N/D"
    year = str(m['year']) if m['year'] else "N/D"
    lat = f"{m['lat']:.2f}" if m['lat'] is not None else "N/D"
    lon = f"{m['lon']:.2f}" if m['lon'] is not None else "N/D"
    return (
        f"{prefix}Nome: {m['name']}  |  Classe: {m['recclass']}  |  "
        f"Massa: {mass}  |  Ano: {year}  |  Lat/Lon: {lat}/{lon}"
    )


def _pause():
    input("\nPressione Enter para continuar...")


# ─────────────────────────────────────────────
# Opcoes do menu
# ─────────────────────────────────────────────

def carregar_dados():
    global _loaded, _sorted_by_year
    _header("CARREGANDO DADOS")
    try:
        log("Iniciando carregamento dos dados")
        data = load_data(logger=log)
        _meteorites_ll.from_list(data)
        _sorted_by_year = merge_sort(data, key_func=lambda m: m['year'])
        _loaded = True
        log(f"Carregados {len(_meteorites_ll)} meteoritos na lista ligada")
        print(f"\n  Total carregado: {len(_meteorites_ll):,} meteoritos")
    except RuntimeError as e:
        log(str(e), level="ERROR")
    _pause()


def estatisticas_gerais():
    _header("ESTATISTICAS GERAIS")
    if not _loaded:
        print("  [!] Carregue os dados primeiro (opcao 1).")
        _pause()
        return
    try:
        stats = general_stats(_meteorites_ll.to_list())
        print(f"  Total de meteoritos  : {stats['total']:,}")
        print(f"  Com massa registrada : {stats.get('com_massa', 0):,}")
        print(f"  Massa total          : {stats.get('massa_total_kg', 0):,.2f} kg")
        print(f"  Massa media          : {stats.get('massa_media_g', 0):,.2f} g")
        print(f"  Massa maxima         : {stats.get('massa_maxima_g', 0):,.2f} g")
        print(f"  Massa minima         : {stats.get('massa_minima_g', 0):,.4f} g")
        print(f"  Ano mais antigo      : {stats.get('ano_mais_antigo', 'N/D')}")
        print(f"  Ano mais recente     : {stats.get('ano_mais_recente', 'N/D')}")
        print(f"  Classes distintas    : {stats.get('total_classes', 0):,}")
        print("\n  Top 10 classes de meteoritos:")
        for cls, cnt in stats.get('top_classes', []):
            bar = '#' * min(cnt // 50, 30)
            print(f"    {cls:<25} {cnt:>5}  {bar}")

        fell = fell_vs_found(_meteorites_ll.to_list())
        print("\n  Queda vs Encontrado:")
        for k, v in fell.items():
            print(f"    {k:<12}: {v:,}")
        log("Estatisticas gerais exibidas")
    except Exception as e:
        log(str(e), level="ERROR")
    _pause()


def busca_linear_nome():
    _header("BUSCA LINEAR POR NOME / CLASSE")
    if not _loaded:
        print("  [!] Carregue os dados primeiro (opcao 1).")
        _pause()
        return
    query = input("  Digite o nome ou classe a buscar: ").strip()
    if not query:
        _pause()
        return
    try:
        campo = input("  Buscar em [1] Nome  [2] Classe (default=1): ").strip()
        field = 'recclass' if campo == '2' else 'name'
        log(f"Busca linear: campo='{field}' query='{query}'")
        results = linear_search(_meteorites_ll.to_list(), query, field)
        print(f"\n  {len(results)} resultado(s) encontrado(s):\n")
        for i, m in enumerate(results[:20], 1):
            print(f"  {_fmt_meteorite(m, i)}")
            _history_stack.push(m)
        if len(results) > 20:
            print(f"  ... e mais {len(results) - 20} resultado(s).")
        log(f"Busca linear retornou {len(results)} resultados")
    except Exception as e:
        log(str(e), level="ERROR")
    _pause()


def busca_binaria_ano():
    _header("BUSCA BINARIA POR ANO")
    if not _loaded:
        print("  [!] Carregue os dados primeiro (opcao 1).")
        _pause()
        return
    try:
        ano_str = input("  Digite o ano (ex: 1969): ").strip()
        ano = int(ano_str)
        log(f"Busca binaria por ano={ano} em lista ordenada por Merge Sort")
        results = binary_search_by_year(_sorted_by_year, ano)
        print(f"\n  {len(results)} meteorito(s) registrado(s) em {ano}:\n")
        for i, m in enumerate(results[:20], 1):
            print(f"  {_fmt_meteorite(m, i)}")
            _history_stack.push(m)
        if len(results) > 20:
            print(f"  ... e mais {len(results) - 20} resultado(s).")
        log(f"Busca binaria ano={ano} retornou {len(results)} resultados")
    except ValueError:
        print("  [!] Ano invalido.")
        log("Ano invalido na busca binaria", level="WARN")
    except Exception as e:
        log(str(e), level="ERROR")
    _pause()


def ordenar_por_massa():
    _header("ORDENAR POR MASSA — QUICK SORT")
    if not _loaded:
        print("  [!] Carregue os dados primeiro (opcao 1).")
        _pause()
        return
    try:
        ordem = input("  [1] Maior para menor  [2] Menor para maior (default=1): ").strip()
        reverse = (ordem != '2')
        log(f"Quick Sort por massa, decrescente={reverse}")
        data = _meteorites_ll.to_list()
        sorted_data = quick_sort(data, key_func=lambda m: m['mass'], reverse=reverse)
        print(f"\n  Top 15 meteoritos por massa:\n")
        for i, m in enumerate(sorted_data[:15], 1):
            print(f"  {_fmt_meteorite(m, i)}")
        n_str = input("\n  Quantos exportar para CSV? (Enter para pular): ").strip()
        if n_str.isdigit():
            n = int(n_str)
            path = os.path.join(os.path.dirname(__file__), 'data', 'por_massa.csv')
            export_to_csv(sorted_data[:n], path)
            log(f"Exportados {n} registros para {path}")
            print(f"  Exportado: {path}")
        log("Quick Sort concluido")
    except Exception as e:
        log(str(e), level="ERROR")
    _pause()


def ordenar_por_ano():
    _header("ORDENAR POR ANO — MERGE SORT")
    if not _loaded:
        print("  [!] Carregue os dados primeiro (opcao 1).")
        _pause()
        return
    try:
        ordem = input("  [1] Mais antigo primeiro  [2] Mais recente primeiro (default=1): ").strip()
        reverse = (ordem == '2')
        log(f"Merge Sort por ano, decrescente={reverse}")
        data = _meteorites_ll.to_list()
        sorted_data = merge_sort(data, key_func=lambda m: m['year'], reverse=reverse)
        print(f"\n  Primeiros 15 na ordenacao:\n")
        for i, m in enumerate(sorted_data[:15], 1):
            print(f"  {_fmt_meteorite(m, i)}")
        log("Merge Sort concluido")
    except Exception as e:
        log(str(e), level="ERROR")
    _pause()


def analise_geografica():
    _header("ANALISE GEOGRAFICA E TEMPORAL")
    if not _loaded:
        print("  [!] Carregue os dados primeiro (opcao 1).")
        _pause()
        return
    try:
        data = _meteorites_ll.to_list()
        geo = geographic_distribution(data)
        print("  Distribuicao por hemisferio:")
        total = sum(geo.values())
        for k, v in geo.items():
            pct = (v / total * 100) if total else 0
            bar = '#' * int(pct / 2)
            print(f"    {k:<22}: {v:>6,}  ({pct:5.1f}%)  {bar}")

        temp = temporal_distribution(data)
        print("\n  Distribuicao por seculo:")
        for century, count in temp.items():
            bar = '#' * min(count // 100, 40)
            print(f"    {century}: {count:>6,}  {bar}")
        log("Analise geografica e temporal exibida")
    except Exception as e:
        log(str(e), level="ERROR")
    _pause()


def historico_pilha():
    _header("HISTORICO DE VISUALIZACOES (PILHA)")
    print(f"  Itens na pilha: {_history_stack.size()}")
    if _history_stack.is_empty():
        print("  Pilha vazia. Realize buscas para popular o historico.")
        _pause()
        return
    print("\n  Ultimos meteoritos visualizados (topo → base):\n")
    for i, m in enumerate(_history_stack.to_list(), 1):
        print(f"  {_fmt_meteorite(m, i)}")
    op = input("\n  [D] Desempilhar ultimo  [L] Limpar  [Enter] Voltar: ").strip().upper()
    if op == 'D' and not _history_stack.is_empty():
        removed = _history_stack.pop()
        log(f"Desempilhado: {removed['name']}")
        print(f"  Removido: {removed['name']}")
    elif op == 'L':
        while not _history_stack.is_empty():
            _history_stack.pop()
        log("Pilha de historico limpa")
        print("  Pilha limpa.")
    _pause()


def fila_analise():
    _header("FILA DE ANALISE EM LOTE")
    print(f"  Itens na fila: {_analysis_queue.size()}")
    print("\n  [1] Adicionar meteorito por nome")
    print("  [2] Processar proximo da fila")
    print("  [3] Processar todos (exportar CSV)")
    print("  [4] Ver fila atual")
    print("  [0] Voltar")
    op = input("\n  Opcao: ").strip()

    if op == '1':
        if not _loaded:
            print("  [!] Carregue os dados primeiro.")
        else:
            nome = input("  Nome do meteorito: ").strip()
            results = linear_search(_meteorites_ll.to_list(), nome, 'name')
            if results:
                m = results[0]
                _analysis_queue.enqueue(m)
                log(f"Enfileirado: {m['name']}")
                print(f"  Enfileirado: {m['name']}")
            else:
                print("  Meteorito nao encontrado.")

    elif op == '2':
        if _analysis_queue.is_empty():
            print("  Fila vazia.")
        else:
            m = _analysis_queue.dequeue()
            log(f"Processado da fila: {m['name']}")
            print(f"\n  Processado:\n  {_fmt_meteorite(m)}")

    elif op == '3':
        if _analysis_queue.is_empty():
            print("  Fila vazia.")
        else:
            batch = []
            while not _analysis_queue.is_empty():
                batch.append(_analysis_queue.dequeue())
            path = os.path.join(os.path.dirname(__file__), 'data', 'fila_exportada.csv')
            export_to_csv(batch, path)
            log(f"Lote de {len(batch)} meteoritos exportado para {path}")
            print(f"  {len(batch)} meteorito(s) exportado(s) para:\n  {path}")

    elif op == '4':
        items = _analysis_queue.to_list()
        if not items:
            print("  Fila vazia.")
        else:
            for i, m in enumerate(items, 1):
                print(f"  {_fmt_meteorite(m, i)}")

    _pause()


def ver_lista_ligada():
    _header("LISTA DUPLAMENTE LIGADA — NAVEGACAO")
    if not _loaded:
        print("  [!] Carregue os dados primeiro (opcao 1).")
        _pause()
        return
    total = len(_meteorites_ll)
    print(f"  Total na lista: {total:,} nos")
    try:
        idx_str = input("  Ver a partir do indice (0 a N-1, default=0): ").strip()
        idx = int(idx_str) if idx_str.isdigit() else 0
        idx = max(0, min(idx, total - 1))
        current = _meteorites_ll.head
        for _ in range(idx):
            if current.next:
                current = current.next
        print(f"\n  Exibindo 10 nos a partir do indice {idx}:\n")
        for i in range(10):
            if current is None:
                break
            print(f"  [{idx + i}] {_fmt_meteorite(current.data)}")
            print(f"       Anterior: {current.prev.data['name'] if current.prev else 'None'}")
            print(f"       Proximo : {current.next.data['name'] if current.next else 'None'}\n")
            current = current.next
        log(f"Navegacao na lista ligada a partir do indice {idx}")
    except Exception as e:
        log(str(e), level="ERROR")
    _pause()


# ─────────────────────────────────────────────
# Loop principal
# ─────────────────────────────────────────────

def menu():
    while True:
        os.system('clear' if os.name != 'nt' else 'cls')
        print(SEPARATOR)
        print("  SISTEMA DE ANALISE DE METEORITOS — NASA")
        print("  Estruturas de Dados | Global Solution")
        print(SEPARATOR)
        status = f"  Dados: {'CARREGADOS (' + str(len(_meteorites_ll)) + ' registros)' if _loaded else 'NAO CARREGADOS'}"
        status += f"  |  Pilha: {_history_stack.size()}  |  Fila: {_analysis_queue.size()}"
        print(status)
        print(SEPARATOR)
        print("  1. Carregar dados (NASA Meteorite Landings)")
        print("  2. Estatisticas gerais")
        print("  3. Busca linear (por nome ou classe)")
        print("  4. Busca binaria (por ano)")
        print("  5. Ordenar por massa — Quick Sort")
        print("  6. Ordenar por ano  — Merge Sort")
        print("  7. Analise geografica e temporal")
        print("  8. Historico de visualizacoes (Pilha)")
        print("  9. Fila de analise em lote")
        print("  L. Navegar na lista duplamente ligada")
        print("  0. Sair")
        print(SEPARATOR)

        op = input("  Opcao: ").strip().upper()

        dispatch = {
            '1': carregar_dados,
            '2': estatisticas_gerais,
            '3': busca_linear_nome,
            '4': busca_binaria_ano,
            '5': ordenar_por_massa,
            '6': ordenar_por_ano,
            '7': analise_geografica,
            '8': historico_pilha,
            '9': fila_analise,
            'L': ver_lista_ligada,
        }

        if op == '0':
            log("Aplicacao encerrada pelo usuario")
            print("\n  Ate logo!\n")
            break
        elif op in dispatch:
            dispatch[op]()
        else:
            print("  Opcao invalida.")
            _pause()


if __name__ == '__main__':
    log("Aplicacao iniciada")
    menu()
