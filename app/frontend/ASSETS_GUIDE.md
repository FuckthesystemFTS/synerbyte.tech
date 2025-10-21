# SynerChat - Guida Assets Mobile

## Icone App

Per avere un'app professionale, devi fornire le icone nelle dimensioni corrette.

### Android

Crea le seguenti icone nella cartella `android/app/src/main/res/`:

```
mipmap-mdpi/ic_launcher.png         (48x48 px)
mipmap-hdpi/ic_launcher.png         (72x72 px)
mipmap-xhdpi/ic_launcher.png        (96x96 px)
mipmap-xxhdpi/ic_launcher.png       (144x144 px)
mipmap-xxxhdpi/ic_launcher.png      (192x192 px)
```

**Icona Adaptive (Android 8+):**
```
mipmap-mdpi/ic_launcher_foreground.png
mipmap-hdpi/ic_launcher_foreground.png
mipmap-xhdpi/ic_launcher_foreground.png
mipmap-xxhdpi/ic_launcher_foreground.png
mipmap-xxxhdpi/ic_launcher_foreground.png
```

### iOS

Crea le icone in `ios/App/App/Assets.xcassets/AppIcon.appiconset/`:

```
Icon-20.png           (20x20 px)
Icon-20@2x.png        (40x40 px)
Icon-20@3x.png        (60x60 px)
Icon-29.png           (29x29 px)
Icon-29@2x.png        (58x58 px)
Icon-29@3x.png        (87x87 px)
Icon-40.png           (40x40 px)
Icon-40@2x.png        (80x80 px)
Icon-40@3x.png        (120x120 px)
Icon-60@2x.png        (120x120 px)
Icon-60@3x.png        (180x180 px)
Icon-76.png           (76x76 px)
Icon-76@2x.png        (152x152 px)
Icon-83.5@2x.png      (167x167 px)
Icon-1024.png         (1024x1024 px)
```

## Splash Screen

### Android

Crea le splash screen in `android/app/src/main/res/`:

```
drawable/splash.png              (320x480 px)
drawable-land/splash.png         (480x320 px)
drawable-hdpi/splash.png         (480x800 px)
drawable-land-hdpi/splash.png    (800x480 px)
drawable-xhdpi/splash.png        (720x1280 px)
drawable-land-xhdpi/splash.png   (1280x720 px)
drawable-xxhdpi/splash.png       (960x1600 px)
drawable-land-xxhdpi/splash.png  (1600x960 px)
drawable-xxxhdpi/splash.png      (1280x1920 px)
drawable-land-xxxhdpi/splash.png (1920x1280 px)
```

### iOS

Crea le splash screen in `ios/App/App/Assets.xcassets/Splash.imageset/`:

```
splash.png           (2732x2732 px - universale)
splash@2x.png        (2732x2732 px)
splash@3x.png        (2732x2732 px)
```

## Tool Automatici

### Generatore di Icone Online

Usa questi tool per generare automaticamente tutte le dimensioni:

1. **App Icon Generator**
   - https://www.appicon.co/
   - Carica un'immagine 1024x1024 px
   - Scarica il pacchetto completo

2. **Capacitor Assets**
   ```bash
   npm install -g @capacitor/assets
   
   # Crea una cartella resources/
   mkdir resources
   
   # Aggiungi:
   # - resources/icon.png (1024x1024 px, PNG con trasparenza)
   # - resources/splash.png (2732x2732 px, PNG)
   
   # Genera automaticamente tutte le dimensioni
   npx capacitor-assets generate
   ```

3. **Cordova Resources** (compatibile con Capacitor)
   ```bash
   npm install -g cordova-res
   
   # Nella cartella resources/
   # - icon.png (1024x1024 px)
   # - splash.png (2732x2732 px)
   
   cordova-res android --skip-config --copy
   cordova-res ios --skip-config --copy
   ```

## Linee Guida Design

### Icona App

- **Dimensione base:** 1024x1024 px
- **Formato:** PNG con trasparenza (per Android) o senza (per iOS)
- **Colori:** Usa i colori del brand (#2c3e50, #3498db)
- **Semplicità:** L'icona deve essere riconoscibile anche a 48x48 px
- **Margini:** Lascia 10% di margine sui bordi

**Suggerimento per SynerChat:**
- Logo centrale con sfondo gradiente blu
- Simbolo di chat o connessione
- Testo "SC" stilizzato

### Splash Screen

- **Dimensione base:** 2732x2732 px (quadrato)
- **Formato:** PNG
- **Colore sfondo:** #2c3e50 (come da config)
- **Contenuto:** Logo centrato + nome app
- **Safe area:** Mantieni contenuto importante nel centro (1200x1200 px)

**Suggerimento per SynerChat:**
```
┌─────────────────────────┐
│                         │
│                         │
│       [LOGO]            │
│      SynerChat          │
│   Secure Messaging      │
│                         │
│       ⏳ Loading...     │
│                         │
└─────────────────────────┘
```

## Esempio Rapido

Se vuoi iniziare velocemente, usa il logo esistente:

1. **Copia il logo:**
```bash
# Dalla root del progetto
cp app/frontend/public/logosy.jpg resources/icon-base.jpg
```

2. **Converti in PNG 1024x1024:**
   - Usa un editor (Photoshop, GIMP, Figma)
   - Oppure online: https://www.iloveimg.com/resize-image

3. **Genera le dimensioni:**
```bash
npx @capacitor/assets generate --iconBackgroundColor '#2c3e50' --splashBackgroundColor '#2c3e50'
```

## Colori Brand SynerChat

Usa questi colori per coerenza:

```
Primary:   #2c3e50 (Blu scuro)
Secondary: #3498db (Blu)
Accent:    #27ae60 (Verde)
Error:     #e74c3c (Rosso)
Warning:   #f39c12 (Arancione)
```

## Checklist Pre-Build

Prima di fare la build finale:

- [ ] Icona app 1024x1024 creata
- [ ] Splash screen 2732x2732 creata
- [ ] Icone generate per tutte le dimensioni
- [ ] Splash screen generate per tutte le dimensioni
- [ ] Testato su dispositivo reale
- [ ] Colori brand applicati
- [ ] Nome app corretto in tutti i file

## File da Modificare

### Android
- `android/app/src/main/res/values/strings.xml` - Nome app
- `android/app/src/main/AndroidManifest.xml` - Permessi e configurazioni
- `android/app/build.gradle` - Version code e version name

### iOS
- `ios/App/App/Info.plist` - Nome app e configurazioni
- `ios/App/App.xcodeproj/project.pbxproj` - Version e build number
- Xcode: General > Identity > Display Name

## Risorse Utili

- [Android Icon Guidelines](https://developer.android.com/guide/practices/ui_guidelines/icon_design_launcher)
- [iOS Icon Guidelines](https://developer.apple.com/design/human-interface-guidelines/app-icons)
- [Capacitor Assets Plugin](https://github.com/ionic-team/capacitor-assets)
- [Material Design Icons](https://materialdesignicons.com/)
