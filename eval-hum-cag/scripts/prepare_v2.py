#!/usr/bin/env python3
"""Prépare Airtable pour la grille v2 : sauvegarde → vidage → ajout des nouveaux champs.

Pour chaque table (pilote GHM + évaluation principale) :
  1. sauvegarde de TOUS les enregistrements dans airtable_backups/<table>_<date>.json
  2. suppression de tous les enregistrements
  3. ajout des champs de la grille v2 qui manquent (les anciens champs sont conservés)

Usage (depuis eval-hum-cag/) :
    AIRTABLE_TOKEN=pat... python3 scripts/prepare_v2.py
Le token doit avoir les scopes data.records:read, data.records:write et schema.bases:write.
"""
import os, sys, json, datetime, requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from airtable_fields_v2 import FIELDS_V2

TOKEN = os.environ.get("AIRTABLE_TOKEN", "")
BASE_ID = "appCpDq5UMLxZidBX"
TABLES = {"pilote GHM": "tblz9BkuQesGc4Yyr", "évaluation principale": "tbl0Qd1ZYN7OiwXj7"}
if not TOKEN:
    sys.exit("Erreur : définissez AIRTABLE_TOKEN dans l'environnement")
H = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

import time
_raw = requests.request
def _req(method, url, **kw):
    """Requête avec nouvelles tentatives (proxy Jean Zay parfois capricieux)."""
    for i in range(6):
        try:
            r = _raw(method, url, timeout=30, **kw)
            time.sleep(0.25)  # limite Airtable : 5 requêtes / s
            if r.status_code == 429:
                time.sleep(30); continue
            return r
        except requests.exceptions.RequestException as e:
            print(f"    (réseau : {type(e).__name__}, nouvelle tentative dans {5*(i+1)} s)")
            time.sleep(5 * (i + 1))
    sys.exit("Échec réseau répété : relancez le script (il reprend là où il s'est arrêté).")
requests.get = lambda url, **kw: _req("GET", url, **kw)
requests.post = lambda url, **kw: _req("POST", url, **kw)
requests.delete = lambda url, **kw: _req("DELETE", url, **kw)

def fetch_all(tid):
    recs, offset = [], None
    while True:
        params = {"pageSize": 100}
        if offset: params["offset"] = offset
        d = requests.get(f"https://api.airtable.com/v0/{BASE_ID}/{tid}", headers=H, params=params).json()
        if "error" in d: sys.exit(f"Erreur Airtable ({tid}) : {d['error']}")
        recs += d.get("records", []); offset = d.get("offset")
        if not offset: return recs

def delete_all(tid, recs):
    ids = [r["id"] for r in recs]; n = 0
    for i in range(0, len(ids), 10):
        r = requests.delete(f"https://api.airtable.com/v0/{BASE_ID}/{tid}", headers=H,
                            params=[("records[]", x) for x in ids[i:i+10]])
        if r.status_code != 200: sys.exit(f"Erreur suppression : {r.text}")
        n += len(ids[i:i+10])
    return n

def add_fields(tid):
    # Lister les champs existants demande le scope schema.bases:read ; s'il manque,
    # on tente directement la création et on ignore les champs déjà présents.
    meta = requests.get(f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables", headers=H).json()
    existing = set()
    if "error" not in meta:
        table = next((t for t in meta.get("tables", []) if t["id"] == tid), None)
        existing = {f["name"] for f in table["fields"]} if table else set()
    added = 0
    for name, ftype, opts in FIELDS_V2:
        if name in existing: continue
        body = {"name": name, "type": ftype, **({"options": opts} if opts else {})}
        r = requests.post(f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables/{tid}/fields", headers=H, json=body)
        if r.status_code in (200, 201):
            added += 1; print(f"    + {name}")
            continue
        err = r.json().get("error", {})
        if "DUPLICATE" in str(err.get("type", "")) or "already exists" in str(err).lower():
            continue  # champ déjà présent
        sys.exit(f"Erreur ajout champ {name} : {err} (scope schema.bases:write et droits « créateur » sur la base ?)")
    return added

counts = {lbl: fetch_all(tid) for lbl, tid in TABLES.items()}
for lbl, recs in counts.items():
    print(f"  {lbl:<22} : {len(recs)} enregistrement(s)")
if input("\nSauvegarder puis SUPPRIMER tous ces enregistrements ? Tapez OUI : ").strip() != "OUI":
    sys.exit("Annulé.")

os.makedirs("airtable_backups", exist_ok=True)
stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
for lbl, tid in TABLES.items():
    recs = counts[lbl]
    path = f"airtable_backups/{tid}_{stamp}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(recs, f, ensure_ascii=False, indent=1)
    print(f"\n[{lbl}] sauvegarde : {path}")
    print(f"[{lbl}] supprimés  : {delete_all(tid, recs)}")
    print(f"[{lbl}] champs v2 ajoutés : {add_fields(tid)}")
print("\n✅ Airtable prêt pour la grille v2.")
