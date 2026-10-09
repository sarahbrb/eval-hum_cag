import os, sys

token = os.environ.get("AIRTABLE_TOKEN", "")
if not token:
    print("Erreur : variable AIRTABLE_TOKEN manquante", file=sys.stderr)
    sys.exit(1)

for filename in ["eval_main.html", "eval_pilot.html"]:
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("%%AT_TOKEN%%", token)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Token injecté dans {filename}")
