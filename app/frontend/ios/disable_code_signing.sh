#!/bin/bash

# Navigate to the iOS project directory
cd "$(dirname "$0")"

# Update project.pbxproj to disable code signing
sed -i '' 's/CODE_SIGN_STYLE = Automatic;/CODE_SIGN_STYLE = Manual;/g' App.xcodeproj/project.pbxproj
sed -i '' 's/DEVELOPMENT_TEAM = \(.*\);/DEVELOPMENT_TEAM = "";/g' App.xcodeproj/project.pbxproj

# Ensure the script is executable
chmod +x disable_code_signing.sh
