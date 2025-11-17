import random
from typing import Dict, List, Tuple
from models import Prodotto, LineaProduttiva, Impianto


# Funzione per generare le quantità da produrre per ciascuna tipologia
def genera_quantita_produzione(prodotti: List[Prodotto]) -> Dict[Prodotto, int]:
    return {prodotto: random.randint(*prodotto.range_quantita_produzione) for prodotto in prodotti}

# Funzione per generare i parametri configurabili
def genera_parametri_configurabili(
    prodotti: List[Prodotto]
) -> Tuple[Dict[Prodotto, float], Impianto]:
    
    # Genera tempi di produzione per unità (in ore)
    tempo_per_unita = {
        prodotto: round(random.uniform(*prodotto.range_tempo_produzione), 2) 
        for prodotto in prodotti
    }
    
    # Crea 4 linee produttive con coefficienti di efficienza diversi
    coefficienti = [
        round(random.uniform(0.7, 1.0), 2),
        round(random.uniform(0.8, 1.1), 2),
        round(random.uniform(0.9, 1.2), 2),
        round(random.uniform(1.0, 1.3), 2)
    ]
    
    nomi_linee = ['A', 'B', 'C', 'D']
    linee = [LineaProduttiva(nomi_linee[i], coefficienti[i]) for i in range(4)]
    
    impianto = Impianto(linee)
    
    return tempo_per_unita, impianto


def assegna_linee_a_prodotti(
    prodotti: List[Prodotto],
    quantita: Dict[Prodotto, int],
    tempo_per_unita: Dict[Prodotto, float],
    impianto: Impianto
) -> Dict[Prodotto, LineaProduttiva]:

    # Calcola il carico di lavoro totale per ogni prodotto (in ore)
    carico_lavoro = {prodotto: quantita[prodotto] * tempo_per_unita[prodotto] for prodotto in prodotti}
    
    # Ordina i prodotti per carico di lavoro decrescente
    prodotti_ordinati = sorted(carico_lavoro.keys(), key=lambda prodotto: carico_lavoro[prodotto], reverse=True)
    
    # Ordina le linee per coefficiente decrescente
    linee_ordinate = sorted(impianto.linee, key=lambda linea: linea.coefficiente_efficienza, reverse=True)
    
    # Assegna: prodotto con più carico alla linea con efficienza migliore
    assegnazioni = {}
    for i, prodotto in enumerate(prodotti_ordinati):
        assegnazioni[prodotto] = linee_ordinate[i]
    
    return assegnazioni

def valida_input_utente(data: dict, prodotti: list, modalita: str = 'automatico') -> list:
    errori = []
    
    # Validazione quantità (obbligatoria in entrambe le modalità)
    campi_quantita = ['quantita_giacche', 'quantita_tshirt', 'quantita_felpe', 'quantita_pantaloni']
    for campo in campi_quantita:
        if campo not in data or data[campo] is None or data[campo] == '':
            errori.append(f"Il campo {campo} è obbligatorio")
            continue
        
        try:
            valore = int(data[campo])
            if valore <= 0:
                errori.append(f"{campo} deve essere maggiore di 0")
            elif valore > 1000:
                errori.append(f"{campo} non può superare 1000")
        except (ValueError, TypeError):
            errori.append(f"{campo} deve essere un numero intero valido")
    
    # Validazione parametri manuali
    if modalita == 'manuale':
        # Valida tempi di produzione
        campi_tempo = ['tempo_giacche', 'tempo_tshirt', 'tempo_felpe', 'tempo_pantaloni']
        for campo in campi_tempo:
            if campo not in data or data[campo] is None or data[campo] == '':
                errori.append(f"Il campo {campo} è obbligatorio in modalità manuale")
                continue
            
            try:
                valore = float(data[campo])
                if valore <= 0:
                    errori.append(f"{campo} deve essere maggiore di 0")
                elif valore > 24:
                    errori.append(f"{campo} non può superare 24 ore")
            except (ValueError, TypeError):
                errori.append(f"{campo} deve essere un numero valido")
        
        # Valida coefficienti linee
        campi_coeff = ['coeff_linea_a', 'coeff_linea_b', 'coeff_linea_c', 'coeff_linea_d']
        for campo in campi_coeff:
            if campo not in data or data[campo] is None or data[campo] == '':
                errori.append(f"Il campo {campo} è obbligatorio in modalità manuale")
                continue
            
            try:
                valore = float(data[campo])
                if valore <= 0:
                    errori.append(f"{campo} deve essere maggiore di 0")
                elif valore > 2:
                    errori.append(f"{campo} non può superare 2.0")
            except (ValueError, TypeError):
                errori.append(f"{campo} deve essere un numero valido")
    
    return errori


def _arrotonda_tempo_in_minuti(ore_decimali: float) -> float:

    ore_intere = int(ore_decimali)
    minuti_decimali = (ore_decimali - ore_intere) * 60
    minuti_arrotondati = round(minuti_decimali)
    return ore_intere + minuti_arrotondati / 60


# Funzione per calcolare le tempistiche di produzione
def calcola_tempo_produzione_lotto(
    quantita: Dict[Prodotto, int],
    tempo_per_unita: Dict[Prodotto, float],
    assegnazioni_linee: Dict[Prodotto, LineaProduttiva],
    ore_per_giorno: int = 24
) -> Dict[str, object]:
    
    risultati_per_prodotto = {}
    
    for prodotto, linea in assegnazioni_linee.items():
        # Calcola tempo effettivo sulla linea
        tempo_teorico = tempo_per_unita[prodotto]
        tempo_effettivo_preciso = tempo_teorico / linea.coefficiente_efficienza
        tempo_effettivo = _arrotonda_tempo_in_minuti(tempo_effettivo_preciso)
        
        # Calcola capacità giornaliera usando il tempo effettivo arrotondato
        capacita_giornaliera = int((ore_per_giorno * linea.coefficiente_efficienza) / tempo_teorico)
        
        # Ore totali necessarie usando il tempo effettivo
        ore_totali = quantita[prodotto] * tempo_effettivo
        
        # Giorni necessari
        giorni_necessari = ore_totali / ore_per_giorno
        
        risultati_per_prodotto[prodotto] = {
            'linea_assegnata': linea,
            'tempo_effettivo': tempo_effettivo,
            'capacita_giornaliera': capacita_giornaliera,
            'ore_totali': round(ore_totali, 2),
            'giorni_necessari': round(giorni_necessari, 3)
        }
    
    # Durata complessiva del lotto
    durata_ore = max(r['ore_totali'] for r in risultati_per_prodotto.values())
    durata_giorni = durata_ore / ore_per_giorno
    
    # Capacità giornaliera complessiva
    capacita_giornaliera_complessiva = sum(
        risultato['capacita_giornaliera'] for risultato in risultati_per_prodotto.values()
    )
    
    return {
        'quantita': quantita,
        'tempo_per_unita': tempo_per_unita,
        'assegnazioni_linee': assegnazioni_linee,
        'risultati_per_prodotto': risultati_per_prodotto,
        'capacita_giornaliera_complessiva': capacita_giornaliera_complessiva,
        'durata_lotto_ore': round(durata_ore, 2),
        'durata_lotto_giorni': round(durata_giorni, 3),
        'ore_per_giorno': ore_per_giorno
    }
