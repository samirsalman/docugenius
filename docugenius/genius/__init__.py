from docugenius.genius import openai_genius
from docugenius.genius.genius import Genius

SUPPORTED_MODELS = ["openai:gpt-4o", "openai:gpt-4o-mini"]


def genius_factory(model: str, **kwargs) -> Genius:
    if model not in SUPPORTED_MODELS:
        raise ValueError(f"Unsupported model {model}. Must be one of {SUPPORTED_MODELS}.")

    if model in ["openai:gpt-4o", "openai:gpt-4o-mini"]:
        model = model.split(":")[1]
        return openai_genius.OpenAIGenius(model=model, **kwargs)
