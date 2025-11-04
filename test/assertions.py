"""Helper assertion functions for astchunk tests.

This module provides reusable assertion helpers that make test code more readable
and maintainable. These are NOT pytest fixtures - they are pure helper functions
that encapsulate common assertion patterns used across multiple test modules.

Important: This module should be imported by test modules, not used as a fixture.
Fixtures should remain in conftest.py.
"""

from typing import Any, List


def assert_chunk_ancestors(
    chunk: Any, expected_ancestors: List[str], message: str = ""
) -> None:
    """Assert that a chunk's ancestors match expected values.

    Args:
        chunk: ASTChunk object to verify
        expected_ancestors: List of expected ancestor strings (first lines)
        message: Optional custom message if assertion fails

    Raises:
        AssertionError: If chunk.chunk_ancestors does not match expected_ancestors
    """
    assert isinstance(
        chunk.chunk_ancestors, list
    ), f"chunk_ancestors should be a list, got {type(chunk.chunk_ancestors)}"

    assert (
        chunk.chunk_ancestors == expected_ancestors
    ), f"Expected ancestors {expected_ancestors}, but got {chunk.chunk_ancestors}. {message}"


def assert_chunk_count(chunks: List[Any], expected_count: int, message: str = "") -> None:
    """Assert that the number of chunks matches expected count.

    Args:
        chunks: List of ASTChunk objects or code windows
        expected_count: Expected number of chunks
        message: Optional custom message if assertion fails

    Raises:
        AssertionError: If chunk count does not match expected
    """
    assert isinstance(chunks, list), f"chunks should be a list, got {type(chunks)}"

    assert (
        len(chunks) == expected_count
    ), f"Expected {expected_count} chunks, but got {len(chunks)}. {message}"


def assert_chunk_metadata(
    chunk: Any, expected_keys: List[str], message: str = ""
) -> None:
    """Assert that a chunk's metadata contains expected keys.

    Args:
        chunk: ASTChunk object to verify
        expected_keys: List of keys expected in metadata dict
        message: Optional custom message if assertion fails

    Raises:
        AssertionError: If metadata keys do not match expected
    """
    assert hasattr(
        chunk, "metadata"
    ), f"chunk does not have 'metadata' attribute. {message}"

    metadata = chunk.metadata
    assert isinstance(metadata, dict), f"metadata should be a dict, got {type(metadata)}"

    for key in expected_keys:
        assert key in metadata, (
            f"Expected key '{key}' in metadata, but got keys {list(metadata.keys())}. {message}"
        )


def assert_chunk_text_not_empty(chunk: Any, message: str = "") -> None:
    """Assert that a chunk's text is not empty.

    Args:
        chunk: ASTChunk object to verify
        message: Optional custom message if assertion fails

    Raises:
        AssertionError: If chunk text is empty or None
    """
    assert hasattr(chunk, "chunk_text"), f"chunk does not have 'chunk_text' attribute. {message}"

    assert chunk.chunk_text, f"chunk_text should not be empty. {message}"

    assert isinstance(chunk.chunk_text, str), (
        f"chunk_text should be a string, got {type(chunk.chunk_text)}. {message}"
    )


def assert_chunk_size_valid(chunk: Any, message: str = "") -> None:
    """Assert that a chunk's size is a valid positive number.

    Args:
        chunk: ASTChunk object to verify
        message: Optional custom message if assertion fails

    Raises:
        AssertionError: If chunk size is not a valid positive number
    """
    assert hasattr(chunk, "chunk_size"), f"chunk does not have 'chunk_size' attribute. {message}"

    assert isinstance(
        chunk.chunk_size, int
    ), f"chunk_size should be int, got {type(chunk.chunk_size)}. {message}"

    assert chunk.chunk_size >= 0, f"chunk_size should be non-negative, got {chunk.chunk_size}. {message}"


def assert_chunks_have_proper_order(
    chunks: List[Any], message: str = ""
) -> None:
    """Assert that chunks maintain proper line ordering.

    Args:
        chunks: List of ASTChunk objects to verify
        message: Optional custom message if assertion fails

    Raises:
        AssertionError: If chunks are not in proper line order
    """
    if len(chunks) <= 1:
        return

    for i in range(len(chunks) - 1):
        current_end = chunks[i].end_line
        next_start = chunks[i + 1].start_line
        assert (
            current_end < next_start
        ), f"Chunk {i} ends at line {current_end}, but chunk {i+1} starts at line {next_start}. {message}"


def assert_ancestor_is_string(ancestor: Any, message: str = "") -> None:
    """Assert that an ancestor value is a string.

    Args:
        ancestor: Ancestor value to verify
        message: Optional custom message if assertion fails

    Raises:
        AssertionError: If ancestor is not a string
    """
    assert isinstance(
        ancestor, str
    ), f"Ancestor should be string, got {type(ancestor)}. {message}"


def assert_ancestors_are_first_lines(
    chunk: Any, expected_count: int = None, message: str = ""
) -> None:
    """Assert that ancestors appear to be first lines (no newlines).

    Args:
        chunk: ASTChunk object to verify
        expected_count: Optional expected number of ancestors
        message: Optional custom message if assertion fails

    Raises:
        AssertionError: If ancestors contain unexpected newlines or wrong count
    """
    for i, ancestor in enumerate(chunk.chunk_ancestors):
        assert isinstance(ancestor, str), (
            f"Ancestor {i} should be string, got {type(ancestor)}. {message}"
        )
        assert (
            "\n" not in ancestor
        ), f"Ancestor {i} contains newline: {repr(ancestor)}. {message}"

    if expected_count is not None:
        assert (
            len(chunk.chunk_ancestors) == expected_count
        ), f"Expected {expected_count} ancestors, got {len(chunk.chunk_ancestors)}. {message}"


def assert_empty_ancestors(chunk: Any, message: str = "") -> None:
    """Assert that a chunk has no ancestors.

    Args:
        chunk: ASTChunk object to verify
        message: Optional custom message if assertion fails

    Raises:
        AssertionError: If chunk has ancestors
    """
    assert (
        len(chunk.chunk_ancestors) == 0
    ), f"Expected empty ancestors, but got {chunk.chunk_ancestors}. {message}"
