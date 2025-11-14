from dataclasses import dataclass
from typing import Optional, List, Dict, Callable

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

# =========================
#  PRESET UFFICIALI
# =========================
def _apply_overrides(cfg: LottoConfig, overrides: Dict[str, object]) -> LottoConfig:
    """
    Applica override ai campi di LottoConfig (es. preset_medium(max_sum=250)).
    """
    for key, value in overrides.items():
        if not hasattr(cfg, key):
            raise AttributeError("LottoConfig non ha un campo chiamato '%s'" % key)
        setattr(cfg, key, value)
    return cfg

def preset_soft(**overrides: object) -> LottoConfig:
    """
    Preset 'soft':
    - nessun vincolo su somma / range
    - leggero vincolo su pari/dispari e decine per evitare casi estremi.
    """
    cfg = LottoConfig(
        k=5,
        min_sum=None,
        max_sum=None,
        min_even=1,
        min_odd=1,
        min_decades=2,
        max_range=None,
    )
    return _apply_overrides(cfg, overrides)

def preset_medium(**overrides: object) -> LottoConfig:
    """
    Preset 'medium' (profilo di default consigliato):
    - 5 numeri
    - somma tra 120 e 220
    - almeno 2 pari e 2 dispari
    - almeno 3 decine diverse
    - range massimo 60
    """
    cfg = LottoConfig(
        k=5,
        min_sum=120,
        max_sum=220,
        min_even=2,
        min_odd=2,
        min_decades=3,
        max_range=60,
    )
    return _apply_overrides(cfg, overrides)

def preset_hard(**overrides: object) -> LottoConfig:
    """
    Preset 'hard':
    - vincoli più stretti su somma e range
    - distribuzione più 'sparpagliata' sulle decine
    """
    cfg = LottoConfig(
        k=5,
        min_sum=140,
        max_sum=200,
        min_even=2,
        min_odd=2,
        min_decades=4,
        max_range=45,
    )
    return _apply_overrides(cfg, overrides)

_PRESET_FACTORIES: Dict[str, Callable[..., LottoConfig]] = {
    "soft": preset_soft,
    "medium": preset_medium,
    "hard": preset_hard,
}

def get_preset(name: str, **overrides: object) -> LottoConfig:
    """
    Restituisce un LottoConfig a partire dal nome di un preset ('soft', 'medium', 'hard').

    Esempi:
        cfg = get_preset("medium")
        cfg = get_preset("hard", max_sum=210)
    """
    key = name.strip().lower()
    if key not in _PRESET_FACTORIES:
        raise KeyError(
            "Preset sconosciuto '%s'. Valori validi: %s"
            % (name, ", ".join(sorted(_PRESET_FACTORIES.keys())))
        )
    factory = _PRESET_FACTORIES[key]

    return factory(**overrides)
