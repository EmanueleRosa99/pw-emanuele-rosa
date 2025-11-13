import random
from typing import Dict, Tuple, List
from models import Prodotto, Impianto

_LINEE_RANGE: Tuple[int, int] = (4, 8)
# La capacita di una linea può variare, in base alla modernità dei macchinari
_CAPACITA_LINEA_RANGE: Tuple[float, float] = (0.8, 1.2)



def _genera_nomi_linee(n: int) -> List[str]:
    # Restituisce nomi delle linee in ordine alfabetico
    return [chr(ord('A') + i) for i in range(n)]

# Funzione per generare randomicamente le quantita da produrre per ogni prodotto
def genera_quantita_produzione(
    prodotti: List[Prodotto],
    quantita_min: int = 50,
    quantita_max: int = 250,
) -> Dict[Prodotto, int]:
        
    if quantita_min < 0 or quantita_max < quantita_min:
        raise ValueError("Range quantità non valido")
    
    return {p: random.randint(quantita_min, quantita_max) for p in prodotti}


# Genera i parametri configurabili per la simulazione
def genera_parametri_configurabili(
    prodotti: List[Prodotto]
) -> Tuple[Dict[Prodotto, float], Dict[Prodotto, int], int, Impianto]:
    
    # Genera tempi di produzione per unità
    tempo_per_unita = {
        p: round(random.uniform(*p.range_tempo_produzione), 2) for p in prodotti
    }

    # Genera capacità giornaliera per tipologia di prodotto
    capacita_giornaliera_per_prodotto = {
        p: random.randint(*p.range_capacita_giornaliera) for p in prodotti
    }
    
    # Genera linee di produzione
    numero_linee = random.randint(*_LINEE_RANGE)
    nomi_linee = _genera_nomi_linee(numero_linee)
    linee = [
        (nomi_linee[i], round(random.uniform(*_CAPACITA_LINEA_RANGE), 2)) 
        for i in range(numero_linee)
    ]
    # Crea oggetto Impianto
    impianto = Impianto(linee)
    
    # Calcola capacità giornaliera complessiva (ossia la somma delle capacità per prodotto)
    capacita_giornaliera_complessiva = sum(capacita_giornaliera_per_prodotto.values())
 
    return (
        tempo_per_unita, 
        capacita_giornaliera_per_prodotto,
        capacita_giornaliera_complessiva,
        impianto
    )

def _alloca_linee(
    lavoro_per_prodotto: Dict[Prodotto, float],
    impianto: Impianto
) -> Dict[Prodotto, List[Tuple[str, float]]]:
    
    # Alloca le linee alle tipologie da produrre, basandosi sul carico di lavoro richiesto per ciascuna di esse
    linee_nominate = impianto.linee.copy()

    # Ordina prodotti e linee
    prodotti = sorted(
        lavoro_per_prodotto.keys(), 
        key=lambda p: lavoro_per_prodotto[p], 
        reverse=True
    )
    linee_nominate.sort(key=lambda lc: lc[1], reverse=True)

    linee_assegnate: Dict[Prodotto, List[Tuple[str, float]]] = {p: [] for p in prodotti}

    for nome, capacita in linee_nominate:
        def score(p: Prodotto) -> tuple:
            capacita_prodotto = sum(c for _, c in linee_assegnate[p])
            # Condizione se non ha ancora linee assegnate
            if capacita_prodotto <= 1e-12:
                return (float('inf'), lavoro_per_prodotto[p])
            return (lavoro_per_prodotto[p] / capacita_prodotto, lavoro_per_prodotto[p])
        
        target = max(prodotti, key=score)
        linee_assegnate[target].append((nome, capacita))

    return linee_assegnate

def calcola_tempo_produzione_lotto(
    quantita: Dict[Prodotto, int],
    tempo_per_unita: Dict[Prodotto, float],
    capacita_giornaliera_per_prodotto: Dict[Prodotto, int],
    capacita_giornaliera_complessiva: int,
    impianto: Impianto,
    ore_per_giorno: int = 24
) -> Dict[str, object]:
   
    # Tempo per prodotto su singola linea produttiva
    lavoro_per_prodotto = {p: quantita[p] * tempo_per_unita[p] for p in quantita}
    
    # Allocazione proporzionale delle linee (in base alla quantita di lavoro necessario alla produzione)
    linee_per_prodotto = _alloca_linee(lavoro_per_prodotto, impianto)
    
    # Calcolo tempi per prodotto con dettagli utili da mostrare in output
    tempo_per_prodotto_ore: Dict[Prodotto, float] = {}
    dettagli: Dict[Prodotto, dict] = {}
    
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

    # Durata complessiva del lotto (in ore e giorni)
    durata_ore = round(max(tempo_per_prodotto_ore.values()), 2)
    durata_giorni = round(durata_ore / max(1, ore_per_giorno), 3)

    # Dati per output
    impianto_dettaglio = [f"{nome}: {cap:.2f}" for nome, cap in impianto.linee]
    
    return {
        "quantita": quantita,
        "tempo_per_unita": tempo_per_unita,
        "capacita_giornaliera_per_prodotto": capacita_giornaliera_per_prodotto,
        "capacita_giornaliera_complessiva": capacita_giornaliera_complessiva,
        "lavoro_per_prodotto_ore": {p.nome: dettagli[p]["lavoro_ore"] for p in dettagli},
        "linee_assegnate_dettaglio": {
            p.nome: dettagli[p]["linee_assegnate_dettaglio"] for p in dettagli
        },
        "capacita_totale_linee_assegnate": {
            p.nome: dettagli[p]["capacita_totale"] for p in dettagli
        },
        "tempo_per_prodotto_ore": {
            p.nome: dettagli[p]["totale_ore"] for p in dettagli
        },
        "tempo_per_prodotto_giorni": {
            p.nome: dettagli[p]["totale_giorni"] for p in dettagli
        },
        "impianto": impianto,
        "impianto_linee": impianto_dettaglio,
        "capacita_totale_impianto": impianto.capacita_totale,
        "durata_lotto_ore": durata_ore,
        "durata_lotto_giorni": durata_giorni,
        "ore_per_giorno": ore_per_giorno,
    }