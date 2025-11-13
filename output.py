from typing import Dict
from models import Prodotto


def output_simulazione_produzione(risultati: Dict[str, object]) -> None:

    larg = 96
    
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
    capacita_complessiva = sum(risultati['capacita_giornaliera_per_prodotto'].values())
    print(f"\nCapacità giornaliera complessiva: {capacita_complessiva} capi/giorno")
    
    # Linee disponibili
    impianto = risultati['impianto']
    print(f"\nLinee disponibili (nome: capacità) e somma:")
    print(f"  • Numero linee: {impianto.numero_linee}")
    print(f"  • Capacità linee: {risultati['impianto_linee']}")
    print(f"  • Capacità totale impianto: {risultati['capacita_totale_impianto']:.2f}")
    
    # Tabella dettagli per prodotto
    _stampa_tabella_dettaglio(risultati)
    
    # Riepilogo complessivo
    print("\nRiepilogo complessivo:")
    print(f"  • Durata totale del lotto (ore):    {risultati['durata_lotto_ore']:.2f}")
    print(f"  • Durata totale del lotto (giorni): {risultati['durata_lotto_giorni']:.3f}")


def _stampa_tabella_dettaglio(risultati: dict) -> None:
    """Stampa la tabella di dettaglio delle assegnazioni e tempi per prodotto."""
    nomi = list(risultati["lavoro_per_prodotto_ore"].keys())
    
    # Calcolo larghezze colonne
    w_prod = max(len("Prodotto"), max(len(n) for n in nomi))
    w_lav = max(
        len("Lavoro (h)"),
        max(len(f'{risultati["lavoro_per_prodotto_ore"][n]:.2f}') for n in nomi),
    )
    w_linee = max(
        len("Linee assegnate (nome:cap)"),
        max(len(", ".join(risultati["linee_assegnate_dettaglio"][n]) or "-") for n in nomi),
    )
    w_cap = max(
        len("Capacità (giorno)"),
        max(len(f'{risultati["capacita_totale_linee_assegnate"][n]:.2f}') for n in nomi),
    )
    w_t_ore = max(
        len("Totale ore"),
        max(len(f'{risultati["tempo_per_prodotto_ore"][n]:.2f}') for n in nomi),
    )
    w_t_gio = max(
        len("Totale giorni"),
        max(len(f'{risultati["tempo_per_prodotto_giorni"][n]:.3f}') for n in nomi),
    )
    
    # Header tabella
    header = (
        f"  {'Prodotto':^{w_prod}} | "
        f"{'Lavoro (h)':^{w_lav}} | "
        f"{'Linee assegnate (nome:cap)':^{w_linee}} | "
        f"{'Capacità (giorno)':^{w_cap}} | "
        f"{'Totale ore':^{w_t_ore}} | "
        f"{'Totale giorni':^{w_t_gio}}"
    )
    sep = "  " + "-" * (len(header) - 2)
    
    print("\nDettaglio assegnazioni e tempi per prodotto:")
    print(header)
    print(sep)
    
    # Righe tabella
    for nome in nomi:
        lavoro = risultati["lavoro_per_prodotto_ore"][nome]
        linee_det = ", ".join(risultati["linee_assegnate_dettaglio"][nome]) or "-"
        cap_tot = risultati["capacita_totale_linee_assegnate"][nome]
        t_ore = risultati["tempo_per_prodotto_ore"][nome]
        t_gio = risultati["tempo_per_prodotto_giorni"][nome]
        
        riga = (
            f"  {nome:<{w_prod}} | "
            f"{lavoro:>{w_lav}.2f} | "
            f"{linee_det:<{w_linee}} | "
            f"{cap_tot:>{w_cap}.2f} | "
            f"{t_ore:>{w_t_ore}.2f} | "
            f"{t_gio:>{w_t_gio}.3f}"
        )
        print(riga)
