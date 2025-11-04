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
                "class Ñame:\n" "    def métod(self):\n" "        pass\n"
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
                '        Runnable r = () -> System.out.println("Hello");\n'
                "    }\n"
                "}\n"
            ),
            "interface_with_default_method": (
                "public interface MyInterface {\n"
                "    default void defaultMethod() {\n"
                '        System.out.println("Default");\n'
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
                "public class Ñame {\n" "    public void métod() {}\n" "}\n"
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
                "public class Ñame {\n" "    public void Métod() {}\n" "}\n"
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
            "unicode_identifiers": ("class Ñame {\n" "    métod() {}\n" "}\n"),
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
        "cpp": {
            "empty": "",
            "comments_only": "// This is a comment\n// Another comment",
            "single_class": (
                "class MyClass {\n" "public:\n" "    void method() {}\n" "};\n"
            ),
            "single_function": "int myFunction() {\n    return 42;\n}\n",
            "function_declaration": "int myFunction() {\n    return 42;\n}\n",
            "nested_classes": (
                "class Outer {\n"
                "public:\n"
                "    class Inner {\n"
                "        void method() {}\n"
                "    };\n"
                "};\n"
            ),
            "class_with_multiple_methods": (
                "class Calculator {\n"
                "public:\n"
                "    int add(int a, int b) { return a + b; }\n"
                "    int subtract(int a, int b) { return a - b; }\n"
                "};\n"
            ),
            "deeply_nested": (
                "class L1 {\n"
                "    class L2 {\n"
                "        class L3 {\n"
                "            class L4 {\n"
                "                void method() {}\n"
                "            };\n"
                "        };\n"
                "    };\n"
                "};\n"
            ),
            "unicode_identifiers": (
                "class Ñame {\n" "public:\n" "    void métod() {}\n" "};\n"
            ),
            # C++-specific scenarios
            "namespace": (
                "namespace Math {\n"
                "    int multiply(int a, int b) {\n"
                "        return a * b;\n"
                "    }\n"
                "}\n"
            ),
            "nested_namespace": (
                "namespace Outer {\n"
                "    namespace Inner {\n"
                "        class Nested {};\n"
                "    }\n"
                "}\n"
            ),
            "struct": (
                "struct Point {\n"
                "    int x;\n"
                "    int y;\n"
                "    void method() {}\n"
                "};\n"
            ),
            "mixed_elements": (
                "namespace App {\n"
                "    class MyClass {\n"
                "    public:\n"
                "        void method() {}\n"
                "    };\n"
                "    int function() { return 0; }\n"
                "}\n"
            ),
        },
    }


@pytest.fixture(scope="function")
def cpp_template_samples() -> dict[str, str]:
    """C++ template code samples organized by complexity.

    Each sample demonstrates a specific C++ template feature.
    Used to test that template_declaration nodes are properly recognized
    as ancestor nodes in chunk context.

    Returns:
        dict: Mapping of template type names to C++ code snippets
              - template_function: Basic function template
              - template_class: Basic class template
              - template_default_args: Template with default arguments
              - template_non_type_param: Template with non-type parameter
              - template_template_param: Template with template parameter
              - template_nested_in_class: Template nested inside a class
              - template_specialization: Template specialization
              - template_variadic: Variadic template (C++11)
              - template_multiple_params: Multiple type parameters
    """
    return {
        "template_function": """
template<typename T>
T max(T a, T b) { return (a > b) ? a : b; }
        """,
        "template_class": """
template<typename T>
class Container { T value; };
        """,
        "template_default_args": """
template<typename T = int>
class Container { };
        """,
        "template_non_type_param": """
template<int N>
class Array { };
        """,
        "template_template_param": """
template<template<typename> class C>
class Wrapper { };
        """,
        "template_nested_in_class": """
class Outer {
public:
    template<typename T>
    class Inner { };
};
        """,
        "template_specialization": """
template<>
class Container<int> { int special; };
        """,
        "template_variadic": """
template<typename... Args>
class Tuple { };
        """,
        "template_multiple_params": """
template<typename T, typename U>
class Pair { };
        """,
    }


@pytest.fixture(scope="function")
def cpp_lambda_samples() -> dict[str, str]:
    """C++ lambda code samples organized by complexity.

    Each sample demonstrates a specific C++ lambda feature.
    Used to test that lambda_expression nodes are properly recognized
    as function-like ancestor nodes in chunk context.

    Returns:
        dict: Mapping of lambda type names to C++ code snippets
              - lambda_basic: Basic lambda without capture
              - lambda_capture: Lambda with capture clause
              - lambda_generic_c14: Generic lambda (C++14 auto parameters)
              - lambda_explicit_return: Lambda with explicit return type
              - lambda_in_function: Lambda inside a function
              - lambda_nested: Nested lambda expressions
              - lambda_in_stl: Lambda used in STL algorithm
              - lambda_in_template: Lambda in template context
              - template_lambda_interaction: Template containing lambda
    """
    return {
        "lambda_basic": """
auto f = [](int x) { return x * 2; };
        """,
        "lambda_capture": """
int mult = 3;
auto g = [mult](int x) { return x * mult; };
        """,
        "lambda_generic_c14": """
auto f = [](auto x) { return x * 2; };
        """,
        "lambda_explicit_return": """
auto f = [](int x) -> double { return x * 2.5; };
        """,
        "lambda_in_function": """
void func() {
    auto h = [](int x) { return x; };
}
        """,
        "lambda_nested": """
auto outer = []() {
    auto inner = []() { return 42; };
    return inner;
};
        """,
        "lambda_in_stl": """
std::sort(v.begin(), v.end(), [](int a, int b) { return a < b; });
        """,
        "lambda_in_template": """
template<typename T>
void f() {
    auto l = [](T x) { return x; };
}
        """,
        "template_lambda_interaction": """
template<typename T>
class Processor {
public:
    void run() {
        auto l = [](T x) { };
    }
};
        """,
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


@pytest.fixture
def cpp_builder(language_samples: dict[str, dict[str, str]]) -> object:
    """Provide a C++ AST builder for testing.

    Returns an ASTChunkBuilder configured for C++ parsing.

    Args:
        language_samples: The language_samples fixture (unused but indicates dependency)

    Returns:
        Configured ASTChunkBuilder instance for C++
    """
    from astchunk.astchunk_builder import ASTChunkBuilder

    return ASTChunkBuilder(
        max_chunk_size=512,
        language="cpp",
        metadata_template="default",
    )
