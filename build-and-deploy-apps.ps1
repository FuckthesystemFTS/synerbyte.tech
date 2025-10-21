# SynerChat - Automated Build and Deploy Script
# Questo script crea automaticamente APK e IPA e li mette nella cartella downloads

param(
    [Parameter(Mandatory=$false)]
    [switch]$SkipAndroid,
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipIOS,
    
    [Parameter(Mandatory=$false)]
    [switch]$Release
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 SynerChat - Automated Build & Deploy" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Paths
$ROOT_DIR = $PSScriptRoot
$FRONTEND_DIR = Join-Path $ROOT_DIR "app\frontend"
$BACKEND_DIR = Join-Path $ROOT_DIR "app\backend"
$DOWNLOADS_DIR = Join-Path $BACKEND_DIR "downloads"

# Create downloads directory
if (-not (Test-Path $DOWNLOADS_DIR)) {
    New-Item -ItemType Directory -Path $DOWNLOADS_DIR | Out-Null
    Write-Host "✅ Created downloads directory" -ForegroundColor Green
}

# Navigate to frontend
Set-Location $FRONTEND_DIR

Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
npm install --silent
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Build web app
Write-Host "🏗️  Building web application..." -ForegroundColor Yellow
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to build web app" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Web app built successfully" -ForegroundColor Green
Write-Host ""

# Initialize Capacitor if needed
if (-not (Test-Path "capacitor.config.ts")) {
    Write-Host "🔧 Initializing Capacitor..." -ForegroundColor Yellow
    npx cap init SynerChat com.synerchat.app --web-dir=dist
    Write-Host "✅ Capacitor initialized" -ForegroundColor Green
    Write-Host ""
}

# Build Android
if (-not $SkipAndroid) {
    Write-Host "🤖 Building Android APK..." -ForegroundColor Cyan
    Write-Host "================================" -ForegroundColor Cyan
    
    # Add Android platform if needed
    if (-not (Test-Path "android")) {
        Write-Host "📱 Adding Android platform..." -ForegroundColor Yellow
        npx cap add android
        Write-Host "✅ Android platform added" -ForegroundColor Green
    }
    
    # Sync with Android
    Write-Host "🔄 Syncing with Android..." -ForegroundColor Yellow
    npx cap sync android
    Write-Host "✅ Sync complete" -ForegroundColor Green
    Write-Host ""
    
    # Check for Android SDK
    if ($env:ANDROID_HOME) {
        Write-Host "✅ ANDROID_HOME found: $env:ANDROID_HOME" -ForegroundColor Green
        
        # Build APK
        Set-Location android
        
        if ($Release) {
            Write-Host "🔨 Building Release APK..." -ForegroundColor Yellow
            .\gradlew.bat assembleRelease --quiet
            $APK_PATH = "app\build\outputs\apk\release\app-release.apk"
        } else {
            Write-Host "🔨 Building Debug APK..." -ForegroundColor Yellow
            .\gradlew.bat assembleDebug --quiet
            $APK_PATH = "app\build\outputs\apk\debug\app-debug.apk"
        }
        
        Set-Location ..
        
        if (Test-Path "android\$APK_PATH") {
            # Copy to downloads folder
            $DEST_APK = Join-Path $DOWNLOADS_DIR "synerchat.apk"
            Copy-Item "android\$APK_PATH" $DEST_APK -Force
            
            $APK_SIZE = [math]::Round((Get-Item $DEST_APK).Length / 1MB, 2)
            Write-Host "✅ Android APK built successfully!" -ForegroundColor Green
            Write-Host "📦 Size: $APK_SIZE MB" -ForegroundColor Cyan
            Write-Host "📍 Location: $DEST_APK" -ForegroundColor Cyan
            Write-Host ""
        } else {
            Write-Host "❌ APK not found after build" -ForegroundColor Red
        }
    } else {
        Write-Host "⚠️  ANDROID_HOME not set. Skipping APK build." -ForegroundColor Yellow
        Write-Host "   To build APK, install Android Studio and set ANDROID_HOME" -ForegroundColor White
        Write-Host ""
    }
}

# Build iOS
if (-not $SkipIOS) {
    Write-Host "🍎 Building iOS IPA..." -ForegroundColor Cyan
    Write-Host "================================" -ForegroundColor Cyan
    
    if ($IsWindows) {
        Write-Host "⚠️  iOS build requires macOS and Xcode" -ForegroundColor Yellow
        Write-Host "   Skipping iOS build on Windows" -ForegroundColor White
        Write-Host ""
    } else {
        # Add iOS platform if needed
        if (-not (Test-Path "ios")) {
            Write-Host "📱 Adding iOS platform..." -ForegroundColor Yellow
            npx cap add ios
            Write-Host "✅ iOS platform added" -ForegroundColor Green
        }
        
        # Sync with iOS
        Write-Host "🔄 Syncing with iOS..." -ForegroundColor Yellow
        npx cap sync ios
        Write-Host "✅ Sync complete" -ForegroundColor Green
        Write-Host ""
        
        Write-Host "📝 iOS build requires manual steps in Xcode:" -ForegroundColor Yellow
        Write-Host "   1. Open project: npx cap open ios" -ForegroundColor White
        Write-Host "   2. Select your team in Signing & Capabilities" -ForegroundColor White
        Write-Host "   3. Product > Archive" -ForegroundColor White
        Write-Host "   4. Export IPA and copy to: $DOWNLOADS_DIR\synerchat.ipa" -ForegroundColor White
        Write-Host ""
    }
}

# Create README for downloads
$README_CONTENT = @"
# SynerChat Mobile Apps

## Download Links

### Android
- **File:** synerchat.apk
- **Size:** $(if (Test-Path (Join-Path $DOWNLOADS_DIR "synerchat.apk")) { [math]::Round((Get-Item (Join-Path $DOWNLOADS_DIR "synerchat.apk")).Length / 1MB, 2) } else { "N/A" }) MB
- **Installation:** 
  1. Download the APK
  2. Enable "Install from Unknown Sources" in Android settings
  3. Open the APK file and install

### iOS
- **File:** synerchat.ipa
- **Size:** $(if (Test-Path (Join-Path $DOWNLOADS_DIR "synerchat.ipa")) { [math]::Round((Get-Item (Join-Path $DOWNLOADS_DIR "synerchat.ipa")).Length / 1MB, 2) } else { "N/A" }) MB
- **Installation:**
  - Use TestFlight for beta testing
  - Or install via enterprise certificate
  - Or use AltStore/Sideloadly

## Features
- 🔒 End-to-end encrypted messaging
- 💬 Real-time chat with WebSocket
- 📱 Native mobile experience
- 🚀 Fast and lightweight

## Requirements
- **Android:** 7.0 (API 24) or higher
- **iOS:** 13.0 or higher

## Support
For issues or questions, contact support.

---
Last updated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@

Set-Content -Path (Join-Path $DOWNLOADS_DIR "README.md") -Value $README_CONTENT

Write-Host "✨ Build process completed!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Summary:" -ForegroundColor Cyan
Write-Host "   - Web build: ✅ dist/" -ForegroundColor White

if (-not $SkipAndroid -and (Test-Path (Join-Path $DOWNLOADS_DIR "synerchat.apk"))) {
    Write-Host "   - Android APK: ✅ $DOWNLOADS_DIR\synerchat.apk" -ForegroundColor White
} else {
    Write-Host "   - Android APK: ⏭️  Skipped or failed" -ForegroundColor Yellow
}

if (-not $SkipIOS) {
    if (Test-Path (Join-Path $DOWNLOADS_DIR "synerchat.ipa")) {
        Write-Host "   - iOS IPA: ✅ $DOWNLOADS_DIR\synerchat.ipa" -ForegroundColor White
    } else {
        Write-Host "   - iOS IPA: ⏭️  Manual build required" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "🌐 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Start backend: cd app\backend && python -m uvicorn app.main:app --reload" -ForegroundColor White
Write-Host "   2. Users can download apps from: http://localhost:8000/downloads/synerchat.apk" -ForegroundColor White
Write-Host "   3. Or from the login page download buttons" -ForegroundColor White
Write-Host ""

# Return to root directory
Set-Location $ROOT_DIR
