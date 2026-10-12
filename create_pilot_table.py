#!/usr/bin/env python3
"""Crée la table Airtable pour la phase pilote CAG et affiche son ID."""
import os, sys, requests, json

TOKEN   = os.environ.get("AIRTABLE_TOKEN", "")
BASE_ID = "appCpDq5UMLxZidBX"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

if not TOKEN:
    print("Erreur : définissez AIRTABLE_TOKEN dans l'environnement", file=sys.stderr)
    sys.exit(1)

FIELDS = [
    {"name": "cr_id",                             "type": "singleLineText"},
    {"name": "statut",                            "type": "singleLineText"},
    {"name": "pm_evaluateur",                     "type": "singleLineText"},
    {"name": "pm_timestamp",                      "type": "singleLineText"},
    {"name": "pm_Dose totale",                    "type": "number", "options": {"precision": 0}},
    {"name": "pm_Fractionnement",                 "type": "number", "options": {"precision": 0}},
    {"name": "pm_Technique",                      "type": "number", "options": {"precision": 0}},
    {"name": "pm_Hall. dosimétriques",            "type": "number", "options": {"precision": 0}},
    {"name": "pm_Terminologie",                   "type": "number", "options": {"precision": 0}},
    {"name": "pm_commentaire",                    "type": "multilineText"},
    {"name": "mr_evaluateur",                     "type": "singleLineText"},
    {"name": "mr_timestamp",                      "type": "singleLineText"},
    {"name": "mr_Volumes cibles",                 "type": "number", "options": {"precision": 0}},
    {"name": "mr_Chirurgie",                      "type": "number", "options": {"precision": 0}},
    {"name": "mr_Hormonothérapie",                "type": "number", "options": {"precision": 0}},
    {"name": "mr_Hall. cliniques",                "type": "number", "options": {"precision": 0}},
    {"name": "mr_Contradictions internes",        "type": "number", "options": {"precision": 0}},
    {"name": "mr_Indication / diagnostic",        "type": "number", "options": {"precision": 0}},
    {"name": "mr_Contexte thérapeutique",         "type": "number", "options": {"precision": 0}},
    {"name": "mr_Caractéristiques du traitement", "type": "number", "options": {"precision": 0}},
    {"name": "mr_Toxicités (CTCAE)",              "type": "number", "options": {"precision": 0}},
    {"name": "mr_Bilan de fin",                   "type": "number", "options": {"precision": 0}},
    {"name": "mr_Suites thérapeutiques",          "type": "number", "options": {"precision": 0}},
    {"name": "mr_Organisation",                   "type": "number", "options": {"precision": 0}},
    {"name": "mr_Synthèse & Lisibilité",          "type": "number", "options": {"precision": 0}},
    {"name": "mr_Correspondance profil → CR",     "type": "number", "options": {"precision": 0}},
    {"name": "mr_Impression globale",             "type": "number", "options": {"precision": 0}},
    {"name": "mr_commentaire",                    "type": "multilineText"},
]

url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
body = {"name": "CAG_Evaluation_Pilot", "fields": FIELDS}

print("Création de la table CAG_Evaluation_Pilot…")
r = requests.post(url, headers=HEADERS, json=body)

if r.status_code in (200, 201):
    table_id = r.json()["id"]
    print(f"\n✅ Table créée avec succès !")
    print(f"\nPILOT_TABLE_ID = {table_id}")
    print(f"\n→ Ajoutez ce secret GitHub : PILOT_TABLE_ID = {table_id}")
else:
    data = r.json()
    err = data.get("error", {})
    if err.get("type") == "TABLE_NAME_CONFLICT" or "already exists" in str(err).lower():
        # Table existe déjà, récupérer son ID
        print("Table déjà existante. Recherche de son ID…")
        r2 = requests.get(url, headers=HEADERS)
        tables = r2.json().get("tables", [])
        for t in tables:
            if t["name"] == "CAG_Evaluation_Pilot":
                print(f"\n✅ Table trouvée !")
                print(f"\nPILOT_TABLE_ID = {t['id']}")
                print(f"\n→ Ajoutez ce secret GitHub : PILOT_TABLE_ID = {t['id']}")
                sys.exit(0)
        print("Erreur : table introuvable après conflit de nom.", file=sys.stderr)
    else:
        print(f"\n✗ Erreur : {json.dumps(data, ensure_ascii=False, indent=2)}", file=sys.stderr)
        print("\nVérifiez que votre token a le scope 'schema.bases:write'.", file=sys.stderr)
        sys.exit(1)
