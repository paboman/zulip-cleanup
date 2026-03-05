# Zulip Attachment Cleanup

Tool per liberare spazio eliminando i file caricati su Zulip Cloud.

---

## Cosa fa

Lo script si connette alla tua istanza Zulip tramite API, elenca tutti i file che hai caricato e ti permette di eliminarli selettivamente per recuperare spazio nello storage dell'organizzazione.

- Mostra dimensione, data e stato di ogni file (libero o referenziato in messaggi)
- Ordina i file per dimensione (i più grandi prima)
- Offre modalità di eliminazione: tutti, solo liberi, o selezione manuale
- Chiede sempre conferma prima di procedere

---

## Requisiti

- Python 3.x
- Modulo `requests` (installato automaticamente da `INSTALLA_E_AVVIA.bat`)
- File `zuliprc` con le tue credenziali API Zulip

---

## Utilizzo su Windows (metodo semplice)

1. **Disattiva l'alias Python di Windows** (obbligatorio su Windows 11):
   - Impostazioni → App → Advanced app settings → App execution aliases
   - Metti su **OFF** sia `python.exe` che `python3.exe`

2. **Scarica il file `zuliprc`** con le tue credenziali:
   - Zulip → Impostazioni personali → Account & privacy → API key → Download .zuliprc
   - Salva il file nella stessa cartella dello script
   - Rinominalo esattamente `zuliprc` (senza punto iniziale, senza estensione)

3. **Fai doppio clic su `INSTALLA_E_AVVIA.bat`**

   Il batch installa Python e le dipendenze automaticamente se necessario, poi avvia lo script.

---

## Utilizzo da riga di comando

```bash
pip install requests
python zulip_cleanup_attachments.py
```

---

## Opzioni di pulizia

| Opzione | Cosa fa |
|---------|---------|
| **[A]** | Elimina tutti i file (anche quelli referenziati nei messaggi) |
| **[L]** | Elimina solo i file non collegati a messaggi |
| **[S]** | Selezione manuale file per file |
| **[Q]** | Esci senza eliminare nulla |

> **Attenzione:** l'eliminazione è permanente. I link nei messaggi che puntano a file eliminati risulteranno rotti.

---

## Sicurezza

- Il file `zuliprc` contiene la tua API key personale — **non condividerlo mai**
- Lo script elimina **solo** i file dell'utente autenticato
- Per una pulizia completa dell'organizzazione, ogni membro deve eseguire lo script con le proprie credenziali

---

## Struttura del progetto

```
zulip_cleanup/
  ├── zulip_cleanup_attachments.py   # script principale
  ├── INSTALLA_E_AVVIA.bat           # launcher Windows
  ├── ISTRUZIONI_UTENTI.md           # guida dettagliata per utenti non tecnici
  └── zuliprc                        # credenziali API (non incluso nel repo)
```
