from argparse import ArgumentParser
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from docugenius.common.file_utils import find_python_files
from docugenius.genius import genius_factory


class RunArgs(BaseModel):
    """
    A class to hold the arguments for running the docstring generation.

    Attributes:
        input_path (str): The path to the input file or directory.
        model (str): The model to use for generating docstrings.
                     Must be one of ["openai:gpt-4o", "openai:gpt-4o-mini"].
        docstring_format (str): The format of the generated docstrings.
                                Must be one of ["google", "numpy", "sprinx"].
        skip_raises (bool): Whether to include information about exceptions raised by the code.
        skip_returns (bool): Whether to include information about the return value of the code.
        skip_examples (bool): Whether to include examples of how to use the code.
        output_path (str): The path to the output file/destination.
                           If not provided, the output will overwrite the input file.
                           If a directory is passed as input, this should be a directory.
    Raises:
        ValueError: If the model or docstring_format is not one of the specified literals.
    """

    input_path: str
    model: str = Literal["openai:gpt-4o", "openai:gpt-4o-mini"]
    docstring_format: Literal["google", "numpy", "sprinx"] = "google"
    skip_raises: bool = True
    skip_returns: bool = True
    skip_examples: bool = True
    output_path: str | None = None

    def is_recursive(self) -> bool:
        """
        Check if the input path is a directory or a file.

        Returns:
            bool: True if the input path is a directory, False if it is a file.
        """
        return Path(self.input_path).is_dir()


def run_on_file(input_file: str, model: str, output_file: str = None):
    """
    Generate docstrings for the code in the specified input file.

    Args:
        input_file (str): The path to the input file.
        model (str): The model to use for generating docstrings.
        output_file (str, optional): The path to the output file. Defaults to None.

    Raises:
        FileNotFoundError: If the input file does not exist.
        Exception: If there is an error during docstring generation.

    Returns:
        None: This function does not return a value.

    Example:
        >>> run_on_file('example.py', 'openai:gpt-4o')
    """

    with open(input_file) as f:
        code = f.read()

    genius = genius_factory(model)

    docstring = genius.generate(code)

    output_file = output_file or input_file

    with open(output_file, "w") as f:
        f.write(docstring)


def run(args: RunArgs):
    """
    Run the docstring generation process based on the provided arguments.

    Args:
        args (RunArgs): The arguments for running the docstring generation.

    Raises:
        FileNotFoundError: If the input file/directory does not exist.
        Exception: If there is an error during docstring generation.

    Returns:
        None: This function does not return a value.

    Example:
        >>> run(RunArgs(input_path='example.py', model='openai:gpt-4o'))
    """

    input_path = args.input_path
    model = args.model
    output_path = args.output_path

    if args.is_recursive():
        for file in find_python_files(input_path):
            run_on_file(file, model, output_path)
    else:
        run_on_file(input_path, model, output_path)


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "input_path",
        help="The path to the input. You can also pass a directory to process all files in it.",
    )

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
        "--skip-raises",
        "-r",
        action="store_false",
        help="Whether to include information about exceptions raised by the code.",
    )

    parser.add_argument(
        "--skip-returns",
        "-R",
        action="store_false",
        help="Whether to include information about the return value of the code.",
    )

    parser.add_argument(
        "--skip-examples",
        "-e",
        action="store_false",
        help="Whether to include examples of how to use the code.",
    )
    parser.add_argument(
        "--output-path",
        "-o",
        default=None,
        help="The path to the output file/destination. If not provided, the output will overwrite the input file. If a directory is passed as input, this should be a directory.",
    )

    args = parser.parse_args()
    run(RunArgs(**vars(args)))


if __name__ == "__main__":
    main()
