#!/usr/bin/env python3
"""
Zulip Attachment Cleanup Script
================================
Script per liberare spazio eliminando i file caricati su Zulip Cloud.

ISTRUZIONI PER GLI UTENTI:
1. Vai su Zulip → Impostazioni personali → API → Scarica il file zuliprc
2. Salva il file nella stessa cartella di questo script
3. Esegui: python zulip_cleanup_attachments.py

Nota: Questo script elimina SOLO i file caricati dall'utente corrente.
      I file ancora referenziati nei messaggi verranno eliminati automaticamente
      quando tutti i messaggi che li contengono saranno cancellati.
"""

import json
import os
import sys
from datetime import datetime
from configparser import ConfigParser

try:
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    print("[!] Errore: il modulo 'requests' non e' installato.")
    print("   Installa con: pip install requests")
    sys.exit(1)


def load_zuliprc(filepath="zuliprc"):
    """Carica le credenziali dal file zuliprc."""
    if not os.path.exists(filepath):
        print(f"[!] File '{filepath}' non trovato!")
        print("\n[*] Come ottenere il file zuliprc:")
        print("   1. Accedi a Zulip")
        print("   2. Vai su Impostazioni personali → Account & privacy")
        print("   3. Nella sezione 'API key', clicca 'Show/change your API key'")
        print("   4. Clicca 'Download .zuliprc'")
        print("   5. Salva il file nella stessa cartella di questo script")
        sys.exit(1)
    
    config = ConfigParser()
    config.read(filepath)
    
    try:
        return {
            "site": config.get("api", "site"),
            "email": config.get("api", "email"),
            "key": config.get("api", "key")
        }
    except Exception as e:
        print(f"[!] Errore nel parsing del file zuliprc: {e}")
        sys.exit(1)


def format_size(size_bytes):
    """Formatta la dimensione in formato leggibile."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def format_date(timestamp_ms):
    """Converte timestamp milliseconds in data leggibile."""
    return datetime.fromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M')


def get_attachments(credentials):
    """Recupera la lista degli attachment dell'utente."""
    url = f"{credentials['site']}/api/v1/attachments"
    
    response = requests.get(
        url,
        auth=(credentials['email'], credentials['key']),
        verify=False
    )
    
    if response.status_code != 200:
        print(f"[!] Errore API: {response.status_code}")
        print(response.text)
        sys.exit(1)
    
    return response.json()


def delete_attachment(credentials, attachment_id):
    """Elimina un singolo attachment."""
    url = f"{credentials['site']}/api/v1/attachments/{attachment_id}"
    
    response = requests.delete(
        url,
        auth=(credentials['email'], credentials['key']),
        verify=False
    )
    
    return response.json()


