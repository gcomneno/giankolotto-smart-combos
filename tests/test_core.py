# tests/test_core.py
import math

from pathlib import Path
from giankolotto_smart_combos import (
    LottoConfig,
    smart_lotto_search,
    benchmark_search,
    preset_soft,
    preset_medium,
    preset_hard,
    get_preset,
    evaluate_combo,
    evaluate_combos_from_file,
)

def test_combinations_small_space():
    """
    Verifica che smart_lotto_search generi tutte le C(n,k) combinazioni
    in un caso piccolo senza vincoli aggiuntivi.
    """
    cfg = LottoConfig(k=3)  # nessun vincolo extra
    numbers = range(1, 6)   # {1,2,3,4,5}

    combos = list(smart_lotto_search(cfg, numbers))

    # C(5,3) = 10
    assert len(combos) == math.comb(5, 3)

    # ogni combo ha lunghezza k
    assert all(len(c) == cfg.k for c in combos)

    # tutte le combo sono uniche
    assert len({tuple(c) for c in combos}) == len(combos)

    # le combo sono ordinate in modo crescente
    assert all(c == sorted(c) for c in combos)

def test_parity_constraints_respected():
    """
    Verifica che i vincoli su min_even / min_odd siano rispettati.
    """
    cfg = LottoConfig(
        k=4,
        min_even=2,
        min_odd=1,
    )
    numbers = range(1, 10)

    combos = list(smart_lotto_search(cfg, numbers))

    # Ci aspettiamo almeno una combinazione valida
    assert combos

    for combo in combos:
        evens = sum(1 for x in combo if x % 2 == 0)
        odds = len(combo) - evens
        assert evens >= cfg.min_even
        assert odds >= cfg.min_odd

def test_decades_constraints_respected():
    """
    Verifica che il vincolo su min_decades venga applicato correttamente.
    """
    cfg = LottoConfig(
        k=3,
        min_decades=3,
    )
    # Numeri da 1 a 30 → tre decine: 0 (1–10), 1 (11–20), 2 (21–30)
    numbers = range(1, 31)

    combos = list(smart_lotto_search(cfg, numbers))

    # Deve esserci almeno una combinazione con 3 decine distinte
    assert combos

    for combo in combos:
        decades = {(n - 1) // 10 for n in combo}
        assert len(decades) >= cfg.min_decades

def test_range_constraint_respected():
    """
    Verifica che il vincolo su max_range (max-min) sia rispettato.
    """
    cfg = LottoConfig(
        k=3,
        max_range=5,
    )
    numbers = range(1, 11)

    combos = list(smart_lotto_search(cfg, numbers))

    assert combos

    for combo in combos:
        r = max(combo) - min(combo)
        assert r <= cfg.max_range

def test_preset_medium_and_evaluate_combo_agree():
    """
    Usa preset_medium per generare una combinazione valida e verifica
    che evaluate_combo la consideri valid=True e senza reasons.
    """
    cfg = preset_medium()

    # Se per qualche motivo non ci fossero combinazioni, il test fallisce esplicitamente
    gen = smart_lotto_search(cfg)
    first_combo = None
    for c in gen:
        first_combo = c
        break

    assert first_combo is not None, "Nessuna combinazione trovata con preset_medium"

    res = evaluate_combo(first_combo, cfg)

    assert res["valid"] is True
    assert res["reasons"] == []
    assert res["combo"] == first_combo

    metrics = res["metrics"]
    assert metrics["sum"] == sum(first_combo)
    assert metrics["min"] == min(first_combo)
    assert metrics["max"] == max(first_combo)
    assert metrics["range"] == max(first_combo) - min(first_combo)


def test_evaluate_combo_invalid_example():
    """
    Verifica che una combinazione chiaramente 'brutta' venga segnalata come non valida
    rispetto a preset_medium.
    """
    cfg = preset_medium()

    bad_combo = [1, 2, 3, 4, 5]  # somma bassa, decine poche, range piccolo
    res = evaluate_combo(bad_combo, cfg)

    assert res["valid"] is False
    assert res["combo"] == bad_combo
    assert res["reasons"]  # ci devono essere motivazioni

def test_evaluate_combos_from_file(tmp_path):
    """
    Verifica che evaluate_combos_from_file legga correttamente un file
    con combinazioni, producendo struttura coerente.
    """
    content = "\n".join(
        [
            "# Commento",
            "5 18 32 47 80",
            "1 2 3 4 5",
            "99 2 3 4 5",      # fuori range
            "1, 1, 2, 3, 4",   # duplicati
        ]
    )

    path = tmp_path / "combos.txt"
    path.write_text(content, encoding="utf-8")

    cfg = preset_medium()

    results = evaluate_combos_from_file(str(path), cfg)

    # Dovremmo avere 4 risultati (1 commento saltato, nessuna riga vuota)
    assert len(results) == 4

    for res in results:
        assert "combo" in res
        assert "valid" in res
        assert "reasons" in res
        assert "metrics" in res
        assert "line_no" in res

    # Verifichiamo che almeno una combinazione sia KO
    assert any(not r["valid"] for r in results)

def test_benchmark_search_small_space():
    """
    Verifica che benchmark_search ritorni statistiche coerenti
    in uno scenario piccolo senza vincoli.
    """
    cfg = LottoConfig(k=3)
    numbers = range(1, 8)  # {1..7}

    stats = benchmark_search(
        cfg=cfg,
        numbers=numbers,
        print_combos=False,
        max_print=None,
        show_progress=False,
    )

    # chiavi previste
    for key in [
        "count",
        "elapsed",
        "combos_per_sec",
        "nodes_visited",
        "total_nodes",
        "nodes_ratio",
        "total_combos",
        "combos_ratio",
    ]:
        assert key in stats

    # combinazioni totali = C(7,3)
    assert stats["count"] == math.comb(7, 3)

    # total_combos deve coincidere con C(7,3)
    assert stats["total_combos"] == math.comb(7, 3)

    # nodi visitati > 0
    assert stats["nodes_visited"] > 0

    # non dovremmo esplorare più nodi di quelli teorici
    assert stats["nodes_visited"] <= stats["total_nodes"]

    # tempi e rate sensati
    assert stats["elapsed"] >= 0.0
    assert stats["combos_per_sec"] >= 0.0

def test_get_preset_variants():
    """
    Verifica che get_preset ritorni config diversi e che gli override funzionino.
    """
    cfg_soft = get_preset("soft")
    cfg_medium = get_preset("medium")
    cfg_hard = get_preset("hard")

    assert isinstance(cfg_soft, LottoConfig)
    assert isinstance(cfg_medium, LottoConfig)
    assert isinstance(cfg_hard, LottoConfig)

    # Gli hard devono avere vincoli più stretti di soft in generale
    assert cfg_soft.min_decades <= cfg_hard.min_decades
    assert (
        cfg_hard.max_range is None
        or cfg_soft.max_range is None
        or cfg_hard.max_range <= cfg_soft.max_range
    )

    # Override
    cfg_custom = get_preset("medium", max_sum=999)
    assert cfg_custom.max_sum == 999
