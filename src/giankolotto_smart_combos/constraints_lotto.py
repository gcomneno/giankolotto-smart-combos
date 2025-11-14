from typing import List
from .config_lotto import LottoConfig, decade_of, Number, Combo

# =========================
#  VINCOLI PARZIALI
# =========================
# Firma:
#   partial_x(prefix: Combo, cfg: LottoConfig, numbers: List[int]) -> bool
def partial_sum_range(prefix: Combo, cfg: LottoConfig, numbers: List[int]) -> bool:
    """Pruning sulla somma totale: controlla se è ancora possibile rientrare in [min_sum, max_sum]."""
    if cfg.min_sum is None and cfg.max_sum is None:
        return True

    curr_sum = sum(prefix)
    k = cfg.k
    placed = len(prefix)
    slots_left = k - placed
    if slots_left < 0:
        return False

    if slots_left == 0:
        # ramo completo: il controllo finale verrà fatto dai vincoli full
        return True

    # Min/max teorici con i numeri rimanenti
    remaining_nums = [n for n in numbers if n not in prefix]
    if not remaining_nums:
        return False

    min_rem = min(remaining_nums)
    max_rem = max(remaining_nums)

    min_add = slots_left * min_rem
    max_add = slots_left * max_rem

    min_possible = curr_sum + min_add
    max_possible = curr_sum + max_add

    if cfg.min_sum is not None and max_possible < cfg.min_sum:
        return False
    if cfg.max_sum is not None and min_possible > cfg.max_sum:
        return False

    return True

def partial_parity(prefix: Combo, cfg: LottoConfig, numbers: List[int]) -> bool:
    """Pruning su pari/dispari: controlla se possiamo ancora raggiungere min_even/min_odd."""
    if cfg.min_even == 0 and cfg.min_odd == 0:
        return True

    k = cfg.k
    placed = len(prefix)
    slots_left = k - placed
    if slots_left < 0:
        return False

    evens = sum(1 for x in prefix if x % 2 == 0)
    odds = placed - evens

    max_even = evens + slots_left
    max_odd = odds + slots_left

    if cfg.min_even > max_even:
        return False
    if cfg.min_odd > max_odd:
        return False

    return True

def partial_decades(prefix: Combo, cfg: LottoConfig, numbers: List[int]) -> bool:
    """Pruning sul numero minimo di decine distinte."""
    if cfg.min_decades <= 0:
        return True

    used_decades = {decade_of(x) for x in prefix}
    curr_d = len(used_decades)
    k = cfg.k
    placed = len(prefix)
    slots_left = k - placed
    if slots_left < 0:
        return False

    total_decades = 9  # 1–90
    remaining_decades = total_decades - curr_d

    max_decades_possible = curr_d + min(slots_left, remaining_decades)

    if max_decades_possible < cfg.min_decades:
        return False

    return True

def partial_range(prefix: Combo, cfg: LottoConfig, numbers: List[int]) -> bool:
    """Pruning sul range (max-min) se già violato."""
    if cfg.max_range is None:
        return True
    if len(prefix) < 2:
        return True
    r = max(prefix) - min(prefix)
    return r <= cfg.max_range

# Lista di vincoli parziali di default
PARTIAL_CHECKS = [
    partial_sum_range,
    partial_parity,
    partial_decades,
    partial_range,
]

# =========================
#  VINCOLI COMPLETI
# =========================
# Firma:
#   full_x(combo: Combo, cfg: LottoConfig) -> bool
def full_sum_range(combo: Combo, cfg: LottoConfig) -> bool:
    s = sum(combo)
    if cfg.min_sum is not None and s < cfg.min_sum:
        return False
    if cfg.max_sum is not None and s > cfg.max_sum:
        return False
    return True

def full_parity(combo: Combo, cfg: LottoConfig) -> bool:
    if cfg.min_even == 0 and cfg.min_odd == 0:
        return True
    evens = sum(1 for x in combo if x % 2 == 0)
    odds = len(combo) - evens
    if evens < cfg.min_even:
        return False
    if odds < cfg.min_odd:
        return False
    return True

def full_decades(combo: Combo, cfg: LottoConfig) -> bool:
    if cfg.min_decades <= 0:
        return True
    used_decades = {decade_of(x) for x in combo}
    return len(used_decades) >= cfg.min_decades

def full_range(combo: Combo, cfg: LottoConfig) -> bool:
    if cfg.max_range is None:
        return True
    r = max(combo) - min(combo)
    return r <= cfg.max_range

# Lista di vincoli finali di default
FULL_CHECKS = [
    full_sum_range,
    full_parity,
    full_decades,
    full_range,
]
