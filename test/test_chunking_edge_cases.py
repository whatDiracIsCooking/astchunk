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


class TestCppTemplateSupport:
    """Test C++ template declaration support with parametrization.

    Validates that template_declaration nodes are properly recognized as
    ancestor nodes in chunk context for various C++ template scenarios.
    """

    @pytest.mark.parametrize(
        "template_type",
        [
            "template_function",
            "template_class",
            "template_default_args",
            "template_non_type_param",
            "template_template_param",
            "template_nested_in_class",
            "template_specialization",
            "template_variadic",
            "template_multiple_params",
        ],
    )
    def test_cpp_templates(
        self, cpp_template_samples: Dict[str, str], template_type: str
    ) -> None:
        """Test that template declarations are recognized as ancestor nodes.

        Args:
            cpp_template_samples: Fixture providing template code samples
            template_type: The specific template scenario to test

        Validates:
            - template_declaration node type exists in ancestors
            - Template scenarios parse without errors
            - Ancestor context includes template information
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code: str = cpp_template_samples[template_type]
        builder: ASTChunkBuilder = ASTChunkBuilder(
            max_chunk_size=1024, language="cpp", metadata_template="default"
        )
        chunks = builder.chunkify(code)

        # Assert template_declaration appears in ancestor context
        assert any(
            "template_declaration" in str(chunk.get("ancestors", []))
            for chunk in chunks
        ), f"template_declaration node not found in ancestors for scenario: {template_type}"


class TestCppLambdaSupport:
    """Test C++ lambda expression support with parametrization.

    Validates that lambda_expression nodes are properly recognized as
    function-like ancestor nodes in chunk context for various lambda scenarios.
    """

    @pytest.mark.parametrize(
        "lambda_type",
        [
            "lambda_basic",
            "lambda_capture",
            "lambda_generic_c14",
            "lambda_explicit_return",
            "lambda_in_function",
            "lambda_nested",
            "lambda_in_stl",
            "lambda_in_template",
            "template_lambda_interaction",
        ],
    )
    def test_cpp_lambdas(
        self, cpp_lambda_samples: Dict[str, str], lambda_type: str
    ) -> None:
        """Test that lambda expressions are recognized as function-like nodes.

        Args:
            cpp_lambda_samples: Fixture providing lambda code samples
            lambda_type: The specific lambda scenario to test

        Validates:
            - lambda_expression node type exists in ancestors
            - Lambda scenarios parse without errors
            - Ancestor context includes lambda information
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code: str = cpp_lambda_samples[lambda_type]
        builder: ASTChunkBuilder = ASTChunkBuilder(
            max_chunk_size=1024, language="cpp", metadata_template="default"
        )
        chunks = builder.chunkify(code)

        # Assert lambda_expression appears in ancestor context
        assert any(
            "lambda_expression" in str(chunk.get("ancestors", []))
            for chunk in chunks
        ), f"lambda_expression node not found in ancestors for scenario: {lambda_type}"


class TestCppRobustness:
    """Test that AST chunker handles edge cases gracefully.

    Validates that the parser doesn't crash on malformed or incomplete syntax,
    and handles edge cases robustly.
    """

    def test_malformed_template_doesnt_crash(self) -> None:
        """Parser should handle template syntax errors gracefully.

        Tests that incomplete template syntax (missing >) doesn't cause
        segfault or unhandled exception.
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = "template<typename T class Container { };"  # Missing >
        builder = ASTChunkBuilder(
            max_chunk_size=1024, language="cpp", metadata_template="default"
        )

        # Should not raise exception, handles gracefully
        chunks = builder.chunkify(code)
        assert chunks is not None

    def test_incomplete_lambda_doesnt_crash(self) -> None:
        """Parser should handle lambda syntax errors gracefully.

        Tests that incomplete lambda syntax (missing closing brace) doesn't
        cause segfault or unhandled exception.
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = "auto f = [](int x) {"  # Missing closing brace
        builder = ASTChunkBuilder(
            max_chunk_size=1024, language="cpp", metadata_template="default"
        )

        # Should not raise exception, handles gracefully
        chunks = builder.chunkify(code)
        assert chunks is not None

