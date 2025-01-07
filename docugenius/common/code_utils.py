import ast


def is_just_imports(code: str):
    """
    Check if the code is just imports.

    Args:
        code (str): The code to check.

    Returns:
        bool: True if the code consists only of import statements, False otherwise.

    Raises:
        SyntaxError: If the code contains invalid syntax.

    Examples:
        >>> is_just_imports("import os")
        True
        >>> is_just_imports("import os\nimport sys")
        True
        >>> is_just_imports("x = 5")
        False
    """

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    return all(
        isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom)
        for node in tree.body
    )


def is_just_docstring(code: str):
    """
    Check if the code is just a docstring.

    Args:
        code (str): The code to check.

    Returns:
        bool: True if the code consists only of a single docstring, False otherwise.

    Raises:
        SyntaxError: If the code contains invalid syntax.

    Examples:
        >>> is_just_docstring('\"\"\"This is a docstring.\"\"\"')
        True
        >>> is_just_docstring("def func(): pass")
        False
    """

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    return (
        len(tree.body) == 1
        and isinstance(tree.body[0], ast.Expr)
        and isinstance(tree.body[0].value, ast.Constant)
    )


def is_just_constants(code: str):
    """
    Check if the code is just constants.

    Args:
        code (str): The code to check.

    Returns:
        bool: True if the code consists only of constant assignments, False otherwise.

    Raises:
        SyntaxError: If the code contains invalid syntax.

    Examples:
        >>> is_just_constants("x = 5")
        True
        >>> is_just_constants("x, y = 5, 10")
        False
        >>> is_just_constants("x = 'hello'")
        True
    """

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    return all(
        isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
        for node in tree.body
    )


def is_skippable(code: str):
    """
    Check if the code is skippable.

    Args:
        code (str): The code to check.

    Returns:
        bool: True if the code is skippable (i.e., consists only of imports, docstrings, or constants), False otherwise.

    Examples:
        >>> is_skippable("import os")
        True
        >>> is_skippable("\"\"\"This is a docstring.\"\"\"")
        True
        >>> is_skippable("x = 5")
        True
        >>> is_skippable("def func(): pass")
        False
    """
    return is_just_imports(code) or is_just_docstring(code) or is_just_constants(code)
