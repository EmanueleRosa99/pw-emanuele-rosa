import unittest
from app import app, valida_input_utente, PRODOTTI


class TestValidazioneInput(unittest.TestCase):
    
    def test_input_valido_completo(self):
        # Test che l'input sia valido
        data = {
            'quantita_giacche': '50',
            'quantita_tshirt': '150',
            'quantita_felpe': '100',
            'quantita_pantaloni': '80',
            'coeff_linea_a': '0.95',
            'coeff_linea_b': '1.10',
            'coeff_linea_c': '1.05',
            'coeff_linea_d': '1.25'
        }
        errori = valida_input_utente(data)
        self.assertEqual(len(errori), 0)
    
    def test_quantita_mancante(self):
        data = {
            'quantita_giacche': '',
            'quantita_tshirt': '150',
            'quantita_felpe': '100',
            'quantita_pantaloni': '80',
            'coeff_linea_a': '0.95',
            'coeff_linea_b': '1.10',
            'coeff_linea_c': '1.05',
            'coeff_linea_d': '1.25'
        }
        errori = valida_input_utente(data)
        self.assertGreater(len(errori), 0)
        self.assertTrue(any('Giacche' in e for e in errori))
    
    def test_quantita_fuori_range(self):
        # Test che la quantita di giacche fuori range, generi errore di validazione
        data = {
            'quantita_giacche': '200', 
            'quantita_tshirt': '150',
            'quantita_felpe': '100',
            'quantita_pantaloni': '80',
            'coeff_linea_a': '0.95',
            'coeff_linea_b': '1.10',
            'coeff_linea_c': '1.05',
            'coeff_linea_d': '1.25'
        }
        errori = valida_input_utente(data)
        self.assertGreater(len(errori), 0)
    
    def test_coefficiente_mancante(self):
        data = {
            'quantita_giacche': '50',
            'quantita_tshirt': '150',
            'quantita_felpe': '100',
            'quantita_pantaloni': '80',
            'coeff_linea_a': '',
            'coeff_linea_b': '1.10',
            'coeff_linea_c': '1.05',
            'coeff_linea_d': '1.25'
        }
        errori = valida_input_utente(data)
        self.assertGreater(len(errori), 0)
        self.assertTrue(any('Linea A' in e for e in errori))
    
    def test_coefficiente_fuori_range(self):
        data = {
            'quantita_giacche': '50',
            'quantita_tshirt': '150',
            'quantita_felpe': '100',
            'quantita_pantaloni': '80',
            'coeff_linea_a': '2.5',
            'coeff_linea_b': '1.10',
            'coeff_linea_c': '1.05',
            'coeff_linea_d': '1.25'
        }
        errori = valida_input_utente(data)
        self.assertGreater(len(errori), 0)


if __name__ == '__main__':
    unittest.main()
