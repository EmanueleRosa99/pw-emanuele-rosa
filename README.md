# Alla Moda 2.0

Applicazione per la simulazione e pianificazione di lotti di produzione, per aziende operanti nel settore dell'alta moda. Il simulatore è basato su un impianto produttivo con quattro linee di lavoro e calcola tempi e capacità per la produzione di giacche invernali, t-shirt, felpe e pantaloni.

## Requisiti

- Python 3.8 o superiore
- Flask 2.0 o superiore (Opzionale)

## Utilizzo

### Versione Web

La versione web offre un'interfaccia grafica per inserire i parametri e visualizzare i risultati da interfaccia grafica.

Avviare il server Flask:
python3 app.py

Aprire il browser all'indirizzo `http://localhost:5000` e compilare il form.
I tempi di produzione unitari vengono generati casualmente dall'applicazione all'interno dei range realistici per ciascun tipo di prodotto.

### Versione a riga di comando
Questa modalità genera automaticamente tutti i parametri (quantità, tempi, coefficienti) e mostra l'output formattato direttamente nel terminale.


## Licenza

Progetto sviluppato per scopi didattici.