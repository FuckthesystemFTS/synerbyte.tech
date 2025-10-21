# 📱 SynerChat - Guida Deploy App Mobile

## 🎯 Obiettivo

Gli utenti possono scaricare direttamente le app Android e iOS dalla pagina di login, senza bisogno di Play Store o App Store.

## ✅ Cosa è Stato Fatto

### 1. **Pagina Login Aggiornata**
- ✅ Aggiunto pulsante download Android (verde)
- ✅ Aggiunto pulsante download iOS (nero)
- ✅ Design professionale con icone e animazioni
- ✅ Istruzioni per l'installazione

### 2. **Backend Configurato**
- ✅ Endpoint `/downloads/{filename}` per servire APK/IPA
- ✅ Cartella `app/backend/downloads/` creata automaticamente
- ✅ Headers corretti per il download dei file

### 3. **Script Automatici**
- ✅ `build-and-deploy-apps.ps1` (Windows)
- ✅ `build-and-deploy-apps.sh` (Linux/macOS)
- ✅ Build automatica e copia in cartella downloads

## 🚀 Come Usare

### Opzione 1: Script Automatico (RACCOMANDATO)

#### Windows:
```powershell
# Dalla root del progetto
.\build-and-deploy-apps.ps1

# Solo Android
.\build-and-deploy-apps.ps1 -SkipIOS

# Build Release
.\build-and-deploy-apps.ps1 -Release
```

#### Linux/macOS:
```bash
# Dalla root del progetto
chmod +x build-and-deploy-apps.sh
./build-and-deploy-apps.sh

# Solo Android
./build-and-deploy-apps.sh --skip-ios

# Build Release
./build-and-deploy-apps.sh --release
```

### Opzione 2: Build Manuale

1. **Build Web App:**
```bash
cd app/frontend
npm install
npm run build
```

2. **Inizializza Capacitor (solo prima volta):**
```bash
npx cap init SynerChat com.synerchat.app --web-dir=dist
```

3. **Aggiungi Piattaforme (solo prima volta):**
```bash
npx cap add android
npx cap add ios  # solo su macOS
```

4. **Build Android APK:**
```bash
npx cap sync android
cd android
./gradlew assembleDebug
# APK in: android/app/build/outputs/apk/debug/app-debug.apk
```

5. **Copia APK nella cartella downloads:**
```bash
cp android/app/build/outputs/apk/debug/app-debug.apk ../../../backend/downloads/synerchat.apk
```

6. **Build iOS (solo macOS):**
```bash
npx cap sync ios
npx cap open ios
# In Xcode: Product > Archive > Export
# Copia IPA in: app/backend/downloads/synerchat.ipa
```

## 📦 Struttura File

```
SYNERCHAT/
├── app/
│   ├── backend/
│   │   ├── downloads/          ← File APK/IPA qui
│   │   │   ├── synerchat.apk   ← Android
│   │   │   ├── synerchat.ipa   ← iOS
│   │   │   └── README.md
│   │   └── app/
│   │       └── main.py         ← Endpoint /downloads/
│   └── frontend/
│       ├── src/
│       │   └── pages/
│       │       └── Login.tsx   ← Pulsanti download
│       └── capacitor.config.ts
├── build-and-deploy-apps.ps1   ← Script Windows
└── build-and-deploy-apps.sh    ← Script Linux/Mac
```

## 🌐 Test Locale

1. **Avvia il backend:**
```bash
cd app/backend
python -m uvicorn app.main:app --reload
```

2. **Apri browser:**
```
http://localhost:8000
```

3. **Nella pagina login:**
   - Vedrai i pulsanti "Android" e "iOS"
   - Click per scaricare direttamente

4. **Test download diretto:**
```
http://localhost:8000/downloads/synerchat.apk
http://localhost:8000/downloads/synerchat.ipa
```

## 📱 Installazione per Utenti

### Android:
1. Click su pulsante "Android" nella pagina login
2. Scarica il file `SynerChat.apk`
3. Vai su Impostazioni > Sicurezza
4. Abilita "Installa app da origini sconosciute"
5. Apri il file APK scaricato
6. Click "Installa"

### iOS:
1. Click su pulsante "iOS" nella pagina login
2. Scarica il file `SynerChat.ipa`
3. **Opzioni di installazione:**
   - **TestFlight:** Per beta testing (richiede Apple Developer)
   - **AltStore:** App store alternativo (gratis)
   - **Sideloadly:** Tool per sideload (gratis)
   - **Enterprise Certificate:** Per distribuzione aziendale

