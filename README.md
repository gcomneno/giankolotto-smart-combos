# giankolotto-smart-combos
Motore Lotto-compliant per la generazione di **combinazioni** di numeri (1–90) con **vincoli configurabili** e pruning aggressivo.
- ✅ Solo combinazioni, niente permutazioni (ordine irrilevante come nel Lotto).
- ✅ Vincoli su somma, pari/dispari, decine coinvolte, range massimo.
- ✅ Motore a backtracking con vincoli **parziali** e **finali**, separati per modulo.

## Installazione (locale)
```text
git clone https://github.com/gcomneno/giankolotto-smart-combos.git
cd giankolotto-smart-combos
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## 🧬 Cos’è questo affare?
`giankolotto-smart-combos` è un motore combinatorio **Lotto-compliant** progettato per:
- generare **combinazioni** (non permutazioni!) di numeri 1–90  
- rispettare vincoli **configurabili** e **serissimi**
- eliminare miliardi di rami inutili con un sorriso  
- mantenere la sanità mentale del programmatore (forse)

Il tutto con una spolverata dell’inconfondibile stile **Giadaware™**: semi-serio, matematico, e più pulito di quanto dovrebbe esserlo.

---

## 🚀 Perché esiste?
Perché le 43.949.268 combinazioni del Lotto non si generano da sole, e perché il brute force puro ormai è out, mentre il **pruning intelligente** è la nuova moda.

Se vuoi:
- filtrare per **somma minima/massima**,  
- imporre **almeno X pari e Y dispari**,  
- garantire **N decine diverse**,  
- limitare il **range massimo**,  
- o costruire le tue **regole custom**…

allora questo motore ti farà risparmiare vita, RAM e caffeina.

---

## 🌿 Filosofia Giadaware™

- **Zero fuffa.** Se un vincolo non taglia rami, fuori.  
- **Eleganza prima della violenza.** Backtracking sì, ma con pruning chirurgico.  
- **Modularità totale.** Vincoli separati in un modulo dedicato.  
- **Lotto-compliant.** Solo combinazioni ordinate; niente permutazioni!!
- **Prototipo, non oracolo.** Se vuoi predire il futuro.. servono moduli aggiuntivi che solo la Dea Bendata ti vorrà dare 😄

---

## 🛠️ Come si usa
Esempio da 10 righe:

```python
from giankolotto_smart_combos import LottoConfig, smart_lotto_search

cfg = LottoConfig(
    k=5,
    min_sum=100,
    max_sum=220,
    min_even=2,
    min_odd=2,
    min_decades=3,
    max_range=60,
)

for combo in smart_lotto_search(cfg):
    print(combo)
```

## 🧩 Moduli
config_lotto.py → configurazione + utilities
constraints_lotto.py → vincoli parziali e completi
smart_lotto_search.py → il motore combinatorio con pruning

## 🤝 Contribuire
Bug? Idee? Vincoli assurdi che vorresti aggiungere?
Le PR sono benvenute, specialmente quelle che aumentano l’entropia controllata.

## 💖 Ringraziamenti
A te, esploratore combinatorio, che sfidi l’ordine casuale e la logica del caso con il sorriso di un folle lucido.
Benvenuto nel laboratorio Giadaware™.
