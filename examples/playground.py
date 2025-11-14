import argparse
from giankolotto_smart_combos import LottoConfig, benchmark_search


def parse_args():
    parser = argparse.ArgumentParser(
        description="Benchmark di giankolotto-smart-combos"
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
    return parser.parse_args()


def main():
    args = parse_args()

    # Config di esempio: cambiala come ti pare
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
        show_progress=not args.print_combos,  # progress bar solo se non stampi combos
    )

    print("\n=== Benchmark ===")
    print(f"Combinazioni generate       : {stats['count']}")
    print(f"Tempo totale                : {stats['elapsed']:.6f} s")
    print(f"Combinazioni / secondo      : {stats['combos_per_sec']:.2f} combos/s")
    print()
    print(
        f"Totale combinazioni possibili (C(n,k)) : {stats['total_combos']}"
    )
    print(
        f"Percentuale combos generate           : {stats['combos_ratio']:.6f} %"
    )
    print()
    print(f"Nodi visitati (prefissi)    : {stats['nodes_visited']}")
    print(f"Nodi teorici senza pruning  : {stats['total_nodes']}")
    print(
        f"% spazio combinatorio esplorato       : {stats['nodes_ratio']:.6f} %"
    )


if __name__ == "__main__":
    main()