## 🔧 Prerequisiti

### Per Build Android:
- Node.js 18+
- Java JDK 17+
- Android Studio
- Variabile `ANDROID_HOME` configurata

### Per Build iOS:
- macOS
- Xcode 14+
- CocoaPods
- Apple Developer Account (opzionale per distribuzione)

## 🚨 Risoluzione Problemi

### "ANDROID_HOME not found"
```powershell
# Windows
$env:ANDROID_HOME = "C:\Users\YourName\AppData\Local\Android\Sdk"

# Linux/Mac
export ANDROID_HOME=$HOME/Library/Android/sdk
```

### "Gradle build failed"
```bash
cd app/frontend/android
./gradlew clean
cd ..
npm run build
npx cap sync android
```

### "File not found" quando scarico
- Verifica che i file siano in `app/backend/downloads/`
- Controlla i permessi dei file
- Riavvia il backend

### iOS non si installa
- iOS richiede firma digitale
- Usa TestFlight per distribuzione beta
- O usa AltStore/Sideloadly per installazione locale

## 🌍 Deploy in Produzione

### 1. Build Release

```bash
# Android Release
./build-and-deploy-apps.sh --release

# Firma l'APK (opzionale)
cd app/frontend/android
./gradlew bundleRelease
```

### 2. Carica su Server

```bash
# Copia file su server
scp app/backend/downloads/synerchat.apk user@server:/path/to/backend/downloads/
scp app/backend/downloads/synerchat.ipa user@server:/path/to/backend/downloads/
```

### 3. Configura HTTPS

Per Android, assicurati che il server usi HTTPS:
```nginx
location /downloads/ {
    alias /path/to/backend/downloads/;
    add_header Content-Disposition "attachment";
}
```

### 4. Aggiorna URL nella Login Page

Se il backend è su un dominio diverso, aggiorna in `Login.tsx`:
```typescript
href="https://your-domain.com/downloads/synerchat.apk"
```

## 📊 Monitoraggio Download

Aggiungi tracking nel backend (`main.py`):

```python
@app.get("/downloads/{filename}")
async def download_app(filename: str):
    # Log download
    print(f"Download requested: {filename}")
    
    # Increment counter
    # ... your tracking logic
    
    return FileResponse(...)
```

## 🔐 Sicurezza

### Android:
- ✅ APK firmato per release
- ✅ ProGuard per offuscazione codice
- ✅ HTTPS per download

### iOS:
- ✅ Firma con certificato Apple
- ✅ Distribuzione via TestFlight o Enterprise
- ✅ App Transport Security configurato

## 📈 Aggiornamenti

Per rilasciare una nuova versione:

1. **Aggiorna version code:**
   - Android: `android/app/build.gradle`
   - iOS: Xcode > General > Version

2. **Build nuova versione:**
```bash
./build-and-deploy-apps.sh --release
```

3. **Sostituisci file in downloads:**
```bash
# I file vengono automaticamente sovrascritti
```

4. **Notifica utenti:**
   - Aggiungi banner nella app
   - O invia notifica push

## 🎉 Vantaggi di Questo Sistema

✅ **Distribuzione Immediata:** Nessuna attesa per review store
✅ **Controllo Totale:** Gestisci tu gli aggiornamenti
✅ **Nessun Costo:** Niente fee di Play Store/App Store
✅ **Flessibilità:** Rilascia quando vuoi
✅ **Beta Testing:** Facile distribuire versioni beta

## ⚠️ Limitazioni

❌ **Android:** Utenti devono abilitare "Origini sconosciute"
❌ **iOS:** Richiede firma o tool di sideload
❌ **Aggiornamenti:** Non automatici (devi implementare check versione)
❌ **Visibilità:** Non appari negli store ufficiali

## 🔄 Prossimi Passi

1. ✅ Build le app con lo script
2. ✅ Testa download dalla pagina login
3. ✅ Installa su dispositivo reale
4. ✅ Deploy su server di produzione
5. ⏭️ Implementa sistema di aggiornamenti automatici
6. ⏭️ Aggiungi analytics per tracking download

## 📚 Risorse

- [Capacitor Docs](https://capacitorjs.com/docs)
- [Android APK Signing](https://developer.android.com/studio/publish/app-signing)
- [iOS Distribution](https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases)
- [AltStore](https://altstore.io/) - iOS sideload
- [Sideloadly](https://sideloadly.io/) - iOS sideload tool

---

**Versione:** 1.0.0  
**Ultimo aggiornamento:** Ottobre 2025

Per domande: support@synerchat.com
