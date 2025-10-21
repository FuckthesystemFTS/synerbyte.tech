# 🚀 SynerChat - Guida Rapida

## ✨ Novità: Download App dalla Pagina Login!

Gli utenti possono ora scaricare direttamente le app Android e iOS dalla pagina di login, senza bisogno di store!

## 📱 Per Creare le App (Una Volta Sola)

### Windows:
```powershell
# Dalla root del progetto
.\build-and-deploy-apps.ps1
```

### Linux/macOS:
```bash
chmod +x build-and-deploy-apps.sh
./build-and-deploy-apps.sh
```

Questo script:
1. ✅ Installa dipendenze
2. ✅ Build web app
3. ✅ Configura Capacitor
4. ✅ Crea APK Android
5. ✅ Prepara iOS (richiede Xcode su Mac)
6. ✅ Copia tutto in `app/backend/downloads/`

## 🌐 Per Avviare il Server

```bash
cd app/backend
python -m uvicorn app.main:app --reload
```

Apri: http://localhost:8000

## 👥 Per gli Utenti

1. Vai sulla pagina di login
2. Scorri in basso
3. Click su "Android" o "iOS"
4. Installa l'app

### Android:
- Abilita "Installa da origini sconosciute"
- Apri APK e installa

### iOS:
- Usa TestFlight, AltStore o Sideloadly
- Oppure certificato enterprise

## 🎯 Cosa Hai Ora

### ✅ Sincronizzazione Messaggi Perfetta
- Messaggi appaiono IMMEDIATAMENTE
- Retry automatico se fallisce
- Indicatori visivi: ⏳ ✓ ✗ ✓✓
- Zero duplicati

### ✅ Download App Integrato
- Pulsanti nella pagina login
- Download diretto APK/IPA
- Nessun store necessario
- Aggiornamenti controllati da te

### ✅ Script Automatici
- Build con un comando
- Deploy automatico
- Supporto Windows/Linux/Mac

## 📂 File Importanti

```
SYNERCHAT/
├── build-and-deploy-apps.ps1      ← Esegui questo (Windows)
├── build-and-deploy-apps.sh       ← Esegui questo (Linux/Mac)
├── DEPLOY_APPS_GUIDE.md           ← Guida completa
├── app/
│   ├── backend/
│   │   ├── downloads/             ← APK/IPA vanno qui
│   │   │   ├── synerchat.apk
│   │   │   └── synerchat.ipa
│   │   └── app/
│   │       └── main.py            ← Endpoint download
│   └── frontend/
│       └── src/
│           ├── contexts/
│           │   └── ChatContext.tsx  ← Sincronizzazione messaggi
│           └── pages/
│               └── Login.tsx        ← Pulsanti download
```

## 🔧 Prerequisiti (Solo per Build)

### Android:
- Node.js 18+
- Java JDK 17+
- Android Studio
- `ANDROID_HOME` configurato

### iOS (solo macOS):
- Xcode 14+
- CocoaPods

## 🚨 Problemi Comuni

### "ANDROID_HOME not found"
```powershell
# Windows - Aggiungi alle variabili d'ambiente
$env:ANDROID_HOME = "C:\Users\TuoNome\AppData\Local\Android\Sdk"

# Linux/Mac - Aggiungi a ~/.bashrc o ~/.zshrc
export ANDROID_HOME=$HOME/Library/Android/sdk
```

### "Gradle build failed"
```bash
cd app/frontend/android
./gradlew clean
cd ../..
./build-and-deploy-apps.sh
```

### "Download non funziona"
- Verifica che i file siano in `app/backend/downloads/`
- Riavvia il backend
- Controlla console per errori

## 📊 Test Completo

1. **Build le app:**
```bash
./build-and-deploy-apps.ps1  # o .sh
```

2. **Avvia backend:**
```bash
cd app/backend
python -m uvicorn app.main:app --reload
```

3. **Apri browser:**
```
http://localhost:8000
```

4. **Testa download:**
   - Vai alla pagina login
   - Click su "Android" → Scarica APK
   - Click su "iOS" → Scarica IPA

5. **Testa messaggi:**
   - Fai login
   - Invia messaggio → Appare subito con ⏳
   - Dopo 1-2 sec → Diventa ✓
   - Apri in altro browser → Messaggio appare istantaneamente

## 🌍 Deploy in Produzione

1. **Build release:**
```bash
./build-and-deploy-apps.sh --release
```

2. **Carica su server:**
```bash
# Copia file
scp app/backend/downloads/* user@server:/path/to/downloads/
```

3. **Configura dominio:**
   - Punta dominio al server
   - Configura HTTPS
   - Aggiorna URL in `Login.tsx` se necessario

## 💡 Tips

- **Aggiornamenti:** Rigenera APK/IPA e sostituisci in `downloads/`
- **Versioning:** Aggiorna version code in `build.gradle` (Android) e Xcode (iOS)
- **Tracking:** Aggiungi analytics nell'endpoint `/downloads/`
- **Notifiche:** Implementa check versione nell'app per notificare aggiornamenti

## 📚 Documentazione Completa

- **Deploy App:** `DEPLOY_APPS_GUIDE.md`
- **Build Mobile:** `app/frontend/BUILD_MOBILE.md`
- **Assets:** `app/frontend/ASSETS_GUIDE.md`

## 🎉 Fatto!

Ora hai:
- ✅ Messaggi sincronizzati perfettamente
- ✅ App Android e iOS pronte
- ✅ Download diretto dalla pagina login
- ✅ Controllo totale su distribuzione

Gli utenti possono scaricare e usare l'app immediatamente! 🚀

---

**Supporto:** Per problemi, consulta `DEPLOY_APPS_GUIDE.md` o apri un issue.
