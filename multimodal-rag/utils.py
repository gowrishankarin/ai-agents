import os
import textwrap
import base64
import glob 
import PIL.Image
import cv2 
import json 
import PIL 
import dataclasses
import random 

from dotenv import load_dotenv, find_dotenv
from io import StringIO, BytesIO
from typing import Iterator, TextIO, List, Dict, Any, Optional, Sequence, Union 
from enum import auto, Enum 
from tqdm import tqdm 
from pytubefix import YouTube, Stream 
from youtube_transcript_api import YouTubeTranscriptApi 
from youtube_transcript_api.formatters import WebVTTFormatter 
from predictionguard import PredictionGuard
from datasets import load_dataset

from langchain_core.prompt_values import PromptValue 
from langchain_core.messages import MessageLikeRepresentation

# The MultimodalModelInput is a Union type that can be one of the following:
# - PromptValue: A value that can be used as a prompt in a multimodal model.
# - str: A string value.
# - Sequence[MessageLikeRepresentation]: A sequence of message-like representations.
# - Dict[str, Any]: A dictionary with string keys and any values.
MultimodalModelInput = Union[PromptValue, str, Sequence[MessageLikeRepresentation], Dict[str, Any]]

def get_from_dict_or_env(
    data: Dict[str, Any], key: str, env_key: str, default: Optional[str] = None
) -> str:
    """Get a value from a dictionary or an environment variable."""
    if key in data and data[key]:
        return data[key]
    else:
        return get_from_env(key, env_key, default=default)

def get_from_env(key: str, env_key: str, default: Optional[str] = None) -> str:
    """Get a value from a dictionary or an environment variable."""
    if env_key in os.environ and os.environ[env_key]:
        return os.environ[env_key]
    else:
        return default
        
def load_env():
    _ = load_dotenv(find_dotenv())

def get_openai_api_key():
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key


# IMAGE FORMAT UTILS
# checking whether the given string is base64 or not
def isBase64(sb):
    try:
        if isinstance(sb, str):
                # If there's any unicode here, an exception will be thrown and the function will return false
                sb_bytes = bytes(sb, 'ascii')
        elif isinstance(sb, bytes):
                sb_bytes = sb
        else:
                raise ValueError("Argument must be string or bytes")
        return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except Exception:
            return False

# Encoding image at given path OR PIL Image using base64
def encode_image(image_path_or_PIL_img):
    if isinstance(image_path_or_PIL_img, PIL.Image.Image):
        # This is a PIL image
        buffered = BytesIO()
        image_path_or_PIL_img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    else: # This is an image path
        with open(image_path_or_PIL_img, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
        



# PREDICTION GUARD HELPERS

def get_prediction_guard_api_key():
    load_env()
    PREDICTION_GUARD_API_KEY = os.getenv("PREDICTION_GUARD_API_KEY", None)
    if PREDICTION_GUARD_API_KEY is None:
        PREDICTION_GUARD_API_KEY = input("Please enter your Prediction Guard API Key: ")
    return PREDICTION_GUARD_API_KEY
    
PREDICTION_GUARD_URL_ENDPOINT = os.getenv("DLAI_PREDICTION_GUARD_URL_ENDPOINT", "https://dl-itdc.predictionguard.com") ###"https://proxy-dl-itdc.predictionguard.com"


# get PredictionGuard Client
def _getPredictionGuardClient():
    PREDICTION_GUARD_API_KEY = get_prediction_guard_api_key()
    client = PredictionGuard(
        api_key=PREDICTION_GUARD_API_KEY,
        url=PREDICTION_GUARD_URL_ENDPOINT,
    )
    return client

# Helper function to compute the joint embedding of a prompt 
# and a base 64 encoded image thru PredictionGuard
def bt_embedding_from_prediction_guard(prompt, base64_image):
    # Get PredictionGuard client
    client = _getPredictionGuardClient()
    message = {
        "text": prompt,
    }

    if base64_image is not None and base64_image != "":
        if not isBase64(base64_image):
            raise TypeError("image input must be in base64 encoding!")
        message['image'] = base64_image

    response = client.embeddings.create(
        model="bridgetower-large-itm-mlm-itc",
        input=[message]
    )
    return response['data'][0]['embedding']