# Telegram Message Logger

Questo script python è un logger di messaggi di Telegram che salva i messaggi ricevuti e inviati in chat, gruppi e canali in formato CSV e JSON. 
- Le chat vengono monitorate in tempo reale e i messaggi vengono salvati in un file di log.
- Le chat sono salvate in cartelle separate per tipologia (chat, gruppi, canali) e per ogni chat viene creata una cartella.
- I messaggi vengono salvati in file CSV e JSON. Inoltre, viene creata una cartella per ogni tipologia di allegato.
- Quando si riceve un messaggio con un allegato, viene salvato il percorso del file nel campo corrispondente.

## Requisiti

- Python 3.7+
- Telegram API ID e Hash
- Librerie Python necessarie (telethon / python-dotenv)

## Installazione

1. **Clonare il repository**

   ```bash
   git clone https://github.com/rosscript/telegram-message-logger.git
   cd telegram-message-logger

2. **Creare un ambiente virtuale**

   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. **Installare le librerie necessarie**

   ```bash
    pip install -r requirements.txt

4. **Configurare le variabili d'ambiente**

   ```bash
   cp .env.example .env
   nano .env

   Modificare le variabili con i propri dati:
   - `API_ID` e `API_HASH` (ottenibili su https://my.telegram.org)

5. **Eseguire il programma**

   ```bash
    python app.py
