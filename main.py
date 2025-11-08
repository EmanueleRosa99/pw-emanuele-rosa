# main.py
from models import TipoProdotto
from production import (
    genera_quantita_produzione,
    genera_parametri_configurabili,
    calcola_tempo_produzione_lotto,
)

def main():
    # Richiamo la funzione per generarmi randomicamente le quantita da produrre
    quantita = genera_quantita_produzione()

    # Richiamo la funzione per generarmi randomicamente i parametri
    tempo_per_unita, impianto_linee = genera_parametri_configurabili()

    # Richiamo funzione per calcolare il tempo complessivo del lotto
    risultati = calcola_tempo_produzione_lotto(
        quantita,
        tempo_per_unita,
        impianto_linee,
        ore_per_giorno=24
    )

    larg = 96
    print("╔" + "═" * larg + "╗")
    print(f" {'· SIMULAZIONE LOTTO PRODUZIONE ·':^{larg}}")
    print("╚" + "═" * larg + "╝")

    
    print("\nQuantità (capi):")
    for p, q in quantita.items():
        print(f"  • {p.value:20s}: {q:4d}")

    print("\nTempi unitari di produzione (h/capo):")
    for p in TipoProdotto:
        print(f"  • {p.value:20s}: {tempo_per_unita[p]:4.2f} h/capo")

    print("\nLinee disponibili (nome: capacità) e somma:")
    print(f"  • Numero linee: {len(risultati['impianto_linee'])}")
    print(f"  • Capacità linee: {risultati['impianto_linee']}")
    print(f"  • Capacità totale impianto: {risultati['capacita_totale_impianto']:.2f}")

    # Tabella dettagli per prodotto
    _stampa_tabella_dettaglio(risultati)
    # Riepilogo complessivo.
    print("\nRiepilogo complessivo:")
    print(f"  • Durata totale del lotto (ore):   {risultati['durata_lotto_ore']:.2f}")
    print(f"  • Durata totale del lotto (giorni): {risultati['durata_lotto_giorni']:.3f}")


def _stampa_tabella_dettaglio(risultati: dict) -> None:
    # Stampa la tabella di dettaglio centrata
    nomi = list(risultati["lavoro_per_prodotto_ore"].keys())

   
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
  
if __name__ == "__main__":
    main()
