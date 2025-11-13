from models import GiaccaInvernale, TShirt, Felpa, Pantalone
from produzione import (
    genera_quantita_produzione,
    genera_parametri_configurabili,
    calcola_tempo_produzione_lotto,
)
from output import output_simulazione_produzione

def main():
    # Definizione dei prodotti (istanze delle classi)
    prodotti = [
        GiaccaInvernale(),
        TShirt(),
        Felpa(),
        Pantalone()
    ]
    
    # Richiamo la funzione per generarmi randomicamente le quantita da produrre
    quantita = genera_quantita_produzione(prodotti)

    # Richiamo la funzione per generarmi randomicamente i parametri
    (
        tempo_per_unita, 
        capacita_giornaliera_per_prodotto,
        capacita_giornaliera_complessiva,
        impianto
    ) = genera_parametri_configurabili(prodotti)

    # Richiamo funzione per calcolare il tempo complessivo del lotto
    risultati = calcola_tempo_produzione_lotto(
        quantita,
        tempo_per_unita,
        capacita_giornaliera_per_prodotto,
        capacita_giornaliera_complessiva,
        impianto,
        ore_per_giorno=24
    )

    # Stampa l'output in console
    output_simulazione_produzione(risultati)
  
if __name__ == "__main__":
    main()
