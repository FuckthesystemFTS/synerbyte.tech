# 📱 SynerChat - Guida Rapida Build Mobile

## 🚀 Inizio Rapido

### Windows (PowerShell)

```powershell
cd app/frontend

# Build Android APK
.\build-mobile.ps1 -Platform android

# Build con inizializzazione (prima volta)
.\build-mobile.ps1 -Platform android -Init

# Build Release (firmato)
.\build-mobile.ps1 -Platform android -Release
```

### Linux/macOS (Bash)

```bash
cd app/frontend
chmod +x build-mobile.sh

# Build Android APK
./build-mobile.sh --platform android

# Build iOS (solo macOS)
./build-mobile.sh --platform ios

# Build entrambi
./build-mobile.sh --platform both

# Build con inizializzazione (prima volta)
./build-mobile.sh --platform android --init

# Build Release
./build-mobile.sh --platform android --release
```

## 📋 Prerequisiti Minimi

### Per Android:
1. **Node.js 18+** - [Download](https://nodejs.org/)
2. **Java JDK 17+** - [Download](https://adoptium.net/)
3. **Android Studio** - [Download](https://developer.android.com/studio)

### Per iOS (solo macOS):
1. **macOS** (Monterey o superiore)
2. **Xcode 14+** - [App Store](https://apps.apple.com/app/xcode/id497799835)
3. **CocoaPods** - `sudo gem install cocoapods`

## 🎯 Build in 3 Passi

### Passo 1: Installa Dipendenze

```bash
cd app/frontend
npm install
```

### Passo 2: Build Web App

```bash
npm run build
```

### Passo 3: Build Mobile

**Android (Automatico):**
```bash
# Windows
.\build-mobile.ps1 -Platform android

# Linux/Mac
./build-mobile.sh --platform android
```

**Android (Manuale con Android Studio):**
```bash
npm run build:mobile
npx cap open android
```
Poi in Android Studio: `Build` → `Build Bundle(s) / APK(s)` → `Build APK(s)`

**iOS (solo macOS):**
```bash
npm run build:mobile
npx cap open ios
```
Poi in Xcode: `Product` → `Archive`

## 📦 Dove Trovare i File

### Android APK:
```
app/frontend/android/app/build/outputs/apk/debug/app-debug.apk
app/frontend/android/app/build/outputs/apk/release/app-release.apk
```

### Android AAB (per Play Store):
```
app/frontend/android/app/build/outputs/bundle/release/app-release.aab
```

### iOS IPA:
Generato tramite Xcode Archive → Export

## ⚙️ Configurazione Ambiente

### Windows - Variabili d'Ambiente

1. **JAVA_HOME:**
   ```
   C:\Program Files\Eclipse Adoptium\jdk-17.0.x-hotspot
   ```

2. **ANDROID_HOME:**
   ```
   C:\Users\[TuoNome]\AppData\Local\Android\Sdk
   ```

3. **PATH:** Aggiungi:
   ```
   %ANDROID_HOME%\platform-tools
   %ANDROID_HOME%\tools
   %JAVA_HOME%\bin
   ```

### macOS/Linux - .bashrc o .zshrc

```bash
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/tools
```

## 🔧 Risoluzione Problemi Comuni

### ❌ "ANDROID_HOME not found"

**Soluzione:**
1. Apri Android Studio
2. Vai su `Tools` → `SDK Manager`
3. Copia il percorso "Android SDK Location"
4. Imposta la variabile d'ambiente ANDROID_HOME

### ❌ "Gradle build failed"

**Soluzione:**
```bash
cd app/frontend/android
./gradlew clean
cd ..
npm run build:mobile
```

### ❌ "Java version mismatch"

**Soluzione:**
```bash
# Verifica versione Java
java -version

# Deve essere 17 o superiore
# Se no, scarica JDK 17 da https://adoptium.net/
```

### ❌ "Pod install failed" (iOS)

**Soluzione:**
```bash
cd ios/App
pod repo update
pod install --repo-update
cd ../..
```

### ❌ "WebSocket connection failed"

**Soluzione:**
Assicurati che il backend supporti WSS (WebSocket Secure) e che l'URL sia corretto in `src/lib/api.ts`

## 🎨 Personalizzazione

### Cambia Nome App

**Android:** `android/app/src/main/res/values/strings.xml`
```xml
<string name="app_name">SynerChat</string>
```

**iOS:** Xcode → General → Display Name

### Cambia Icona

Vedi `ASSETS_GUIDE.md` per istruzioni dettagliate.

Quick: Usa [appicon.co](https://www.appicon.co/) per generare tutte le dimensioni.

### Cambia Package ID

**Capacitor:** `capacitor.config.ts`
```typescript
appId: 'com.synerchat.app'
```

Poi rigenera le piattaforme:
```bash
npx cap sync
```

## 📱 Test su Dispositivo

### Android:
```bash
# Abilita Debug USB sul telefono
# Connetti via USB
npm run build:mobile
npx cap run android
```

### iOS:
```bash
# Connetti iPhone via USB
# Fidati del computer su iPhone
npm run build:mobile
npx cap run ios
```

## 🚀 Distribuzione

### Google Play Store

1. **Crea account** su [Google Play Console](https://play.google.com/console)
2. **Genera keystore:**
   ```bash
   keytool -genkey -v -keystore synerchat.keystore -alias synerchat -keyalg RSA -keysize 2048 -validity 10000
   ```
3. **Configura firma** in `android/app/build.gradle`
4. **Build AAB:**
   ```bash
   cd android
   ./gradlew bundleRelease
   ```
5. **Carica** su Play Console

### Apple App Store

1. **Crea account** su [Apple Developer](https://developer.apple.com/)
2. **Registra app** su [App Store Connect](https://appstoreconnect.apple.com/)
3. **Archive in Xcode:** Product → Archive
4. **Upload:** Window → Organizer → Distribute App
5. **Submit** per review

## 📚 Documentazione Completa

- **Build dettagliata:** `app/frontend/BUILD_MOBILE.md`
- **Assets e icone:** `app/frontend/ASSETS_GUIDE.md`
- **Capacitor docs:** https://capacitorjs.com/docs

## 🆘 Supporto

### Errori Comuni
- Controlla che tutte le dipendenze siano installate
- Verifica le variabili d'ambiente
- Pulisci la build: `./gradlew clean` (Android)
- Riavvia Android Studio / Xcode

### Log e Debug
```bash
# Android logs
npx cap run android -l

# iOS logs  
npx cap run ios -l

# WebSocket debug
# Apri DevTools nella WebView: chrome://inspect (Android)
```

## ✅ Checklist Pre-Release

- [ ] Testato su dispositivi reali (Android + iOS)
- [ ] Icone e splash screen configurati
- [ ] Nome app corretto
- [ ] Version code/number aggiornato
- [ ] Backend URL di produzione configurato
- [ ] WebSocket funzionante (WSS)
- [ ] Permessi necessari dichiarati
- [ ] Build firmata per distribuzione
- [ ] Screenshot per store preparati
- [ ] Descrizione app scritta

## 🎉 Fatto!

Ora hai tutto il necessario per creare le app Android e iOS di SynerChat!

Per domande o problemi, consulta la documentazione completa o apri un issue.

---

**Versione:** 1.0.0  
**Ultimo aggiornamento:** Ottobre 2025
