"""
Supervised module constants.
"""

# Model info
ALL_MODELS = {
    "default": {
        "model_name": "lr_50",
        "model_type": "sklearn",
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "embedding_type": "sentence_transformers",
        "embed_targets": ["title"],
        "n_tag": 50,
    },
    "lr_50": {
        "model_name": "lr_50",
        "model_type": "sklearn",
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "embedding_type": "sentence_transformers",
        "embed_targets": ["title"],
        "n_tag": 50,
    },
    "lr_20": {
        "model_name": "lr_20",
        "model_type": "sklearn",
        "embedding_model": "sentence-transformers/all-mpnet-base-v2",
        "embedding_type": "sentence_transformers",
        "embed_targets": ["title", "body_code"],
        "n_tag": 20,
    },
}

LENGTH_LIMIT = 1000
