# Zulip Attachment Cleanup

A command-line tool to free up storage space by deleting files you uploaded to Zulip Cloud.

---

## What it does

The script connects to your Zulip instance via API, lists all files you have uploaded, and lets you selectively delete them to recover storage space in your organization.

- Shows size, date and status of each file (free or still referenced in messages)
- Sorts files by size (largest first)
- Offers deletion modes: all, only unreferenced, or manual selection
- Always asks for confirmation before proceeding

---

## Requirements

- Python 3.x
- `requests` module (auto-installed by `INSTALLA_E_AVVIA.bat` on Windows)
- A `zuliprc` file with your Zulip API credentials

---

## Usage

### Command line (all platforms)

```bash
pip install requests
python zulip_cleanup_attachments.py
```

### Windows (easy launcher)

1. **Disable the Windows Python alias** (required on Windows 11):
   - Settings → Apps → Advanced app settings → App execution aliases
   - Turn **OFF** both `python.exe` and `python3.exe`

2. **Download your `zuliprc`** credentials file:
   - Zulip → Personal settings → Account & privacy → API key → Download .zuliprc
   - Save the file in the same folder as the script
   - Rename it exactly `zuliprc` (no leading dot, no extension)

3. **Double-click `INSTALLA_E_AVVIA.bat`**

   The launcher installs Python and dependencies automatically if needed, then runs the script.

---

## Deletion options

| Option | Action |
|--------|--------|
| **[A]** | Delete all files (including those referenced in messages) |
| **[L]** | Delete only files not linked to any message |
| **[S]** | Select files one by one |
| **[Q]** | Quit without deleting anything |

> **Warning:** deletion is permanent. Message links pointing to deleted files will break.

---

## Security

- The `zuliprc` file contains your personal API key — **never share it**
- The script only deletes files belonging to the authenticated user
- For a full organization cleanup, each member must run the script with their own credentials

---

## Project structure

```
zulip_cleanup/
  ├── zulip_cleanup_attachments.py   # main script
  ├── INSTALLA_E_AVVIA.bat           # Windows launcher
  ├── ISTRUZIONI_UTENTI.md           # detailed guide in Italian for non-technical users
  └── zuliprc                        # API credentials (not included in repo)
```