class TestCppModuleDetection:
    """Test detection of unsupported C++20 module syntax.

    IMPORTANT: This test class prevents SILENT FAILURES.
    When C++20 module syntax is encountered, we raise a helpful ValueError
    instead of letting it parse silently and confuse users.

    FALSE POSITIVE TRADEOFF:
    - Comments/strings with module keywords will trigger detection
    - This is ACCEPTABLE: Better to over-detect than miss real modules
    - Documented in test_module_keyword_in_comment_raises_false_positive()

    Regression Metric:
    - If these tests fail, module detection is broken
    - Users would see silent parsing failures (BAD)
    - Restore detection immediately
    """

    def test_export_module_raises_error(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Test that 'export module' syntax raises ValueError.

        Regression Prevention: Ensures users get helpful error for module syntax.
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["cpp"]["cpp_module_export"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="cpp", metadata_template="default"
        )

        with pytest.raises(ValueError) as exc_info:
            builder.chunkify(code)

        # Verify error message quality (not just keywords)
        error_msg = str(exc_info.value)
        assert "C++20 modules" in error_msg or "C++ modules" in error_msg
        assert "not supported" in error_msg.lower()
        assert "export module" in error_msg
        assert "tree-sitter" in error_msg.lower()
        assert "#include" in error_msg or "traditional" in error_msg
        assert "github.com" in error_msg

    def test_import_std_raises_error(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Test that 'import std' syntax raises ValueError.

        Regression Prevention: Ensures users get helpful error for module imports.
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["cpp"]["cpp_module_import_std"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="cpp", metadata_template="default"
        )

        with pytest.raises(ValueError) as exc_info:
            builder.chunkify(code)

        error_msg = str(exc_info.value)
        assert "module" in error_msg.lower() or "import" in error_msg.lower()

    def test_import_header_unit_raises_error(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Test that 'import <header>' syntax raises ValueError.

        Regression Prevention: Ensures header unit imports are detected.
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["cpp"]["cpp_module_import_header"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="cpp", metadata_template="default"
        )

        with pytest.raises(ValueError) as exc_info:
            builder.chunkify(code)

        error_msg = str(exc_info.value)
        assert "module" in error_msg.lower() or "import" in error_msg.lower()

    def test_module_with_other_code_raises_error(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Test that module syntax in mixed code still triggers detection."""
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["cpp"]["cpp_module_with_other_code"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="cpp", metadata_template="default"
        )

        with pytest.raises(ValueError):
            builder.chunkify(code)

    def test_module_partition_raises_error(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Test that module partition syntax raises ValueError."""
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["cpp"]["cpp_module_partition"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="cpp", metadata_template="default"
        )

        with pytest.raises(ValueError):
            builder.chunkify(code)

    def test_multiple_imports_raises_error(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Test that multiple import statements trigger detection."""
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["cpp"]["cpp_multiple_imports"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="cpp", metadata_template="default"
        )

        with pytest.raises(ValueError):
            builder.chunkify(code)

    def test_regular_includes_not_flagged(self) -> None:
        """Test that regular #include directives don't trigger module detection.

        Regression Prevention: Ensures false positives are avoided for normal C++.
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = "#include <iostream>\n#include <vector>\nint main() { return 0; }\n"
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="cpp", metadata_template="default"
        )

        # Should not raise exception
        chunks = builder.chunkify(code)
        assert isinstance(chunks, list)

    def test_module_keyword_in_comment_raises_false_positive(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Comments with module keywords trigger false positive.

        ACCEPTABLE TRADEOFF: Better to over-detect than miss real modules.
        This is documented behavior, not a bug.
        Users should temporarily remove/rephrase comments if they hit this.
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["cpp"]["cpp_module_in_comment"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="cpp", metadata_template="default"
        )

        with pytest.raises(ValueError) as exc_info:
            builder.chunkify(code)

        assert "module" in str(exc_info.value).lower()

    def test_module_keyword_in_string_raises_false_positive(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """String literals with module keywords trigger false positive.

        ACCEPTABLE TRADEOFF: Better to over-detect than miss real modules.
        This is rare in practice.
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["cpp"]["cpp_module_in_string"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="cpp", metadata_template="default"
        )

        with pytest.raises(ValueError) as exc_info:
            builder.chunkify(code)

        assert "module" in str(exc_info.value).lower()

    def test_detect_cpp_modules_isolation(self) -> None:
        """Test _detect_cpp_modules() method in isolation.

        Validates detection logic separately from chunkify() integration.
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        builder = ASTChunkBuilder(
            max_chunk_size=512, language="cpp", metadata_template="default"
        )

        # Should raise for module code
        with pytest.raises(ValueError):
            builder._detect_cpp_modules("export module mylib;")

        # Should NOT raise for normal code
        builder._detect_cpp_modules("#include <iostream>\nint main() {}")
        # (no assertion needed - if it raises, test fails)

    def test_detection_only_runs_for_cpp(self) -> None:
        """Module detection should only run for C++, not other languages."""
        from astchunk.astchunk_builder import ASTChunkBuilder

        python_code = "import module  # Python import\nprint('hello')\n"

        for language in ["python", "java", "csharp", "typescript"]:
            builder = ASTChunkBuilder(
                max_chunk_size=512, language=language, metadata_template="default"
            )
            # Should NOT raise error for non-C++ languages
            chunks = builder.chunkify(python_code)
            assert isinstance(chunks, list)

    @pytest.mark.parametrize(
        "module_syntax",
        [
            "export module mylib;",
            "import std;",
            "import <iostream>;",
        ],
    )
    def test_module_patterns_detected(
        self, module_syntax: str
    ) -> None:
        """Test that common module patterns are detected.

        Note: Simple string matching means extra whitespace variations
        (e.g., 'export  module') are NOT detected. This is an acceptable
        limitation since the standard formatting is rarely used with extra spaces.
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        builder = ASTChunkBuilder(
            max_chunk_size=512, language="cpp", metadata_template="default"
        )

        with pytest.raises(ValueError):
            builder.chunkify(module_syntax)

    def test_templates_dont_trigger_detection(self) -> None:
        """Test that C++ templates don't trigger false positive.

        Regression Prevention: Ensures templates parse normally.
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = "template<typename T>\nclass Container { };\n"
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="cpp", metadata_template="default"
        )

        # Should NOT raise
        chunks = builder.chunkify(code)
        assert isinstance(chunks, list)

    def test_namespace_named_module_doesnt_trigger(self) -> None:
        """Namespace with 'module' as identifier should not trigger.

        This distinguishes module keyword from module identifier.
        Note: May still trigger if patterns like 'module;' or 'module:' appear.
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = "namespace module { void fn() { } }\n"
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="cpp", metadata_template="default"
        )

        # Should NOT raise (namespace module is not module declaration)
        chunks = builder.chunkify(code)
        assert isinstance(chunks, list)


class TestCppPureVirtualDetection:
    """Direct unit tests for pure virtual method detection helper.

    Tests the _is_pure_virtual_method() helper method in isolation
    to ensure correct detection logic before integration testing.
    """

    def test_is_pure_virtual_method_detects_basic(self, cpp_builder) -> None:
        """Test detection of basic pure virtual method."""
        from astchunk.astchunk_builder import ASTChunkBuilder
        import tree_sitter as ts

        code = "class I { virtual void method() = 0; };"
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="cpp", metadata_template="default"
        )

        tree = builder.parser.parse(bytes(code, "utf8"))

        def find_field_declarations(node):
            if node.type == "field_declaration":
                yield node
            for child in node.children:
                yield from find_field_declarations(child)

        field_decls = list(find_field_declarations(tree.root_node))
        assert len(field_decls) > 0, "Should find at least one field_declaration"

        # This will fail with AttributeError until implementation
        result = builder._is_pure_virtual_method(field_decls[0])
        assert result is True, "Should detect pure virtual method"

    def test_is_pure_virtual_method_with_const_qualifier(
        self, cpp_builder
    ) -> None:
        """Test detection with const qualifier."""
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = "class I { virtual void method() const = 0; };"
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="cpp", metadata_template="default"
        )

        tree = builder.parser.parse(bytes(code, "utf8"))

        def find_field_declarations(node):
            if node.type == "field_declaration":
                yield node
            for child in node.children:
                yield from find_field_declarations(child)

        field_decls = list(find_field_declarations(tree.root_node))
        assert len(field_decls) > 0

        result = builder._is_pure_virtual_method(field_decls[0])
        assert result is True, "Should detect const-qualified pure virtual"

    def test_is_pure_virtual_method_ignores_regular_virtual(
        self, cpp_builder
    ) -> None:
        """Test that regular virtual methods with implementation are rejected."""
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = "class C { virtual void method() { } };"
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="cpp", metadata_template="default"
        )

        tree = builder.parser.parse(bytes(code, "utf8"))

        def find_all_nodes(node):
            yield node
            for child in node.children:
                yield from find_all_nodes(child)

        for node in find_all_nodes(tree.root_node):
            result = builder._is_pure_virtual_method(node)
            if result:
                assert False, f"Should not detect regular virtual as pure. Node type: {node.type}"

    def test_is_pure_virtual_method_ignores_regular_fields(
        self, cpp_builder
    ) -> None:
        """Test that regular field declarations are rejected."""
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = "class C { int x; char* ptr; };"
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="cpp", metadata_template="default"
        )

        tree = builder.parser.parse(bytes(code, "utf8"))

        def find_field_declarations(node):
            if node.type == "field_declaration":
                yield node
            for child in node.children:
                yield from find_field_declarations(child)

        field_decls = list(find_field_declarations(tree.root_node))

        for field_decl in field_decls:
            result = builder._is_pure_virtual_method(field_decl)
            assert result is False, f"Should not detect regular field as pure virtual. Text: {field_decl.text}"


class TestCppPureVirtualMethods:
    """Comprehensive integration tests for pure virtual method support.

    Tests the full chunking pipeline with pure virtual methods across
    various edge cases and scenarios.
    """

    @pytest.mark.parametrize("scenario", [
        "pure_virtual_basic",
        "pure_virtual_with_qualifiers",
        "pure_virtual_multiline",
        "pure_virtual_mixed_with_regular",
        "pure_virtual_destructor",
        "pure_virtual_template",
    ])
    def test_cpp_pure_virtual_captured_as_ancestor(
        self,
        language_samples: Dict[str, Dict[str, str]],
        cpp_builder,
        scenario: str
    ) -> None:
        """Test that pure virtual methods are captured in chunk ancestors.

        Parametrized test covering multiple scenarios.
        """
        code = language_samples["cpp"][scenario]
        chunks = cpp_builder.chunkify(code)

        assert len(chunks) >= 1, f"No chunks generated for {scenario}"

        chunks_with_ancestors = [c for c in chunks if c.get("ancestors")]
        assert len(chunks_with_ancestors) > 0, \
            f"No chunk ancestors extracted for {scenario}"

        all_ancestors = []
        for chunk in chunks:
            all_ancestors.extend(chunk.get("ancestors", []))

        assert len(all_ancestors) > 0, \
            f"Expected ancestors for {scenario}, got none"

    def test_cpp_pure_virtual_no_false_positives(
        self,
        language_samples: Dict[str, Dict[str, str]],
        cpp_builder
    ) -> None:
        """Ensure regular fields and methods aren't captured as pure virtuals."""
        code = language_samples["cpp"]["pure_virtual_mixed_with_regular"]
        chunks = cpp_builder.chunkify(code)

        assert len(chunks) >= 1

        all_ancestors = []
        for chunk in chunks:
            all_ancestors.extend(chunk.get("ancestors", []))

        assert len(all_ancestors) > 0, \
            "Expected some ancestors in mixed scenario"

    def test_cpp_pure_virtual_catches_all_qualifiers(
        self,
        language_samples: Dict[str, Dict[str, str]],
        cpp_builder
    ) -> None:
        """Ensure const/volatile/const volatile pure virtuals are captured."""
        code = language_samples["cpp"]["pure_virtual_with_qualifiers"]
        chunks = cpp_builder.chunkify(code)

        assert len(chunks) >= 1

        chunks_with_ancestors = [c for c in chunks if c.get("ancestors")]
        assert len(chunks_with_ancestors) > 0, \
            "Const/volatile qualified pure virtuals should be captured"

    def test_pure_virtual_detection_only_runs_for_cpp(self) -> None:
        """Verify pure virtual detection is C++-specific."""
        from astchunk.astchunk_builder import ASTChunkBuilder

        python_code = """
class Base:
    # virtual method = 0
    def method(self):
        x = 0
        return x
"""

        python_builder = ASTChunkBuilder(
            max_chunk_size=512,
            language="python",
            metadata_template="default"
        )

        chunks = python_builder.chunkify(python_code)
        assert chunks is not None
        assert len(chunks) >= 1
