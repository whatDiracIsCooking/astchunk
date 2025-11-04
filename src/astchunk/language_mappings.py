"""Language-specific AST node type mappings for astchunk.

This module maps programming languages to their tree-sitter node types
that represent semantic boundaries (classes, functions, methods, etc.).

Adding a New Language
---------------------
To add support for a new language:

1. Install the tree-sitter grammar: pip install tree-sitter-{language}
2. Research node type names using tree-sitter playground or grammar docs
3. Add entry to LANGUAGE_NODE_TYPES dictionary with Sets (not lists)
4. Add parametrized test cases in test/test_chunking_all_languages.py
5. Run: pytest test/ -v && mypy src/astchunk/

Example:
    >>> LANGUAGE_NODE_TYPES["rust"] = {
    ...     "class": {"impl_item", "struct_item", "enum_item"},
    ...     "function": {"function_item", "method_item"},
    ... }

Type Definitions:
    LanguageMapping: Dict mapping category ("class", "function") to Set of node type names
    LanguageMappings: Dict mapping language name to LanguageMapping
"""

from typing import Dict, Set

# Type aliases for clarity
LanguageMapping = Dict[str, Set[str]]
LanguageMappings = Dict[str, LanguageMapping]

# Language-specific AST node type mappings
# Using Sets for O(1) membership testing (not lists)
LANGUAGE_NODE_TYPES: LanguageMappings = {
    "python": {
        "class": {"class_definition"},
        "function": {"function_definition"},
    },
    "java": {
        "class": {"class_declaration", "interface_declaration", "enum_declaration"},
        "function": {"method_declaration", "constructor_declaration"},
    },
    "csharp": {
        "class": {"class_declaration", "interface_declaration", "struct_declaration"},
        "function": {"method_declaration", "constructor_declaration"},
    },
    "typescript": {
        "class": {"class_declaration", "interface_declaration"},
        "function": {"function_declaration", "method_definition", "arrow_function"},
    },
}


def get_ancestor_node_types(language: str) -> Set[str]:
    """Get combined set of class and function node types for a language.

    This function returns the tree-sitter node type names that should be
    considered as ancestors when building chunk context. Ancestors are
    typically class definitions, function definitions, and similar scoping
    constructs.

    Args:
        language: Programming language name. Must be one of the supported
            languages: 'python', 'java', 'csharp', 'typescript'.

    Returns:
        Set of tree-sitter node type strings that represent ancestor nodes
        for the given language. Returns union of "class" and "function" sets.

    Raises:
        ValueError: If the language is not supported. Error message includes
            list of supported languages.

    Examples:
        >>> get_ancestor_node_types("python")
        {'class_definition', 'function_definition'}

        >>> get_ancestor_node_types("java")
        {'class_declaration', 'interface_declaration', 'enum_declaration',
         'method_declaration', 'constructor_declaration'}

        >>> get_ancestor_node_types("ruby")  # Unsupported
        Traceback (most recent call last):
            ...
        ValueError: Unsupported language: 'ruby'. Supported languages: ...

    Performance:
        O(1) lookup in LANGUAGE_NODE_TYPES dict, O(k) where k is number of
        node types (typically <10).
    """
    if language not in LANGUAGE_NODE_TYPES:
        supported = ", ".join(sorted(LANGUAGE_NODE_TYPES.keys()))
        raise ValueError(
            f"Unsupported language: '{language}'. " f"Supported languages: {supported}"
        )

    mapping = LANGUAGE_NODE_TYPES[language]
    # Union of class and function node types (both are Sets for O(1) membership)
    return mapping.get("class", set()) | mapping.get("function", set())
