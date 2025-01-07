from abc import ABC, abstractmethod
from typing import Literal

from mako.template import Template

from docugenius.common.code_utils import is_skippable

_DEFAULT_PROMPT = Template(
    """
Given a python code, that could contains class(es), function(s), method(s), variable(s), etc. generate a docstring for it using the ${docstring_format} format.

# Requirements
% if not (skip_raises and skip_returns and skip_examples):
The generated docstring should include for each class, function, method, variable, etc.:
% if not skip_raises:
- The exceptions that the code can raise.
% endif
% if not skip_returns:
- The return value of the code.
% endif
% if not skip_examples:
- Examples of how to use the code.
% endif

% endif

# Rules
- Be sure to not introduce any avoided characters in the generated docstring, respect the indentation and the line breaks.
- Make sure to keep the original code as it is, without any modification.
- The output code must be only the input code populated with the generated docstrings.
- No bug fixing or code refactoring should be done.
- The code should be able to run without any error after adding the docstrings.
- If you find constants or imports in the code, you can skip them and leave them as they are.

# Output Format
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
        skip_raises (bool, optional): Whether to include exceptions in the docstring. Defaults to False.
        skip_returns (bool, optional): Whether to include return values in the docstring. Defaults to False.
        skip_examples (bool, optional): Whether to include examples in the docstring. Defaults to False.

    Raises:
        ValueError: If the provided docstring_format is not valid.
    """

    def __init__(
        self,
        docstring_format: Literal["google", "numpy", "sprinx"] = "google",
        skip_raises: bool = False,
        skip_returns: bool = False,
        skip_examples: bool = False,
        **kwargs,
    ):
        self.docstring_format = docstring_format
        if docstring_format not in ["google", "numpy", "sprinx"]:
            raise ValueError(
                f"Invalid docstring format {docstring_format}. Must be one of 'google', 'numpy', or 'sprinx'."
            )
        self.skip_raises = skip_raises
        self.skip_returns = skip_returns
        self.skip_examples = skip_examples
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
            skip_raises=self.skip_raises,
            skip_returns=self.skip_returns,
            skip_examples=self.skip_examples,
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
            output = output[0]
        else:
            output = ""

        return output

    def generate(self, code: str) -> str:
        """
        Generate a docstring for the given code.

        Parameters:
            code (str): The code to generate a docstring for.

        Returns:
            str: The code with the generated docstring added.
        """
        if not code or is_skippable(code):
            return code

        output = self._generate_docstring(code)
        return self.clean_llm_output(output)
