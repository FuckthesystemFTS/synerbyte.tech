# SynerChat - Mobile Build Instructions

## Prerequisiti

### Per Android:
- **Node.js** 18.x o superiore
- **Android Studio** (ultima versione)
- **Java JDK** 17 o superiore
- **Android SDK** (API 33 o superiore)

### Per iOS:
- **macOS** (richiesto per build iOS)
- **Xcode** 14 o superiore
- **CocoaPods** installato (`sudo gem install cocoapods`)
- **Apple Developer Account** (per distribuzione)

## Setup Iniziale

1. **Installa le dipendenze:**
```bash
cd app/frontend
npm install
```

2. **Inizializza Capacitor (solo prima volta):**
```bash
npm run cap:init
```

3. **Aggiungi le piattaforme:**
```bash
# Android
npm run cap:add:android

# iOS (solo su macOS)
npm run cap:add:ios
```

## Build Android APK

### Metodo 1: Build tramite npm script
```bash
cd app/frontend
npm run android:build
```

L'APK sarà disponibile in:
`app/frontend/android/app/build/outputs/apk/release/app-release-unsigned.apk`

### Metodo 2: Build manuale con Android Studio

1. **Build del progetto web:**
```bash
npm run build
```

2. **Sincronizza con Android:**
```bash
npm run cap:sync
```

3. **Apri in Android Studio:**
```bash
npx cap open android
```

4. **In Android Studio:**
   - Vai su `Build` → `Build Bundle(s) / APK(s)` → `Build APK(s)`
   - Oppure per release: `Build` → `Generate Signed Bundle / APK`

### Firma dell'APK (per distribuzione)

1. **Genera keystore (solo prima volta):**
```bash
keytool -genkey -v -keystore synerchat-release.keystore -alias synerchat -keyalg RSA -keysize 2048 -validity 10000
```

2. **Configura in `android/app/build.gradle`:**
```gradle
android {
    signingConfigs {
        release {
            storeFile file("../../synerchat-release.keystore")
            storePassword "YOUR_KEYSTORE_PASSWORD"
            keyAlias "synerchat"
            keyPassword "YOUR_KEY_PASSWORD"
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
}
```

3. **Build APK firmato:**
```bash
cd android
./gradlew assembleRelease
```

## Build iOS (solo su macOS)

### Metodo 1: Build tramite npm script
```bash
cd app/frontend
npm run ios:build
```

### Metodo 2: Build manuale con Xcode

1. **Build del progetto web:**
```bash
npm run build
```

2. **Sincronizza con iOS:**
```bash
npm run cap:sync
```

3. **Installa CocoaPods dependencies:**
```bash
cd ios/App
pod install
cd ../..
```

4. **Apri in Xcode:**
```bash
npx cap open ios
```

5. **In Xcode:**
   - Seleziona il tuo team di sviluppo in `Signing & Capabilities`
   - Seleziona un dispositivo o simulatore
   - Vai su `Product` → `Archive`
   - Distribuisci tramite App Store Connect o Ad Hoc

### Configurazione per distribuzione iOS

1. **Aggiorna Bundle ID in Xcode:**
   - Apri il progetto in Xcode
   - Seleziona il target `App`
   - Cambia Bundle Identifier in `com.synerchat.app` (o il tuo)

2. **Configura Capabilities:**
   - Abilita `Background Modes` se necessario
   - Configura `App Transport Security` per connessioni HTTPS

## Build Rapida (Sviluppo)

Per testare rapidamente su dispositivo:

### Android:
```bash
npm run build:mobile
npx cap run android
```

### iOS:
```bash
npm run build:mobile
npx cap run ios
```

## Aggiornamento dell'App

Dopo modifiche al codice:

```bash
# Build e sincronizza
npm run build:mobile

# Oppure solo sincronizza (se non hai modificato il web)
npm run cap:sync
```

## Configurazione API Endpoint

Assicurati che l'app punti al server corretto. Modifica in `src/lib/api.ts`:

```typescript
const API_BASE_URL = process.env.VITE_API_URL || 'https://your-backend-url.com';
```

Crea `.env.production`:
```
VITE_API_URL=https://your-production-api.com
```

## Risoluzione Problemi

### Android:
- **Errore Gradle:** Assicurati di avere Java 17
- **SDK non trovato:** Configura `ANDROID_HOME` nelle variabili d'ambiente
- **Build fallita:** Pulisci con `cd android && ./gradlew clean`

### iOS:
- **Pod install fallito:** Esegui `pod repo update` poi `pod install`
- **Firma fallita:** Verifica il tuo Apple Developer Account in Xcode
- **Simulator non funziona:** Riavvia Xcode e il simulatore

## File Generati

Dopo la build troverai:

### Android:
- **Debug APK:** `android/app/build/outputs/apk/debug/app-debug.apk`
- **Release APK:** `android/app/build/outputs/apk/release/app-release.apk`
- **AAB (Play Store):** `android/app/build/outputs/bundle/release/app-release.aab`

### iOS:
- **IPA:** Generato tramite Xcode Archive → Export

## Distribuzione

### Google Play Store (Android):
1. Crea un account Google Play Developer
2. Genera un AAB firmato: `./gradlew bundleRelease`
3. Carica su Play Console
4. Compila le informazioni dell'app
5. Pubblica

### Apple App Store (iOS):
1. Crea un account Apple Developer
2. Registra l'app su App Store Connect
3. Archive in Xcode
4. Upload tramite Xcode Organizer
5. Compila le informazioni dell'app
6. Invia per review

## Note Importanti

- **Icone:** Aggiungi le icone dell'app in `public/` prima della build
- **Splash Screen:** Personalizza in `capacitor.config.ts`
- **Permessi:** Configura i permessi necessari in `AndroidManifest.xml` e `Info.plist`
- **WebSocket:** Assicurati che il backend supporti connessioni WSS (WebSocket Secure)

## Supporto

Per problemi specifici, consulta:
- [Capacitor Documentation](https://capacitorjs.com/docs)
- [Android Developer Guide](https://developer.android.com)
- [iOS Developer Guide](https://developer.apple.com)
