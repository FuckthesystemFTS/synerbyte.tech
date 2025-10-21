# SynerChat Mobile Build Script
# PowerShell script per Windows

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('android', 'ios', 'both')]
    [string]$Platform = 'android',
    
    [Parameter(Mandatory=$false)]
    [switch]$Init,
    
    [Parameter(Mandatory=$false)]
    [switch]$Release
)

Write-Host "🚀 SynerChat Mobile Build Script" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check if Node.js is installed
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js version: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js non trovato. Installa Node.js 18.x o superiore." -ForegroundColor Red
    exit 1
}

# Check if npm is installed
try {
    $npmVersion = npm --version
    Write-Host "✅ npm version: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm non trovato." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Install dependencies
Write-Host "📦 Installazione dipendenze..." -ForegroundColor Yellow
npm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Errore durante l'installazione delle dipendenze" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Dipendenze installate" -ForegroundColor Green
Write-Host ""

# Initialize Capacitor if requested
if ($Init) {
    Write-Host "🔧 Inizializzazione Capacitor..." -ForegroundColor Yellow
    npx cap init SynerChat com.synerchat.app --web-dir=dist
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Errore durante l'inizializzazione di Capacitor" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Capacitor inizializzato" -ForegroundColor Green
    Write-Host ""
}

# Build web app
Write-Host "🏗️  Building web application..." -ForegroundColor Yellow
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Errore durante la build web" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Build web completata" -ForegroundColor Green
Write-Host ""

# Add platforms if needed
if ($Platform -eq 'android' -or $Platform -eq 'both') {
    if (-not (Test-Path "android")) {
        Write-Host "📱 Aggiunta piattaforma Android..." -ForegroundColor Yellow
        npx cap add android
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Errore durante l'aggiunta di Android" -ForegroundColor Red
            exit 1
        }
        Write-Host "✅ Piattaforma Android aggiunta" -ForegroundColor Green
        Write-Host ""
    }
}

if ($Platform -eq 'ios' -or $Platform -eq 'both') {
    if (-not (Test-Path "ios")) {
        Write-Host "🍎 Aggiunta piattaforma iOS..." -ForegroundColor Yellow
        npx cap add ios
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Errore durante l'aggiunta di iOS" -ForegroundColor Red
            exit 1
        }
        Write-Host "✅ Piattaforma iOS aggiunta" -ForegroundColor Green
        Write-Host ""
    }
}

# Sync with platforms
Write-Host "🔄 Sincronizzazione con le piattaforme..." -ForegroundColor Yellow
npx cap sync
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Errore durante la sincronizzazione" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Sincronizzazione completata" -ForegroundColor Green
Write-Host ""

# Build Android
if ($Platform -eq 'android' -or $Platform -eq 'both') {
    Write-Host "🤖 Building Android APK..." -ForegroundColor Yellow
    
    # Check if Android SDK is available
    if (-not $env:ANDROID_HOME) {
        Write-Host "⚠️  ANDROID_HOME non configurato. Apro Android Studio..." -ForegroundColor Yellow
        npx cap open android
        Write-Host ""
        Write-Host "📝 Per completare la build:" -ForegroundColor Cyan
        Write-Host "   1. In Android Studio, vai su Build > Build Bundle(s) / APK(s) > Build APK(s)" -ForegroundColor White
        Write-Host "   2. L'APK sarà in: android/app/build/outputs/apk/debug/app-debug.apk" -ForegroundColor White
    } else {
        Write-Host "✅ ANDROID_HOME trovato: $env:ANDROID_HOME" -ForegroundColor Green
        
        if ($Release) {
            Write-Host "🔨 Building Release APK..." -ForegroundColor Yellow
            Set-Location android
            .\gradlew.bat assembleRelease
            Set-Location ..
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Release APK creato!" -ForegroundColor Green
                Write-Host "📦 Percorso: android\app\build\outputs\apk\release\app-release.apk" -ForegroundColor Cyan
            } else {
                Write-Host "❌ Errore durante la build Release" -ForegroundColor Red
            }
        } else {
            Write-Host "🔨 Building Debug APK..." -ForegroundColor Yellow
            Set-Location android
            .\gradlew.bat assembleDebug
            Set-Location ..
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Debug APK creato!" -ForegroundColor Green
                Write-Host "📦 Percorso: android\app\build\outputs\apk\debug\app-debug.apk" -ForegroundColor Cyan
            } else {
                Write-Host "❌ Errore durante la build Debug" -ForegroundColor Red
            }
        }
    }
    Write-Host ""
}

# Build iOS
if ($Platform -eq 'ios' -or $Platform -eq 'both') {
    Write-Host "🍎 Building iOS..." -ForegroundColor Yellow
    
    if ($IsWindows) {
        Write-Host "⚠️  La build iOS richiede macOS e Xcode" -ForegroundColor Yellow
        Write-Host "   Puoi comunque preparare il progetto per la build su Mac" -ForegroundColor White
    } else {
        Write-Host "🔨 Apertura progetto in Xcode..." -ForegroundColor Yellow
        npx cap open ios
        Write-Host ""
        Write-Host "📝 Per completare la build:" -ForegroundColor Cyan
        Write-Host "   1. In Xcode, seleziona il tuo team di sviluppo" -ForegroundColor White
        Write-Host "   2. Seleziona un dispositivo o simulatore" -ForegroundColor White
        Write-Host "   3. Vai su Product > Archive per creare l'IPA" -ForegroundColor White
    }
    Write-Host ""
}

Write-Host "✨ Build completata!" -ForegroundColor Green
Write-Host ""
Write-Host "📚 Per maggiori informazioni, consulta BUILD_MOBILE.md" -ForegroundColor Cyan
Write-Host ""

# Summary
Write-Host "📊 Riepilogo:" -ForegroundColor Cyan
Write-Host "   - Web build: ✅ dist/" -ForegroundColor White
if ($Platform -eq 'android' -or $Platform -eq 'both') {
    Write-Host "   - Android: ✅ android/" -ForegroundColor White
}
if ($Platform -eq 'ios' -or $Platform -eq 'both') {
    Write-Host "   - iOS: ✅ ios/" -ForegroundColor White
}
Write-Host ""
