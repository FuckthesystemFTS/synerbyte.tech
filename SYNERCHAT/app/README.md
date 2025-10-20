Synerchat Monorepo
==================

Struttura:

```
/app
  /contracts  (Hardhat, Solidity 0.8.x)
  /backend    (FastAPI, JWT 10 min, WS relay)
  /frontend   (React+TS Vite)
```

Setup rapido
------------

Contratti:

```bash
cd app/contracts
npm i
npx hardhat compile
```

Backend:

```bash
cd app/backend
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd app/frontend
npm i
npm run dev
```

Note
----
- Usa solo Polygon (137) o Amoy (80002) per test.
- Nessuna firma per messaggio: AEAD XChaCha20-Poly1305.
- Sessione 10 minuti: al termine, `secureWipe()` elimina tutto e porta a `/expired`.