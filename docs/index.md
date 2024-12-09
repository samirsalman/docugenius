# Docugenius

Docugenius is a tool that generates documentation for your python code using LLMs. 
The library provides a simple CLI interface to generate documentation for your python code.

## Installation

```bash
pip install docugenius
```

## Quickstart

Before running docugenius, make sure you exported your OpenAI API key as an environment variable.

```bash
export OPENAI_API_KEY="your-api-key"
```


To generate documentation for your python code, run the following command:

```bash
docugenius path/to/python/code.py
```

The default model used is OpenAI `openai:gpt-4o`, but you can specify a different model using the `--model` flag.

```
docugenius path/to/python/code.py --model openai:gpt-4-mini
```

See the Supported Models section for a list of supported models. [Supported Models](supported-models.md)

If you want to run docugenius on an entire directory, you can pass the directory path as input.

```bash
docugenius path/to/python/directory
```



## CLI Usage

```bash
usage: docugenius [-h] [--model {openai:gpt-4o,openai:gpt-4o-mini}] [--docstring-format {google,numpy,sprinx}] [--skip-raises] [--skip-returns]
                  [--skip-examples] [--output-path OUTPUT_PATH]
                  input_path

positional arguments:
  input_path            The path to the input. You can also pass a directory to process all files in it.

options:
  -h, --help            show this help message and exit
  --model {openai:gpt-4o,openai:gpt-4o-mini}, -m {openai:gpt-4o,openai:gpt-4o-mini}
                        The model to use for generating docstrings.
  --docstring-format {google,numpy,sprinx}, -d {google,numpy,sprinx}
                        The format of the generated docstrings.
  --skip-raises, -r     Whether to include information about exceptions raised by the code.
  --skip-returns, -R    Whether to include information about the return value of the code.
  --skip-examples, -e   Whether to include examples of how to use the code.
  --output-path OUTPUT_PATH, -o OUTPUT_PATH
                        The path to the output file/destination. If not provided, the output will overwrite the input file. If a directory is passed as
                        input, this should be a directory.
```

The output overwrites the input file. If you want to save the output to a different file, you can use the `--output-path` flag.

```bash
docugenius path/to/python/code.py --output path/to/output/file.py
```