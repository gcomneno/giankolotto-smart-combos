## 📦 Versioni

### v0.1.0
- Prima release pubblica
- Motore combinazioni Lotto-compliant
- Vincoli su somma, pari/dispari, decine, range
- Benchmark integrato con progress bar e misure di pruning

---

## 🧭 Roadmap
Questo progetto è nato come motore combinatorio Lotto-compliant “smart”, ma la roadmap prevede diversi step di evoluzione, sia tecnici che ergonomici.

### 1️⃣ Preset ufficiali di configurazione
Introdurre una serie di preset predefiniti, ad esempio:
- `preset_soft`   → vincoli leggeri, ampia esplorazione
- `preset_medium` → set di vincoli simile all’esempio di default
- `preset_hard`   → vincoli molto selettivi, forte pruning

Ogni preset sarà documentato con una tabella dei parametri (`k`, `min_sum`, `max_sum`, `min_even`, `min_odd`, `min_decades`, `max_range`) e una breve descrizione dell’intento.

### 2️⃣ Interfaccia a riga di comando (CLI)
Aggiungere uno script/entry point per usare il motore direttamente da terminale, ad esempio:
```bash
giankolotto-smart-combos \
  --k 5 \
  --min-sum 120 \
  --max-sum 220 \
  --min-even 2 \
  --min-odd 2 \
  --min-decades 3 \
  --max-range 60
```

La CLI permetterà di:
- scegliere i parametri di LottoConfig
- selezionare eventuali preset (--preset medium)
- opzionalmente salvare l’output su file (--output combos.txt)

### 3️⃣ Test unitari
Aggiungere una batteria di test (es. con pytest) per:
- verificare la correttezza combinatoria:
- con pochi numeri (n piccolo, k piccolo) confrontando con math.comb
- testare i vincoli singolarmente: solo somma, solo pari/dispari, solo decine, solo range
- validare il comportamento del pruning: riduzione del numero di nodi rispetto al caso teorico?
- assicurare che il benchmark non esploda e produca metriche coerenti!

### 4️⃣ Packaging e rilascio su PyPI
Preparare il progetto per la pubblicazione su PyPI:
- rifinire pyproject.toml
- assegnare una versione semantica (0.1.0, 0.2.0, …)
- caricare il package su PyPI per installazione via: pip install giankolotto-smart-combos

### 5️⃣ Preset basati su analisi storica
Integrare preset derivati da analisi statistica reale delle estrazioni:
- distribuzione tipica di somma
- frequenza di range
- distribuzione decine
- pattern pari/dispari

L’obiettivo non è “predire il futuro”, ma proporre configurazioni compatibili con il comportamento storico delle combinazioni realmente estratte.

Valutare l'integrazione di una agent AI.

### 6️⃣ Mini-profiler interno
Estendere il motore di benchmark con metriche più dettagliate:
- nodi/secondo e combinazioni/secondo (medie e istantanee)
- stima del tempo residuo (ETA) durante la ricerca
- eventuale log ASCII più ricco (stile mini-dashboard) per esplorazioni molto lunghe

Tutto senza compromettere la semplicità dell’API base.

### 7️⃣ Modulo di valutazione di combinazioni da file di testo
Aggiungere un modulo dedicato alla valutazione di combinazioni fornite dall’utente tramite file di testo, ad esempio:

input: file .txt con una combinazione per riga
(es. 5 18 32 47 80)

per ogni combinazione:
- parsing e validazione (numeri in [1..90], lunghezza corrispondente a k, ecc.)
- verifica rispetto ai vincoli (LottoConfig corrente)
- output di un report: combinazione accettata/scartata con motivazione (quali vincoli viola)
- eventuali metriche (somma, range, decine, pattern pari/dispari)

Questo modulo permetterà di “testare” rapidamente combinazioni generate da altri strumenti o già giocate, confrontandole con il profilo impostato nel motore (Giadaware™-style).
