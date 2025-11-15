from models import GiaccaInvernale, TShirt, Felpa, Pantalone
from produzione import (
    genera_quantita_produzione,
    genera_parametri_configurabili,
    assegna_linee_a_prodotti,
    calcola_tempo_produzione_lotto,
)
from output import output_simulazione_produzione


def main():
    # Definizione dei 4 prodotti
    prodotti = [
        GiaccaInvernale(),
        TShirt(),
        Felpa(),
        Pantalone()
    ]
    
    # Richiamo la funzione per generare randomicamente le quantità da produrre
    quantita = genera_quantita_produzione(prodotti)
    
    # Richiamo la funzione per generare i parametri configurabili
    tempo_per_unita, impianto = genera_parametri_configurabili(prodotti)
    
    # Richiamo la funzione per assegnare le linee ai prodotti
    assegnazioni_linee = assegna_linee_a_prodotti(
        prodotti, 
        quantita, 
        tempo_per_unita, 
        impianto
    )
    
    # Richiamo la funzione per calcolare il tempo complessivo del lotto
    risultati = calcola_tempo_produzione_lotto(
        quantita,
        tempo_per_unita,
        assegnazioni_linee,
        ore_per_giorno=24
    )
    
    # Richiamo funzione per stampa dell'output in console
    output_simulazione_produzione(risultati)


if __name__ == "__main__":
    main()
