import random
from models import TipoProdotto
from production import (
    genera_quantita_produzione,
    genera_parametri_configurabili,
    calcola_tempo_produzione_lotto
)


def stampa_intestazione():
    print("="*70)
    print("SIMULAZIONE PRODUZIONE LOTTO - AZIENDA TESSILE ALTA MODA")
    print("="*70)
    print()


def stampa_quantita(quantita: dict):
    print(" GENERAZIONE QUANTITÀ DA PRODURRE ")
    print("-"*70)

    totale_capi = 0
    for prodotto, qta in quantita.items():
        print(f"   {prodotto.value:30s}: {qta:4d} capi")
        totale_capi += qta

    print(f"\n   TOTALE CAPI: {totale_capi}")
    print()

    return totale_capi


def stampa_parametri(tempo_per_unita: dict, capacita_per_prodotto: dict, capacita_complessiva: int):
    print(" GENERAZIONE PARAMETRI CONFIGURABILI ")
    print("-"*70)

    print("   Tempo di produzione per unità (ore/capo):")
    for prodotto, tempo in tempo_per_unita.items():
        print(f"     • {prodotto.value:28s}: {tempo:5.2f} ore/capo")

    print()
    print("   Capacità massima giornaliera per prodotto (capi/giorno):")
    for prodotto, capacita in capacita_per_prodotto.items():
        print(f"     • {prodotto.value:28s}: {capacita:3d} capi/giorno")

    print()
    print(f"   Capacità massima complessiva: {capacita_complessiva} capi/giorno")
    print()


def stampa_risultati(risultati: dict):
    print(" TEMPO DI PRODUZIONE COMPLESSIVO DELL'INTERO LOTTO ")
    print("-"*70)

    print("   Ore necessarie per prodotto:")
    for prodotto, ore in risultati['ore_per_prodotto'].items():
        print(f"     • {prodotto.value:28s}: {ore:7.1f} ore")

    print()
    print(f"   ORE TOTALI NECESSARIE: {risultati['ore_totali']:.1f} ore")
    print()
    print(f"   GIORNI DI PRODUZIONE NECESSARI: {risultati['giorni_produzione_totali']:.1f} giorni")
    print(f"   ORE LAVORATIVE TOTALI: {risultati['ore_lavorative_totali']:.1f} ore")
    print()


def main():
    random.seed(42)

    stampa_intestazione()

    quantita = genera_quantita_produzione()
    stampa_quantita(quantita)

    tempo_per_unita, capacita_per_prodotto, capacita_complessiva = \
        genera_parametri_configurabili()
    stampa_parametri(tempo_per_unita, capacita_per_prodotto, capacita_complessiva)

    risultati = calcola_tempo_produzione_lotto(
        quantita,
        tempo_per_unita,
        capacita_per_prodotto,
        capacita_complessiva
    )
    stampa_risultati(risultati)

    print("="*70)
    print("SIMULAZIONE COMPLETATA")
    print("="*70)

    return risultati


if __name__ == "__main__":
    main()
