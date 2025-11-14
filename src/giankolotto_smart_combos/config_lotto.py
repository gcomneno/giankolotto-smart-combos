from dataclasses import dataclass
from typing import Optional, List

Number = int
Combo = List[Number]

@dataclass
class LottoConfig:
    k: int = 5                          # quanti numeri estrarre
    min_sum: Optional[int] = None       # somma minima totale (opzionale)
    max_sum: Optional[int] = None       # somma massima totale (opzionale)
    min_even: int = 0                   # minimo numeri pari
    min_odd: int = 0                    # minimo numeri dispari
    min_decades: int = 0                # minimo decine distinte (1–10, 11–20, ...)
    max_range: Optional[int] = None     # max (max(num) - min(num)), opzionale

    def __post_init__(self) -> None:
        if self.k <= 0:
            raise ValueError("k deve essere > 0")
        if self.min_even < 0 or self.min_odd < 0:
            raise ValueError("min_even e min_odd devono essere >= 0")

def decade_of(n: Number) -> int:
    """
    Restituisce la 'decina' di n, da 0 a 8:
    1–10 -> 0, 11–20 -> 1, ..., 81–90 -> 8.
    """
    if not (1 <= n <= 90):
        raise ValueError("n deve essere in [1, 90]")
    return (n - 1) // 10
