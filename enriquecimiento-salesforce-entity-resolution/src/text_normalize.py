import re
import unicodedata

STOPWORDS = {
    "sas", "sa", "ltda", "cia", "compania", "compañia",
    "de", "la", "el", "los", "las", "y", "e", "en", "del",
    "un", "una", "por", "con", "para", "al", "su", "sus",
    "colombia", "col",
}


def remove_accents(text: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


def normalize_company_name(text: str) -> str:
    if not text or not isinstance(text, str):
        return ""
    t = text.lower().strip()
    t = remove_accents(t)
    t = re.sub(r"[^\w\s]", " ", t)
    tokens = [tok for tok in t.split() if tok not in STOPWORDS and len(tok) > 1]
    return " ".join(tokens)


def clean_nit(value) -> str | None:
    if value is None:
        return None
    s = re.sub(r"[^\d]", "", str(value))
    return s.zfill(9) if s else None
