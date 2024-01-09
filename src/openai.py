import re
import json
import base64
import logging
import requests
from config import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def encode_image_to_base64(byte_image: bytes) -> str:
    return base64.b64encode(byte_image).decode("utf-8")


def call_gpt4vision(
    prompt: str,
    byte_image: bytes,
    max_tokens: int = 1200,
    model: str = "gpt-4-vision-preview",
    url: str = "https://api.openai.com/v1/chat/completions",
):
    base64_image = encode_image_to_base64(byte_image)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.openai_api_key}",
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": max_tokens,
    }

    response = requests.post(url, headers=headers, json=payload)

    # Assuming the API responds with the necessary data, parse the response
    # and construct the desired JSON structure
    if response.status_code != 200:
        raise RuntimeError(response.text)

    content = response.json()["choices"][0]["message"]["content"].strip()
    logger.info(f"Content: {content}")

    # Extract the JSON paragraph:
    return _json_extraction(content)


def _json_extraction(content: str) -> dict:
    # Extract the JSON paragraph:
    json_data = "{".join(content.split("{")[1:])
    json_data = "}".join(json_data.split("}")[:-1])
    json_data = "{" + json_data + "}"
    return _fix_json(json_data)


def _fix_json(json_string: str) -> dict:
    """
    Function to fix the JSON string generated by GPT
    """
    # Replace None with null
    json_string = json_string.replace("None", "null")
    json_string = json_string.replace("True", "true")
    json_string = json_string.replace("False", "false")

    # Remove comments (anything that starts with '#' and ends with a newline)
    json_string = re.sub(r"\s*#.*(?=\n)", "", json_string)

    # Replace escaped single quotes with just single quotes
    json_string = json_string.replace("\\'", "'")

    # Now attempt to parse the string into a JSON object
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing JSON: {e}")