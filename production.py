import random
from typing import Dict, Tuple, List
from models import TipoProdotto


def genera_quantita_produzione(prodotti: List[TipoProdotto] = None, 
                               quantita_min: int = 30, 
                               quantita_max: int = 150) -> Dict[TipoProdotto, int]:
    if prodotti is None:
        prodotti = list(TipoProdotto)

    quantita = {}
    for prodotto in prodotti:
        quantita[prodotto] = random.randint(quantita_min, quantita_max)

    return quantita


def genera_parametri_configurabili(prodotti: List[TipoProdotto] = None) -> Tuple[Dict[TipoProdotto, float], Dict[TipoProdotto, int], int]:

    if prodotti is None:
        prodotti = list(TipoProdotto)

    tempo_per_unita = {
        prodotto: round(random.uniform(2.0, 10.0), 2) 
        for prodotto in prodotti
    }

    capacita_per_prodotto = {
        prodotto: random.randint(10, 50) 
        for prodotto in prodotti
    }

    somma_capacita = sum(capacita_per_prodotto.values())
    capacita_complessiva = random.randint(
        int(somma_capacita * 0.7), 
        int(somma_capacita * 0.9)
    )

    return tempo_per_unita, capacita_per_prodotto, capacita_complessiva


def calcola_tempo_produzione_lotto(quantita: Dict[TipoProdotto, int], 
                                   tempo_per_unita: Dict[TipoProdotto, float],
                                   capacita_per_prodotto: Dict[TipoProdotto, int],
                                   capacita_complessiva: int) -> Dict[str, float]:

    risultati = {}

    ore_per_prodotto = {}
    ore_totali = 0

    for prodotto, qta in quantita.items():
        ore = qta * tempo_per_unita[prodotto]
        ore_per_prodotto[prodotto] = ore
        ore_totali += ore

    risultati['ore_per_prodotto'] = ore_per_prodotto
    risultati['ore_totali'] = ore_totali

    giorni_per_prodotto = {}

    for prodotto, qta in quantita.items():
        giorni = qta / capacita_per_prodotto[prodotto]
        giorni_per_prodotto[prodotto] = giorni

    totale_capi = sum(quantita.values())
    giorni_vincolo_complessivo = totale_capi / capacita_complessiva

    giorni_massimi_per_prodotto = max(giorni_per_prodotto.values())
    giorni_produzione = max(giorni_massimi_per_prodotto, giorni_vincolo_complessivo)

    risultati['giorni_per_prodotto'] = giorni_per_prodotto
    risultati['giorni_produzione_totali'] = giorni_produzione

    risultati['ore_lavorative_totali'] = giorni_produzione * 8

    return risultati
