# SynerChat Mobile Apps Download Folder

Questa cartella contiene i file APK e IPA per il download delle app mobile.

## File

- **synerchat.apk** - App Android
- **synerchat.ipa** - App iOS

## Come Generare i File

Dalla root del progetto, esegui:

### Windows:
```powershell
.\build-and-deploy-apps.ps1
```

### Linux/macOS:
```bash
./build-and-deploy-apps.sh
```

## Download URL

Gli utenti possono scaricare le app da:
- Android: `http://your-domain.com/downloads/synerchat.apk`
- iOS: `http://your-domain.com/downloads/synerchat.ipa`

Oppure direttamente dalla pagina di login usando i pulsanti di download.

## Note

- I file APK/IPA non sono tracciati da git (sono troppo grandi)
- Rigenera i file ogni volta che aggiorni l'app
- Assicurati che il server abbia i permessi corretti per servire questi file

## Dimensioni Tipiche

- APK: 5-15 MB
- IPA: 10-20 MB

---

Per maggiori informazioni, consulta `DEPLOY_APPS_GUIDE.md` nella root del progetto.
