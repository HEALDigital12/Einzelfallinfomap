RULES = {
    "weapon": ["messer", "stichwaffe", "schuss", "waffe"],
    "assault": ["koerperverletzung", "körperverletzung", "attacke"],
    "sexual": ["vergewaltigung", "sexualdelikt"],
    "robbery": ["raub", "ueberfall", "überfall"],
    "homicide": ["mord", "totschlag"]
}


def classify(text):
    value = (text or "").lower()
    for category, terms in RULES.items():
        for term in terms:
            if term in value:
                return category
    return None
