# Deploy SynerChat to Heroku with Mobile Apps
# Questo script crea le app e le deploya su Heroku

param(
    [Parameter(Mandatory=$false)]
    [string]$HerokuApp = "",
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipBuild
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 Deploy SynerChat to Heroku" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git non trovato. Installa Git prima di continuare." -ForegroundColor Red
    exit 1
}

# Check if heroku CLI is installed
if (-not (Get-Command heroku -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Heroku CLI non trovato. Installa da: https://devcenter.heroku.com/articles/heroku-cli" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Git e Heroku CLI trovati" -ForegroundColor Green
Write-Host ""

# Get Heroku app name
if ($HerokuApp -eq "") {
    Write-Host "🔍 Cerco il nome dell'app Heroku..." -ForegroundColor Yellow
    $gitRemotes = git remote -v
    $herokuRemote = $gitRemotes | Select-String "heroku" | Select-Object -First 1
    
    if ($herokuRemote) {
        $HerokuApp = ($herokuRemote -split "/")[-1] -replace ".git.*", ""
        Write-Host "✅ App Heroku trovata: $HerokuApp" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Nessun remote Heroku trovato" -ForegroundColor Yellow
        $HerokuApp = Read-Host "Inserisci il nome della tua app Heroku"
    }
}

Write-Host ""
Write-Host "📱 App Heroku: $HerokuApp" -ForegroundColor Cyan
Write-Host ""

# Build mobile apps if not skipped
if (-not $SkipBuild) {
    Write-Host "🏗️  Building mobile apps..." -ForegroundColor Yellow
    Write-Host ""
    
    # Run build script
    if (Test-Path ".\build-and-deploy-apps.ps1") {
        & .\build-and-deploy-apps.ps1
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Build fallita" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "⚠️  Script di build non trovato, salto questo step" -ForegroundColor Yellow
    }
    
    Write-Host ""
}

# Check if APK exists
$APK_PATH = "app\backend\downloads\synerchat.apk"
if (Test-Path $APK_PATH) {
    $APK_SIZE = [math]::Round((Get-Item $APK_PATH).Length / 1MB, 2)
    Write-Host "✅ APK trovato: $APK_SIZE MB" -ForegroundColor Green
} else {
    Write-Host "⚠️  APK non trovato in $APK_PATH" -ForegroundColor Yellow
    Write-Host "   L'app sarà deployata senza APK Android" -ForegroundColor White
}

# Check if IPA exists
$IPA_PATH = "app\backend\downloads\synerchat.ipa"
if (Test-Path $IPA_PATH) {
    $IPA_SIZE = [math]::Round((Get-Item $IPA_PATH).Length / 1MB, 2)
    Write-Host "✅ IPA trovato: $IPA_SIZE MB" -ForegroundColor Green
} else {
    Write-Host "⚠️  IPA non trovato in $IPA_PATH" -ForegroundColor Yellow
    Write-Host "   L'app sarà deployata senza IPA iOS" -ForegroundColor White
}

Write-Host ""

# Git status
Write-Host "📝 Preparazione commit..." -ForegroundColor Yellow

# Add files
git add .

# Check if there are changes
$changes = git status --porcelain
if ($changes) {
    Write-Host "✅ Modifiche trovate, creo commit..." -ForegroundColor Green
    
    # Commit
    $commitMessage = "Deploy: Update mobile apps and sync improvements"
    git commit -m $commitMessage
    
    Write-Host "✅ Commit creato: $commitMessage" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Nessuna modifica da committare" -ForegroundColor Cyan
}

Write-Host ""

# Push to Heroku
Write-Host "🚀 Deploy su Heroku..." -ForegroundColor Cyan
Write-Host ""

git push heroku main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✨ Deploy completato con successo!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 La tua app è disponibile su:" -ForegroundColor Cyan
    Write-Host "   https://$HerokuApp.herokuapp.com" -ForegroundColor White
    Write-Host ""
    Write-Host "📱 Download links:" -ForegroundColor Cyan
    Write-Host "   Android: https://$HerokuApp.herokuapp.com/downloads/synerchat.apk" -ForegroundColor White
    Write-Host "   iOS: https://$HerokuApp.herokuapp.com/downloads/synerchat.ipa" -ForegroundColor White
    Write-Host ""
    Write-Host "👥 Gli utenti possono scaricare le app dalla pagina di login!" -ForegroundColor Green
    Write-Host ""
    
    # Open app in browser
    $openBrowser = Read-Host "Vuoi aprire l'app nel browser? (y/n)"
    if ($openBrowser -eq "y" -or $openBrowser -eq "Y") {
        Start-Process "https://$HerokuApp.herokuapp.com"
    }
} else {
    Write-Host ""
    Write-Host "❌ Deploy fallito" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔍 Controlla i log con:" -ForegroundColor Yellow
    Write-Host "   heroku logs --tail -a $HerokuApp" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "💡 Comandi utili:" -ForegroundColor Cyan
Write-Host "   heroku logs --tail -a $HerokuApp    # Vedi i log" -ForegroundColor White
Write-Host "   heroku open -a $HerokuApp           # Apri app nel browser" -ForegroundColor White
Write-Host "   heroku restart -a $HerokuApp        # Riavvia app" -ForegroundColor White
Write-Host ""
