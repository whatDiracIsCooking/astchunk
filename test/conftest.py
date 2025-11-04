"""Pytest configuration and fixtures for astchunk tests.

This module provides session-scoped fixtures for language-specific code samples
used across all test modules. Fixtures are session-scoped for performance since
they involve language parser initialization.

IMPORTANT: Helper functions should NOT be defined here. Use test/assertions.py
for helper assertion functions to maintain clean separation of concerns.
"""

import pytest


@pytest.fixture(scope="session")
def language_samples() -> dict[str, dict[str, str]]:
    """Provide language-specific code samples for testing.

    Returns a nested dictionary mapping language names to scenario names to
    code samples. This fixture is session-scoped for performance.

    Returns:
        dict: Structure: {language: {scenario: code_string}}
            - language: "python", "java", "csharp", "typescript"
            - scenario: "empty", "single_class", "single_function", "nested",
                       "multiple_chunks", "no_ancestors", etc.

    Example:
        >>> samples = language_samples()
        >>> python_code = samples["python"]["single_class"]
        >>> java_code = samples["java"]["nested"]
    """
    return {
        "python": {
            "empty": "",
            "comments_only": "# This is a comment\n# Another comment",
            "docstring_only": '"""\nModule docstring\n"""\n',
            "no_ancestors": "x = 1\ny = 2\nz = x + y\n",
            "single_class": "class MyClass:\n    def method(self):\n        pass\n",
            "single_function": "def my_function():\n    return 42\n",
            "nested_classes": (
                "class Outer:\n"
                "    class Inner:\n"
                "        def method(self):\n"
                "            pass\n"
            ),
            "nested_functions": (
                "def outer():\n"
                "    def inner():\n"
                "        return 42\n"
                "    return inner\n"
            ),
            "class_with_multiple_methods": (
                "class Calculator:\n"
                "    def add(self, a, b):\n"
                "        return a + b\n"
                "    def subtract(self, a, b):\n"
                "        return a - b\n"
            ),
            "mixed_classes_and_functions": (
                "def standalone_function():\n"
                "    pass\n"
                "class MyClass:\n"
                "    def method(self):\n"
                "        pass\n"
                "def another_function():\n"
                "    pass\n"
            ),
            "unicode_identifiers": (
                "class Ñame:\n"
                "    def métod(self):\n"
                "        pass\n"
            ),
            "deeply_nested": (
                "class L1:\n"
                "    class L2:\n"
                "        class L3:\n"
                "            class L4:\n"
                "                class L5:\n"
                "                    def method(self):\n"
                "                        pass\n"
            ),
            "class_inside_function": (
                "def outer():\n"
                "    class LocalClass:\n"
                "        def method(self):\n"
                "            pass\n"
                "    return LocalClass\n"
            ),
            "function_inside_function": (
                "def outer():\n"
                "    def inner():\n"
                "        def innermost():\n"
                "            pass\n"
                "        return innermost\n"
                "    return inner\n"
            ),
        },
        "java": {
            "empty": "",
            "package_only": "package com.example;\n",
            "imports_only": "import java.util.*;\nimport java.io.*;\n",
            "single_class": "public class MyClass {\n    public void method() {}\n}\n",
            "single_interface": "public interface MyInterface {\n    void method();\n}\n",
            "single_enum": "public enum Color {\n    RED, GREEN, BLUE\n}\n",
            "nested_classes": (
                "public class Outer {\n"
                "    public class Inner {\n"
                "        public void method() {}\n"
                "    }\n"
                "}\n"
            ),
            "static_nested_class": (
                "public class Outer {\n"
                "    public static class Inner {\n"
                "        public void method() {}\n"
                "    }\n"
                "}\n"
            ),
            "anonymous_inner_class": (
                "public class Outer {\n"
                "    Runnable r = new Runnable() {\n"
                "        public void run() {}\n"
                "    };\n"
                "}\n"
            ),
            "method_with_lambda": (
                "public class Lambda {\n"
                "    void test() {\n"
                "        Runnable r = () -> System.out.println(\"Hello\");\n"
                "    }\n"
                "}\n"
            ),
            "interface_with_default_method": (
                "public interface MyInterface {\n"
                "    default void defaultMethod() {\n"
                "        System.out.println(\"Default\");\n"
                "    }\n"
                "}\n"
            ),
            "class_with_multiple_methods": (
                "public class Calculator {\n"
                "    public int add(int a, int b) { return a + b; }\n"
                "    public int subtract(int a, int b) { return a - b; }\n"
                "}\n"
            ),
            "mixed_elements": (
                "package com.example;\n"
                "public class Outer {\n"
                "    public static final int CONSTANT = 42;\n"
                "    public class Inner {}\n"
                "    public void method() {}\n"
                "}\n"
            ),
            "unicode_identifiers": (
                "public class Ñame {\n"
                "    public void métod() {}\n"
                "}\n"
            ),
            "deeply_nested": (
                "public class L1 {\n"
                "    public class L2 {\n"
                "        public class L3 {\n"
                "            public class L4 {\n"
                "                public void method() {}\n"
                "            }\n"
                "        }\n"
                "    }\n"
                "}\n"
            ),
            "constructor": (
                "public class WithConstructor {\n"
                "    public WithConstructor(String param) {}\n"
                "}\n"
            ),
        },
        "csharp": {
            "empty": "",
            "using_only": "using System;\nusing System.Collections.Generic;\n",
            "single_class": "public class MyClass {\n    public void Method() {}\n}\n",
            "single_interface": "public interface IMyInterface {\n    void Method();\n}\n",
            "single_struct": "public struct MyStruct {\n    public void Method() {}\n}\n",
            "nested_classes": (
                "public class Outer {\n"
                "    public class Inner {\n"
                "        public void Method() {}\n"
                "    }\n"
                "}\n"
            ),
            "extension_method": (
                "public static class Extensions {\n"
                "    public static void ExtendMe(this string s) {}\n"
                "}\n"
            ),
            "async_method": (
                "public class AsyncClass {\n"
                "    public async Task MyAsyncMethod() {}\n"
                "}\n"
            ),
            "property": (
                "public class WithProperty {\n"
                "    public string Name { get; set; }\n"
                "}\n"
            ),
            "delegates_and_events": (
                "public class EventExample {\n"
                "    public delegate void MyDelegate();\n"
                "    public event MyDelegate MyEvent;\n"
                "}\n"
            ),
            "partial_class": (
                "public partial class PartialClass {\n"
                "    public void Method1() {}\n"
                "}\n"
                "public partial class PartialClass {\n"
                "    public void Method2() {}\n"
                "}\n"
            ),
            "class_with_multiple_methods": (
                "public class Calculator {\n"
                "    public int Add(int a, int b) { return a + b; }\n"
                "    public int Subtract(int a, int b) { return a - b; }\n"
                "}\n"
            ),
            "unicode_identifiers": (
                "public class Ñame {\n"
                "    public void Métod() {}\n"
                "}\n"
            ),
            "deeply_nested": (
                "public class L1 {\n"
                "    public class L2 {\n"
                "        public class L3 {\n"
                "            public class L4 {\n"
                "                public void Method() {}\n"
                "            }\n"
                "        }\n"
                "    }\n"
                "}\n"
            ),
            "constructor": (
                "public class WithConstructor {\n"
                "    public WithConstructor(string param) {}\n"
                "}\n"
            ),
        },
        "typescript": {
            "empty": "",
            "import_only": "import { Module } from './module';\nimport fs from 'fs';\n",
            "single_class": "class MyClass {\n    method() {}\n}\n",
            "single_interface": "interface IMyInterface {\n    method(): void;\n}\n",
            "function_declaration": "function myFunction(): number {\n    return 42;\n}\n",
            "arrow_function": "const myArrow = (): number => 42;\n",
            "nested_classes": (
                "class Outer {\n"
                "    class Inner {\n"
                "        method() {}\n"
                "    }\n"
                "}\n"
            ),
            "class_with_decorators": (
                "@Component\nclass MyComponent {\n"
                "    @Input()\n"
                "    name: string = '';\n"
                "}\n"
            ),
            "generic_class": (
                "class Container<T> {\n"
                "    value: T;\n"
                "    constructor(val: T) { this.value = val; }\n"
                "}\n"
            ),
            "namespace": (
                "namespace MyNamespace {\n"
                "    class MyClass {\n"
                "        method() {}\n"
                "    }\n"
                "}\n"
            ),
            "module_augmentation": (
                "declare module 'express' {\n"
                "    interface Request {\n"
                "        user?: any;\n"
                "    }\n"
                "}\n"
            ),
            "class_with_multiple_methods": (
                "class Calculator {\n"
                "    add(a: number, b: number): number { return a + b; }\n"
                "    subtract(a: number, b: number): number { return a - b; }\n"
                "}\n"
            ),
            "unicode_identifiers": (
                "class Ñame {\n"
                "    métod() {}\n"
                "}\n"
            ),
            "deeply_nested": (
                "class L1 {\n"
                "    class L2 {\n"
                "        class L3 {\n"
                "            class L4 {\n"
                "                method() {}\n"
                "            }\n"
                "        }\n"
                "    }\n"
                "}\n"
            ),
            "arrow_functions_in_class": (
                "class MyClass {\n"
                "    myMethod = () => {\n"
                "        return 42;\n"
                "    };\n"
                "}\n"
            ),
        },
    }


