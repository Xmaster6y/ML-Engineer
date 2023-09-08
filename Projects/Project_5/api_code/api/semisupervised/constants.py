"""
Semi-supervised module constants.
"""

import os

# Model info
ALL_MODELS = {
    "default": {
        "model_name": "gpt-3.5-turbo",
        "model_type": "openai",
    },
    "gpt-3.5-turbo": {
        "model_name": "gpt-3.5-turbo",
        "model_type": "openai",
    },
}

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

PROMPT_TEMPLATE = """
You will be provided with the following information:
1. A Stack Overflow question. The question is delimited with triple backticks. The question has three parts: title, body_text and body_code.
2. List of tags the question can be assigned to. The tags in the list are enclosed in the single quotes and comma separated.

Perform the following tasks:
1. Identify to which tags the provided question belongs to with the highest probability.
2. Assign the question to any tags based on the probabilities. If no tag is perninent don't asign any tag to the question.
3. Provide your response in a JSON format containing a single key `label` and a value corresponding to the array of assigned tags. Do not provide any additional information except the JSON.

List of tags: {labels}

Stack Overflow question:
```
[title]
{title}

[body_text]
{body_text}

[body_code]
{body_code}
```

Your JSON response:
"""  # noqa: E501

LENGTH_LIMIT = 2000
