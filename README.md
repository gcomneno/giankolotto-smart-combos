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

## Playground
Riassunto del mix impostato per default in playground.py

Con:
```python
cfg = LottoConfig(
    k=5,
    min_sum=120,
    max_sum=220,
    min_even=2,
    min_odd=2,
    min_decades=3,
    max_range=60,
)
```

Sati dicendo al motore: “voglio solo le combinazioni che rispettano TUTTE queste condizioni contemporaneamente”.

In particolare:
> “Voglio cinquine di 5 numeri,
> con somma tra 120 e 220,
> con almeno 2 pari e 2 dispari,
> che coprano almeno 3 decine diverse,
> e che stiano dentro una finestra massima di ampiezza 60 sul tabellone.”

È già un set di vincoli abbastanza serio: taglia un botto di combinazioni senza essere esageratamente restrittivo.

#### `k=5`
Quanti numeri devono esserci in ogni combinazione.
- Per il Lotto classico: `k=5`
- Se volessi terzine, quartine, sestine, ecc. cambi solo questo.

> È il “peso” della combinazione.

#### `min_sum=120`, `max_sum=220`
Vincolo sulla somma totale dei numeri scelti.

Per una combinazione `[n1, n2, n3, n4, n5]`:
```python
s = n1 + n2 + n3 + n4 + n5
```

Il motore accetta solo le combinazioni con:
```text
120 ≤ s ≤ 220
```

Effetti pratici:
- taglia combinazioni con numeri troppo piccoli (somma bassa)
- taglia combinazioni con numeri troppo grandi (somma alta)

E grazie al pruning:
- se i primi 3 numeri danno già una somma che non potrà mai rientrare nell’intervallo, il ramo viene troncato subito.

#### `min_even=2`, `min_odd=2`
Vincolo su quanti pari e quanti dispari minimo devono esserci.

Nell'esempio esempio:
- almeno 2 numeri pari
- almeno 2 numeri dispari

Con `k=5`, vuol dire che sono ammessi pattern tipo:
  - 2 pari + 3 dispari
  - 3 pari + 2 dispari

- NON sono ammessi:
  - 4 pari + 1 dispari (dispari troppo pochi)
  - 5 pari o 5 dispari

Effetto combinatorio: elimina le combinazioni sbilanciate “tutti pari” o “tutti dispari”, e anche quelle molto sbilanciate.

In più, il pruning lo usa durante la costruzione:
- se hai già usato quasi tutti gli slot e non puoi più raggiungere i minimi (es. hai messo troppi dispari, non hai più spazio per i pari richiesti) → ramo morto.

#### `min_decades=3`
Vincolo sul numero minimo di decine diverse presenti.

La “decina” è definita così:
- 1–10  → decina 0
- 11–20 → decina 1
- 21–30 → decina 2
- …
- 81–90 → decina 8

Con `min_decades=3` stai dicendo:
> In ogni combinazione voglio almeno 3 decine diverse coinvolte.

Esempi:
- `[5, 8, 12, 14, 18]`
  decine: 0 (1–10), 1 (11–20) → solo 2 decine → scartata

- `[5, 18, 32, 47, 80]`
  decine: 0 (1–10), 1 (11–20), 3 (31–40), 4 (41–50), 7 (71–80) → 5 decine → accettata

Serve a evitare combinazioni “ammucchiate” tutte nella stessa fascia.

Il pruning lo usa così:
- se hai scelto pochi numeri e si vede già che anche riempiendo tutti gli slot non arriveresti mai a 3 decine diverse, taglia il ramo.

#### `max_range=60`
Vincolo sul range:
```python
range = max(combo) - min(combo)
```

Con `max_range=60` imponi:
```text
max(combo) - min(combo) ≤ 60
```

Esempi:
- `[5, 18, 32, 47, 60]`
  max=60, min=5 → range = 55 → OK

- `[5, 18, 32, 47, 80]`
  max=80, min=5 → range = 75 → scartata

Serve a:
- evitare combinazioni troppo “sparse” (tipo 1, 23, 45, 67, 89)
- concentrare la combinazione in una finestra più “compatta” del tabellone

Il vincolo viene controllato già sui prefissi:
- se dopo aver scelto 3–4 numeri il range parziale è già > 60 → ramo morto.

## 🎚 Preset di configurazione
Per evitare di dover impostare ogni volta tutti i parametri di `LottoConfig`, sono disponibili alcuni preset:

| Preset  | k  | min_sum | max_sum | min_even | min_odd | min_decades | max_range | Note                      |
|--------|----|---------|---------|----------|---------|-------------|-----------|---------------------------|
| soft   | 5  | –       | –       | 1        | 1       | 2           | –         | Vincoli leggeri           |
| medium | 5  | 120     | 220     | 2        | 2       | 3           | 60        | Profilo consigliato       |
| hard   | 5  | 140     | 200     | 2        | 2       | 4           | 45        | Vincoli più selettivi     |

Esempi:
```python
from giankolotto_smart_combos import smart_lotto_search, preset_medium, get_preset

cfg = preset_medium()                  # usa il preset 'medium'
cfg2 = get_preset("hard", max_sum=210) # preset 'hard' con override

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