def main():
    print(r" _____  ____  ____  _   _ ____")
    print(r"|___ / |  _ \| __ )| \ | |__  /")
    print(r"  |_ \ | | | |  _ \|  \| | / / ")
    print(r" ___) || |_| | |_) | |\  |/ /_ ")
    print(r"|____/  \___/|____/|_| \_/____|")
    print()
    print("=" * 60)
    print("   ZULIP ATTACHMENT CLEANUP")
    print("   github.com/paboman/zulip-cleanup")
    print("=" * 60)
    print()
    
    # Cerca il file zuliprc
    zuliprc_path = "zuliprc"
    if not os.path.exists(zuliprc_path):
        zuliprc_path = os.path.expanduser("~/zuliprc")
    if not os.path.exists(zuliprc_path):
        zuliprc_path = os.path.expanduser("~/.zuliprc")
    
    credentials = load_zuliprc(zuliprc_path)
    print(f"[OK] Credenziali caricate per: {credentials['email']}")
    print(f"   Server: {credentials['site']}")
    print()
    
    # Recupera gli attachment
    print("[*] Recupero lista file caricati...")
    data = get_attachments(credentials)
    
    attachments = data.get("attachments", [])
    total_space = data.get("upload_space_used", 0)
    
    if not attachments:
        print("\n[OK] Nessun file caricato trovato. Lo storage e' gia' pulito!")
        return
    
    print(f"\nRIEPILOGO:")
    print(f"   File trovati: {len(attachments)}")
    print(f"   Spazio totale utilizzato: {format_size(total_space)}")
    print()
    
    # Mostra i file
    print("FILE CARICATI:")
    print("-" * 60)
    
    # Ordina per dimensione (più grandi prima)
    attachments_sorted = sorted(attachments, key=lambda x: x['size'], reverse=True)
    
    deletable = []
    referenced = []
    
    for att in attachments_sorted:
        size_str = format_size(att['size'])
        date_str = format_date(att['create_time'])
        msg_count = len(att.get('messages', []))
        
        status = "[REF]" if msg_count > 0 else "[DEL]"
        print(f"   {status} [{size_str:>10}] {att['name'][:40]:<40} ({date_str})")
        
        if msg_count > 0:
            print(f"      └─ Usato in {msg_count} messaggio/i (verrà eliminato con i messaggi)")
            referenced.append(att)
        else:
            deletable.append(att)
    
    print("-" * 60)
    print()
    print("Legenda: [DEL] = eliminabile subito | [REF] = ancora referenziato nei messaggi")
    print()
    
    # Calcola spazio recuperabile
    deletable_space = sum(att['size'] for att in deletable)
    referenced_space = sum(att['size'] for att in referenced)

    if deletable:
        print(f"[DEL] FILE ELIMINABILI SUBITO: {len(deletable)} ({format_size(deletable_space)})")
    if referenced:
        print(f"[REF] FILE REFERENZIATI NEI MESSAGGI: {len(referenced)} ({format_size(referenced_space)})")
    print()

    # Chiedi conferma
    print("[!] ATTENZIONE: L'eliminazione e' PERMANENTE e non puo' essere annullata!")
    if referenced:
        print("   I file referenziati verranno rimossi dallo storage ma i link nei messaggi rimarranno rotti.")
    print()

    while True:
        choice = input("Cosa vuoi fare?\n"
                      "  [A] Elimina TUTTI (inclusi quelli referenziati nei messaggi)\n"
                      + ("  [L] Elimina solo quelli LIBERI (non referenziati)\n" if deletable else "")
                      + "  [S] Seleziona singolarmente\n"
                      "  [Q] Esci senza eliminare\n"
                      "Scelta: ").strip().upper()

        if choice == 'Q':
            print("\nOperazione annullata.")
            return
        elif choice == 'A':
            to_delete = attachments_sorted
            break
        elif choice == 'L' and deletable:
            to_delete = deletable
            break
        elif choice == 'S':
            to_delete = []
            print("\nPer ogni file, premi [S] per saltare o [INVIO] per eliminare:")
            for att in attachments_sorted:
                msg_count = len(att.get('messages', []))
                tag = f" [referenziato in {msg_count} msg]" if msg_count > 0 else ""
                response = input(f"  {att['name'][:45]}{tag} ({format_size(att['size'])})? ").strip().upper()
                if response != 'S':
                    to_delete.append(att)
            break
        else:
            print("Scelta non valida. Riprova.\n")
    
    if not to_delete:
        print("\nNessun file selezionato per l'eliminazione.")
        return
    
    # Conferma finale
    delete_space = sum(att['size'] for att in to_delete)
    print(f"\nStai per eliminare {len(to_delete)} file ({format_size(delete_space)})")
    confirm = input("Confermi? [s/N]: ").strip().lower()
    
    if confirm != 's':
        print("\nOperazione annullata.")
        return

    # Elimina i file
    print("\n[*] Eliminazione in corso...")
    success = 0
    failed = 0
    
    for att in to_delete:
        result = delete_attachment(credentials, att['id'])
        if result.get('result') == 'success':
            print(f"   [OK] {att['name']}")
            success += 1
        else:
            print(f"   [!] {att['name']}: {result.get('msg', 'Errore sconosciuto')}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"COMPLETATO!")
    print(f"   File eliminati: {success}")
    if failed:
        print(f"   Errori: {failed}")
    print(f"   Spazio liberato: ~{format_size(delete_space)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
