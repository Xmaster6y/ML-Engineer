"""
Script to resolve the models in the json files.
"""

import json
import os

TO_RESOLVE = [
    "supervised.json",
    "unsupervised.json",
    "semisupervised.json",
]
PAYLOAD = """
wget --load-cookies /tmp/cookies.txt \
    "https://docs.google.com/uc?export=download&confirm=$(wget --quiet \
    --save-cookies /tmp/cookies.txt --keep-session-cookies \
    --no-check-certificate \
    'https://docs.google.com/uc?export=download&id=FILEID' \
    -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id={id}" \
    -O {file_name}  && rm -rf /tmp/cookies.txt
"""

for file in TO_RESOLVE:
    models = json.load(open(file))
    for model in models.values():
        id = model["id"]
        file_name = f"{model['model_name']}.pkl"
        formatted_payload = PAYLOAD.format(id=id, file_name=file_name)
        os.system(formatted_payload)
