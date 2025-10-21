# 🚀 DEPLOY SYNERCHAT SU HEROKU CON APP MOBILE

## 🎯 TL;DR - Fai Tutto in 1 Comando

```powershell
# Windows
.\deploy-to-heroku.ps1

# Linux/Mac
chmod +x deploy-to-heroku.sh
./deploy-to-heroku.sh
```

**Questo script fa TUTTO:**
1. ✅ Crea APK Android e IPA iOS
2. ✅ Li mette in `app/backend/downloads/`
3. ✅ Fa commit su git
4. ✅ Push su Heroku
5. ✅ Ti dà i link per scaricare le app

---

## 📱 Risultato Finale

Dopo il deploy, gli utenti:

1. Vanno su **`https://your-app.herokuapp.com`**
2. Vedono la pagina di login
3. Sotto il form vedono:
   ```
   📱 Download Mobile App
   [🤖 Android]  [🍎 iOS]
   ```
4. Click su "Android" → Scaricano APK
5. Click su "iOS" → Scaricano IPA
6. Installano e usano l'app!

---

## 🔧 Prerequisiti

### Per Usare lo Script:
- Git installato
- Heroku CLI installato
- Account Heroku
- App già su Heroku (se no, vedi sotto)

### Per Build Android:
- Node.js 18+
- Java JDK 17+
- Android Studio
- `ANDROID_HOME` configurato

### Per Build iOS (opzionale):
- macOS
- Xcode 14+

---

## 📝 Setup Iniziale (Solo Prima Volta)

### 1. Installa Heroku CLI

**Windows:**
```powershell
# Scarica da: https://devcenter.heroku.com/articles/heroku-cli
```

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

**macOS:**
```bash
brew tap heroku/brew && brew install heroku
```

### 2. Login su Heroku

```bash
heroku login
```

### 3. Crea App Heroku (se non esiste)

```bash
heroku create your-app-name
```

### 4. Collega Git a Heroku

```bash
git remote add heroku https://git.heroku.com/your-app-name.git
```

---

## 🚀 Deploy Completo

### Opzione 1: Script Automatico (RACCOMANDATO)

```powershell
# Windows
.\deploy-to-heroku.ps1

# Linux/Mac
./deploy-to-heroku.sh
```

Lo script ti chiederà conferma e poi:
- Builda le app mobile
- Fa commit
- Push su Heroku
- Ti mostra i link

### Opzione 2: Passo per Passo

#### 1. Build le App Mobile

```powershell
# Windows
.\build-and-deploy-apps.ps1

# Linux/Mac
./build-and-deploy-apps.sh
```

#### 2. Verifica File Creati

```bash
ls app/backend/downloads/
```

Dovresti vedere:
- `synerchat.apk` (Android)
- `synerchat.ipa` (iOS, opzionale)

#### 3. Commit e Push

```bash
git add .
git commit -m "Add mobile apps and sync improvements"
git push heroku main
```

#### 4. Verifica Deploy

```bash
heroku open
```

---

## 🌐 Link Finali

Dopo il deploy, le app saranno disponibili su:

```
https://your-app.herokuapp.com/downloads/synerchat.apk  ← Android
https://your-app.herokuapp.com/downloads/synerchat.ipa  ← iOS
```

E i pulsanti nella pagina login punteranno automaticamente a questi link!

---

## ✅ Test Completo

### 1. Testa Backend

```bash
curl https://your-app.herokuapp.com/healthz
# Risposta: {"ok": true, "version": "1.0.0"}
```

### 2. Testa Download APK

```bash
curl -I https://your-app.herokuapp.com/downloads/synerchat.apk
# Risposta: HTTP/1.1 200 OK
```

### 3. Testa Pagina Login

1. Apri: `https://your-app.herokuapp.com`
2. Vedi la pagina login
3. Scorri in basso
4. Vedi i pulsanti "Android" e "iOS"
5. Click su "Android" → Scarica APK

