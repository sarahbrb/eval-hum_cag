"""Liste des champs Airtable — grille d'évaluation v2 (révision des critères PM, nov. 2026).

Codage :
  * questions Oui/Non  → 1 = Oui, 0 = Non
  * échelles 1–4       → 1..4, champ vide = N/A (y compris N/A automatique
                          quand la question parente a reçu « Non »)
"""

NUM = {"precision": 0}

COMMON_HEAD = [
    ("cr_id",          "singleLineText", None),
    ("statut",         "singleLineText", None),
    ("pm_evaluateur",  "singleLineText", None),
    ("pm_timestamp",   "singleLineText", None),
]

# Nouveaux champs PM (grille v2)
PM_FIELDS_V2 = [
    ("pm_Prescription - dose par volume",      "number", NUM),  # Oui/Non
    ("pm_Prescription - cohérence",            "number", NUM),
    ("pm_Étalement - mentionné",               "number", NUM),  # Oui/Non
    ("pm_Étalement - cohérence",               "number", NUM),
    ("pm_OAR - mentionnées",                   "number", NUM),  # Oui/Non
    ("pm_OAR - cohérence",                     "number", NUM),
    ("pm_Technique - technique dosimétrique",  "number", NUM),  # Oui/Non
    ("pm_Technique - nature faisceaux",        "number", NUM),  # Oui/Non
    ("pm_Technique - énergie",                 "number", NUM),  # Oui/Non
    ("pm_Technique - cohérence",               "number", NUM),
    ("pm_Justesse des termes techniques",      "number", NUM),
    ("pm_Correspondance profil → CR",          "number", NUM),
    ("pm_commentaire",                         "multilineText", None),
]

MR_FIELDS = [
    ("mr_evaluateur",                      "singleLineText", None),
    ("mr_timestamp",                       "singleLineText", None),
    ("mr_Volumes cibles",                  "number", NUM),
    ("mr_Chirurgie",                       "number", NUM),
    ("mr_Hormonothérapie",                 "number", NUM),
    ("mr_Hall. cliniques",                 "number", NUM),
    ("mr_Contradictions internes",         "number", NUM),
    ("mr_Indication / diagnostic",         "number", NUM),
    ("mr_Contexte thérapeutique",          "number", NUM),
    ("mr_Caractéristiques du traitement",  "number", NUM),
    ("mr_Toxicités (CTCAE)",               "number", NUM),
    ("mr_Bilan de fin",                    "number", NUM),
    ("mr_Suites thérapeutiques",           "number", NUM),
    ("mr_Organisation",                    "number", NUM),
    ("mr_Synthèse & Lisibilité",           "number", NUM),
    ("mr_Impression globale",              "number", NUM),
    ("mr_commentaire",                     "multilineText", None),
]

FIELDS_V2 = COMMON_HEAD + PM_FIELDS_V2 + MR_FIELDS


def as_api(fields):
    out = []
    for name, ftype, opts in fields:
        f = {"name": name, "type": ftype}
        if opts:
            f["options"] = opts
        out.append(f)
    return out
