import time
import math

from typing import Iterable, Dict, Any, Optional, List
from .config_lotto import LottoConfig, Combo, Number
from .smart_lotto_search import smart_lotto_search

def _materialize_numbers(numbers: Iterable[Number]) -> List[Number]:
    """Utility: converte l'iterable numbers in una lista ordinata senza duplicati."""
    return sorted(set(numbers))

def _total_nodes_no_pruning(n: int, k: int) -> int:
    """
    Numero totale di nodi (prefissi non vuoti) dell'albero delle combinazioni
    senza pruning:

        somma_{d=1..k} C(n, d)
    """
    total = 0
    for d in range(1, k + 1):
        total += math.comb(n, d)
    return total

def benchmark_search(
    cfg: LottoConfig,
    numbers: Iterable[int] = range(1, 91),
    print_combos: bool = False,
    max_print: Optional[int] = None,
    show_progress: bool = False,
) -> Dict[str, Any]:
    """
    Esegue una ricerca con smart_lotto_search misurando con precisione:
    - tempo totale
    - numero di combinazioni generate
    - combinazioni al secondo
    - nodi visitati
    - % di spazio combinatorio esplorato (stimato)
    - opzionale: progress bar live (se show_progress=True e print_combos=False)
    """
    base_nums = _materialize_numbers(numbers)
    n = len(base_nums)

    total_nodes = _total_nodes_no_pruning(n, cfg.k)
    total_combos = math.comb(n, cfg.k)

    stats: Dict[str, Any] = {}

    start = time.perf_counter()
    last_update = start
    count = 0
    printed = 0

    for combo in smart_lotto_search(cfg, base_nums, stats=stats):
        if print_combos:
            if max_print is None or printed < max_print:
                print(combo)
                printed += 1

        count += 1

        # --- PROGRESS BAR --- #
        if show_progress and not print_combos:
            now = time.perf_counter()
            if now - last_update >= 0.20:  # aggiornamento ogni 200ms
                nodes_visited = int(stats.get("nodes", 0))

                progress = (
                    float(nodes_visited) / float(total_nodes)
                    if total_nodes > 0 else 0.0
                )
                if progress > 1:  # sicurezza
                    progress = 1

                bar_len = 30
                filled = int(bar_len * progress)
                bar = "[" + "#" * filled + "-" * (bar_len - filled) + "]"

                percent = progress * 100.0

                # MOSTRIAMO: barra, %, nodi visitati, nodi totali, count
                msg = (
                    f"\rProgress {bar} {percent:6.2f}%  "
                    f"Nodes: {nodes_visited}/{total_nodes}  "
                    f"Combos: {count}"
                )
                print(msg, end="", flush=True)

                last_update = now

    elapsed = time.perf_counter() - start
    combos_per_sec = count / elapsed if elapsed > 0 else float("inf")

    # newline finale per pulire la progress bar
    if show_progress and not print_combos:
        print()

    nodes_visited = int(stats.get("nodes", 0))
    nodes_ratio = (
        nodes_visited / float(total_nodes) * 100.0
        if total_nodes > 0 else 0.0
    )
    combos_ratio = (
        count / float(total_combos) * 100.0
        if total_combos > 0 else 0.0
    )

    return {
        "count": count,
        "elapsed": elapsed,
        "combos_per_sec": combos_per_sec,
        "nodes_visited": nodes_visited,
        "total_nodes": total_nodes,
        "nodes_ratio": nodes_ratio,
        "total_combos": total_combos,
        "combos_ratio": combos_ratio,
    }