### 4. Testa Messaggi

1. Registrati/Login
2. Crea una chat
3. Invia messaggio
4. Vedi ⏳ (sending)
5. Dopo 1-2 sec vedi ✓ (sent)
6. Apri in altro browser → Messaggio appare subito!

---

## 🔄 Aggiornamenti Futuri

Quando vuoi aggiornare le app:

```bash
# 1. Fai modifiche al codice
# 2. Rigenera le app e deploya
.\deploy-to-heroku.ps1

# Fatto! Le nuove app sono online
```

---

## 🚨 Problemi Comuni

### "ANDROID_HOME not found"

```powershell
# Windows
$env:ANDROID_HOME = "C:\Users\YourName\AppData\Local\Android\Sdk"

# Linux/Mac
export ANDROID_HOME=$HOME/Library/Android/sdk
```

### "Heroku CLI not found"

Installa da: https://devcenter.heroku.com/articles/heroku-cli

### "Git remote heroku not found"

```bash
heroku git:remote -a your-app-name
```

### "Build failed"

```bash
# Pulisci e riprova
cd app/frontend/android
./gradlew clean
cd ../../..
.\deploy-to-heroku.ps1
```

### "File troppo grande per git"

I file APK/IPA sono grandi (5-20 MB). Se git si lamenta:

```bash
# Aumenta limite
git config http.postBuffer 524288000
```

Oppure usa Git LFS:

```bash
git lfs install
git lfs track "*.apk"
git lfs track "*.ipa"
git add .gitattributes
```

---

## 📊 Monitoraggio

### Vedi Log in Tempo Reale

```bash
heroku logs --tail -a your-app-name
```

### Riavvia App

```bash
heroku restart -a your-app-name
```

### Apri Dashboard

```bash
heroku dashboard
```

---

## 💡 Tips

### Velocizza Build

Se hai già buildato le app e vuoi solo deployare:

```bash
.\deploy-to-heroku.ps1 -SkipBuild
```

### Specifica App Heroku

```bash
.\deploy-to-heroku.ps1 -HerokuApp "your-app-name"
```

### Build Solo Android

```bash
.\build-and-deploy-apps.ps1 -SkipIOS
```

---

## 📱 Dimensioni File

Tipiche:
- **APK Android:** 5-15 MB
- **IPA iOS:** 10-20 MB
- **Totale:** ~20-30 MB

Heroku supporta file fino a 500 MB, quindi nessun problema!

---

## 🎉 Checklist Finale

Prima di considerare il deploy completo:

- [ ] Script `deploy-to-heroku.ps1` eseguito con successo
- [ ] APK presente in `app/backend/downloads/synerchat.apk`
- [ ] IPA presente in `app/backend/downloads/synerchat.ipa` (opzionale)
- [ ] Push su Heroku completato
- [ ] Pagina login aperta e pulsanti visibili
- [ ] Download APK funzionante
- [ ] Download IPA funzionante (opzionale)
- [ ] Messaggi sincronizzati istantaneamente
- [ ] Indicatori di stato (⏳ ✓ ✗) funzionanti

---

## 🌟 Fatto!

Ora hai:
- ✅ App web su Heroku
- ✅ APK Android scaricabile
- ✅ IPA iOS scaricabile
- ✅ Pulsanti download nella pagina login
- ✅ Messaggi sincronizzati perfettamente
- ✅ Sistema di retry automatico
- ✅ Indicatori visivi di stato

Gli utenti possono scaricare e usare l'app immediatamente! 🚀

---

## 📚 Documentazione Completa

- **Deploy Heroku:** `HEROKU_DEPLOY.md`
- **Build Mobile:** `app/frontend/BUILD_MOBILE.md`
- **Deploy Apps:** `DEPLOY_APPS_GUIDE.md`
- **Quick Start:** `QUICK_START.md`

---

**Domande? Problemi?**  
Controlla i log: `heroku logs --tail`
