#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de création des champs Airtable pour le projet CAG.
À exécuter UNE SEULE FOIS après avoir ajouté le scope 'schema.bases:write'
à votre token Airtable.

Instructions :
  1. Allez sur https://airtable.com/create/tokens
  2. Cliquez sur votre token 'cag-eval'
  3. Sous "Scopes", ajoutez  schema.bases:write
  4. Sauvegardez, puis exécutez :  python3 setup_airtable.py
"""
import requests

TOKEN  = ""  # Définir via : export AIRTABLE_TOKEN="pat..."
BASE_ID  = "appCpDq5UMLxZidBX"
TABLE_ID = "tbl0Qd1ZYN7OiwXj7"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# (nom, type, options)
FIELDS = [
    ("cr_id",                              "singleLineText", None),
    ("statut",                             "singleLineText", None),
    ("pm_evaluateur",                      "singleLineText", None),
    ("pm_timestamp",                       "singleLineText", None),
    ("pm_Dose totale",                     "number",         {"precision": 0}),
    ("pm_Fractionnement",                  "number",         {"precision": 0}),
    ("pm_Technique",                       "number",         {"precision": 0}),
    ("pm_Hall. dosimétriques",             "number",         {"precision": 0}),
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
    ("mr_Terminologie",                    "number",         {"precision": 0}),
    ("mr_Lisibilité & style",              "number",         {"precision": 0}),
    ("mr_Organisation",                    "number",         {"precision": 0}),
    ("mr_Synthèse",                        "number",         {"precision": 0}),
    ("pm_Correspondance profil → CR",      "number",         {"precision": 0}),
    ("mr_commentaire",                     "multilineText",  None),
]

url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables/{TABLE_ID}/fields"

print("Création des champs Airtable...\n")
ok = 0
for name, ftype, options in FIELDS:
    body = {"name": name, "type": ftype}
    if options:
        body["options"] = options
    r = requests.post(url, headers=HEADERS, json=body)
    if r.status_code in (200, 201):
        print(f"  ✓  {name}")
        ok += 1
    else:
        err = r.json().get("error", {})
        etype = err.get("type", "")
        msg   = err.get("message", r.text)
        if "DUPLICATE_FIELD" in etype or "already exists" in msg.lower():
            print(f"  ~  {name}  (déjà existant)")
            ok += 1
        else:
            print(f"  ✗  {name}: {msg}")

print(f"\n{ok}/{len(FIELDS)} champs traités avec succès.")
if ok == len(FIELDS):
    print("\nTable Airtable prête ✅  Vous pouvez maintenant tester l'interface.")
else:
    print("\nCorriger les erreurs ci-dessus, puis relancer le script.")
