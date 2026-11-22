"""Group need statements into themes with BERTopic (decision D7)."""

from __future__ import annotations

import logging

import numpy as np

from . import embed

# BERTopic warns after manual topic reassignment; we don't reduce topics afterwards.
logging.getLogger("BERTopic").setLevel(logging.ERROR)

MIN_THEME_SIZE = 5  # Phase 2 exit: each top gap must link >= 5 real signals


def signal_text(sig: dict) -> str:
    return f"{sig['title']}. {sig['body'][:400]}".strip()


OUTLIER_THRESHOLD = 0.6  # min similarity for BERTopic to move an outlier into a theme


def find_themes(signals: list[dict], min_size: int = MIN_THEME_SIZE, seed: int = 42,
                outlier_threshold: float | None = OUTLIER_THRESHOLD) -> dict:
    """Cluster signals; returns themes (keywords, member ids, centroid) and outlier ids."""
    from bertopic import BERTopic
    from hdbscan import HDBSCAN
    from sklearn.feature_extraction.text import CountVectorizer
    from umap import UMAP

    docs = [signal_text(s) for s in signals]
    emb = embed.encode(docs)
    topic_model = BERTopic(
        embedding_model=embed.model(),
        umap_model=UMAP(n_neighbors=min(10, len(docs) - 1), n_components=5, min_dist=0.0,
                        metric="cosine", random_state=seed),
        hdbscan_model=HDBSCAN(min_cluster_size=min_size, min_samples=2, metric="euclidean",
                              cluster_selection_method="leaf", prediction_data=True),
        vectorizer_model=CountVectorizer(stop_words="english", ngram_range=(1, 2), min_df=2),
        min_topic_size=min_size,
    )
    topics, _ = topic_model.fit_transform(docs, emb)
    if outlier_threshold is not None and -1 in topics:
        # Reassign outliers only when they're clearly close to a theme (BERTopic built-in).
        topics = topic_model.reduce_outliers(docs, topics, strategy="embeddings",
                                             embeddings=emb, threshold=outlier_threshold)
        topic_model.update_topics(docs, topics=topics,
                                  vectorizer_model=topic_model.vectorizer_model)
    themes = []
    for tid in sorted(set(topics) - {-1}):
        idx = [i for i, t in enumerate(topics) if t == tid]
        centroid = emb[idx].mean(axis=0)
        centroid /= np.linalg.norm(centroid) or 1
        themes.append({
            "theme_id": int(tid),
            "keywords": [w for w, _ in topic_model.get_topic(tid)][:10],
            "signal_ids": [signals[i]["id"] for i in idx],
            "centroid": centroid.tolist(),
        })
    outliers = [signals[i]["id"] for i, t in enumerate(topics) if t == -1]
    return {"themes": themes, "outliers": outliers}


STABILITY_SEEDS = (7, 123, 2024)


def stability(theme_members: list[set[str]], other_runs: list[list[set[str]]]) -> list[float]:
    """Per theme: mean best-match Jaccard overlap with the themes of other runs (0..1).

    1.0 means the same signals form a theme whatever the random seed.
    """
    scores = []
    for members in theme_members:
        best = []
        for run in other_runs:
            best.append(max((len(members & o) / len(members | o) for o in run), default=0.0))
        scores.append(round(sum(best) / len(best), 2) if best else 1.0)
    return scores


def find_themes_with_stability(signals: list[dict], seed: int = 42,
                               other_seeds: tuple[int, ...] = STABILITY_SEEDS) -> dict:
    result = find_themes(signals, seed=seed)
    others = [[set(t["signal_ids"]) for t in find_themes(signals, seed=s)["themes"]]
              for s in other_seeds]
    scores = stability([set(t["signal_ids"]) for t in result["themes"]], others)
    for t, sc in zip(result["themes"], scores):
        t["stability"] = sc
    result["seeds"] = {"main": seed, "stability": list(other_seeds)}
    return result
