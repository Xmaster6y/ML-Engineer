"""
API constants.
"""

import pickle

# Dataset info
with open("api/models/tag_list.pkl", "rb") as f:
    TAG_LIST = pickle.load(f)
