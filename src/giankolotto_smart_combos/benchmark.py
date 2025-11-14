# src/giankolotto_smart_combos/benchmark.py
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

def _format_seconds(seconds: float) -> str:
    """
    Converte un numero di secondi in stringa H:MM:SS.
    """
    if seconds is None or seconds < 0:
        return "n/a"
    s = int(round(seconds))
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    if h > 0:
        return "%d:%02d:%02d" % (h, m, sec)
    return "%02d:%02d" % (m, sec)

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
    - combinazioni al secondo (media)
    - nodi visitati (prefissi)
    - % di spazio combinatorio esplorato (stimato)
    - nodi/secondo (media)
    - ETA stimato (in secondi) basato sui nodi

    Se show_progress=True e print_combos=False, mostra una progress bar con:
        - percentuale
        - nodi visitati / totali
        - nodi/s e combos/s istantanei (approssimati)
        - ETA stimato
    """
    base_nums = _materialize_numbers(numbers)
    n = len(base_nums)

    total_nodes = _total_nodes_no_pruning(n, cfg.k)
    total_combos = math.comb(n, cfg.k)

    stats: Dict[str, Any] = {}

    start = time.perf_counter()
    last_update_time = start
    last_nodes = 0
    last_combos = 0

    count = 0
    printed = 0

    for combo in smart_lotto_search(cfg, base_nums, stats=stats):
        if print_combos:
            if max_print is None or printed < max_print:
                print(combo)
                printed += 1

        count += 1

        # --- PROGRESS BAR + MINI-PROFILER LIVE --- #
        if show_progress and not print_combos:
            now = time.perf_counter()
            # aggiorniamo ogni ~0.20s
            if now - last_update_time >= 0.20:
                nodes_visited = int(stats.get("nodes", 0))

                progress = (
                    float(nodes_visited) / float(total_nodes)
                    if total_nodes > 0 else 0.0
                )
                if progress > 1.0:
                    progress = 1.0

                bar_len = 30
                filled = int(bar_len * progress)
                bar = "[" + "#" * filled + "-" * (bar_len - filled) + "]"
                percent = progress * 100.0

                elapsed_so_far = now - start

                # Medie fino ad ora
                avg_nodes_per_sec = (
                    float(nodes_visited) / elapsed_so_far
                    if elapsed_so_far > 0 else 0.0
                )
                avg_combos_per_sec = (
                    float(count) / elapsed_so_far
                    if elapsed_so_far > 0 else 0.0
                )

                # Istantanei (delta rispetto all'ultimo update)
                dt = now - last_update_time
                dn_nodes = nodes_visited - last_nodes
                dn_combos = count - last_combos

                inst_nodes_per_sec = (
                    float(dn_nodes) / dt if dt > 0 else 0.0
                )
                inst_combos_per_sec = (
                    float(dn_combos) / dt if dt > 0 else 0.0
                )

                # ETA basata sulle medie sui nodi
                if avg_nodes_per_sec > 0.0 and total_nodes > 0:
                    est_total_time = float(total_nodes) / avg_nodes_per_sec
                    eta_seconds = max(0.0, est_total_time - elapsed_so_far)
                else:
                    eta_seconds = None

                eta_str = _format_seconds(eta_seconds)

                msg = (
                    "\rProgress {bar} {percent:6.2f}%  "
                    "Nodes: {nodes}/{tot_nodes}  "
                    "n/s: {nps_inst:7.1f} (avg {nps_avg:7.1f})  "
                    "Combos: {combos}  "
                    "c/s: {cps_inst:7.1f} (avg {cps_avg:7.1f})  "
                    "ETA: {eta}"
                ).format(
                    bar=bar,
                    percent=percent,
                    nodes=nodes_visited,
                    tot_nodes=total_nodes,
                    nps_inst=inst_nodes_per_sec,
                    nps_avg=avg_nodes_per_sec,
                    combos=count,
                    cps_inst=inst_combos_per_sec,
                    cps_avg=avg_combos_per_sec,
                    eta=eta_str,
                )

                print(msg, end="", flush=True)

                last_update_time = now
                last_nodes = nodes_visited
                last_combos = count

    elapsed = time.perf_counter() - start
    combos_per_sec = count / elapsed if elapsed > 0 else 0.0

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

    nodes_per_sec = (
        float(nodes_visited) / elapsed
        if elapsed > 0 and nodes_visited > 0 else 0.0
    )

    if nodes_per_sec > 0.0 and total_nodes > 0:
        est_total_time = float(total_nodes) / nodes_per_sec
        eta_seconds = max(0.0, est_total_time - elapsed)
    else:
        est_total_time = None
        eta_seconds = None

    return {
        "count": count,
        "elapsed": elapsed,
        "combos_per_sec": combos_per_sec,
        "nodes_visited": nodes_visited,
        "total_nodes": total_nodes,
        "nodes_ratio": nodes_ratio,
        "total_combos": total_combos,
        "combos_ratio": combos_ratio,
        "nodes_per_sec": nodes_per_sec,
        "estimated_total_time_seconds": est_total_time,
        "eta_seconds": eta_seconds,
    }
