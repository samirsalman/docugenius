# Docugenius

Docugenius is a Python library that uses large language models (LLMs) to automatically generate high-quality documentation for your code. With support for multiple docstring formats and customizable options, Docugenius simplifies the process of writing clear and professional documentation.

## Features
- Automatically generate docstrings for your Python code.
- Support for popular docstring formats, including Google, NumPy, and Sphinx.
- Flexible CLI interface for easy integration into your workflow.
- Customize generated docstrings with details like exceptions, return values, and examples.
- Save output to a specified file or overwrite the input file.

---

## Installation

You can install Docugenius via pip:

```bash
pip install docugenius
```

## Quickstart
To generate documentation for a Python file, simply run:

```bash
docugenius path/to/python/code.py
```

By default, Docugenius uses the OpenAI `openai:gpt-4o` model. You can specify a different model using the `--model` flag:

```bash
docugenius path/to/python/code.py --model openai:gpt-4-mini
```


## CLI Usage

```bash
usage: docugenius [-h] [--model {openai:gpt-4o,openai:gpt-4o-mini}] [--docstring-format {google,numpy,sprinx}] [--add-raises] [--add-returns] [--add-examples] [--output-file OUTPUT_FILE]
               input_file

positional arguments:
  input_file            The path to the input file.

options:
  -h, --help            Show this help message and exit.
  --model {openai:gpt-4o,openai:gpt-4o-mini}, -m {openai:gpt-4o,openai:gpt-4o-mini}
                        The model to use for generating docstrings.
  --docstring-format {google,numpy,sprinx}, -d {google,numpy,sprinx}
                        The format of the generated docstrings.
  --add-raises, -r      Include information about exceptions raised by the code.
  --add-returns, -R     Include information about the return values.
  --add-examples, -e    Add usage examples to the docstrings.
  --output-file OUTPUT_FILE, -o OUTPUT_FILE
                        Path to save the generated docstrings. Defaults to overwriting the input file.

```
