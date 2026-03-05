@echo off
chcp 65001 >nul
title Zulip Cleanup - 3DBNZ

echo.
echo ============================================================
echo    ZULIP ATTACHMENT CLEANUP
echo ============================================================
echo.

:: STEP 1: Controlla se Python e' installato
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python non trovato sul tuo PC.
    echo.
    echo [*] Avvio installazione automatica...
    echo     Potrebbe apparire una richiesta di autorizzazione Windows: clicca Si.
    echo.
    "%~dp0python-3.14.3-amd64.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
    if errorlevel 1 (
        echo.
        echo [!] Installazione automatica fallita.
        echo     Prova a fare doppio clic su: python-3.14.3-amd64.exe
        echo     Segui l'installazione e spunta "Add python.exe to PATH".
        echo     Poi riavvia questo script.
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [OK] Python installato con successo!
    echo.
    echo ============================================================
    echo  IMPORTANTE: chiudi questa finestra e fai doppio clic
    echo  di nuovo su INSTALLA_E_AVVIA.bat per continuare.
    echo ============================================================
    echo.
    pause
    exit /b 0
)

echo [OK] Python trovato sul tuo PC.
echo.
echo     Lo script controllera le dipendenze e avviera la pulizia.
echo.

:: STEP 2: Installa requests se mancante
echo [*] Controllo dipendenze...
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo [*] Installazione modulo requests in corso...
    python -m pip install requests --quiet
    if errorlevel 1 (
        echo.
        echo [!] Errore durante l'installazione di requests.
        echo     Prova a eseguire manualmente: pip install requests
        echo.
        pause
        exit /b 1
    )
    echo [OK] Modulo requests installato.
) else (
    echo [OK] Dipendenze ok.
)
echo.

:: STEP 3: Controlla che zuliprc esista
if not exist "%~dp0zuliprc" (
    echo [!] Manca il file con le tue credenziali Zulip ^(zuliprc^).
    echo.
    echo     Segui questi passi per scaricarlo:
    echo.
    echo     1. Apri Zulip nel browser
    echo     2. Clicca sulla tua foto/icona profilo in alto a destra
    echo     3. Vai su "Impostazioni personali"
    echo     4. Nel menu a sinistra clicca "Account e privacy"
    echo     5. Trova la sezione "API key" e clicca "Download .zuliprc"
    echo.
    echo     Poi salva il file scaricato QUI:
    echo     %~dp0
    echo.
    echo     IMPORTANTE: rinomina il file esattamente cosi':  zuliprc
    echo     ^(togli il punto iniziale se c'e', e togli qualsiasi estensione come .txt^)
    echo.
    echo     Quando hai salvato il file in quella cartella,
    echo     fai doppio clic di nuovo su INSTALLA_E_AVVIA.bat per riprendere.
    echo.
    pause
    exit /b 1
)

echo [OK] File zuliprc trovato.
echo.
echo ============================================================
echo.

:: STEP 4: Avvia lo script
cd /d "%~dp0"
python zulip_cleanup_attachments.py

echo.
pause
