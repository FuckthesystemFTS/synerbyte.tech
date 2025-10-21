# 🚀 Guida Deployment Heroku - Synerchat

## 📋 Prerequisiti

1. **Account Heroku**: Crea un account su [heroku.com](https://heroku.com)
2. **Heroku CLI**: Installa da [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Assicurati di avere Git installato

---

## 🔧 Preparazione

### 1. Login su Heroku
```bash
heroku login
```

### 2. Crea l'applicazione Heroku
```bash
heroku create synerchat-app
```
*(Sostituisci `synerchat-app` con un nome univoco)*

---

## 📦 Deploy Backend

### 1. Inizializza Git (se non già fatto)
```bash
cd c:\Users\Hp\Desktop\SYNERCHAT
git init
git add .
git commit -m "Initial commit"
```

### 2. Collega a Heroku
```bash
heroku git:remote -a synerchat-app
```

### 3. Deploy
```bash
git push heroku main
```

---

## 🌐 Deploy Frontend

### Opzione A: Netlify (Consigliato)

1. Vai su [netlify.com](https://netlify.com)
2. Clicca "Add new site" → "Deploy manually"
3. Build il frontend:
   ```bash
   cd app/frontend
   npm run build
   ```
4. Trascina la cartella `dist` su Netlify

5. **Configura variabili ambiente** in Netlify:
   - `VITE_API_URL`: `https://synerchat-app.herokuapp.com`
   - `VITE_WS_URL`: `wss://synerchat-app.herokuapp.com`

### Opzione B: Vercel

1. Installa Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Deploy:
   ```bash
   cd app/frontend
   vercel --prod
   ```

3. Configura le variabili ambiente quando richiesto

---

## ⚙️ Configurazione Backend su Heroku

### Variabili Ambiente
```bash
heroku config:set SECRET_KEY="your-super-secret-key-change-this"
heroku config:set CORS_ORIGINS="https://your-frontend-url.netlify.app"
```

### Verifica configurazione
```bash
heroku config
```

---

## 🔍 Verifica Deployment

### Backend
```bash
heroku open
# Dovresti vedere: {"message": "Welcome to Synerchat API"}
```

### Logs
```bash
heroku logs --tail
```

---

## 🐛 Troubleshooting

### Errore: "Application Error"
```bash
heroku logs --tail
```
Controlla i log per errori specifici

### Database non funziona
Il database SQLite è incluso nel filesystem. Per produzione seria, considera PostgreSQL:
```bash
heroku addons:create heroku-postgresql:mini
```

### WebSocket non funziona
Assicurati che il frontend usi `wss://` (non `ws://`) per HTTPS

---

## 📝 Comandi Utili

```bash
# Riavvia l'app
heroku restart

# Scala dyno
heroku ps:scale web=1

# Apri dashboard
heroku dashboard

# Esegui comando remoto
heroku run bash
```

---

## 🔒 Sicurezza Post-Deploy

1. **Cambia SECRET_KEY**:
   ```bash
   heroku config:set SECRET_KEY="$(openssl rand -hex 32)"
   ```

2. **Abilita HTTPS** (automatico su Heroku)

3. **Limita CORS** solo al tuo dominio frontend

---

## 📊 Monitoraggio

- **Dashboard Heroku**: [dashboard.heroku.com](https://dashboard.heroku.com)
- **Metrics**: Heroku fornisce metriche base gratuite
- **Logs**: `heroku logs --tail`

---

## 💰 Costi

- **Free Tier**: 550-1000 ore/mese gratuite
- **Hobby**: $7/mese per dyno sempre attivo
- **Database**: SQLite gratis, PostgreSQL da $5/mese

---

## ✅ Checklist Pre-Deploy

- [ ] `Procfile` presente
- [ ] `requirements.txt` aggiornato
- [ ] `runtime.txt` con versione Python corretta
- [ ] Variabili ambiente configurate
- [ ] Frontend buildato e deployato
- [ ] CORS configurato correttamente
- [ ] SECRET_KEY cambiata
- [ ] Test funzionalità base

---

## 📱 Deploy App Mobile su Heroku

### Metodo Automatico (RACCOMANDATO)

#### Windows:
```powershell
# Dalla root del progetto
.\deploy-to-heroku.ps1
```

#### Linux/macOS:
```bash
chmod +x deploy-to-heroku.sh
./deploy-to-heroku.sh
```

Questo script:
1. ✅ Crea le app Android e iOS
2. ✅ Le mette in `app/backend/downloads/`
3. ✅ Fa commit su git
4. ✅ Push su Heroku
5. ✅ Ti dà i link di download

### Metodo Manuale

1. **Build le app:**
```bash
.\build-and-deploy-apps.ps1  # Windows
# oppure
./build-and-deploy-apps.sh   # Linux/Mac
```

2. **Verifica che i file siano creati:**
```bash
ls app/backend/downloads/
# Dovresti vedere:
# - synerchat.apk
# - synerchat.ipa (opzionale)
```

3. **Commit e push:**
```bash
git add .
git commit -m "Add mobile apps"
git push heroku main
```

4. **Le app saranno disponibili su:**
- Android: `https://your-app.herokuapp.com/downloads/synerchat.apk`
- iOS: `https://your-app.herokuapp.com/downloads/synerchat.ipa`

### Download dalla Pagina Login

Gli utenti vedranno i pulsanti di download nella pagina di login:
- **Pulsante verde "Android"** → Scarica APK
- **Pulsante nero "iOS"** → Scarica IPA

### Verifica Download

```bash
# Testa i link
curl -I https://your-app.herokuapp.com/downloads/synerchat.apk
curl -I https://your-app.herokuapp.com/downloads/synerchat.ipa
```

Dovresti vedere `200 OK` se i file sono presenti.

---

## 🎉 Deploy Completato!

La tua app Synerchat è ora live su:
- **Backend**: `https://synerchat-app.herokuapp.com`
- **Frontend**: `https://your-app.netlify.app`
- **Android APK**: `https://synerchat-app.herokuapp.com/downloads/synerchat.apk`
- **iOS IPA**: `https://synerchat-app.herokuapp.com/downloads/synerchat.ipa`

**Testa tutte le funzionalità:**
1. ✅ Registrazione
2. ✅ Login
3. ✅ Ricerca utenti
4. ✅ Richiesta chat
5. ✅ Invio messaggi (con sync istantanea!)
6. ✅ Upload immagini
7. ✅ Verifica periodica
8. ✅ Clear/Delete chat
9. ✅ Download app mobile dalla pagina login

---

## 📱 Per gli Utenti

### Android:
1. Vai su `https://your-app.herokuapp.com`
2. Nella pagina login, click su "Android"
3. Scarica e installa l'APK
4. Abilita "Installa da origini sconosciute" se richiesto

### iOS:
1. Vai su `https://your-app.herokuapp.com`
2. Nella pagina login, click su "iOS"
3. Installa con TestFlight, AltStore o Sideloadly
