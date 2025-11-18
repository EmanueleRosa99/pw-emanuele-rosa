from typing import Dict, Tuple

# Funzioni per le conversioni e formattazioni
def _converti_ore_in_ore_minuti(ore_decimali: float) -> Tuple[int, int]:
    
    ore_intere = int(ore_decimali)
    minuti = round((ore_decimali - ore_intere) * 60)
    
    return ore_intere, minuti


def _converti_ore_in_giorni_ore(ore_decimali: float, ore_per_giorno: int = 24) -> Tuple[int, int]:

    giorni_interi = int(ore_decimali / ore_per_giorno)
    ore_rimanenti = round(ore_decimali % ore_per_giorno)

    return giorni_interi, ore_rimanenti


def _formatta_tempo_ore(ore_decimali: float) -> str:

    ore, minuti = _converti_ore_in_ore_minuti(ore_decimali)
    if minuti == 0:
        return f"{ore} ore"

    return f"{ore} ore e {minuti} minuti"


def _formatta_tempo_giorni(ore_decimali: float, ore_per_giorno: int = 24) -> str:

    giorni, ore = _converti_ore_in_giorni_ore(ore_decimali, ore_per_giorno)
    if giorni == 0:
        return f"{ore} ore"
    elif ore == 0:
        return f"{giorni} giorni"
    
    return f"{giorni} giorni e {ore} ore"


def _formatta_tempo_unitario(ore_decimali: float) -> str:

    ore, minuti = _converti_ore_in_ore_minuti(ore_decimali)
    
    if ore == 0:
        return f"{minuti}min/capo"
    elif minuti == 0:
        return f"{ore}h/capo"
    else:
        return f"{ore}h e {minuti}min/capo"


# Funzione per generare l'output mostrato in console
def output_simulazione_produzione(risultati: Dict[str, object]) -> None:
    
    larghezza = 100
    ore_per_giorno = risultati['ore_per_giorno']

    print("\n" + "-" * larghezza)
    print(f" {'SIMULAZIONE LOTTO PRODUZIONE':^{larghezza}}")
    print("\n" + "-" * larghezza)
        
    # Quantità prodotte
    print("\n [ QUANTITÀ DA PRODURRE ]")
    for prodotto, quantita in risultati['quantita'].items():
        print(f"  - {prodotto.nome:25s}: {quantita:4d} capi")
    
    # Tempi unitari di produzione (TEORICI e base)
    print("\n [ TEMPI UNITARI DI PRODUZIONE (teorici di base) ]")
    for prodotto, tempo in risultati['tempo_per_unita'].items():
        tempo_formattato = _formatta_tempo_unitario(tempo)
        print(f"  - {prodotto.nome:25s}: {tempo_formattato}")
    
    # Configurazione impianto
    print("\n [ CONFIGURAZIONE IMPIANTO ]")
    print(f"  Numero linee produttive: {len(risultati['assegnazioni_linee'])}")
    

    print("\n [ ASSEGNAZIONE LINEE E CAPACITÀ PRODUTTIVA ]")
    for prodotto, linea in risultati['assegnazioni_linee'].items():
        dati = risultati['risultati_per_prodotto'][prodotto]
        tempo_teorico = risultati['tempo_per_unita'][prodotto]
        tempo_effettivo = dati['tempo_effettivo']
        carico_ore = risultati['quantita'][prodotto] * tempo_teorico
        
        tempo_teorico_format = _formatta_tempo_unitario(tempo_teorico)
        tempo_effettivo_format = _formatta_tempo_unitario(tempo_effettivo)
        carico_ore_format = _formatta_tempo_ore(carico_ore)
        
        print(f"\n  {prodotto.nome}:")
        print(f"    ├─ Linea assegnata:              {linea.nome} (efficienza: {linea.coefficiente_efficienza:.2f})")
        print(f"    ├─ Tempo teorico per unità:      {tempo_teorico_format}")
        print(f"    ├─ Tempo effettivo sulla linea:  {tempo_effettivo_format}")
        print(f"    ├─ Carico di lavoro teorico totale:      {carico_ore_format}")
        print(f"    ├─ Capacità giornaliera:         {dati['capacita_giornaliera']} capi/giorno")
        print(f"    ├─ Tempo di produzione:          {_formatta_tempo_ore(dati['ore_totali'])}")
        print(f"    └─ Giorni necessari:             {dati['giorni_necessari']:.2f} giorni")
    
    
    # Capacità complessiva
    print(f"\n  [ CAPACITÀ GIORNALIERA COMPLESSIVA ]")
    print(f"  - Totale impianto: {risultati['capacita_giornaliera_complessiva']} capi/giorno")
    print(f"    (somma delle capacità di tutte le linee)")
    
    # Tabella dettagliata
    _stampa_tabella_dettaglio(risultati)
    
    # Riepilogo complessivo
    tempo_ore_formattato = _formatta_tempo_ore(risultati['durata_lotto_ore'])
    tempo_giorni_formattato = _formatta_tempo_giorni(risultati['durata_lotto_ore'], ore_per_giorno)
    
    print("\n" + "-" * larghezza)
    print(f" {' RIEPILOGO COMPLESSIVO ':^{larghezza}}")
    print("\n" + "-" * larghezza)
    print(f"\n   Durata totale del lotto:")
    print(f"      - In ore:    {tempo_ore_formattato}")
    print(f"      - In giorni: {tempo_giorni_formattato}")


def _stampa_tabella_dettaglio(risultati: dict) -> None:
    """Stampa una tabella riassuntiva dei dettagli per prodotto"""
    
    print("\n [ TABELLA RIASSUNTIVA ] ")
    
    # Header
    header = (
        f"  {'Prodotto':^25} | "
        f"{'Quantità':^10} | "
        f"{'Tempo base':^18} | "
        f"{'Linea':^6} | "
        f"{'Effic.':^7} | "
        f"{'Tempo effettivo':^18} | "
        f"{'Cap./gg':^9} | "
        f"{'Tempo tot.':^20}"
    )
    sep = "  " + "-" * (len(header) - 2)
    
    print(header)
    print(sep)
    
    # Righe
    for prodotto in risultati['quantita'].keys():
        qta = risultati['quantita'][prodotto]
        tempo_base = risultati['tempo_per_unita'][prodotto]
        linea = risultati['assegnazioni_linee'][prodotto]
        tempo_effettivo = tempo_base / linea.coefficiente_efficienza
        dati = risultati['risultati_per_prodotto'][prodotto]
        
        tempo_base_format = _formatta_tempo_unitario(tempo_base)
        tempo_effettivo_format = _formatta_tempo_unitario(tempo_effettivo)
        
        riga = (
            f"  {prodotto.nome:<25} | "
            f"{qta:^10d} | "
            f"{tempo_base_format:^18} | "
            f"{linea.nome:^6} | "
            f"{linea.coefficiente_efficienza:^7.2f} | "
            f"{tempo_effettivo_format:^18} | "
            f"{dati['capacita_giornaliera']:^9d} | "
            f"{_formatta_tempo_ore(dati['ore_totali']):^20}"
        )
        print(riga)
    
    print("\n  Legenda:")
    print("    - Tempo base: tempo teorico per produrre un capo")
    print("    - Effic.: coefficiente di efficienza della linea")
    print("    - Tempo effettivo: tempo reale sulla linea = Tempo base / Efficienza")
    print("    - Cap./gg: capacità giornaliera = 24 ore / Tempo effettivo di produzione")
