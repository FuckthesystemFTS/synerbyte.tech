#!/bin/bash

# SynerChat - Automated Build and Deploy Script
# Questo script crea automaticamente APK e IPA e li mette nella cartella downloads

set -e

SKIP_ANDROID=false
SKIP_IOS=false
RELEASE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-android)
            SKIP_ANDROID=true
            shift
            ;;
        --skip-ios)
            SKIP_IOS=true
            shift
            ;;
        --release)
            RELEASE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}🚀 SynerChat - Automated Build & Deploy${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# Paths
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$ROOT_DIR/app/frontend"
BACKEND_DIR="$ROOT_DIR/app/backend"
DOWNLOADS_DIR="$BACKEND_DIR/downloads"

# Create downloads directory
if [ ! -d "$DOWNLOADS_DIR" ]; then
    mkdir -p "$DOWNLOADS_DIR"
    echo -e "${GREEN}✅ Created downloads directory${NC}"
fi

# Navigate to frontend
cd "$FRONTEND_DIR"

echo -e "${YELLOW}📦 Installing dependencies...${NC}"
npm install --silent
echo -e "${GREEN}✅ Dependencies installed${NC}"
echo ""

# Build web app
echo -e "${YELLOW}🏗️  Building web application...${NC}"
npm run build
echo -e "${GREEN}✅ Web app built successfully${NC}"
echo ""

# Initialize Capacitor if needed
if [ ! -f "capacitor.config.ts" ]; then
    echo -e "${YELLOW}🔧 Initializing Capacitor...${NC}"
    npx cap init SynerChat com.synerchat.app --web-dir=dist
    echo -e "${GREEN}✅ Capacitor initialized${NC}"
    echo ""
fi

# Build Android
if [ "$SKIP_ANDROID" = false ]; then
    echo -e "${CYAN}🤖 Building Android APK...${NC}"
    echo -e "${CYAN}================================${NC}"
    
    # Add Android platform if needed
    if [ ! -d "android" ]; then
        echo -e "${YELLOW}📱 Adding Android platform...${NC}"
        npx cap add android
        echo -e "${GREEN}✅ Android platform added${NC}"
    fi
    
    # Sync with Android
    echo -e "${YELLOW}🔄 Syncing with Android...${NC}"
    npx cap sync android
    echo -e "${GREEN}✅ Sync complete${NC}"
    echo ""
    
    # Check for Android SDK
    if [ -n "$ANDROID_HOME" ]; then
        echo -e "${GREEN}✅ ANDROID_HOME found: $ANDROID_HOME${NC}"
        
        # Build APK
        cd android
        chmod +x gradlew
        
        if [ "$RELEASE" = true ]; then
            echo -e "${YELLOW}🔨 Building Release APK...${NC}"
            ./gradlew assembleRelease --quiet
            APK_PATH="app/build/outputs/apk/release/app-release.apk"
        else
            echo -e "${YELLOW}🔨 Building Debug APK...${NC}"
            ./gradlew assembleDebug --quiet
            APK_PATH="app/build/outputs/apk/debug/app-debug.apk"
        fi
        
        cd ..
        
        if [ -f "android/$APK_PATH" ]; then
            # Copy to downloads folder
            DEST_APK="$DOWNLOADS_DIR/synerchat.apk"
            cp "android/$APK_PATH" "$DEST_APK"
            
            APK_SIZE=$(du -h "$DEST_APK" | cut -f1)
            echo -e "${GREEN}✅ Android APK built successfully!${NC}"
            echo -e "${CYAN}📦 Size: $APK_SIZE${NC}"
            echo -e "${CYAN}📍 Location: $DEST_APK${NC}"
            echo ""
        else
            echo -e "${RED}❌ APK not found after build${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  ANDROID_HOME not set. Skipping APK build.${NC}"
        echo -e "   To build APK, install Android Studio and set ANDROID_HOME"
        echo ""
    fi
fi

# Build iOS
if [ "$SKIP_IOS" = false ]; then
    echo -e "${CYAN}🍎 Building iOS IPA...${NC}"
    echo -e "${CYAN}================================${NC}"
    
    if [[ "$OSTYPE" != "darwin"* ]]; then
        echo -e "${YELLOW}⚠️  iOS build requires macOS and Xcode${NC}"
        echo -e "   Skipping iOS build on non-macOS system"
        echo ""
    else
        # Add iOS platform if needed
        if [ ! -d "ios" ]; then
            echo -e "${YELLOW}📱 Adding iOS platform...${NC}"
            npx cap add ios
            echo -e "${GREEN}✅ iOS platform added${NC}"
        fi
        
        # Sync with iOS
        echo -e "${YELLOW}🔄 Syncing with iOS...${NC}"
        npx cap sync ios
        echo -e "${GREEN}✅ Sync complete${NC}"
        echo ""
        
        # Install CocoaPods
        if [ -d "ios/App" ]; then
            echo -e "${YELLOW}📦 Installing CocoaPods...${NC}"
            cd ios/App
            pod install --quiet
            cd ../..
            echo -e "${GREEN}✅ CocoaPods installed${NC}"
        fi
        
        echo -e "${YELLOW}📝 iOS build requires manual steps in Xcode:${NC}"
        echo -e "   1. Open project: npx cap open ios"
        echo -e "   2. Select your team in Signing & Capabilities"
        echo -e "   3. Product > Archive"
        echo -e "   4. Export IPA and copy to: $DOWNLOADS_DIR/synerchat.ipa"
        echo ""
    fi
fi

# Create README for downloads
README_CONTENT="# SynerChat Mobile Apps

## Download Links

### Android
- **File:** synerchat.apk
- **Size:** $(if [ -f "$DOWNLOADS_DIR/synerchat.apk" ]; then du -h "$DOWNLOADS_DIR/synerchat.apk" | cut -f1; else echo "N/A"; fi)
- **Installation:** 
  1. Download the APK
  2. Enable \"Install from Unknown Sources\" in Android settings
  3. Open the APK file and install

### iOS
- **File:** synerchat.ipa
- **Size:** $(if [ -f "$DOWNLOADS_DIR/synerchat.ipa" ]; then du -h "$DOWNLOADS_DIR/synerchat.ipa" | cut -f1; else echo "N/A"; fi)
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
Last updated: $(date '+%Y-%m-%d %H:%M:%S')
"

echo "$README_CONTENT" > "$DOWNLOADS_DIR/README.md"

echo -e "${GREEN}✨ Build process completed!${NC}"
echo ""
echo -e "${CYAN}📊 Summary:${NC}"
echo -e "   - Web build: ✅ dist/"

if [ "$SKIP_ANDROID" = false ] && [ -f "$DOWNLOADS_DIR/synerchat.apk" ]; then
    echo -e "   - Android APK: ✅ $DOWNLOADS_DIR/synerchat.apk"
else
    echo -e "   - Android APK: ⏭️  Skipped or failed"
fi

if [ "$SKIP_IOS" = false ]; then
    if [ -f "$DOWNLOADS_DIR/synerchat.ipa" ]; then
        echo -e "   - iOS IPA: ✅ $DOWNLOADS_DIR/synerchat.ipa"
    else
        echo -e "   - iOS IPA: ⏭️  Manual build required"
    fi
fi

echo ""
echo -e "${CYAN}🌐 Next steps:${NC}"
echo -e "   1. Start backend: cd app/backend && python -m uvicorn app.main:app --reload"
echo -e "   2. Users can download apps from: http://localhost:8000/downloads/synerchat.apk"
echo -e "   3. Or from the login page download buttons"
echo ""

# Return to root directory
cd "$ROOT_DIR"
