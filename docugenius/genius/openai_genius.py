from typing import Literal

from docugenius.genius.genius import Genius


class OpenAIGenius(Genius):
    """
    A class to generate docstrings using OpenAI's API.

    Args:
        model (str): The model to use for generating docstrings.
        docstring_format (Literal["google", "numpy", "sprinx"], optional): The format of the docstring. Defaults to "google".
        add_raises (bool, optional): Whether to include exceptions in the docstring. Defaults to True.
        add_returns (bool, optional): Whether to include return values in the docstring. Defaults to True.
        add_examples (bool, optional): Whether to include examples in the docstring. Defaults to True.

    Raises:
        ValueError: If the provided model is not valid.

    Examples:
        >>> genius = OpenAIGenius(model="gpt-3.5-turbo")
        >>> print(genius.docstring_format)
        google
    """

    def __init__(
        self,
        model: str,
        docstring_format: Literal["google", "numpy", "sprinx"] = "google",
        add_raises: bool = True,
        add_returns: bool = True,
        add_examples: bool = True,
    ):
        import openai

        super().__init__(docstring_format, add_raises, add_returns, add_examples)
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
