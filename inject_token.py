import os, sys

token       = os.environ.get("AIRTABLE_TOKEN", "")
pilot_table = os.environ.get("PILOT_TABLE_ID", "")
ghm_table   = os.environ.get("GHM_TABLE_ID", "")

if not token:
    print("Erreur : variable AIRTABLE_TOKEN manquante", file=sys.stderr)
    sys.exit(1)

# ── Évaluation principale ──────────────────────────────────────────
with open("eval_main/index.html", "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace("%%AT_TOKEN%%", token)
with open("eval_main/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Token injecté dans eval_main/index.html")

# ── Phase pilote labo (Diandra / Markarit / Lisa) ─────────────────
if pilot_table:
    for fname in ["pilot/index.html", "pilot/resultats.html"]:
        with open(fname, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("%%AT_TOKEN%%", token)
        content = content.replace("%%PILOT_TABLE_ID%%", pilot_table)
        with open(fname, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Token + PILOT_TABLE_ID injectés dans {fname}")
else:
    print("PILOT_TABLE_ID absent — fichiers pilot/ ignorés", file=sys.stderr)

# ── Phase pilote GHM (4 PM + 2 MR cliniciens) ────────────────────
if ghm_table:
    with open("pilot_ghm/index.html", "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("%%AT_TOKEN%%", token)
    content = content.replace("%%GHM_TABLE_ID%%", ghm_table)
    with open("pilot_ghm/index.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("Token + GHM_TABLE_ID injectés dans pilot_ghm/index.html")
else:
    print("GHM_TABLE_ID absent — pilot_ghm/ ignoré", file=sys.stderr)
