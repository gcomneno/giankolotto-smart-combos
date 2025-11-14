import argparse

from giankolotto_smart_combos import LottoConfig, benchmark_search

def parse_args():
    parser = argparse.ArgumentParser(
        description="Benchmark di giankolotto-smart-combos (con mini-profiler)."
    )
    parser.add_argument(
        "--print-combos",
        action="store_true",
        help="Stampa le combinazioni trovate (sconsigliato per benchmark seri).",
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

def main():
    args = parse_args()

    # Config di esempio: preset 'medium' equivalente
    cfg = LottoConfig(
        k=5,
        min_sum=120,
        max_sum=220,
        min_even=2,
        min_odd=2,
        min_decades=3,
        max_range=60,
    )

    stats = benchmark_search(
        cfg=cfg,
        numbers=range(1, 91),
        print_combos=args.print_combos,
        max_print=args.max_print,
        show_progress=(not args.no_progress and not args.print_combos),
    )

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
