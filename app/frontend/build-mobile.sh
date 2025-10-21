#!/bin/bash

# SynerChat Mobile Build Script
# Bash script per Linux/macOS

set -e

PLATFORM="android"
INIT=false
RELEASE=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --platform)
            PLATFORM="$2"
            shift 2
            ;;
        --init)
            INIT=true
            shift
            ;;
        --release)
            RELEASE=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

echo -e "${CYAN}🚀 SynerChat Mobile Build Script${NC}"
echo -e "${CYAN}=================================${NC}"
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js non trovato. Installa Node.js 18.x o superiore.${NC}"
    exit 1
fi
NODE_VERSION=$(node --version)
echo -e "${GREEN}✅ Node.js version: $NODE_VERSION${NC}"

# Check npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm non trovato.${NC}"
    exit 1
fi
NPM_VERSION=$(npm --version)
echo -e "${GREEN}✅ npm version: $NPM_VERSION${NC}"
echo ""

# Install dependencies
echo -e "${YELLOW}📦 Installazione dipendenze...${NC}"
npm install
echo -e "${GREEN}✅ Dipendenze installate${NC}"
echo ""

# Initialize Capacitor if requested
if [ "$INIT" = true ]; then
    echo -e "${YELLOW}🔧 Inizializzazione Capacitor...${NC}"
    npx cap init SynerChat com.synerchat.app --web-dir=dist
    echo -e "${GREEN}✅ Capacitor inizializzato${NC}"
    echo ""
fi

# Build web app
echo -e "${YELLOW}🏗️  Building web application...${NC}"
npm run build
echo -e "${GREEN}✅ Build web completata${NC}"
echo ""

# Add platforms if needed
if [ "$PLATFORM" = "android" ] || [ "$PLATFORM" = "both" ]; then
    if [ ! -d "android" ]; then
        echo -e "${YELLOW}📱 Aggiunta piattaforma Android...${NC}"
        npx cap add android
        echo -e "${GREEN}✅ Piattaforma Android aggiunta${NC}"
        echo ""
    fi
fi

if [ "$PLATFORM" = "ios" ] || [ "$PLATFORM" = "both" ]; then
    if [ ! -d "ios" ]; then
        echo -e "${YELLOW}🍎 Aggiunta piattaforma iOS...${NC}"
        npx cap add ios
        echo -e "${GREEN}✅ Piattaforma iOS aggiunta${NC}"
        echo ""
    fi
fi

# Sync with platforms
echo -e "${YELLOW}🔄 Sincronizzazione con le piattaforme...${NC}"
npx cap sync
echo -e "${GREEN}✅ Sincronizzazione completata${NC}"
echo ""

# Build Android
if [ "$PLATFORM" = "android" ] || [ "$PLATFORM" = "both" ]; then
    echo -e "${YELLOW}🤖 Building Android APK...${NC}"
    
    if [ -z "$ANDROID_HOME" ]; then
        echo -e "${YELLOW}⚠️  ANDROID_HOME non configurato. Apro Android Studio...${NC}"
        npx cap open android
        echo ""
        echo -e "${CYAN}📝 Per completare la build:${NC}"
        echo -e "   1. In Android Studio, vai su Build > Build Bundle(s) / APK(s) > Build APK(s)"
        echo -e "   2. L'APK sarà in: android/app/build/outputs/apk/debug/app-debug.apk"
    else
        echo -e "${GREEN}✅ ANDROID_HOME trovato: $ANDROID_HOME${NC}"
        
        cd android
        chmod +x gradlew
        
        if [ "$RELEASE" = true ]; then
            echo -e "${YELLOW}🔨 Building Release APK...${NC}"
            ./gradlew assembleRelease
            echo -e "${GREEN}✅ Release APK creato!${NC}"
            echo -e "${CYAN}📦 Percorso: android/app/build/outputs/apk/release/app-release.apk${NC}"
        else
            echo -e "${YELLOW}🔨 Building Debug APK...${NC}"
            ./gradlew assembleDebug
            echo -e "${GREEN}✅ Debug APK creato!${NC}"
            echo -e "${CYAN}📦 Percorso: android/app/build/outputs/apk/debug/app-debug.apk${NC}"
        fi
        
        cd ..
    fi
    echo ""
fi

# Build iOS
if [ "$PLATFORM" = "ios" ] || [ "$PLATFORM" = "both" ]; then
    echo -e "${YELLOW}🍎 Building iOS...${NC}"
    
    if [[ "$OSTYPE" != "darwin"* ]]; then
        echo -e "${YELLOW}⚠️  La build iOS richiede macOS e Xcode${NC}"
        echo -e "   Puoi comunque preparare il progetto per la build su Mac"
    else
        # Check if Xcode is installed
        if ! command -v xcodebuild &> /dev/null; then
            echo -e "${RED}❌ Xcode non trovato. Installa Xcode dall'App Store.${NC}"
        else
            echo -e "${GREEN}✅ Xcode trovato${NC}"
            
            # Install CocoaPods dependencies
            if [ -d "ios/App" ]; then
                echo -e "${YELLOW}📦 Installazione CocoaPods...${NC}"
                cd ios/App
                pod install
                cd ../..
                echo -e "${GREEN}✅ CocoaPods installato${NC}"
            fi
            
            echo -e "${YELLOW}🔨 Apertura progetto in Xcode...${NC}"
            npx cap open ios
            echo ""
            echo -e "${CYAN}📝 Per completare la build:${NC}"
            echo -e "   1. In Xcode, seleziona il tuo team di sviluppo"
            echo -e "   2. Seleziona un dispositivo o simulatore"
            echo -e "   3. Vai su Product > Archive per creare l'IPA"
        fi
    fi
    echo ""
fi

echo -e "${GREEN}✨ Build completata!${NC}"
echo ""
echo -e "${CYAN}📚 Per maggiori informazioni, consulta BUILD_MOBILE.md${NC}"
echo ""

# Summary
echo -e "${CYAN}📊 Riepilogo:${NC}"
echo -e "   - Web build: ✅ dist/"
if [ "$PLATFORM" = "android" ] || [ "$PLATFORM" = "both" ]; then
    echo -e "   - Android: ✅ android/"
fi
if [ "$PLATFORM" = "ios" ] || [ "$PLATFORM" = "both" ]; then
    echo -e "   - iOS: ✅ ios/"
fi
echo ""

echo -e "${CYAN}💡 Comandi utili:${NC}"
echo -e "   - Build Android: ./build-mobile.sh --platform android"
echo -e "   - Build iOS: ./build-mobile.sh --platform ios"
echo -e "   - Build entrambi: ./build-mobile.sh --platform both"
echo -e "   - Build Release: ./build-mobile.sh --platform android --release"
echo -e "   - Prima inizializzazione: ./build-mobile.sh --init"
echo ""
