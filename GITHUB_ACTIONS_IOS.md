# 🍎 Build iOS App con GitHub Actions (GRATIS, SENZA MAC)

## 🎯 Come Funziona

GitHub Actions usa un Mac virtuale nel cloud per buildare la tua app iOS **GRATIS**!

---

## 📝 Setup (5 minuti)

### **PASSO 1: Pusha il Codice su GitHub**

Se non hai ancora un repository GitHub:

```powershell
cd C:\Users\Hp\Desktop\SYNERCHAT

# Inizializza git (se non già fatto)
git init

# Aggiungi tutto
git add .
git commit -m "Initial commit with iOS build workflow"

# Crea repository su GitHub e collegalo
git remote add origin https://github.com/TUO_USERNAME/synerchat.git
git branch -M main
git push -u origin main
```

### **PASSO 2: Esegui il Workflow**

1. Vai su GitHub: `https://github.com/TUO_USERNAME/synerchat`
2. Click su **Actions**
3. Seleziona **Build iOS App**
4. Click su **Run workflow** → **Run workflow**
5. Aspetta 10-15 minuti

### **PASSO 3: Scarica l'IPA**

1. Quando finisce, vedrai un ✅ verde
2. Click sul workflow completato
3. Scroll in basso → **Artifacts**
4. Download **synerchat-ios.zip**
5. Estrai e troverai `synerchat.ipa`

### **PASSO 4: Carica su Heroku**

```powershell
# Copia l'IPA nella cartella downloads
copy synerchat.ipa app\backend\downloads\

# Riabilita il pulsante iOS in Login.tsx (rimuovi {false &&)

# Commit e push
git add .
git commit -m "Add iOS app"
git push heroku master
```

---

## 🚀 Build Automatica

Il workflow si attiva automaticamente quando:
- Fai push su `main` o `master`
- Modifichi file in `app/frontend/`

Oppure puoi eseguirlo manualmente da GitHub Actions!

---

## ⚠️ Limitazioni

**GitHub Actions Free:**
- 2000 minuti/mese gratis
- Ogni build iOS usa ~15 minuti
- = ~133 build gratis al mese

**Firma App:**
- L'IPA non è firmata (serve account Apple Developer $99/anno)
- Puoi installarla con:
  - **TestFlight** (serve firma)
  - **AltStore** (gratis, no firma)
  - **Sideloadly** (gratis, no firma)

---

## 🔧 Alternativa: Build Locale con Mac Virtuale

Se vuoi buildare localmente senza Mac:

### **Opzione A: Hackintosh (Avanzato)**
- Installa macOS su VM
- Richiede configurazione complessa

### **Opzione B: Servizi Cloud a Pagamento**
- **MacStadium** (~$100/mese)
- **MacinCloud** (~$30/mese)
- **AWS Mac Instances** (~$1/ora)

---

## 📱 Come Installare l'IPA (Senza App Store)

### **Metodo 1: AltStore (GRATIS, RACCOMANDATO)**

1. Installa AltStore: https://altstore.io/
2. Collega iPhone al PC
3. Apri AltStore → **My Apps** → **+**
4. Seleziona `synerchat.ipa`
5. Fatto! L'app è installata

**Nota:** Devi reinstallare ogni 7 giorni (limitazione Apple)

### **Metodo 2: Sideloadly (GRATIS)**

1. Download: https://sideloadly.io/
2. Collega iPhone
3. Trascina `synerchat.ipa` su Sideloadly
4. Inserisci Apple ID
5. Click **Start**

### **Metodo 3: TestFlight (Richiede Account Developer)**

1. Serve Apple Developer Account ($99/anno)
2. Carica su App Store Connect
3. Invita beta tester
4. Installano da TestFlight

---

## 🎉 Riepilogo

✅ **GitHub Actions** builda iOS gratis nel cloud  
✅ **Nessun Mac necessario**  
✅ **Build automatica** ad ogni push  
✅ **IPA scaricabile** dagli Artifacts  
✅ **Installabile** con AltStore/Sideloadly  

---

## 🔄 Workflow Completo

```
1. Modifichi codice
2. git push
3. GitHub Actions builda iOS automaticamente
4. Scarichi IPA dagli Artifacts
5. Copi in app/backend/downloads/
6. git push heroku master
7. Utenti scaricano da Heroku!
```

**Tutto automatico! 🚀**
