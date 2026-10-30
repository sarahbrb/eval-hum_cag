#!/usr/bin/env python3
"""Créer les champs Airtable pour la table eval_pilot_ghm."""
import requests, os, sys

TOKEN    = os.environ.get("AIRTABLE_TOKEN", "")
BASE_ID  = "appCpDq5UMLxZidBX"
TABLE_ID = "tblz9BkuQesGc4Yyr"  # eval_pilot_ghm

if not TOKEN:
    print("Usage : AIRTABLE_TOKEN=pat... python3 setup_ghm_table.py", file=sys.stderr)
    sys.exit(1)

HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

FIELDS = [
    ("cr_id",                              "singleLineText", None),
    ("statut",                             "singleLineText", None),
    ("pm_evaluateur",                      "singleLineText", None),
    ("pm_timestamp",                       "singleLineText", None),
    ("pm_Dose totale",                     "number",         {"precision": 0}),
    ("pm_Fractionnement",                  "number",         {"precision": 0}),
    ("pm_Technique",                       "number",         {"precision": 0}),
    ("pm_Hall. dosimétriques",             "number",         {"precision": 0}),
    ("pm_Terminologie",                    "number",         {"precision": 0}),
    ("pm_Correspondance profil → CR",      "number",         {"precision": 0}),
    ("pm_commentaire",                     "multilineText",  None),
    ("mr_evaluateur",                      "singleLineText", None),
    ("mr_timestamp",                       "singleLineText", None),
    ("mr_Volumes cibles",                  "number",         {"precision": 0}),
    ("mr_Chirurgie",                       "number",         {"precision": 0}),
    ("mr_Hormonothérapie",                 "number",         {"precision": 0}),
    ("mr_Hall. cliniques",                 "number",         {"precision": 0}),
    ("mr_Contradictions internes",         "number",         {"precision": 0}),
    ("mr_Indication / diagnostic",         "number",         {"precision": 0}),
    ("mr_Contexte thérapeutique",          "number",         {"precision": 0}),
    ("mr_Caractéristiques du traitement",  "number",         {"precision": 0}),
    ("mr_Toxicités (CTCAE)",               "number",         {"precision": 0}),
    ("mr_Bilan de fin",                    "number",         {"precision": 0}),
    ("mr_Suites thérapeutiques",           "number",         {"precision": 0}),
    ("mr_Organisation",                    "number",         {"precision": 0}),
    ("mr_Synthèse & Lisibilité",           "number",         {"precision": 0}),
    ("mr_Impression globale",              "number",         {"precision": 0}),
    ("mr_commentaire",                     "multilineText",  None),
]

url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables/{TABLE_ID}/fields"
ok = 0
for name, ftype, options in FIELDS:
    body = {"name": name, "type": ftype}
    if options:
        body["options"] = options
    r = requests.post(url, headers=HEADERS, json=body)
    if r.status_code in (200, 201):
        print(f"  ✓  {name}"); ok += 1
    else:
        err = r.json().get("error", {})
        if "DUPLICATE" in err.get("type","") or "already" in err.get("message","").lower():
            print(f"  ~  {name}  (déjà existant)"); ok += 1
        else:
            print(f"  ✗  {name}: {err.get('message', r.text)}")

print(f"\n{ok}/{len(FIELDS)} champs OK")
