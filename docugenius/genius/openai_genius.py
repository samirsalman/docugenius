from typing import Literal

from docugenius.genius.genius import Genius


class OpenAIGenius(Genius):
    """
    A class to generate docstrings using OpenAI's API.

    Args:
        model (str): The model to use for generating docstrings.
        docstring_format (Literal["google", "numpy", "sprinx"], optional): The format of the docstring. Defaults to "google".
        skip_raises (bool, optional): Whether to include exceptions in the docstring. Defaults to False.
        skip_returns (bool, optional): Whether to include return values in the docstring. Defaults to False.
        skip_examples (bool, optional): Whether to include examples in the docstring. Defaults to False.

    Raises:
        ValueError: If the provided model is not valid.

    Examples:
        >>> genius = OpenAIGenius(model="gpt-4o-mini")
        >>> print(genius.docstring_format)
        google
    """

    def __init__(
        self,
        model: str,
        docstring_format: Literal["google", "numpy", "sprinx"] = "google",
        skip_raises: bool = False,
        skip_returns: bool = False,
        skip_examples: bool = False,
    ):
        """
        Initialize the OpenAIGenius instance.

        Args:
            model (str): The model to use for generating docstrings.
            docstring_format (Literal["google", "numpy", "sprinx"], optional): The format of the docstring. Defaults to "google".
            skip_raises (bool, optional): Whether to include exceptions in the docstring. Defaults to False.
            skip_returns (bool, optional): Whether to include return values in the docstring. Defaults to False.
            skip_examples (bool, optional): Whether to include examples in the docstring. Defaults to False.

        Raises:
            ValueError: If the provided model is not valid.

        Examples:
            >>> genius = OpenAIGenius(model="gpt-4o-mini")
        """
        import openai

        super().__init__(docstring_format, skip_raises, skip_returns, skip_examples)
        self._client = openai.OpenAI()
        self.model = model

    def _generate_docstring(self, code: str) -> str:
        """
        Generate a docstring for the provided code using OpenAI's API.

        Args:
            code (str): The code for which to generate a docstring.

        Returns:
            str: The generated docstring.

        Raises:
            Exception: If the OpenAI API call fails.

        Examples:
            >>> docstring = genius._generate_docstring("def example_function(): pass")
            >>> print(docstring)
        """
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._hydrated_prompt},
                {"role": "user", "content": code},
            ],
            temperature=0,
            top_p=1,
        )
        return response.choices[0].message.content
