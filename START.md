# 🚀 Synerchat - Guida Rapida

## ✅ Installazione e Avvio

### 1. Backend (Terminale 1)

```bash
cd app/backend
pip install -r requirements.txt
python simple_server.py
```

Il backend sarà disponibile su: **http://localhost:8000**

### 2. Frontend (Terminale 2)

```bash
cd app/frontend
npm install
npm run dev
```

Il frontend sarà disponibile su: **http://localhost:5173**

---

## 📖 Come Usare Synerchat

### Registrazione
1. Apri http://localhost:5173
2. Clicca su "Register"
3. Inserisci email e password (opzionale: username)
4. Clicca "Register"

### Login
1. Inserisci email e password
2. Clicca "Login"

### Inviare Richiesta di Chat
1. Clicca "+ New Chat"
2. Cerca un utente per email o username
3. Seleziona l'utente
4. Inserisci un codice di 4 caratteri (es: "ABC1")
5. Clicca "Send Request"

### Accettare Richiesta di Chat
1. Clicca "Requests" (vedrai un badge rosso se ci sono richieste)
2. Vedi il codice inviato dall'altro utente
3. Clicca "Accept"
4. Inserisci il TUO codice di 4 caratteri (es: "XYZ9")
5. Clicca "Confirm Accept"

### Chattare
1. Seleziona la chat dalla sidebar
2. Scrivi messaggi (sono crittografati end-to-end automaticamente)
3. Invia con il pulsante "Send"

### Sistema di Verifica (ogni 30 minuti)
- Ogni 30 minuti apparirà un popup di verifica
- Hai 5 minuti per inserire il codice dell'altro utente
- Se non verifichi in tempo, la chat si autodistrugge
- Dopo la verifica, la chat resta attiva per altri 30 minuti

---

## 🔒 Caratteristiche

✅ **Autenticazione con password** - Nessuna blockchain richiesta  
✅ **Crittografia E2EE** - Messaggi crittografati con libsodium (NaCl)  
✅ **Chat temporanee** - Auto-distruzione dopo timeout  
✅ **Verifica periodica** - Sistema di codici ogni 30 minuti  
✅ **Real-time** - WebSocket per messaggi istantanei  
✅ **Database locale** - SQLite per storage sicuro  

---

## 🧪 Test Rapido

### Scenario: Due utenti che chattano

**Utente 1:**
1. Registrati con email: user1@test.com, password: test123
2. Crea richiesta chat per user2@test.com con codice: "AAAA"

**Utente 2:**
1. Registrati con email: user2@test.com, password: test123
2. Vai in "Requests"
3. Vedi il codice "AAAA" di user1
4. Accetta con codice: "BBBB"

**Entrambi:**
- Ora potete chattare!
- Ogni 30 minuti dovrete scambiarvi i codici per mantenere la chat attiva

---

## 📁 Struttura Database

Il database `synerchat.db` viene creato automaticamente in `app/backend/` e contiene:
- **users** - Utenti registrati (password hashate)
- **chat_requests** - Richieste di chat pendenti
- **active_chats** - Chat attive con codici di verifica
- **messages** - Messaggi crittografati
- **sessions** - Token di sessione

---

## 🛠️ Troubleshooting

**Backend non parte:**
```bash
# Verifica Python
python --version  # Deve essere 3.8+

# Reinstalla dipendenze
pip install --upgrade -r requirements.txt
```

**Frontend non parte:**
```bash
# Verifica Node
node --version  # Deve essere 16+

# Pulisci e reinstalla
rm -rf node_modules package-lock.json
npm install
```

**WebSocket non si connette:**
- Verifica che il backend sia in esecuzione su porta 8000
- Controlla la console del browser per errori
- Ricarica la pagina

---

## 🎯 Prossimi Passi

L'applicazione è **completa e funzionante**! Puoi:
- Registrare utenti
- Inviare richieste di chat
- Chattare con crittografia E2E
- Sistema di verifica automatico

Buon divertimento con Synerchat! 🎉
