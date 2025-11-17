from flask import Flask, render_template, request, jsonify
from models import GiaccaInvernale, TShirt, Felpa, Pantalone, LineaProduttiva, Impianto
from produzione import (
    genera_parametri_configurabili,
    assegna_linee_a_prodotti,
    calcola_tempo_produzione_lotto,
)

app = Flask(__name__)

PRODOTTI = [
    GiaccaInvernale(),
    TShirt(),
    Felpa(),
    Pantalone()
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/simula', methods=['POST'])
def simula():
    try:
        data = request.get_json()
        
        errori = valida_input_utente(data)
        if errori:
            return jsonify({'errore': errori}), 400
        
        # Quantità inserite dall'utente
        quantita = {
            PRODOTTI[0]: int(data['quantita_giacche']),
            PRODOTTI[1]: int(data['quantita_tshirt']),
            PRODOTTI[2]: int(data['quantita_felpe']),
            PRODOTTI[3]: int(data['quantita_pantaloni'])
        }
        
        # Tempi di produzione generati automaticamente
        tempo_per_unita, _ = genera_parametri_configurabili(PRODOTTI)
        
        # Coefficienti linee inseriti dall'utente
        linee = [
            LineaProduttiva('A', float(data['coeff_linea_a'])),
            LineaProduttiva('B', float(data['coeff_linea_b'])),
            LineaProduttiva('C', float(data['coeff_linea_c'])),
            LineaProduttiva('D', float(data['coeff_linea_d']))
        ]
        impianto = Impianto(linee)
        
        assegnazioni_linee = assegna_linee_a_prodotti(PRODOTTI, quantita, tempo_per_unita, impianto)
        risultati = calcola_tempo_produzione_lotto(quantita, tempo_per_unita, assegnazioni_linee)
        
        return jsonify(formatta_risultati_json(risultati))
        
    except Exception as e:
        return jsonify({'errore': f'Errore durante la simulazione: {str(e)}'}), 500


def valida_input_utente(data: dict) -> list:
    errori = []
    
    campi_quantita = {
        'quantita_giacche': ('Giacche Invernali', 30, 120),
        'quantita_tshirt': ('T-Shirts', 100, 250),
        'quantita_felpe': ('Felpe', 65, 190),
        'quantita_pantaloni': ('Pantaloni', 50, 170)
    }
    
    for campo, (nome, min_val, max_val) in campi_quantita.items():
        if campo not in data or not data[campo] or data[campo] == '':
            errori.append(f"La quantità di {nome} è obbligatoria")
            continue
        
        try:
            valore = int(data[campo])
            if valore < min_val or valore > max_val:
                errori.append(f"La quantità di {nome} deve essere tra {min_val} e {max_val}")
        except (ValueError, TypeError):
            errori.append(f"La quantità di {nome} deve essere un numero intero")
    
    campi_coeff = {
        'coeff_linea_a': 'A',
        'coeff_linea_b': 'B',
        'coeff_linea_c': 'C',
        'coeff_linea_d': 'D'
    }
    
    for campo, linea_nome in campi_coeff.items():
        if campo not in data or not data[campo] or data[campo] == '':
            errori.append(f"Il coefficiente della Linea {linea_nome} è obbligatorio")
            continue
        
        try:
            valore = float(data[campo])
            if valore <= 0 or valore > 2:
                errori.append(f"Il coefficiente della Linea {linea_nome} deve essere tra 0.1 e 2.0")
        except (ValueError, TypeError):
            errori.append(f"Il coefficiente della Linea {linea_nome} deve essere un numero valido")
    
    return errori


def formatta_risultati_json(risultati):
    output = {
        'risultati_prodotti': [],
        'capacita_complessiva': risultati['capacita_giornaliera_complessiva'],
        'durata_lotto_ore': risultati['durata_lotto_ore'],
        'durata_lotto_giorni': risultati['durata_lotto_giorni']
    }
    
    for prodotto, qta in risultati['quantita'].items():
        linea = risultati['assegnazioni_linee'][prodotto]
        dati = risultati['risultati_per_prodotto'][prodotto]
        
        output['risultati_prodotti'].append({
            'prodotto': prodotto.nome,
            'quantita': qta,
            'tempo_teorico': risultati['tempo_per_unita'][prodotto],
            'linea': linea.nome,
            'efficienza': linea.coefficiente_efficienza,
            'tempo_effettivo': dati['tempo_effettivo'],
            'capacita_giornaliera': dati['capacita_giornaliera'],
            'ore_totali': dati['ore_totali'],
            'giorni_necessari': dati['giorni_necessari']
        })
    
    return output


if __name__ == '__main__':
    app.run(debug=True, port=5000)
