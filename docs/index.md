# Docugenius

Docugenius is a tool that generates documentation for your python code using LLMs. 
The library provides a simple CLI interface to generate documentation for your python code.

## Installation

```bash
pip install docugenius
```

## Quickstart

To generate documentation for your python code, run the following command:

```bash
docugenius path/to/python/code.py
```

The default model used is OpenAI `openai:gpt-4o`, but you can specify a different model using the `--model` flag.

```
docugenius path/to/python/code.py --model openai:gpt-4-mini
```

See the Supported Models section for a list of supported models. [Supported Models](supported-models.md)


## CLI Usage

```bash
usage: docugenius [-h] [--model {openai:gpt-4o,openai:gpt-4o-mini}] [--docstring-format {google,numpy,sprinx}] [--add-raises] [--add-returns] [--add-examples] [--output-file OUTPUT_FILE]
               input_file

positional arguments:
  input_file            The path to the input file.

options:
  -h, --help            show this help message and exit
  --model {openai:gpt-4o,openai:gpt-4o-mini}, -m {openai:gpt-4o,openai:gpt-4o-mini}
                        The model to use for generating docstrings.
  --docstring-format {google,numpy,sprinx}, -d {google,numpy,sprinx}
                        The format of the generated docstrings.
  --add-raises, -r      Whether to include information about exceptions raised by the code.
  --add-returns, -R     Whether to include information about the return value of the code.
  --add-examples, -e    Whether to include examples of how to use the code.
  --output-file OUTPUT_FILE, -o OUTPUT_FILE
                        The path to the output file where the generated docstrings will be written. By default, the input file will be overwritten.

```

The output overwrites the input file. If you want to save the output to a different file, you can use the `--output` flag.

```bash
docugenius path/to/python/code.py --output path/to/output/file.py
```