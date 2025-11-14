# src/giankolotto_smart_combos/cli.py
import argparse

from .config_lotto import LottoConfig, get_preset
from .benchmark import benchmark_search

def _format_seconds(seconds):
    if seconds is None or seconds < 0:
        return "n/a"
    s = int(round(seconds))
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    if h > 0:
        return "%d:%02d:%02d" % (h, m, sec)
    return "%02d:%02d" % (m, sec)

def _build_config_from_args(args: argparse.Namespace) -> LottoConfig:
    """
    Costruisce un LottoConfig partendo da un preset e applicando eventuali override.
    """
    cfg = get_preset(args.preset)

    # Override espliciti se forniti
    def override(field: str) -> None:
        value = getattr(args, field)
        if value is not None:
            setattr(cfg, field, value)

    for field in ["k", "min_sum", "max_sum", "min_even", "min_odd", "min_decades", "max_range"]:
        override(field)

    return cfg

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="giankolotto-smart-combos",
        description="Motore Lotto-compliant per combinazioni con vincoli e pruning (Giadaware™).",
    )

    # Preset e override LottoConfig
    parser.add_argument(
        "--preset",
        choices=["soft", "medium", "hard"],
        default="medium",
        help="Preset di configurazione da usare (default: medium).",
    )

    parser.add_argument(
        "--k",
        type=int,
        default=None,
        help="Override di k (numeri per combinazione).",
    )
    parser.add_argument(
        "--min-sum",
        type=int,
        default=None,
        help="Somma minima della combinazione (override del preset).",
    )
    parser.add_argument(
        "--max-sum",
        type=int,
        default=None,
        help="Somma massima della combinazione (override del preset).",
    )
    parser.add_argument(
        "--min-even",
        type=int,
        default=None,
        help="Numero minimo di pari (override del preset).",
    )
    parser.add_argument(
        "--min-odd",
        type=int,
        default=None,
        help="Numero minimo di dispari (override del preset).",
    )
    parser.add_argument(
        "--min-decades",
        type=int,
        default=None,
        help="Numero minimo di decine distinte (override del preset).",
    )
    parser.add_argument(
        "--max-range",
        type=int,
        default=None,
        help="Range massimo (max-min) consentito (override del preset).",
    )

    # Spazio dei numeri
    parser.add_argument(
        "--min-number",
        type=int,
        default=1,
        help="Numero minimo della base (default: 1).",
    )
    parser.add_argument(
        "--max-number",
        type=int,
        default=90,
        help="Numero massimo della base (default: 90).",
    )

    # Output
    parser.add_argument(
        "--print-combos",
        action="store_true",
        help="Stampa le combinazioni trovate (sconsigliato su spazi molto grandi).",
    )
    parser.add_argument(
        "--max-print",
        type=int,
        default=None,
        help="Numero massimo di combinazioni da stampare (se --print-combos).",
    )
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Disabilita la progress bar/mini-profiler durante il benchmark.",
    )

    return parser.parse_args()

def main() -> None:
    args = _parse_args()

    # Costruzione LottoConfig (preset + override)
    cfg = _build_config_from_args(args)

    # Numeri di base
    if args.min_number > args.max_number:
        raise SystemExit("Errore: --min-number non può essere > --max-number")

    numbers = range(args.min_number, args.max_number + 1)

    # Progress bar solo se non è stata esplicitamente disattivata
    # e se non stiamo già sporcando l'output con le combinazioni
    show_progress = (not args.no_progress) and (not args.print_combos)

    stats = benchmark_search(
        cfg=cfg,
        numbers=numbers,
        print_combos=args.print_combos,
        max_print=args.max_print,
        show_progress=show_progress,
    )

    print("\n=== Configurazione ===")
    print(f"Preset           : {args.preset}")
    print(f"k                : {cfg.k}")
    print(f"min_sum          : {cfg.min_sum}")
    print(f"max_sum          : {cfg.max_sum}")
    print(f"min_even         : {cfg.min_even}")
    print(f"min_odd          : {cfg.min_odd}")
    print(f"min_decades      : {cfg.min_decades}")
    print(f"max_range        : {cfg.max_range}")
    print(f"Numeri base      : [{args.min_number}..{args.max_number}]")

    print("\n=== Benchmark ===")
    print(f"Combinazioni generate       : {stats['count']}")
    print(f"Tempo totale                : {stats['elapsed']:.6f} s")
    print(f"Combinazioni / secondo (avg): {stats['combos_per_sec']:.2f} combos/s")
    print(f"Nodi / secondo (avg)        : {stats['nodes_per_sec']:.2f} nodes/s")
    print()
    print(f"Totale combinazioni possibili (C(n,k)) : {stats['total_combos']}")
    print(f"Percentuale combos generate           : {stats['combos_ratio']:.6f} %")
    print()
    print(f"Nodi visitati (prefissi)    : {stats['nodes_visited']}")
    print(f"Nodi teorici senza pruning  : {stats['total_nodes']}")
    print(f"% spazio combinatorio esplorato       : {stats['nodes_ratio']:.6f} %")
    print()
    print(
        "Tempo totale stimato (da nodi)       :",
        _format_seconds(stats["estimated_total_time_seconds"]),
    )
    print(
        "ETA residua stimata (da nodi)        :",
        _format_seconds(stats["eta_seconds"]),
    )

if __name__ == "__main__":
    main()
