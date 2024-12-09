from argparse import ArgumentParser
from typing import Literal

from pydantic import BaseModel

from docugenius.genius import genius_factory


class RunArgs(BaseModel):
    """
    A class to hold the arguments for running the docstring generation.

    Attributes:
        input_file (str): The path to the input file.
        model (str): The model to use for generating docstrings.
                     Must be one of ["openai:gpt-4o", "openai:gpt-4o-mini"].
        docstring_format (str): The format of the generated docstrings.
                                Must be one of ["google", "numpy", "sprinx"].
        add_raises (bool): Whether to include information about exceptions raised by the code.
        add_returns (bool): Whether to include information about the return value of the code.
        add_examples (bool): Whether to include examples of how to use the code.

    Raises:
        ValueError: If the model or docstring_format is not one of the specified literals.
    """

    input_file: str
    model: str = Literal["openai:gpt-4o", "openai:gpt-4o-mini"]
    docstring_format: Literal["google", "numpy", "sprinx"] = "google"
    add_raises: bool = True
    add_returns: bool = True
    add_examples: bool = True
    output_file: str = None


def run(args: RunArgs):
    """
    Generate docstrings for the code in the specified input file.

    Args:
        args (RunArgs): The arguments containing input file and generation options.

    Raises:
        FileNotFoundError: If the input file does not exist.
        Exception: If there is an error during docstring generation.

    Returns:
        None: This function does not return a value.

    Example:
        >>> run(RunArgs(input_file='example.py', model='openai:gpt-4o'))
    """
    with open(args.input_file) as f:
        code = f.read()

    genius = genius_factory(args.model)

    docstring = genius.generate(code)

    output_file = args.output_file or args.input_file

    with open(output_file, "w") as f:
        f.write(docstring)


def main():
    parser = ArgumentParser()
    parser.add_argument("input_file", help="The path to the input file.")

    parser.add_argument(
        "--model",
        "-m",
        default="openai:gpt-4o",
        choices=["openai:gpt-4o", "openai:gpt-4o-mini"],
        help="The model to use for generating docstrings.",
    )

    parser.add_argument(
        "--docstring-format",
        "-d",
        default="google",
        choices=["google", "numpy", "sprinx"],
        help="The format of the generated docstrings.",
    )

    parser.add_argument(
        "--add-raises",
        "-r",
        action="store_true",
        help="Whether to include information about exceptions raised by the code.",
    )

    parser.add_argument(
        "--add-returns",
        "-R",
        action="store_true",
        help="Whether to include information about the return value of the code.",
    )

    parser.add_argument(
        "--add-examples",
        "-e",
        action="store_true",
        help="Whether to include examples of how to use the code.",
    )
    parser.add_argument(
        "--output-file",
        "-o",
        default=None,
        help="The path to the output file where the generated docstrings will be written. By default, the input file will be overwritten.",
    )

    args = parser.parse_args()
    run(RunArgs(**vars(args)))


if __name__ == "__main__":
    main()
