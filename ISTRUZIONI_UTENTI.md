# Zulip - Pulizia File Caricati
---

## Cosa fa questo strumento?
Elimina i file che hai caricato su Zulip per liberare spazio nello storage dell'organizzazione.

---

## Istruzioni (segui i passi in ordine)

### PASSO 1 — Disattiva l'alias Python di Windows

Questo passo e' obbligatorio su Windows 11, anche se non hai mai installato Python.

Windows 11 include di default un alias che intercetta il comando `python` e apre il Microsoft Store invece di eseguire Python. Va disattivato prima di procedere.

1. Premi **Win + I** per aprire le Impostazioni
2. Vai su **App**
3. Clicca su **Advanced app settings** (Impostazioni avanzate app)
4. Clicca su **App execution aliases** (Alias di esecuzione app)
5. Trova `python.exe` e `python3.exe` e mettili entrambi su **OFF**

---

### PASSO 2 — Installa Python

Nella cartella trovi il file **`python-3.14.3-amd64.exe`**.

1. Fai **doppio clic** su `python-3.14.3-amd64.exe`
2. **IMPORTANTE:** nella prima schermata spunta la casella **"Add python.exe to PATH"** in basso
3. Clicca **Install Now** e segui l'installazione fino alla fine

> Se Python e' gia' installato sul tuo PC, salta questo passo.

---

### PASSO 3 — Scarica il tuo file zuliprc

Il file zuliprc contiene le tue credenziali per accedere a Zulip. Lo script ne ha bisogno per sapere chi sei.

1. Apri **Zulip** nel browser
2. Clicca sulla tua **icona profilo** in alto a destra
3. Vai su **Impostazioni personali**
4. Nel menu laterale clicca **Account & privacy**
5. Trova la sezione **"API key"** e clicca **Download .zuliprc**
6. Salva il file scaricato **in questa cartella** (dove si trova INSTALLA_E_AVVIA.bat)
7. Rinomina il file in `zuliprc` — esattamente cosi', senza punto iniziale e senza estensione

La cartella deve apparire cosi':
```
zulip_cleanup/
  ├── INSTALLA_E_AVVIA.bat          <- fai doppio clic qui per avviare
  ├── python-3.14.3-amd64.exe       <- installer Python
  ├── zulip_cleanup_attachments.py
  ├── zuliprc                       <- il file che hai appena scaricato
  └── ISTRUZIONI_UTENTI.md
```

---

### PASSO 4 — Avvia lo script

Fai **doppio clic** su **`INSTALLA_E_AVVIA.bat`**.

Lo script controlla le dipendenze e avvia la pulizia automaticamente.

---

## Come funziona la pulizia

Lo script mostra la lista dei tuoi file caricati e ti chiede cosa fare:

| Opzione | Cosa fa |
|---------|---------|
| **[A]** | Elimina TUTTI i file (anche quelli nei messaggi) |
| **[L]** | Elimina solo i file non collegati a messaggi |
| **[S]** | Scegli file per file cosa eliminare |
| **[Q]** | Esci senza eliminare nulla |

> ATTENZIONE: L'eliminazione e' **permanente**. Lo script chiede sempre conferma prima di procedere.

---

## Risoluzione problemi

| Problema | Soluzione |
|----------|-----------|
| La finestra si chiude subito | Completa il Passo 1 (disattiva alias Python) e riprova |
| "Python non trovato" | Reinstalla `python-3.14.3-amd64.exe` e spunta "Add python.exe to PATH" |
| "Manca il file zuliprc" | Assicurati che il file `zuliprc` sia nella stessa cartella |
| "Errore API: 401" | La API key non e' valida — scarica un nuovo file zuliprc |

---

## Sicurezza

- Il file `zuliprc` contiene la tua API key personale — **non condividerlo con nessuno**
- Lo script elimina **solo** i tuoi file, non quelli degli altri utenti
- Per una pulizia completa dell'organizzazione, ogni membro del team deve eseguire lo script con le proprie credenziali

---

