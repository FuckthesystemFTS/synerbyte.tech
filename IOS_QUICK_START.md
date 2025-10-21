# 🍎 iOS App - Quick Start (SENZA MAC)

## ✨ Cosa Ho Configurato

✅ **GitHub Actions workflow** per buildare iOS automaticamente  
✅ **Nessun Mac necessario** - usa Mac virtuale nel cloud  
✅ **GRATIS** - 2000 minuti/mese inclusi  

---

## 🚀 Come Usarlo (3 Passi)

### **PASSO 1: Pusha su GitHub**

Se NON hai ancora un repository GitHub:

1. Vai su: https://github.com/new
2. Nome: `synerchat`
3. Click **Create repository**

### **PASSO 2: Esegui Build**

1. Vai su: `https://github.com/TUO_USERNAME/synerchat/actions`
2. Scegli **"Build iOS App"** o **"Build iOS App - Simple"**
3. Click su **Run workflow** → **Run workflow**
4. Aspetta 10-15 minuti ⏳

### **PASSO 3: Scarica IPA**

1. Quando vedi ✅ verde
2. Click sul workflow
3. Scroll giù → **Artifacts**
4. Download **synerchat-ios.zip**
5. Estrai → `synerchat.ipa`

---

## 📱 Carica su Heroku

```powershell
# Copia IPA nella cartella downloads
copy synerchat.ipa C:\Users\Hp\Desktop\SYNERCHAT\app\backend\downloads\

cd C:\Users\Hp\Desktop\SYNERCHAT

# Riabilita pulsante iOS (vedi sotto)
# Poi commit e push
git add .
git commit -m "Add iOS app"
git push heroku master
```

### Riabilita Pulsante iOS

In `app/frontend/src/pages/Login.tsx`, cerca:

```tsx
{/* iOS Download Button - Coming Soon */}
{false && <a
```

Cambia in:

```tsx
{/* iOS Download Button */}
<a
```

E rimuovi la `}` alla fine del blocco iOS.

---

## 🔄 Build Automatica

Il workflow si attiva automaticamente quando:
- Fai `git push` su GitHub
- Modifichi file in `app/frontend/`

L'IPA sarà sempre disponibile negli **Artifacts**!

---

## 📲 Come Installare l'IPA (Utenti)

### **Metodo 1: AltStore (GRATIS)**

1. Download: https://altstore.io/
2. Installa AltStore sul PC
3. Collega iPhone al PC
4. Apri AltStore → **My Apps** → **+**
5. Seleziona `synerchat.ipa`
6. Fatto!

**Nota:** Reinstalla ogni 7 giorni (limitazione Apple)

### **Metodo 2: Sideloadly (GRATIS)**

1. Download: https://sideloadly.io/
2. Collega iPhone
3. Trascina `synerchat.ipa`
4. Inserisci Apple ID
5. Click **Start**

---

## 💡 Tips

### Build Fallita?

Controlla i log su GitHub Actions:
1. Click sul workflow fallito
2. Click su **build-ios**
3. Leggi l'errore

Errori comuni:
- **Xcode version**: Aggiorna nel workflow
- **Dependencies**: Verifica `package.json`
- **Capacitor**: Esegui `npx cap sync ios` localmente per testare

### Velocizza Build

Aggiungi cache nel workflow:

```yaml
- name: Cache node modules
  uses: actions/cache@v3
  with:
    path: app/frontend/node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

---

## 🎉 Riepilogo

1. ✅ Push su GitHub
2. ✅ Esegui workflow manualmente (o automatico)
3. ✅ Scarica IPA dagli Artifacts
4. ✅ Copia in `app/backend/downloads/`
5. ✅ Push su Heroku
6. ✅ Utenti scaricano da Heroku!

**Tutto senza Mac! 🚀**

---

## 📚 Documentazione Completa

Vedi: `GITHUB_ACTIONS_IOS.md`
