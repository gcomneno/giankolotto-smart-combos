from giankolotto_smart_combos import LottoConfig, smart_lotto_search

def main():
    cfg = LottoConfig(
        k=5,
        min_sum=100,
        max_sum=220,
        min_even=2,
        min_odd=2,
        min_decades=3,
        max_range=60,
    )

    count = 0
    for combo in smart_lotto_search(cfg):
        print(combo)
        count += 1

    print("Totale combinazioni trovate:", count)

if __name__ == "__main__":
    main()
