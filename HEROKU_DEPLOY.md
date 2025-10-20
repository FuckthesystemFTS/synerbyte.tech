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

## 🎉 Deploy Completato!

La tua app Synerchat è ora live su:
- **Backend**: `https://synerchat-app.herokuapp.com`
- **Frontend**: `https://your-app.netlify.app`

**Testa tutte le funzionalità:**
1. ✅ Registrazione
2. ✅ Login
3. ✅ Ricerca utenti
4. ✅ Richiesta chat
5. ✅ Invio messaggi
6. ✅ Upload immagini
7. ✅ Verifica periodica
8. ✅ Clear/Delete chat
