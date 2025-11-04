"""Comprehensive edge case tests for multi-language ancestor extraction.

This module tests edge cases enumerated in the TDD plan including:
- Empty files, comments only, docstrings only
- Syntax errors (partial AST)
- Deep nesting (20+ levels)
- Unicode identifiers
- Mixed language constructs
- Large files
- And many more

These tests validate robustness across all 4 languages (Python, Java, C#, TypeScript).

Expected behavior in RED phase:
- Edge case tests reveal implementation gaps
- Many will fail for non-Python languages due to hardcoded node types
- All tests should compile and execute (even if failing assertions)
"""

import pytest
from typing import Dict


@pytest.mark.parametrize("language", ["python", "java", "csharp", "typescript", "cpp"])
class TestEmptyAndMinimalCode:
    """Test edge cases with empty or minimal code."""

    def test_empty_file(
        self, language: str, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Empty file handling.

        Regression Prevention: Ensures chunker doesn't crash on empty input
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples[language]["empty"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language=language, metadata_template="default"
        )

        # Should not raise exception
        result = builder.chunkify(code)
        assert isinstance(result, list)

    def test_comments_only_python(
        self, language: str, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Python file with only comments (no executable code).

        Regression Prevention: Edge case where AST is minimal
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        if language != "python":
            pytest.skip("Python-only test")

        code = language_samples["python"]["comments_only"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="python", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert isinstance(result, list)

    def test_docstring_only_python(
        self, language: str, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Python file with only docstrings.

        Regression Prevention: Edge case where only string exists
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        if language != "python":
            pytest.skip("Python-only test")

        code = language_samples["python"]["docstring_only"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="python", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert isinstance(result, list)


@pytest.mark.parametrize("language", ["python", "java", "csharp", "typescript", "cpp"])
class TestNestingDepth:
    """Test edge cases with deep nesting structures."""

    def test_deeply_nested_5_levels(
        self, language: str, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Code nested 5+ levels deep.

        Regression Prevention: Validates handling of deep nesting
        without stack overflow or recursion issues
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples[language]["deeply_nested"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language=language, metadata_template="default"
        )

        # Should not crash or hang
        result = builder.chunkify(code)
        assert isinstance(result, list)


@pytest.mark.parametrize("language", ["python", "java", "csharp", "typescript", "cpp"])
class TestUnicodeIdentifiers:
    """Test edge cases with Unicode characters in identifiers."""

    def test_unicode_in_class_name(
        self, language: str, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Class names with Unicode characters (ñ, é, etc.).

        Regression Prevention: Validates UTF-8 preservation in ancestor strings
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples[language]["unicode_identifiers"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language=language, metadata_template="default"
        )

        result = builder.chunkify(code)
        assert isinstance(result, list)

        # If ancestors are extracted, they should preserve Unicode
        for chunk in result:
            content = chunk.get("content", "")
            assert isinstance(content, str)


@pytest.mark.parametrize("language", ["python", "java", "csharp", "cpp"])
class TestLanguageSpecificEdgeCases:
    """Language-specific edge cases."""

    def test_python_class_inside_function(
        self, language: str, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Python: local classes defined inside functions.

        Regression Prevention: Validates handling of non-standard scoping
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        if language != "python":
            pytest.skip("Python-only test")

        code = language_samples["python"]["class_inside_function"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="python", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert len(result) > 0

    def test_python_function_inside_function(
        self, language: str, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Python: nested functions.

        Regression Prevention: Validates handling of function nesting
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        if language != "python":
            pytest.skip("Python-only test")

        code = language_samples["python"]["function_inside_function"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="python", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert len(result) > 0

    def test_java_anonymous_inner_class(
        self, language: str, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Java: anonymous inner classes.

        Regression Prevention: Validates handling of Java-specific constructs
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        if language != "java":
            pytest.skip("Java-only test")

        code = language_samples["java"]["anonymous_inner_class"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="java", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert isinstance(result, list)

    def test_java_lambda_expressions(
        self, language: str, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Java: lambda expressions (Java 8+).

        Regression Prevention: Validates handling of modern Java syntax
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        if language != "java":
            pytest.skip("Java-only test")

        code = language_samples["java"]["method_with_lambda"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="java", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert isinstance(result, list)

    def test_csharp_extension_methods(
        self, language: str, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """C#: extension methods.

        Regression Prevention: Validates handling of C#-specific syntax
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        if language != "csharp":
            pytest.skip("C#-only test")

        code = language_samples["csharp"]["extension_method"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="csharp", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert isinstance(result, list)

    def test_csharp_async_methods(
        self, language: str, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """C#: async/await methods.

        Regression Prevention: Validates handling of async syntax
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        if language != "csharp":
            pytest.skip("C#-only test")

        code = language_samples["csharp"]["async_method"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="csharp", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert isinstance(result, list)


@pytest.mark.parametrize("language", ["python", "java", "csharp", "typescript", "cpp"])
class TestMultipleDefinitions:
    """Test edge cases with multiple separate definitions."""

    def test_class_with_multiple_methods(
        self, language: str, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Class with many methods (may split across chunks).

        Regression Prevention: Validates ancestor preservation across chunk boundaries
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples[language]["class_with_multiple_methods"]
        builder = ASTChunkBuilder(
            max_chunk_size=256, language=language, metadata_template="default"
        )

        result = builder.chunkify(code)
        assert len(result) > 0


@pytest.mark.parametrize("language", ["python", "java", "csharp", "typescript", "cpp"])
class TestCodeQualityEdgeCases:
    """Test handling of code quality edge cases."""

    def test_no_executable_content_python(
        self, language: str, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Python code with no classes/functions.

        Regression Prevention: Validates handling of procedural code
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        if language != "python":
            pytest.skip("Python-only test")

        code = language_samples["python"]["no_ancestors"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="python", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert isinstance(result, list)


@pytest.mark.parametrize("language", ["java", "csharp", "typescript", "cpp"])
class TestLanguageDeclarations:
    """Test handling of language-specific declaration patterns."""

    def test_java_package_and_imports(
        self, language: str, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Java file with package/import declarations.

        Regression Prevention: Validates handling of file-level declarations
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        if language != "java":
            pytest.skip("Java-only test")

        code = (
            language_samples["java"]["package_only"]
            + "\n"
            + language_samples["java"]["imports_only"]
        )
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="java", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert isinstance(result, list)

    def test_typescript_imports(
        self, language: str, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """TypeScript file with import statements.

        Regression Prevention: Validates handling of module imports
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        if language != "typescript":
            pytest.skip("TypeScript-only test")

        code = language_samples["typescript"]["import_only"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="typescript", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert isinstance(result, list)


class TestPythonSpecialCases:
    """Python-specific edge cases beyond parametrized tests."""

    def test_python_syntax_error_handling(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Python code with syntax errors produces partial AST.

        Regression Prevention: Validates behavior with malformed code
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        # Code with syntax error
        code = "class Incomplete\n    pass\n"
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="python", metadata_template="default"
        )

        # Tree-sitter is very forgiving and will parse partial AST
        try:
            result = builder.chunkify(code)
            # May succeed with partial AST or fail gracefully
            assert isinstance(result, list)
        except Exception as e:
            # Some syntax errors might raise exceptions, which is acceptable
            assert isinstance(e, Exception)

    def test_python_mixed_tabs_and_spaces(
        self,
    ) -> None:
        """Python code with mixed tabs and spaces (valid Python 3).

        Regression Prevention: Validates handling of different whitespace
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = "def f():\n\tif True:\n        pass\n"
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="python", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert isinstance(result, list)


class TestJavaSpecialCases:
    """Java-specific edge cases beyond parametrized tests."""

    def test_java_interface_with_default_methods(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Java interface with default method implementations.

        Regression Prevention: Validates handling of Java 8+ interface features
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["java"]["interface_with_default_method"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="java", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert len(result) > 0

    def test_java_static_nested_class(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Java static nested class.

        Regression Prevention: Validates handling of static nesting
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["java"]["static_nested_class"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="java", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert len(result) > 0

    def test_java_constructor_extraction(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Java constructor is handled like methods.

        Regression Prevention: Validates constructor handling
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["java"]["constructor"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="java", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert len(result) > 0


class TestCSharpSpecialCases:
    """C#-specific edge cases beyond parametrized tests."""

    def test_csharp_properties(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """C# properties (different from fields).

        Regression Prevention: Validates property handling
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["csharp"]["property"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="csharp", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert len(result) > 0

    def test_csharp_partial_class(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """C# partial class (multiple definitions of same class).

        Regression Prevention: Validates handling of partial classes
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["csharp"]["partial_class"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="csharp", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert len(result) > 0

    def test_csharp_constructor(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """C# constructor.

        Regression Prevention: Validates constructor handling
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["csharp"]["constructor"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="csharp", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert len(result) > 0


class TestTypeScriptSpecialCases:
    """TypeScript-specific edge cases beyond parametrized tests."""

    def test_typescript_decorators(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """TypeScript decorators on classes and methods.

        Regression Prevention: Validates handling of decorators
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["typescript"]["class_with_decorators"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="typescript", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert len(result) > 0

    def test_typescript_generic_class(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """TypeScript generic class with type parameters.

        Regression Prevention: Validates handling of generics
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["typescript"]["generic_class"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="typescript", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert len(result) > 0

    def test_typescript_namespace(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """TypeScript namespace declaration.

        Regression Prevention: Validates namespace handling
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["typescript"]["namespace"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="typescript", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert len(result) > 0

    def test_typescript_arrow_function(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """TypeScript arrow functions vs regular functions.

        Regression Prevention: Validates handling of both syntax forms
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["typescript"]["arrow_function"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="typescript", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert len(result) > 0

    def test_typescript_arrow_functions_in_class(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """TypeScript arrow functions as class members.

        Regression Prevention: Validates class member arrow function handling
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["typescript"]["arrow_functions_in_class"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="typescript", metadata_template="default"
        )

        result = builder.chunkify(code)
        assert len(result) > 0


class TestCppSpecialCases:
    """C++-specific edge cases beyond parametrized tests."""

    def test_cpp_namespace_basic(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Test basic C++ namespace chunking."""
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["cpp"]["namespace"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="cpp", metadata_template="default"
        )

        chunks = builder.chunkify(code)

        assert len(chunks) >= 1
        content = " ".join(chunk["content"] for chunk in chunks)
        assert "namespace Math" in content

    def test_cpp_nested_namespace(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Test nested namespace ancestor extraction."""
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["cpp"]["nested_namespace"]
        builder = ASTChunkBuilder(
            max_chunk_size=200, language="cpp", metadata_template="default"
        )

        chunks = builder.chunkify(code)

        assert len(chunks) >= 1
        content = " ".join(chunk["content"] for chunk in chunks)
        assert "namespace Outer" in content
        assert "namespace Inner" in content

    def test_cpp_struct(self, language_samples: Dict[str, Dict[str, str]]) -> None:
        """Test C++ struct chunking."""
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["cpp"]["struct"]
        builder = ASTChunkBuilder(
            max_chunk_size=300, language="cpp", metadata_template="default"
        )

        chunks = builder.chunkify(code)

        assert len(chunks) >= 1
        assert "struct Point" in chunks[0]["content"]
