import os, sys

token       = os.environ.get("AIRTABLE_TOKEN", "")
pilot_table = os.environ.get("PILOT_TABLE_ID", "")

if not token:
    print("Erreur : variable AIRTABLE_TOKEN manquante", file=sys.stderr)
    sys.exit(1)

# Production
with open("eval_main.html", "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace("%%AT_TOKEN%%", token)
with open("eval_main.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Token injecté dans eval_main.html")

# Pilote
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
    print("PILOT_TABLE_ID absent — fichiers pilote ignorés", file=sys.stderr)
