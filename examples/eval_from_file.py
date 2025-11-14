import argparse
from giankolotto_smart_combos import (
    get_preset,
    evaluate_combos_from_file,
)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Valutazione combinazioni da file di testo (Giankolotto Smart-Combos)."
    )
    parser.add_argument(
        "path",
        help="Percorso del file di input (una combinazione per riga).",
    )
    parser.add_argument(
        "--preset",
        choices=["soft", "medium", "hard"],
        default="medium",
        help="Preset di configurazione da usare (default: medium).",
    )
    parser.add_argument(
        "--skip-invalid-lines",
        action="store_true",
        help="Ignora le righe con errori di parsing (invece di riportarle nel risultato).",
    )
    return parser.parse_args()

def main():
    args = parse_args()

    cfg = get_preset(args.preset)

    results = evaluate_combos_from_file(
        path=args.path,
        cfg=cfg,
        skip_invalid_lines=args.skip_invalid_lines,
    )

    print("Preset usato:", args.preset)
    print()

    for res in results:
        combo = res["combo"]
        valid = res["valid"]
        reasons = res["reasons"]
        metrics = res["metrics"]
        line_no = res.get("line_no", None)

        prefix = ""
        if line_no is not None:
            prefix = f"[linea {line_no:03d}] "

        combo_str = " ".join(str(x) for x in combo) if combo else "<vuota>"

        if valid:
            status = "OK"
        else:
            status = "KO"

        msg = f"{prefix}{combo_str} -> {status}"

        if metrics["sum"] is not None:
            m = metrics
            msg += "  (sum={sum}, range={range}, decine={decades_count}, pari={even}, dispari={odd})".format(
                sum=m["sum"],
                range=m["range"],
                decades_count=m["decades_count"],
                even=m["even_count"],
                odd=m["odd_count"],
            )

        print(msg)

        if not valid and reasons:
            for r in reasons:
                print("   -", r)

    print()
    print("Totale combinazioni valutate:", len(results))

if __name__ == "__main__":
    main()
