#!/usr/bin/env python3
"""
Script to disable code signing in Xcode project
"""
import re
import sys
from pathlib import Path

def disable_code_signing(project_path):
    """Disable code signing in the Xcode project file"""
    pbxproj_path = Path(project_path) / "project.pbxproj"
    
    if not pbxproj_path.exists():
        print(f"Error: {pbxproj_path} not found")
        sys.exit(1)
    
    print(f"Reading {pbxproj_path}")
    content = pbxproj_path.read_text(encoding='utf-8')
    
    # Replace CODE_SIGN_STYLE from Automatic to Manual
    content = re.sub(
        r'CODE_SIGN_STYLE = Automatic;',
        'CODE_SIGN_STYLE = Manual;',
        content
    )
    
    # Remove or empty DEVELOPMENT_TEAM
    content = re.sub(
        r'DEVELOPMENT_TEAM = [^;]*;',
        'DEVELOPMENT_TEAM = "";',
        content
    )
    
    # Add CODE_SIGNING_REQUIRED = NO if not present
    # Find buildSettings sections and add the setting
    def add_code_signing_not_required(match):
        settings = match.group(0)
        if 'CODE_SIGNING_REQUIRED' not in settings:
            # Add before the closing brace
            settings = settings.replace(
                '};',
                '\t\t\t\tCODE_SIGNING_REQUIRED = NO;\n\t\t\t\tCODE_SIGNING_ALLOWED = NO;\n\t\t\t};'
            )
        return settings
    
    content = re.sub(
        r'buildSettings = \{[^}]*\};',
        add_code_signing_not_required,
        content,
        flags=re.DOTALL
    )
    
    print(f"Writing modified content to {pbxproj_path}")
    pbxproj_path.write_text(content, encoding='utf-8')
    print("Code signing disabled successfully!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python disable_code_signing.py <path_to_xcodeproj>")
        sys.exit(1)
    
    disable_code_signing(sys.argv[1])
