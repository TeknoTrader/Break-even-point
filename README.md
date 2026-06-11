# PIZZA 24 - Break-Even B2C (Streamlit)

Dashboard per il calcolo del punto di pareggio della vendita B2C di pizza tramite distributori automatici. Bilingue IT / UK.

## Struttura

    app.py                 modello e interfaccia Streamlit
    requirements.txt       dipendenze
    .streamlit/config.toml tema

## Esecuzione locale

    pip install -r requirements.txt
    streamlit run app.py

## Deploy su Streamlit Community Cloud (via GitHub)

1. Creare un repository GitHub e caricare i file (`app.py`, `requirements.txt`, `.streamlit/config.toml`).
2. Accedere a https://share.streamlit.io con l'account GitHub.
3. "New app" -> selezionare repository, branch e `app.py` come main file.
4. Deploy. L'app riceve un URL pubblico aggiornato automaticamente a ogni push.

## Parametri

Tutti i parametri (CAPEX, prezzo, food cost, voci OPEX, costo addetto HACCP e distributori per addetto, aliquota IRES+IRAP, orizzonte di ammortamento, pizze/giorno) sono modificabili dalla barra laterale. I risultati, i grafici e gli scenari si aggiornano in tempo reale.
