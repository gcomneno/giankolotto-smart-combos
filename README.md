# giankolotto-smart-combos

Motore Lotto-compliant per la generazione di **combinazioni** di numeri (1–90) con
**vincoli configurabili** e pruning aggressivo.

- ✅ Solo combinazioni, niente permutazioni (ordine irrilevante come nel Lotto).
- ✅ Vincoli su somma, pari/dispari, decine coinvolte, range massimo.
- ✅ Motore a backtracking con vincoli **parziali** e **finali**, separati per modulo.

## Installazione (locale)
```bash
git clone https://github.com/gcomneno/giankolotto-smart-combos.git
cd giankolotto-smart-combos
python -m venv .venv
source .venv/bin/activate
pip install -e .
````
