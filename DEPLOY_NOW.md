# 🚀 DEPLOY ADESSO SU HEROKU

## 1 COMANDO = TUTTO FATTO

```powershell
.\deploy-to-heroku.ps1
```

Questo fa:
1. ✅ Build APK Android
2. ✅ Build IPA iOS  
3. ✅ Commit su git
4. ✅ Push su Heroku
5. ✅ App online con download

---

## Cosa Vedranno gli Utenti

1. Vanno su: **`https://your-app.herokuapp.com`**
2. Pagina login con pulsanti:
   - **[🤖 Android]** → Scarica APK
   - **[🍎 iOS]** → Scarica IPA
3. Installano e usano!

---

## Prerequisiti

- Git installato ✅
- Heroku CLI installato ✅
- App già su Heroku ✅
- Android Studio (per APK) ✅

---

## Se Non Hai Ancora l'App su Heroku

```bash
# 1. Login
heroku login

# 2. Crea app
heroku create your-app-name

# 3. Collega git
heroku git:remote -a your-app-name

# 4. Deploy
.\deploy-to-heroku.ps1
```

---

## Link Finali

Dopo il deploy:
- **App Web:** `https://your-app.herokuapp.com`
- **APK:** `https://your-app.herokuapp.com/downloads/synerchat.apk`
- **IPA:** `https://your-app.herokuapp.com/downloads/synerchat.ipa`

---

## Problemi?

```bash
# Vedi log
heroku logs --tail

# Riavvia
heroku restart

# Riprova deploy
.\deploy-to-heroku.ps1
```

---

## 🎉 FATTO!

Gli utenti possono scaricare le app dalla pagina login! 🚀
