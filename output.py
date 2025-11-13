from typing import Dict, Tuple
from models import Prodotto

def _converti_ore_in_ore_minuti(ore_decimali: float) -> Tuple[int, int]:
    ore_intere = int(ore_decimali)
    minuti = int((ore_decimali - ore_intere) * 60)
    return ore_intere, minuti


def _converti_ore_in_giorni_ore(ore_decimali: float, ore_per_giorno: int = 24) -> Tuple[int, int]:

    giorni_interi = int(ore_decimali / ore_per_giorno)
    ore_rimanenti = int(ore_decimali % ore_per_giorno)
    
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


def output_simulazione_produzione(risultati: Dict[str, object]) -> None:

    larg = 96
    ore_per_giorno = risultati['ore_per_giorno']

    # Header
    print("╔" + "═" * larg + "╗")
    print(f" {'· SIMULAZIONE LOTTO PRODUZIONE ·':^{larg}}")
    print("╚" + "═" * larg + "╝")
    
    # Quantità prodotte
    print("\nQuantità (capi):")
    for p, q in risultati['quantita'].items():
        print(f"  • {p.nome:20s}: {q:4d}")
    
    # Tempi unitari di produzione
    print("\nTempi unitari di produzione (h/capo):")
    for p, t in risultati['tempo_per_unita'].items():
        print(f"  • {p.nome:20s}: {t:4.2f} h/capo")
    
    # Capacità massima giornaliera per tipologia
    print("\nCapacità massima giornaliera per tipologia (capi/giorno):")
    for p, cap in risultati['capacita_giornaliera_per_prodotto'].items():
        print(f"  • {p.nome:20s}: {cap:4d} capi/giorno")
    
    # Capacità giornaliera complessiva
    print(f"\nCapacità giornaliera complessiva: {risultati['capacita_giornaliera_complessiva']} capi/giorno")
    
    # Linee disponibili
    impianto = risultati['impianto']
    print(f"\nLinee disponibili (nome: capacità) e somma:")
    print(f"  • Numero linee: {impianto.numero_linee}")
    print(f"  • Capacità linee: {risultati['impianto_linee']}")
    print(f"  • Capacità totale impianto: {risultati['capacita_totale_impianto']:.2f}")
    
    # Tabella dettagli per prodotto
    _stampa_tabella_dettaglio(risultati)
    tempo_ore_formattato = _formatta_tempo_ore(risultati['durata_lotto_ore'])
    tempo_giorni_formattato = _formatta_tempo_giorni(risultati['durata_lotto_ore'], ore_per_giorno)


    # Riepilogo complessivo
    print("\nRiepilogo complessivo:")
    print(f"  • Durata totale del lotto (Ore):    {tempo_ore_formattato}")
    print(f"  • Durata totale del lotto (Giorni): {tempo_giorni_formattato}")


def _stampa_tabella_dettaglio(risultati: dict, ore_per_giorno: int = 24) -> None:

    nomi = list(risultati["lavoro_per_prodotto_ore"].keys())
    tempi_ore_formattati = {}
    tempi_giorni_formattati = {}
    
    for nome in nomi:
        ore = risultati["tempo_per_prodotto_ore"][nome]
        tempi_ore_formattati[nome] = _formatta_tempo_ore(ore)
        tempi_giorni_formattati[nome] = _formatta_tempo_giorni(ore, ore_per_giorno)
        
    # Calcolo larghezze colonne
    w_prod = max(len("Prodotto"), max(len(n) for n in nomi))
    w_lav = max(
        len("Lavoro (ore.minuti)"),
        max(len(f'{risultati["lavoro_per_prodotto_ore"][n]:.2f}') for n in nomi),
    )
    w_linee = max(
        len("Linee assegnate"),
        max(len(", ".join(risultati["linee_assegnate_dettaglio"][n]) or "-") for n in nomi),
    )
    w_cap = max(
        len("Capacità (gg)"),
        max(len(f'{risultati["capacita_totale_linee_assegnate"][n]:.2f}') for n in nomi),
    )
    w_t_ore = max(
        len("Tempo (ore e minuti)"),
        max(len(tempi_ore_formattati[n]) for n in nomi),
    )
    w_t_gio = max(
        len("Tempo (giorni e ore)"),
        max(len(tempi_giorni_formattati[n]) for n in nomi),
    )
    
    # Header tabella
    header = (
        f"  {'Prodotto':^{w_prod}} | "
        f"{'Lavoro (ore.minuti)':^{w_lav}} | "
        f"{'Linee assegnate':^{w_linee}} | "
        f"{'Capacità (gg)':^{w_cap}} | "
        f"{'Tempo (ore e minuti)':^{w_t_ore}} | "
        f"{'Tempo (giorni e ore)':^{w_t_gio}}"
    )
    sep = "  " + "-" * (len(header) - 2)
    sep = "  " + "-" * (len(header) - 2)
    
    print("\nDettaglio assegnazioni e tempi per prodotto:")
    print(header)
    print(sep)
    
    # Righe tabella
    for nome in nomi:
        lavoro = risultati["lavoro_per_prodotto_ore"][nome]
        linee_det = ", ".join(risultati["linee_assegnate_dettaglio"][nome]) or "-"
        cap_tot = risultati["capacita_totale_linee_assegnate"][nome]
        t_ore_fmt = tempi_ore_formattati[nome]
        t_gio_fmt = tempi_giorni_formattati[nome]
        
        riga = (
            f"  {nome:<{w_prod}} | "
            f"{lavoro:>{w_lav}.2f} | "
            f"{linee_det:<{w_linee}} | "
            f"{cap_tot:>{w_cap}.2f} | "
            f"{t_ore_fmt:<{w_t_ore}} | "
            f"{t_gio_fmt:<{w_t_gio}}"
        )
        print(riga)
