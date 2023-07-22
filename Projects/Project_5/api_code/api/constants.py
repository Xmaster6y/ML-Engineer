"""
API constants.
"""

import os
import pickle

# Dataset info
with open("api/models/tag_list.pkl", "rb") as f:
    TAG_LIST = pickle.load(f)

APP_ENV = os.environ.get("APP_ENV", "unknown")