@pytest.fixture
def python_builder(language_samples: dict[str, dict[str, str]]) -> object:
    """Provide a Python AST builder for testing.

    Returns an ASTChunkBuilder configured for Python parsing.

    Args:
        language_samples: The language_samples fixture (unused but indicates dependency)

    Returns:
        Configured ASTChunkBuilder instance for Python
    """
    from astchunk.astchunk_builder import ASTChunkBuilder

    return ASTChunkBuilder(
        max_chunk_size=512,
        language="python",
        metadata_template="default",
    )


@pytest.fixture
def java_builder(language_samples: dict[str, dict[str, str]]) -> object:
    """Provide a Java AST builder for testing.

    Returns an ASTChunkBuilder configured for Java parsing.

    Args:
        language_samples: The language_samples fixture (unused but indicates dependency)

    Returns:
        Configured ASTChunkBuilder instance for Java
    """
    from astchunk.astchunk_builder import ASTChunkBuilder

    return ASTChunkBuilder(
        max_chunk_size=512,
        language="java",
        metadata_template="default",
    )


@pytest.fixture
def csharp_builder(language_samples: dict[str, dict[str, str]]) -> object:
    """Provide a C# AST builder for testing.

    Returns an ASTChunkBuilder configured for C# parsing.

    Args:
        language_samples: The language_samples fixture (unused but indicates dependency)

    Returns:
        Configured ASTChunkBuilder instance for C#
    """
    from astchunk.astchunk_builder import ASTChunkBuilder

    return ASTChunkBuilder(
        max_chunk_size=512,
        language="csharp",
        metadata_template="default",
    )


@pytest.fixture
def typescript_builder(language_samples: dict[str, dict[str, str]]) -> object:
    """Provide a TypeScript AST builder for testing.

    Returns an ASTChunkBuilder configured for TypeScript parsing.

    Args:
        language_samples: The language_samples fixture (unused but indicates dependency)

    Returns:
        Configured ASTChunkBuilder instance for TypeScript
    """
    from astchunk.astchunk_builder import ASTChunkBuilder

    return ASTChunkBuilder(
        max_chunk_size=512,
        language="typescript",
        metadata_template="default",
    )
