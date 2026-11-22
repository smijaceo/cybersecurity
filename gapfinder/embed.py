"""Sentence embeddings via model2vec static models (numpy only, no PyTorch).

Decision D9: BERTopic's default backend pulls in PyTorch (several GB per session);
model2vec is a supported BERTopic backend with a ~30 MB model.
"""

from __future__ import annotations

import os
from functools import lru_cache

import numpy as np

MODEL = "minishlab/potion-base-8M"            # clustering need statements
RETRIEVAL_MODEL = "minishlab/potion-retrieval-32M"  # shortlisting ATT&CK candidates

# Hugging Face's Xet transfer client needs extra hosts; plain HTTPS downloads work
# through the hosts allowed on the environment (huggingface.co, us.aws.cdn.hf.co).
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")


@lru_cache(maxsize=2)
def model(name: str = MODEL):
    from model2vec import StaticModel

    return StaticModel.from_pretrained(name)


def encode(texts: list[str], model_name: str = MODEL) -> np.ndarray:
    """L2-normalised embeddings, so a dot product is cosine similarity."""
    m = model(model_name)
    if not texts:
        return np.zeros((0, m.dim), dtype=np.float32)
    e = np.asarray(m.encode(texts), dtype=np.float32)
    norms = np.linalg.norm(e, axis=1, keepdims=True)
    return e / np.where(norms == 0, 1, norms)
