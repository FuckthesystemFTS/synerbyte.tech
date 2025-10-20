Synerchat Backend
=================

- FastAPI con autenticazione JWT (TTL 10 minuti)
- Flusso SIWE-like: `/auth/siwe-start` e `/auth/siwe-verify`
- Relay WebSocket `/ws/{conversationId}` che rifiuta token scaduti
- Helper per pagamenti e chiavi pubbliche

Esecuzione
----------

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Imposta le variabili d'ambiente o copia `.env.example` in `.env` e modifica i valori.