import random
from typing import Dict, Tuple, List
from models import TipoProdotto

_TEMPI_ORA_RANGE: Dict[TipoProdotto, Tuple[float, float]] = {
    TipoProdotto.GIACCA_INVERNALE: (3.5, 8.0),
    TipoProdotto.FELPA: (1.5, 4.0),
    TipoProdotto.PANTALONE: (1.8, 4.5),
    TipoProdotto.TSHIRT: (0.5, 1.8),
}
_LINEE_RANGE: Tuple[int, int] = (4, 8)

# La capacita di una linea può variare, in base all'impianto presente
_CAPACITA_LINEA_RANGE: Tuple[float, float] = (0.8, 1.2)


def _genera_nomi_linee(n: int) -> List[str]:
    # Restituisce nomi delle linee, in ordine alfabetico
    return [chr(ord('A') + i) for i in range(n)]

# Funzione per generare randomicamente le quantita da produrre dei prodotti (enum TipoProdotto)
def genera_quantita_produzione(
    prodotti: List[TipoProdotto] = None,
    quantita_min: int = 50,
    quantita_max: int = 250,
) -> Dict[TipoProdotto, int]:

    if prodotti is None:
        prodotti = list(TipoProdotto)
        
    if quantita_min < 0 or quantita_max < quantita_min:
        raise ValueError("Range quantità non valido")
    
    return {p: random.randint(quantita_min, quantita_max) for p in prodotti}

def genera_parametri_configurabili(
    prodotti: List[TipoProdotto] = None
) -> Tuple[Dict[TipoProdotto, float], List[Tuple[str, float]]]:
    
    if prodotti is None:
        prodotti = list(TipoProdotto)

    numero_linee = random.randint(*_LINEE_RANGE)
    tempo_per_unita = {
        p: round(random.uniform(*_TEMPI_ORA_RANGE[p]), 2) for p in prodotti
        }
    nomi_linee = _genera_nomi_linee(numero_linee)
    # Lista di (nome_linea, capacità)
    impianto_linee = [
        (nomi_linee[i], round(random.uniform(*_CAPACITA_LINEA_RANGE), 2)) for i in range(numero_linee)
        ]
    
    return tempo_per_unita, impianto_linee

def _alloca_linee(
    lavoro_per_prodotto: Dict[TipoProdotto, float],
    impianto_linee: List[float]
) -> Dict[TipoProdotto, int]:
    
    # Trasforma le linee in formato (nome, capacità)
    linee_nominate: List[Tuple[str, float]] = []
    for i, item in enumerate(impianto_linee):
        if isinstance(item, tuple):
            nome, capacita = item
            linee_nominate.append((str(nome), float(capacita)))
        else:
            nome = chr(ord("A") + i)
            linee_nominate.append((nome, float(item)))
            
    # Ordina prodotti e linee
    prodotti = sorted(
        lavoro_per_prodotto.keys(), key=lambda p: lavoro_per_prodotto[p], reverse=True
        )
    linee_nominate.sort(key=lambda lc: lc[1], reverse=True)

    assegnate: Dict[TipoProdotto, List[Tuple[str, float]]] = {p: [] for p in prodotti}

    for nome, cap in linee_nominate:
        def score(p: TipoProdotto) -> tuple:
            cap_p = sum(c for _, c in assegnate[p])
            # Se non ha ancora linee assegnate
            if cap_p <= 1e-12:
                return (float('inf'), lavoro_per_prodotto[p])
            return (lavoro_per_prodotto[p] / cap_p, lavoro_per_prodotto[p])

        target = max(prodotti, key=score)
        assegnate[target].append((nome, cap))

    return assegnate

def calcola_tempo_produzione_lotto(
    quantita: Dict[TipoProdotto, int],
    tempo_per_unita: Dict[TipoProdotto, float],
    impianto_linee: List[float],
    ore_per_giorno: int = 24
) -> Dict[str, object]:
   
    # Tempo per prodotto, su singola linea
    lavoro_per_prodotto = {p: quantita[p] * tempo_per_unita[p] for p in quantita}
    
    # Allocazione proporzionale delle linee (in base alla quantita di lavoro necessario alla produzione)
    linee_per_prodotto = _alloca_linee(lavoro_per_prodotto, impianto_linee)
    
    # Calcolo tempi per prodotto con dettagli utili per l'output
    tempo_per_prodotto_ore: Dict[TipoProdotto, float] = {}
    dettagli: Dict[TipoProdotto, dict] = {}
    
    for p, lavoro_ore in lavoro_per_prodotto.items():
        cap_list = linee_per_prodotto[p]
        capacita_tot = sum(c for _, c in cap_list)
        ore = (lavoro_ore / capacita_tot) if capacita_tot > 0 else float("inf")
        tempo_per_prodotto_ore[p] = round(ore, 2)

        linee_label = [f"{nome}: {cap:.2f}" for nome, cap in cap_list]
        dettagli[p] = {
            "lavoro_ore": round(lavoro_ore, 2),
            "linee_assegnate_dettaglio": linee_label,
            "capacita_totale": round(capacita_tot, 2),
            "totale_ore": round(ore, 2),
            "totale_giorni": round(ore / max(1, ore_per_giorno), 3),
        }

    # Durata complessiva del lotto in ore e giorni
    durata_ore = round(max(tempo_per_prodotto_ore.values()), 2)
    durata_giorni = round(durata_ore / max(1, ore_per_giorno), 3)

    # Dati per output
    impianto_dettaglio = [f"{nome}: {cap:.2f}" for nome, cap in impianto_linee]
    capacita_totale_impianto = round(sum(cap for _, cap in impianto_linee), 2)

    return {
        "lavoro_per_prodotto_ore": {p.value: dettagli[p]["lavoro_ore"] for p in dettagli},
        "linee_assegnate_dettaglio": {
            p.value: dettagli[p]["linee_assegnate_dettaglio"] for p in dettagli
        },
        "capacita_totale_linee_assegnate": {
            p.value: dettagli[p]["capacita_totale"] for p in dettagli
        },
        "tempo_per_prodotto_ore": {
            p.value: dettagli[p]["totale_ore"] for p in dettagli
        },
        "tempo_per_prodotto_giorni": {
            p.value: dettagli[p]["totale_giorni"] for p in dettagli
        },
        "impianto_linee": impianto_dettaglio,
        "capacita_totale_impianto": capacita_totale_impianto,
        "durata_lotto_ore": durata_ore,
        "durata_lotto_giorni": durata_giorni,
        "ore_per_giorno": ore_per_giorno,
    }