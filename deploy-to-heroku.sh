#!/bin/bash

# Deploy SynerChat to Heroku with Mobile Apps
# Questo script crea le app e le deploya su Heroku

set -e

HEROKU_APP=""
SKIP_BUILD=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --app)
            HEROKU_APP="$2"
            shift 2
            ;;
        --skip-build)
            SKIP_BUILD=true
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

echo -e "${CYAN}🚀 Deploy SynerChat to Heroku${NC}"
echo -e "${CYAN}==============================${NC}"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git non trovato. Installa Git prima di continuare.${NC}"
    exit 1
fi

# Check if heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo -e "${RED}❌ Heroku CLI non trovato. Installa da: https://devcenter.heroku.com/articles/heroku-cli${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Git e Heroku CLI trovati${NC}"
echo ""

# Get Heroku app name
if [ -z "$HEROKU_APP" ]; then
    echo -e "${YELLOW}🔍 Cerco il nome dell'app Heroku...${NC}"
    HEROKU_REMOTE=$(git remote -v | grep heroku | head -n 1)
    
    if [ -n "$HEROKU_REMOTE" ]; then
        HEROKU_APP=$(echo "$HEROKU_REMOTE" | sed 's/.*heroku.com[:/]\(.*\)\.git.*/\1/')
        echo -e "${GREEN}✅ App Heroku trovata: $HEROKU_APP${NC}"
    else
        echo -e "${YELLOW}⚠️  Nessun remote Heroku trovato${NC}"
        read -p "Inserisci il nome della tua app Heroku: " HEROKU_APP
    fi
fi

echo ""
echo -e "${CYAN}📱 App Heroku: $HEROKU_APP${NC}"
echo ""

# Build mobile apps if not skipped
if [ "$SKIP_BUILD" = false ]; then
    echo -e "${YELLOW}🏗️  Building mobile apps...${NC}"
    echo ""
    
    # Run build script
    if [ -f "./build-and-deploy-apps.sh" ]; then
        chmod +x ./build-and-deploy-apps.sh
        ./build-and-deploy-apps.sh
    else
        echo -e "${YELLOW}⚠️  Script di build non trovato, salto questo step${NC}"
    fi
    
    echo ""
fi

# Check if APK exists
APK_PATH="app/backend/downloads/synerchat.apk"
if [ -f "$APK_PATH" ]; then
    APK_SIZE=$(du -h "$APK_PATH" | cut -f1)
    echo -e "${GREEN}✅ APK trovato: $APK_SIZE${NC}"
else
    echo -e "${YELLOW}⚠️  APK non trovato in $APK_PATH${NC}"
    echo -e "   L'app sarà deployata senza APK Android"
fi

# Check if IPA exists
IPA_PATH="app/backend/downloads/synerchat.ipa"
if [ -f "$IPA_PATH" ]; then
    IPA_SIZE=$(du -h "$IPA_PATH" | cut -f1)
    echo -e "${GREEN}✅ IPA trovato: $IPA_SIZE${NC}"
else
    echo -e "${YELLOW}⚠️  IPA non trovato in $IPA_PATH${NC}"
    echo -e "   L'app sarà deployata senza IPA iOS"
fi

echo ""

# Git status
echo -e "${YELLOW}📝 Preparazione commit...${NC}"

# Add files
git add .

# Check if there are changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${GREEN}✅ Modifiche trovate, creo commit...${NC}"
    
    # Commit
    COMMIT_MESSAGE="Deploy: Update mobile apps and sync improvements"
    git commit -m "$COMMIT_MESSAGE"
    
    echo -e "${GREEN}✅ Commit creato: $COMMIT_MESSAGE${NC}"
else
    echo -e "${CYAN}ℹ️  Nessuna modifica da committare${NC}"
fi

echo ""

# Push to Heroku
echo -e "${CYAN}🚀 Deploy su Heroku...${NC}"
echo ""

git push heroku main

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✨ Deploy completato con successo!${NC}"
    echo ""
    echo -e "${CYAN}🌐 La tua app è disponibile su:${NC}"
    echo -e "   https://$HEROKU_APP.herokuapp.com"
    echo ""
    echo -e "${CYAN}📱 Download links:${NC}"
    echo -e "   Android: https://$HEROKU_APP.herokuapp.com/downloads/synerchat.apk"
    echo -e "   iOS: https://$HEROKU_APP.herokuapp.com/downloads/synerchat.ipa"
    echo ""
    echo -e "${GREEN}👥 Gli utenti possono scaricare le app dalla pagina di login!${NC}"
    echo ""
    
    # Open app in browser
    read -p "Vuoi aprire l'app nel browser? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v xdg-open &> /dev/null; then
            xdg-open "https://$HEROKU_APP.herokuapp.com"
        elif command -v open &> /dev/null; then
            open "https://$HEROKU_APP.herokuapp.com"
        fi
    fi
else
    echo ""
    echo -e "${RED}❌ Deploy fallito${NC}"
    echo ""
    echo -e "${YELLOW}🔍 Controlla i log con:${NC}"
    echo -e "   heroku logs --tail -a $HEROKU_APP"
    echo ""
    exit 1
fi

echo ""
echo -e "${CYAN}💡 Comandi utili:${NC}"
echo -e "   heroku logs --tail -a $HEROKU_APP    # Vedi i log"
echo -e "   heroku open -a $HEROKU_APP           # Apri app nel browser"
echo -e "   heroku restart -a $HEROKU_APP        # Riavvia app"
echo ""
