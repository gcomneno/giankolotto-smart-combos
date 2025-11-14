# src/giankolotto_smart_combos/eval_lotto.py

from typing import List, Dict, Any
from .config_lotto import LottoConfig, Combo, Number, decade_of


class ParseError(Exception):
    """Eccezione interna per errori di parsing di una riga di input."""
    pass


def _parse_line_to_numbers(line: str) -> List[Number]:
    """
    Converte una riga di testo in una lista di interi.
    Supporta separatori spazio e/o virgole.

    Esempi validi:
        "5 18 32 47 80"
        "5,18,32,47,80"
        "5, 18  32,47 80"
    """
    # Sostituisco virgole con spazi, splitto e provo a convertire
    cleaned = line.replace(",", " ")
    parts = [p for p in cleaned.split() if p]

    if not parts:
        raise ParseError("Linea vuota o priva di numeri")

    nums: List[Number] = []
    for p in parts:
        try:
            n = int(p)
        except ValueError:
            raise ParseError("Token non numerico: '%s'" % p)
        nums.append(n)
    return nums


def evaluate_combo(combo: Combo, cfg: LottoConfig) -> Dict[str, Any]:
    """
    Valuta una singola combinazione rispetto a LottoConfig.

    Ritorna un dict con:
        {
          "combo": List[int],
          "valid": bool,
          "reasons": List[str],
          "metrics": {
              "sum": int,
              "min": int,
              "max": int,
              "range": int,
              "even_count": int,
              "odd_count": int,
              "decades_count": int,
              "decades": List[int],
          }
        }
    """
    reasons: List[str] = []
    k = cfg.k

    nums = list(combo)

    # Lunghezza
    if len(nums) != k:
        reasons.append("Lunghezza errata: attesi %d numeri, trovati %d" % (k, len(nums)))

    # Duplicati
    if len(set(nums)) != len(nums):
        reasons.append("Numeri duplicati nella combinazione")

    # Range base 1..90
    has_out_of_range = False
    for n in nums:
        if n < 1 or n > 90:
            reasons.append("Numero fuori range [1..90]: %d" % n)
            has_out_of_range = True

    if not nums:
        # Evitiamo crash sui min/max
        metrics = {
            "sum": 0,
            "min": None,
            "max": None,
            "range": None,
            "even_count": 0,
            "odd_count": 0,
            "decades_count": 0,
            "decades": [],
        }
        return {
            "combo": nums,
            "valid": False,
            "reasons": reasons or ["Combinazione vuota"],
            "metrics": metrics,
        }

    # Metriche (anche se ci sono fuori range, usiamo comunque nums come sono;
    # la combinazione verrà comunque marcata come non valida)
    s = sum(nums)
    mn = min(nums)
    mx = max(nums)
    r = mx - mn
    evens = sum(1 for x in nums if x % 2 == 0)
    odds = len(nums) - evens

    # Decine solo per i numeri validi (evitiamo ValueError da decade_of)
    valid_for_decades = [x for x in nums if 1 <= x <= 90]
    if valid_for_decades:
        decs_set = {decade_of(x) for x in valid_for_decades}
    else:
        decs_set = set()

    decs = sorted(decs_set)
    decs_count = len(decs_set)

    metrics = {
        "sum": s,
        "min": mn,
        "max": mx,
        "range": r,
        "even_count": evens,
        "odd_count": odds,
        "decades_count": decs_count,
        "decades": decs,
    }

    # Vincoli: somma
    if cfg.min_sum is not None and s < cfg.min_sum:
        reasons.append("Somma %d < min_sum %d" % (s, cfg.min_sum))
    if cfg.max_sum is not None and s > cfg.max_sum:
        reasons.append("Somma %d > max_sum %d" % (s, cfg.max_sum))

    # Vincoli: pari/dispari
    if evens < cfg.min_even:
        reasons.append("Troppi pochi pari: %d < min_even %d" % (evens, cfg.min_even))
    if odds < cfg.min_odd:
        reasons.append("Troppi pochi dispari: %d < min_odd %d" % (odds, cfg.min_odd))

    # Vincoli: decine
    if cfg.min_decades > 0 and decs_count < cfg.min_decades:
        reasons.append(
            "Decine distinte %d < min_decades %d" % (decs_count, cfg.min_decades)
        )

    # Vincoli: range
    if cfg.max_range is not None and r > cfg.max_range:
        reasons.append("Range %d > max_range %d" % (r, cfg.max_range))

    valid = len(reasons) == 0

    return {
        "combo": nums,
        "valid": valid,
        "reasons": reasons,
        "metrics": metrics,
    }


def evaluate_combos_from_file(
    path: str,
    cfg: LottoConfig,
    skip_invalid_lines: bool = False,
) -> List[Dict[str, Any]]:
    """
    Valuta tutte le combinazioni presenti in un file di testo.

    Formato atteso:
      - una combinazione per riga
      - numeri separati da spazi e/o virgole
      - righe vuote o che iniziano con '#' vengono ignorate

    Parametri:
        path: percorso del file di input
        cfg: LottoConfig da usare per la valutazione
        skip_invalid_lines: se True, le righe con errori di parsing
                            vengono ignorate; se False, generano
                            un risultato con valid=False e reason adeguata.

    Ritorna:
        lista di risultati, dove ogni elemento è il dict di evaluate_combo(),
        eventualmente arricchito con una chiave 'line_no' per il numero di linea.
    """
    results: List[Dict[str, Any]] = []

    with open(path, "r", encoding="utf-8") as f:
        for idx, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line:
                # riga vuota: la ignoriamo senza aggiungere risultato
                continue
            if line.startswith("#"):
                # commento
                continue

            try:
                nums = _parse_line_to_numbers(line)
            except ParseError as e:
                if skip_invalid_lines:
                    continue
                # Costruiamo un risultato 'falso' per riportare l'errore
                result = {
                    "combo": [],
                    "valid": False,
                    "reasons": ["Errore parsing linea %d: %s" % (idx, str(e))],
                    "metrics": {
                        "sum": None,
                        "min": None,
                        "max": None,
                        "range": None,
                        "even_count": None,
                        "odd_count": None,
                        "decades_count": None,
                        "decades": [],
                    },
                    "line_no": idx,
                }
                results.append(result)
                continue

            eval_result = evaluate_combo(nums, cfg)
            eval_result["line_no"] = idx
            results.append(eval_result)

    return results
