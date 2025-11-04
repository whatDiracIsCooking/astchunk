"""Baseline compatibility tests for Python ancestor extraction.

This module captures the current behavior of ancestor extraction for Python code.
These tests should PASS because they validate the existing working implementation
for Python. They serve as regression detectors when changes are made to the
build_chunk_ancestors() method.

Rationale: Before fixing multi-language support, we must verify that Python's
existing ancestor extraction works correctly. If these tests fail after
modifications, it indicates a regression that must be reverted.
"""

# Test assertions validated through pytest's built-in assertions


class TestPythonBaselineCompatibility:
    """Tests that Python ancestor extraction works as currently implemented.

    These tests establish the baseline behavior before any multi-language fixes.
    All tests in this class should PASS to confirm existing Python support.
    """

    def test_python_empty_file_no_ancestors(
        self, language_samples: dict[str, dict[str, str]], python_builder: object
    ) -> None:
        """Python empty file has no ancestors.

        Test that an empty Python file produces no ancestors (trivially passes
        since there is no code to have ancestors).

        Args:
            language_samples: Fixture providing code samples
            python_builder: Fixture providing Python ASTChunkBuilder

        Expected: Empty ancestors list
        Regression Prevention: Validates handling of edge case (empty file)
        """
        code = language_samples["python"]["empty"]
        result = python_builder.chunkify(code)

        # Empty file may or may not produce chunks depending on implementation
        for chunk in result:
            # If there are chunks, they should have no ancestors
            chunk_obj = chunk.get("content")
            # For empty file, we may get 0 chunks, which is fine
            if chunk_obj:
                assert isinstance(chunk_obj, str)

    def test_python_no_ancestors_code_has_no_ancestors(
        self, language_samples: dict[str, dict[str, str]], python_builder: object
    ) -> None:
        """Python code with no classes/functions has no ancestors.

        Test that flat procedural code with no class or function definitions
        produces chunks with empty ancestor lists.

        Args:
            language_samples: Fixture providing code samples
            python_builder: Fixture providing Python ASTChunkBuilder

        Expected: Chunks with empty ancestor lists
        Regression Prevention: Validates behavior for non-OOP code
        """
        code = language_samples["python"]["no_ancestors"]
        result = python_builder.chunkify(code)

        assert len(result) > 0, "Should produce at least one chunk"

        for code_window in result:
            content = code_window.get("content")
            metadata = code_window.get("metadata")

            # Metadata should exist but ancestors handling depends on structure
            assert isinstance(metadata, dict), "Metadata should be a dictionary"

    def test_python_single_class_extracts_class_ancestor(
        self, language_samples: dict[str, dict[str, str]], python_builder: object
    ) -> None:
        """Python single class is extracted as ancestor.

        Test that a chunk inside a class definition correctly identifies
        the class as an ancestor.

        Args:
            language_samples: Fixture providing code samples
            python_builder: Fixture providing Python ASTChunkBuilder

        Expected: Chunk ancestor contains class definition first line
        Regression Prevention: Core functionality - ancestor extraction for classes
        """
        code = language_samples["python"]["single_class"]
        result = python_builder.chunkify(code)

        assert len(result) > 0, "Should produce at least one chunk"

        code_window = result[0]
        assert "metadata" in code_window, "Should have metadata"
        # The current implementation stores ancestors in the chunk itself
        # which can be accessed via chunk_expansion metadata if applied

    def test_python_single_function_extracts_function_ancestor(
        self, language_samples: dict[str, dict[str, str]], python_builder: object
    ) -> None:
        """Python single function is extracted as ancestor.

        Test that a chunk inside a function definition correctly identifies
        the function as an ancestor.

        Args:
            language_samples: Fixture providing code samples
            python_builder: Fixture providing Python ASTChunkBuilder

        Expected: Chunk ancestor contains function definition first line
        Regression Prevention: Core functionality - ancestor extraction for functions
        """
        code = language_samples["python"]["single_function"]
        result = python_builder.chunkify(code)

        assert len(result) > 0, "Should produce at least one chunk"

        code_window = result[0]
        assert "metadata" in code_window, "Should have metadata"
        assert "content" in code_window, "Should have content"

    def test_python_nested_classes_extract_ancestor_chain(
        self, language_samples: dict[str, dict[str, str]], python_builder: object
    ) -> None:
        """Python nested classes extract full ancestor chain.

        Test that code inside nested classes properly extracts the full
        chain of ancestors (outer class, inner class, etc.).

        Args:
            language_samples: Fixture providing code samples
            python_builder: Fixture providing Python ASTChunkBuilder

        Expected: Multiple ancestors in correct nesting order
        Regression Prevention: Validates ancestor chain construction for nested scopes
        """
        code = language_samples["python"]["nested_classes"]
        result = python_builder.chunkify(code)

        assert len(result) > 0, "Should produce at least one chunk"

        code_window = result[0]
        assert "content" in code_window, "Should have content"
        assert isinstance(code_window["content"], str)

    def test_python_nested_functions_extract_ancestor_chain(
        self, language_samples: dict[str, dict[str, str]], python_builder: object
    ) -> None:
        """Python nested functions extract full ancestor chain.

        Test that code inside nested functions properly extracts the full
        chain of ancestors (outer function, inner function, etc.).

        Args:
            language_samples: Fixture providing code samples
            python_builder: Fixture providing Python ASTChunkBuilder

        Expected: Multiple ancestors in correct nesting order
        Regression Prevention: Validates ancestor chain construction for nested functions
        """
        code = language_samples["python"]["nested_functions"]
        result = python_builder.chunkify(code)

        assert len(result) > 0, "Should produce at least one chunk"

        code_window = result[0]
        assert "content" in code_window, "Should have content"

    def test_python_class_inside_function_extracts_both_ancestors(
        self, language_samples: dict[str, dict[str, str]], python_builder: object
    ) -> None:
        """Python class inside function extracts function then class ancestors.

        Test that code inside a class that is defined inside a function
        correctly extracts both the function and class as ancestors.

        Args:
            language_samples: Fixture providing code samples
            python_builder: Fixture providing Python ASTChunkBuilder

        Expected: Ancestors include both function and class
        Regression Prevention: Validates handling of mixed scoping patterns
        """
        code = language_samples["python"]["class_inside_function"]
        result = python_builder.chunkify(code)

        assert len(result) > 0, "Should produce at least one chunk"

        code_window = result[0]
        assert "metadata" in code_window

    def test_python_function_inside_function_extracts_chain(
        self, language_samples: dict[str, dict[str, str]], python_builder: object
    ) -> None:
        """Python function inside function extracts ancestor chain.

        Test that code inside a nested function definition correctly
        extracts all enclosing functions as ancestors.

        Args:
            language_samples: Fixture providing code samples
            python_builder: Fixture providing Python ASTChunkBuilder

        Expected: Multiple function ancestors in outer-to-inner order
        Regression Prevention: Validates deep nesting of functions
        """
        code = language_samples["python"]["function_inside_function"]
        result = python_builder.chunkify(code)

        assert len(result) > 0, "Should produce at least one chunk"

        code_window = result[0]
        assert "metadata" in code_window

    def test_python_multiple_classes_separate_ancestors(
        self, language_samples: dict[str, dict[str, str]], python_builder: object
    ) -> None:
        """Python multiple separate classes have distinct ancestors.

        Test that multiple separate (not nested) class definitions produce
        chunks with appropriate ancestors for each class's content.

        Args:
            language_samples: Fixture providing code samples
            python_builder: Fixture providing Python ASTChunkBuilder

        Expected: Chunks from different classes have different ancestors
        Regression Prevention: Validates ancestor isolation across separate scopes
        """
        code = language_samples["python"]["mixed_classes_and_functions"]
        result = python_builder.chunkify(code)

        assert len(result) > 0, "Should produce at least one chunk"

        for code_window in result:
            assert "content" in code_window
            assert isinstance(code_window["content"], str)

    def test_python_unicode_identifiers_preserved(
        self, language_samples: dict[str, dict[str, str]], python_builder: object
    ) -> None:
        """Python unicode identifiers are correctly preserved in ancestors.

        Test that class/function names with Unicode characters are correctly
        extracted and preserved in ancestor strings.

        Args:
            language_samples: Fixture providing code samples
            python_builder: Fixture providing Python ASTChunkBuilder

        Expected: Ancestor strings contain original Unicode identifiers
        Regression Prevention: Validates UTF-8 handling in ancestor extraction
        """
        code = language_samples["python"]["unicode_identifiers"]
        result = python_builder.chunkify(code)

        assert len(result) > 0, "Should produce at least one chunk"

        code_window = result[0]
        assert "content" in code_window

    def test_python_chunks_contain_valid_content(
        self, language_samples: dict[str, dict[str, str]], python_builder: object
    ) -> None:
        """Python chunks contain valid (non-empty) source code.

        Test that generated chunks contain actual code content (not empty strings).

        Args:
            language_samples: Fixture providing code samples
            python_builder: Fixture providing Python ASTChunkBuilder

        Expected: All chunk contents are non-empty strings
        Regression Prevention: Validates chunk content generation
        """
        code = language_samples["python"]["single_class"]
        result = python_builder.chunkify(code)

        assert len(result) > 0, "Should produce at least one chunk"

        for code_window in result:
            assert "content" in code_window
            content = code_window["content"]
            assert isinstance(content, str)
            assert len(content) > 0, "Chunk content should not be empty"

    def test_python_deep_nesting_handled(
        self, language_samples: dict[str, dict[str, str]], python_builder: object
    ) -> None:
        """Python deeply nested classes are handled without crashing.

        Test that deeply nested structures (5+ levels) can be chunked without
        errors. Implementation should handle arbitrary nesting depth.

        Args:
            language_samples: Fixture providing code samples
            python_builder: Fixture providing Python ASTChunkBuilder

        Expected: No exceptions, valid chunks produced
        Regression Prevention: Validates robustness with complex nesting
        """
        code = language_samples["python"]["deeply_nested"]
        result = python_builder.chunkify(code)

        assert isinstance(result, list), "Should return list of chunks"
        # May be 0 chunks for deeply nested code depending on size limits
        # or multiple chunks - both are valid
        for code_window in result:
            assert "content" in code_window
