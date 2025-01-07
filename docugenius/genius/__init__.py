from docugenius.genius import openai_genius
from docugenius.genius.genius import Genius

SUPPORTED_MODELS = ["openai:gpt-4o", "openai:gpt-4o-mini"]


def genius_factory(model: str, **kwargs) -> Genius:
    """Creates an instance of the Genius class based on the specified model.

    Args:
        model (str): The model to use for creating the Genius instance.
                     Must be one of the supported models:
                     "openai:gpt-4o" or "openai:gpt-4o-mini".
        **kwargs: Additional keyword arguments to pass to the Genius constructor.

    Raises:
        ValueError: If the provided model is not supported.

    Returns:
        Genius: An instance of the Genius class configured with the specified model.

    Examples:
        >>> genius = genius_factory("openai:gpt-4o", api_key="your_api_key")
        >>> print(type(genius))
        <class 'docugenius.genius.openai_genius.OpenAIGenius'>

        >>> genius_mini = genius_factory("openai:gpt-4o-mini")
        >>> print(genius_mini.model)
        gpt-4o-mini
    """
    if model not in SUPPORTED_MODELS:
        raise ValueError(f"Unsupported model {model}. Must be one of {SUPPORTED_MODELS}.")

    if model in ["openai:gpt-4o", "openai:gpt-4o-mini"]:
        model = model.split(":")[1]
        return openai_genius.OpenAIGenius(model=model, **kwargs)
