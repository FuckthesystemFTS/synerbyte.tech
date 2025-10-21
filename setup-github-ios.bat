@echo off
echo ========================================
echo Setup GitHub Actions per iOS Build
echo ========================================
echo.

cd C:\Users\Hp\Desktop\SYNERCHAT

echo [1/4] Aggiungo file al repository...
git add .

echo [2/4] Creo commit...
git commit -m "Add GitHub Actions workflow for iOS build"

echo [3/4] Verifico remote GitHub...
git remote -v

echo.
echo ========================================
echo PROSSIMI PASSI:
echo ========================================
echo.
echo 1. Se NON hai un repository GitHub, crealo su:
echo    https://github.com/new
echo.
echo 2. Collega il repository:
echo    git remote add origin https://github.com/TUO_USERNAME/synerchat.git
echo.
echo 3. Push su GitHub:
echo    git push -u origin main
echo.
echo 4. Vai su GitHub ^> Actions ^> Build iOS App ^> Run workflow
echo.
echo 5. Aspetta 10-15 minuti
echo.
echo 6. Scarica l'IPA dagli Artifacts
echo.
echo ========================================
pause
