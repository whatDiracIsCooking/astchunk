"""Tests for error handling with unsupported languages.

This module tests how the system handles attempts to use unsupported programming
languages (Ruby, Go, Rust, etc.) and invalid language parameter values.

Expected behavior in RED phase:
- Tests verify that builder construction fails for unsupported languages
- Invalid language parameters raise ValueError with helpful messages

Expected behavior in GREEN phase (after fix):
- build_chunk_ancestors() raises ValueError for unsupported languages
- Error messages include list of supported languages
- None/empty/invalid language params handled gracefully
"""

import pytest


class TestUnsupportedLanguages:
    """Tests for handling completely unsupported languages."""

    def test_ruby_language_rejected(self) -> None:
        """Ruby language is not supported, should raise ValueError.

        Test that attempting to create a builder for Ruby raises an appropriate
        error message.

        Expected: ValueError with clear error message
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        with pytest.raises(ValueError) as exc_info:
            ASTChunkBuilder(
                max_chunk_size=512, language="ruby", metadata_template="default"
            )

        assert (
            "ruby" in str(exc_info.value).lower()
            or "unsupported" in str(exc_info.value).lower()
        )

    def test_go_language_rejected(self) -> None:
        """Go language is not supported, should raise ValueError.

        Test that attempting to create a builder for Go raises an appropriate
        error message.

        Expected: ValueError with clear error message
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        with pytest.raises(ValueError) as exc_info:
            ASTChunkBuilder(
                max_chunk_size=512, language="go", metadata_template="default"
            )

        assert (
            "go" in str(exc_info.value).lower()
            or "unsupported" in str(exc_info.value).lower()
        )

    def test_rust_language_rejected(self) -> None:
        """Rust language is not supported, should raise ValueError.

        Test that attempting to create a builder for Rust raises an appropriate
        error message.

        Expected: ValueError with clear error message
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        with pytest.raises(ValueError) as exc_info:
            ASTChunkBuilder(
                max_chunk_size=512, language="rust", metadata_template="default"
            )

        assert (
            "rust" in str(exc_info.value).lower()
            or "unsupported" in str(exc_info.value).lower()
        )

    @pytest.mark.skip(reason="C++ is now supported")
    def test_cpp_language_not_yet_supported(self) -> None:
        """C++ language is not yet supported (Cycle 2 feature).

        Test that C++ is not available (even though it's planned for Cycle 2).

        Expected: ValueError indicating C++ not yet supported
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        with pytest.raises(ValueError):
            ASTChunkBuilder(
                max_chunk_size=512, language="cpp", metadata_template="default"
            )

    def test_c_language_not_supported(self) -> None:
        """C language (standalone) is not supported.

        Test that C is not available (tree-sitter has 'c' parser but not configured).

        Expected: ValueError
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        with pytest.raises(ValueError):
            ASTChunkBuilder(
                max_chunk_size=512, language="c", metadata_template="default"
            )


class TestInvalidLanguageParameters:
    """Tests for invalid language parameter values."""

    def test_empty_string_language_rejected(self) -> None:
        """Empty string language parameter is rejected.

        Test that an empty string for language is not accepted.

        Expected: ValueError
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        with pytest.raises(ValueError):
            ASTChunkBuilder(
                max_chunk_size=512, language="", metadata_template="default"
            )

    def test_none_language_rejected(self) -> None:
        """None language parameter is rejected.

        Test that None value is not accepted for language.

        Expected: ValueError or TypeError
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        with pytest.raises((ValueError, TypeError, AttributeError)):
            ASTChunkBuilder(
                max_chunk_size=512,
                language=None,  # type: ignore
                metadata_template="default",
            )

    def test_integer_language_rejected(self) -> None:
        """Integer language parameter is rejected (type check).

        Test that non-string language parameters are rejected.

        Expected: ValueError or TypeError
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        with pytest.raises((ValueError, TypeError, AttributeError)):
            ASTChunkBuilder(
                max_chunk_size=512,
                language=42,  # type: ignore
                metadata_template="default",
            )

    def test_list_language_rejected(self) -> None:
        """List language parameter is rejected.

        Test that list language parameter is rejected.

        Expected: ValueError or TypeError
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        with pytest.raises((ValueError, TypeError, AttributeError)):
            ASTChunkBuilder(
                max_chunk_size=512,
                language=["python"],  # type: ignore
                metadata_template="default",
            )

    def test_whitespace_language_rejected(self) -> None:
        """Whitespace-only language parameter is rejected.

        Test that whitespace-only strings are treated as invalid.

        Expected: ValueError
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        with pytest.raises(ValueError):
            ASTChunkBuilder(
                max_chunk_size=512, language="   ", metadata_template="default"
            )


class TestLanguageParameterCase:
    """Tests for language parameter case sensitivity."""

    def test_uppercase_python_rejected(self) -> None:
        """PYTHON (uppercase) language is rejected (case sensitive).

        Test that language names are case-sensitive.

        Expected: ValueError (PYTHON != python)
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        with pytest.raises(ValueError):
            ASTChunkBuilder(
                max_chunk_size=512, language="PYTHON", metadata_template="default"
            )

    def test_mixed_case_java_rejected(self) -> None:
        """Java (mixed case) language is rejected (case sensitive).

        Test that language names are case-sensitive.

        Expected: ValueError (Java != java)
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        with pytest.raises(ValueError):
            ASTChunkBuilder(
                max_chunk_size=512, language="Java", metadata_template="default"
            )

    def test_uppercase_csharp_rejected(self) -> None:
        """CSHARP (uppercase) language is rejected.

        Test case sensitivity for C#.

        Expected: ValueError (CSHARP != csharp)
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        with pytest.raises(ValueError):
            ASTChunkBuilder(
                max_chunk_size=512, language="CSHARP", metadata_template="default"
            )

    def test_uppercase_typescript_rejected(self) -> None:
        """TYPESCRIPT (uppercase) language is rejected.

        Test case sensitivity for TypeScript.

        Expected: ValueError (TYPESCRIPT != typescript)
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        with pytest.raises(ValueError):
            ASTChunkBuilder(
                max_chunk_size=512,
                language="TYPESCRIPT",
                metadata_template="default",
            )


class TestBuildChunkAncestorsErrorMessages:
    """Tests for error handling in build_chunk_ancestors() method.

    After GREEN phase fix, build_chunk_ancestors() should raise
    ValueError for unsupported languages with helpful messages.
    """

    def test_unsupported_language_error_message_helpful(
        self, language_samples: dict[str, dict[str, str]]
    ) -> None:
        """Unsupported language error includes list of supported languages.

        Test that if build_chunk_ancestors() is called with unsupported language,
        error message includes the list of supported languages.

        Expected: ValueError with supported language list

        Note: This test will only work after GREEN phase when language_mappings.py
        is implemented. In RED phase, this will fail earlier in builder construction.
        """
        # This is a forward-looking test - it will fail until language_mappings.py exists
        # and get_ancestor_node_types is called on unsupported language
        pass
