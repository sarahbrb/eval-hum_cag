#!/usr/bin/env python3
"""Supprime TOUS les enregistrements de la table Airtable CAG."""
import os, sys, requests

TOKEN   = os.environ.get("AIRTABLE_TOKEN", "")
BASE_ID = "appCpDq5UMLxZidBX"
TABLE_ID= "tbl0Qd1ZYN7OiwXj7"
URL     = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

if not TOKEN:
    print("Erreur : définissez AIRTABLE_TOKEN dans l'environnement", file=sys.stderr)
    sys.exit(1)

# 1. Récupérer tous les IDs
ids = []
offset = None
while True:
    params = {"fields[]": "cr_id", "pageSize": 100}
    if offset:
        params["offset"] = offset
    r = requests.get(URL, headers=HEADERS, params=params)
    data = r.json()
    if "error" in data:
        print(f"Erreur Airtable : {data['error']} — vérifiez votre token.", file=sys.stderr)
        sys.exit(1)
    ids += [rec["id"] for rec in data.get("records", [])]
    offset = data.get("offset")
    if not offset:
        break

if not ids:
    print("La table est déjà vide.")
    sys.exit(0)

print(f"{len(ids)} enregistrement(s) trouvé(s). Suppression en cours…")

# 2. Supprimer par lots de 10 (limite Airtable)
deleted = 0
for i in range(0, len(ids), 10):
    batch = ids[i:i+10]
    params = [("records[]", rid) for rid in batch]
    r = requests.delete(URL, headers=HEADERS, params=params)
    if r.status_code == 200:
        deleted += len(batch)
        print(f"  ✓ {deleted}/{len(ids)} supprimés")
    else:
        print(f"  ✗ Erreur : {r.text}", file=sys.stderr)

print(f"\nTerminé. {deleted}/{len(ids)} enregistrements supprimés.")
