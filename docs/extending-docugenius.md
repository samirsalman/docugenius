# Extending Docugenius

Docugenius is designed to be easily extensible, so you can add support for other models by subclassing the `Genius` class and implementing the necessary methods.

## Adding Support for Other Models

To add support for other models, you need to subclass the `Genius` class and implement the needed methods, like below:

```python
from docugenius.genius.genius import Genius

class YourCustomGenius(Genius):
    def __init__(
       self,
        docstring_format: Literal["google", "numpy", "sprinx"] = "google",
        add_raises: bool = True,
        add_returns: bool = True,
        add_examples: bool = True,
        custom_param:int = 0,
        **kwargs,
    ):
        super().__init__(docstring_format, add_raises, add_returns,add_examples)
        self.custom_param = custom_param


    def _generate_docstring(self, code: str) -> str:
        # do something
        output = ...
        return output
```

And add your model to the supported models list and to the genius_factory function in `genius/__init__.py`.

If you need to change the prompt and/or the cleaning fn please refer to the [Genius](api-references/genius.md) class.

