#!/usr/bin/env python3
"""Ajoute à une table Airtable existante les champs manquants de la grille v2.

Les anciens champs (pm_Dose totale, pm_Fractionnement, pm_Technique,
pm_Hall. dosimétriques, pm_Terminologie) ne sont PAS supprimés : ils restent
pour l'historique et ne sont simplement plus remplis.

Usage :
    AIRTABLE_TOKEN=pat... python3 scripts/add_fields_v2.py            # table éval principale
    (voir aussi prepare_v2.py : sauvegarde + vidage + ajout des champs sur les 2 tables)
    AIRTABLE_TOKEN=pat... python3 scripts/add_fields_v2.py tblXXXXXXX # autre table
(Le token doit avoir le scope schema.bases:write.)
"""
import os, sys, requests
from airtable_fields_v2 import FIELDS_V2

TOKEN = os.environ.get("AIRTABLE_TOKEN", "")
BASE_ID = "appCpDq5UMLxZidBX"
TABLE_ID = sys.argv[1] if len(sys.argv) > 1 else "tbl0Qd1ZYN7OiwXj7"  # éval principale

if not TOKEN:
    sys.exit("Erreur : définissez AIRTABLE_TOKEN dans l'environnement")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

meta = requests.get(f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables", headers=HEADERS).json()
if "error" in meta:
    sys.exit(f"Erreur Airtable : {meta['error']}")
table = next((t for t in meta.get("tables", []) if t["id"] == TABLE_ID), None)
if not table:
    sys.exit(f"Table {TABLE_ID} introuvable dans la base {BASE_ID}")
existing = {f["name"] for f in table["fields"]}

url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables/{TABLE_ID}/fields"
ok = 0
for name, ftype, opts in FIELDS_V2:
    if name in existing:
        print(f"  ~  {name}  (déjà existant)"); ok += 1; continue
    body = {"name": name, "type": ftype}
    if opts:
        body["options"] = opts
    r = requests.post(url, headers=HEADERS, json=body)
    if r.status_code in (200, 201):
        print(f"  ✓  {name}"); ok += 1
    else:
        print(f"  ✗  {name}: {r.json().get('error', r.text)}")
print(f"\n{ok}/{len(FIELDS_V2)} champs OK dans {table['name']} ({TABLE_ID})")
