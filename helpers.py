def load_knowledge():
    with open("rules.txt", "r", encoding="utf-8") as f:
        return f.read()