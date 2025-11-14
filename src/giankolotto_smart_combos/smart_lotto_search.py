from typing import Iterable, Iterator, List, Callable, Optional
from .config_lotto import LottoConfig, Combo
from .constraints_lotto import PARTIAL_CHECKS, FULL_CHECKS

Number = int

def smart_lotto_search(
    cfg: LottoConfig,
    numbers: Iterable[int] = range(1, 91),
    partial_checks: Optional[
        Iterable[Callable[[Combo, LottoConfig, List[int]], bool]]
    ] = None,
    full_checks: Optional[
        Iterable[Callable[[Combo, LottoConfig], bool]]
    ] = None,
    stats: Optional[dict] = None,
) -> Iterator[Combo]:
    """
    Generatore di combinazioni (ordinate) di k numeri da `numbers` che rispettano
    tutti i vincoli di cfg, con pruning aggressivo.

    Puoi sovrascrivere partial_checks / full_checks per usare vincoli custom.
    Se `stats` è un dict, questo verrà aggiornato con:
        stats["nodes"] = numero di prefissi (nodi) visitati.
    """
    base_nums = sorted(set(numbers))
    if len(base_nums) < cfg.k:
        raise ValueError("Non ci sono abbastanza numeri per scegliere k elementi.")

    if partial_checks is None:
        partial_checks = PARTIAL_CHECKS
    else:
        partial_checks = list(partial_checks)

    if full_checks is None:
        full_checks = FULL_CHECKS
    else:
        full_checks = list(full_checks)

    # Inizializza contatore nodi se richiesto
    if stats is not None and "nodes" not in stats:
        stats["nodes"] = 0

    k = cfg.k
    combo: Combo = [0] * k
    n = len(base_nums)

    def backtrack(start_idx: int, depth: int) -> Iterator[Combo]:
        if depth == k:
            # Controlli finali
            for check in full_checks:
                if not check(combo, cfg):
                    return
            yield list(combo)
            return

        # vincolo: ci devono rimanere abbastanza elementi per completare k
        for i in range(start_idx, n - (k - depth) + 1):
            val = base_nums[i]
            combo[depth] = val
            prefix = combo[:depth + 1]

            # Contiamo ogni prefisso come nodo visitato
            if stats is not None:
                stats["nodes"] += 1

            # vincoli parziali
            ok = True
            for check in partial_checks:
                if not check(prefix, cfg, base_nums):
                    ok = False
                    break
            if not ok:
                continue

            # prosegui al livello successivo
            yield from backtrack(i + 1, depth + 1)

    yield from backtrack(0, 0)
