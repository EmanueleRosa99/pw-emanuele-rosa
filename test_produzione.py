import unittest
from models import GiaccaInvernale, TShirt, Felpa, Pantalone, LineaProduttiva, Impianto
from produzione import (
    genera_quantita_produzione,
    genera_parametri_configurabili,
    assegna_linee_a_prodotti,
    calcola_tempo_produzione_lotto,
    _arrotonda_tempo_in_minuti
)


class TestGeneraQuantita(unittest.TestCase):
    
    def setUp(self):
        self.prodotti = [
            GiaccaInvernale(),
            TShirt(),
            Felpa(),
            Pantalone()
        ]
    
    def test_genera_quantita(self):
        # Verifica che vengano generate le quantità di tutti i prodotti
        quantita = genera_quantita_produzione(self.prodotti)
        self.assertEqual(len(quantita), 4)
    
    def test_quantita_nei_range(self):
        # Verifica che le quantità rispettino i range dei prodotti
        quantita = genera_quantita_produzione(self.prodotti)
        
        for prodotto, qta in quantita.items():
            min_val, max_val = prodotto.range_quantita_produzione
            self.assertGreaterEqual(qta, min_val)
            self.assertLessEqual(qta, max_val)


class TestGeneraParametri(unittest.TestCase):
    
    def setUp(self):
        self.prodotti = [
            GiaccaInvernale(),
            TShirt(),
            Felpa(),
            Pantalone()
        ]
    
    def test_genera_parametri(self):
        # Testa la generazione di tempi e impianto
        tempo_per_unita, impianto = genera_parametri_configurabili(self.prodotti)
        
        self.assertEqual(len(tempo_per_unita), 4)
        self.assertEqual(impianto.numero_linee, 4)
    
    def test_tempi_nei_range(self):
        tempo_per_unita, _ = genera_parametri_configurabili(self.prodotti)
        
        for prodotto, tempo in tempo_per_unita.items():
            min_val, max_val = prodotto.range_tempo_produzione
            self.assertGreaterEqual(tempo, min_val)
            self.assertLessEqual(tempo, max_val)
    
    def test_coefficienti_linee(self):
        # Verifica che i coefficienti siano nel range stabilito
        _, impianto = genera_parametri_configurabili(self.prodotti)
        
        for linea in impianto.linee:
            self.assertGreaterEqual(linea.coefficiente_efficienza, 0.7)
            self.assertLessEqual(linea.coefficiente_efficienza, 1.3)


class TestAssegnaLinee(unittest.TestCase):
    # Testa la corretta allocazione delle linee ai prodotti
    def setUp(self):
        self.prodotti = [
            GiaccaInvernale(),
            TShirt(),
            Felpa(),
            Pantalone()
        ]
        self.quantita = {
            self.prodotti[0]: 50,
            self.prodotti[1]: 150,
            self.prodotti[2]: 100,
            self.prodotti[3]: 80
        }
        self.tempo_per_unita = {
            self.prodotti[0]: 5.0,
            self.prodotti[1]: 1.0,
            self.prodotti[2]: 2.5,
            self.prodotti[3]: 3.0
        }
        linee = [
            LineaProduttiva('A', 0.8),
            LineaProduttiva('B', 1.0),
            LineaProduttiva('C', 1.1),
            LineaProduttiva('D', 1.3)
        ]
        self.impianto = Impianto(linee)
    
    def test_assegna_tutte_le_linee(self):
        # Verifica che venga assegnata una linea per ogni prodotto
        assegnazioni = assegna_linee_a_prodotti(
            self.prodotti,
            self.quantita,
            self.tempo_per_unita,
            self.impianto
        )
        self.assertEqual(len(assegnazioni), 4)
    
    def test_linea_migliore_a_carico_maggiore(self):
        # Verifica che la linea migliore vada al prodotto con lavorazione prevista maggiore
        assegnazioni = assegna_linee_a_prodotti(
            self.prodotti,
            self.quantita,
            self.tempo_per_unita,
            self.impianto
        )
        
        # Calcola carico per ogni prodotto
        carichi = {
            prodotto: self.quantita[prodotto] * self.tempo_per_unita[prodotto]
            for prodotto in self.prodotti
        }
        
        # Trova prodotto con carico massimo
        prodotto_max_carico = max(carichi, key=carichi.get)
        
        # Verifica che abbia la linea migliore (D con coefficiente 1.3)
        self.assertEqual(assegnazioni[prodotto_max_carico].nome, 'D')



class TestCalcoloTempo(unittest.TestCase):
    # Test per il calcolo del tempo di produzione
    
    def setUp(self):
        self.prodotti = [GiaccaInvernale(), TShirt()]
        self.quantita = {
            self.prodotti[0]: 50,
            self.prodotti[1]: 100
        }
        self.tempo_per_unita = {
            self.prodotti[0]: 4.0,
            self.prodotti[1]: 1.0
        }
        linee = [
            LineaProduttiva('A', 1.0),
            LineaProduttiva('B', 1.2)
        ]
        self.impianto = Impianto(linee)
        self.assegnazioni = assegna_linee_a_prodotti(
            self.prodotti,
            self.quantita,
            self.tempo_per_unita,
            self.impianto
        )
    
    def test_calcolo_restituisce_risultati(self):
        risultati = calcola_tempo_produzione_lotto(
            self.quantita,
            self.tempo_per_unita,
            self.assegnazioni
        )
        
        self.assertIn('quantita', risultati)
        self.assertIn('tempo_per_unita', risultati)
        self.assertIn('risultati_per_prodotto', risultati)
        self.assertIn('capacita_giornaliera_complessiva', risultati)
        self.assertIn('durata_lotto_ore', risultati)        


if __name__ == '__main__':
    unittest.main()
