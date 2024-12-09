from abc import ABC, abstractmethod
from typing import Literal

from mako.template import Template

_DEFAULT_PROMPT = Template(
    """
Given a python code, that could contains class(es), function(s), method(s), variable(s), etc. generate a docstring for it using the ${docstring_format} format.

% if add_raises or add_returns or add_examples:
The generated docstring should include for each class, function, method, variable, etc.:
% if add_raises:
- The exceptions that the code can raise.
% endif
% if add_returns:
- The return value of the code.
% endif
% if add_examples:
- Examples of how to use the code.
% endif

% endif

The output code must be only the input code populated with the generated docstrings.
No additional code or comments should be added.
No bug fixing or code refactoring should be done.

Return the output code in the following format:



```generated-python-code
<OUTPUT_CODE>
```

No other output format is accepted.
"""
)


class Genius(ABC):
    """
    An abstract class for generating docstrings for Python code.

    Args:
        docstring_format (Literal["google", "numpy", "sprinx"], optional): The format of the docstring. Defaults to "google".
        add_raises (bool, optional): Whether to include exceptions in the docstring. Defaults to True.
        add_returns (bool, optional): Whether to include return values in the docstring. Defaults to True.
        add_examples (bool, optional): Whether to include examples in the docstring. Defaults to True.

    Raises:
        ValueError: If the provided docstring_format is not valid.
    """

    def __init__(
        self,
        docstring_format: Literal["google", "numpy", "sprinx"] = "google",
        add_raises: bool = True,
        add_returns: bool = True,
        add_examples: bool = True,
        **kwargs,
    ):
        self.docstring_format = docstring_format
        if docstring_format not in ["google", "numpy", "sprinx"]:
            raise ValueError(
                f"Invalid docstring format {docstring_format}. Must be one of 'google', 'numpy', or 'sprinx'."
            )
        self.add_raises = add_raises
        self.add_returns = add_returns
        self.add_examples = add_examples
        super().__init__()

    @property
    def _prompt(self) -> Template:
        """
        Return the default prompt for the client.
        """
        return _DEFAULT_PROMPT

    @property
    def _hydrated_prompt(self) -> str:
        """
        Return the prompt with the necessary variables replaced with their values.
        """
        return self._prompt.render(
            docstring_format=self.docstring_format,
            add_raises=self.add_raises,
            add_returns=self.add_returns,
            add_examples=self.add_examples,
        )

    @abstractmethod
    def _generate_docstring(self, code: str) -> str:
        """
        Generate a docstring for the given code and return the code with the docstring added.

        Parameters:
            code (str): The code to generate a docstring for.

        Returns:
            str: The code with the generated docstring added.
        """
        pass

    def clean_llm_output(self, output: str) -> str:
        """
        Clean the output from the LLM model by removing any leading or trailing whitespace.

        Parameters:
            output (str): The output from the LLM model.

        Returns:
            str: The cleaned output.
        """
        import re

        output = re.findall(r"```generated-python-code\n(.*?)\n```", output, re.DOTALL)
        if output:
            return output[0].strip()
        raise ValueError("No code block found in the output.")

    def generate(self, code: str) -> str:
        """
        Generate a docstring for the given code.

        Parameters:
            code (str): The code to generate a docstring for.

        Returns:
            str: The code with the generated docstring added.
        """
        output = self._generate_docstring(code)
        return self.clean_llm_output(output)
