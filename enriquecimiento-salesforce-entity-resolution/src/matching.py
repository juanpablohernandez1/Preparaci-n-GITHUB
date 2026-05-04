from __future__ import annotations

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .text_normalize import clean_nit, normalize_company_name


def build_tfidf_index(corpus: pd.DataFrame):
    vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), min_df=1, max_features=50_000)
    X = vec.fit_transform(corpus["razon_social_norm"].fillna(""))
    return vec, X


def match_records(
    accounts: pd.DataFrame,
    corpus: pd.DataFrame,
    *,
    name_col: str,
    nit_col: str | None,
    threshold_auto: float = 0.85,
    threshold_review: float = 0.70,
) -> pd.DataFrame:
    """Devuelve un dataframe con columnas agregadas (sin escribir a Salesforce)."""

    corpus = corpus.copy()
    if "razon_social_norm" not in corpus.columns:
        corpus["razon_social_norm"] = corpus["razon_social"].map(normalize_company_name)

    vec, X = build_tfidf_index(corpus)
    nit_index = corpus.dropna(subset=["nit"]).set_index("nit").to_dict("index")

    rows = []
    for _, r in accounts.iterrows():
        name = str(r.get(name_col, "") or "")
        nit_raw = r.get(nit_col) if nit_col else None
        nit = (
            clean_nit(str(nit_raw).split("-")[0].strip())
            if nit_raw is not None and str(nit_raw).strip() != ""
            else None
        )

        method = "no_match"
        score = 0.0
        match: dict = {}

        if nit and nit in nit_index:
            method = "nit_exact"
            score = 1.0
            row = nit_index[nit]
            match = {
                "match_nit": row.get("nit"),
                "match_razon_social": row.get("razon_social"),
                "match_ciiu_code": row.get("ciiu_code"),
                "match_fuente": row.get("fuente"),
            }
        else:
            q = normalize_company_name(name)
            if q.strip():
                qv = vec.transform([q])
                sims = cosine_similarity(qv, X).flatten()
                best = float(sims.max())
                score = round(best, 4)
                if best >= threshold_auto:
                    method = "tfidf_auto"
                elif best >= threshold_review:
                    method = "tfidf_review"
                else:
                    method = "no_match"

                if method != "no_match":
                    idx = int(sims.argmax())
                    br = corpus.iloc[idx]
                    match = {
                        "match_nit": br.get("nit"),
                        "match_razon_social": br.get("razon_social"),
                        "match_ciiu_code": br.get("ciiu_code"),
                        "match_fuente": br.get("fuente"),
                    }

        out = {
            name_col: name,
            "match_method": method,
            "match_score": score,
            **match,
        }
        if nit_col:
            out[nit_col] = nit_raw
        rows.append(out)

    return pd.DataFrame(rows)
