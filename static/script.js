document.getElementById('form-simulazione').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    document.getElementById('risultati').classList.add('hidden');
    document.getElementById('errori').classList.add('hidden');
    
    const formData = new FormData(e.target);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });
    
    try {
        const response = await fetch('/api/simula', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            mostraRisultati(result);
        } else {
            mostraErrori(result.errore);
        }
    } catch (error) {
        mostraErrori(['Errore di connessione al server']);
    }
});

function mostraRisultati(data) {
    const container = document.getElementById('risultati-content');
    
    let html = '';
    
    data.risultati_prodotti.forEach(prod => {
        html += `
            <div class="card">
                <h3>${prod.prodotto}</h3>
                <div class="data-row">
                    <span class="data-label">Quantità</span>
                    <span class="data-value">${prod.quantita} capi</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Tempo teorico per unità</span>
                    <span class="data-value">${formatTempo(prod.tempo_teorico)}</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Linea assegnata</span>
                    <span class="data-value">Linea ${prod.linea} (efficienza ${prod.efficienza})</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Tempo effettivo sulla linea</span>
                    <span class="data-value">${formatTempo(prod.tempo_effettivo)}</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Capacità giornaliera</span>
                    <span class="data-value">${prod.capacita_giornaliera} capi/giorno</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Tempo totale produzione</span>
                    <span class="data-value">${formatTempoOreMinuti(prod.ore_totali)}</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Giorni necessari</span>
                    <span class="data-value">${prod.giorni_necessari.toFixed(2)} giorni</span>
                </div>
            </div>
        `;
    });
    
    html += `
        <div class="summary">
            <h3>Riepilogo Complessivo</h3>
            <div class="data-row">
                <span class="data-label">Capacità giornaliera impianto</span>
                <span class="data-value">${data.capacita_complessiva} capi/giorno</span>
            </div>
            <div class="data-row">
                <span class="data-label">Durata totale lotto</span>
                <span class="data-value">${formatTempoOreMinuti(data.durata_lotto_ore)} (${data.durata_lotto_giorni.toFixed(2)} giorni)</span>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
    document.getElementById('risultati').classList.remove('hidden');
    document.getElementById('risultati').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function mostraErrori(errori) {
    const container = document.getElementById('errori-content');
    
    if (typeof errori === 'string') {
        errori = [errori];
    }
    
    container.innerHTML = errori.map(e => `<li>${e}</li>`).join('');
    document.getElementById('errori').classList.remove('hidden');
    document.getElementById('errori').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function formatTempo(ore) {
    const h = Math.floor(ore);
    const m = Math.round((ore - h) * 60);
    
    if (h === 0) return `${m}min/capo`;
    if (m === 0) return `${h}h/capo`;
    return `${h}h ${m}min/capo`;
}

function formatTempoOreMinuti(ore) {
    const h = Math.floor(ore);
    const m = Math.round((ore - h) * 60);
    
    if (m === 0) return `${h} ore`;
    return `${h} ore e ${m} minuti`;
}
