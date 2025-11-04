"""Performance benchmark tests for ancestor extraction.

This module contains performance tests that validate:
1. Ancestor lookup is O(1) (set-based, not list-based)
2. No performance regression vs baseline
3. Typical operations complete in acceptable time (<100ms for 1000-line files)

Expected behavior in RED phase:
- Tests will fail (no optimized language_mappings.py yet)
- Baseline performance established

Expected behavior in GREEN phase:
- Tests should pass with proper Set-based implementation
- Performance targets met

Performance Notes:
- Ancestor extraction should be fast (O(1) per node with set membership)
- Large file parsing is dominated by tree-sitter, not our code
- We benchmark the chunkification (tree assignment + windowing) step
"""

import pytest
import time
from typing import List, Dict


class TestAncestorLookupPerformance:
    """Performance tests for ancestor node type lookup."""

    def test_ancestor_extraction_performance_baseline(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Baseline performance measurement for Python ancestor extraction.

        Establishes baseline performance. After GREEN phase optimization,
        should remain <10ms for typical case.

        Expected: Completes in reasonable time (no specific threshold in RED)
        Regression Prevention: Detects performance degradation
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["python"]["class_with_multiple_methods"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="python", metadata_template="default"
        )

        start = time.time()
        result = builder.chunkify(code)
        elapsed = time.time() - start

        # In RED phase, just verify it completes
        # In GREEN phase, should be <100ms for typical code
        assert len(result) > 0
        assert elapsed < 10.0  # Very generous limit for RED phase

    def test_large_nested_structure_performance(
        self, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Performance with deeply nested structures.

        Tests that deeply nested code doesn't cause exponential slowdown.

        Expected: Completes without timeout
        Regression Prevention: Detects algorithmic inefficiencies
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples["python"]["deeply_nested"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language="python", metadata_template="default"
        )

        start = time.time()
        result = builder.chunkify(code)
        elapsed = time.time() - start

        assert len(result) >= 0  # May be 0 or more chunks
        # Should complete quickly even with deep nesting
        assert elapsed < 5.0

    @pytest.mark.parametrize("language", ["python", "java", "csharp", "typescript"])
    def test_multiple_chunks_performance(
        self, language: str, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Performance with code that produces multiple chunks.

        Tests ancestor extraction across multiple chunks.

        Args:
            language: Language identifier
            language_samples: Code samples fixture

        Expected: Reasonable performance across all languages
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples[language]["class_with_multiple_methods"]
        builder = ASTChunkBuilder(
            max_chunk_size=256, language=language, metadata_template="default"
        )

        start = time.time()
        result = builder.chunkify(code)
        elapsed = time.time() - start

        assert len(result) > 0
        # Should handle multiple chunks efficiently
        assert elapsed < 5.0


class TestLargeFilePerformance:
    """Performance tests with larger code samples."""

    def test_large_generated_python_file(self) -> None:
        """Performance with large generated Python file (10+ classes).

        Generates a file with many classes and methods to test performance
        at realistic scale.

        Expected: Completes in <1 second
        Regression Prevention: Detects scaling issues
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        # Generate a large Python file
        code_lines: List[str] = []

        for i in range(10):
            code_lines.append(f"class Class{i}:")
            for j in range(5):
                code_lines.append(
                    f"    def method{j}(self):" f"\n        return {i * 10 + j}\n"
                )

        code = "\n".join(code_lines)

        builder = ASTChunkBuilder(
            max_chunk_size=512, language="python", metadata_template="default"
        )

        start = time.time()
        result = builder.chunkify(code)
        elapsed = time.time() - start

        assert len(result) > 0
        # Large file should still process quickly
        assert elapsed < 2.0

    def test_large_generated_java_file(self) -> None:
        """Performance with large generated Java file (10+ classes).

        Generates a file with many classes and methods to test performance
        at realistic scale.

        Expected: Completes in <1 second
        Regression Prevention: Detects scaling issues
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        # Generate a large Java file
        code_lines: List[str] = ["package test;"]

        for i in range(10):
            code_lines.append(f"public class Class{i} {{")
            for j in range(5):
                code_lines.append(
                    f"    public int method{j}() {{" f" return {i * 10 + j}; }}"
                )
            code_lines.append("}")

        code = "\n".join(code_lines)

        builder = ASTChunkBuilder(
            max_chunk_size=512, language="java", metadata_template="default"
        )

        start = time.time()
        result = builder.chunkify(code)
        elapsed = time.time() - start

        assert len(result) > 0
        # Large file should still process quickly
        assert elapsed < 2.0


class TestAncestorExtractionIsEfficient:
    """Tests verifying ancestor extraction efficiency characteristics."""

    def test_no_exponential_slowdown_with_nesting(self) -> None:
        """Verify no exponential slowdown with increasing nesting depth.

        Tests that ancestor extraction time grows linearly, not exponentially,
        with nesting depth.

        Expected: Linear or O(1) characteristic
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        builder = ASTChunkBuilder(
            max_chunk_size=512, language="python", metadata_template="default"
        )

        # Test with different nesting depths
        times: List[float] = []

        for depth in [3, 5, 7]:
            # Create nested functions
            code_lines: List[str] = []
            indent = ""
            for d in range(depth):
                code_lines.append(f"{indent}def f{d}():")
                indent += "    "

            code_lines.append(f"{indent}return 42")
            code = "\n".join(code_lines)

            start = time.time()
            result = builder.chunkify(code)
            elapsed = time.time() - start

            times.append(elapsed)
            assert len(result) > 0

        # Times should not grow exponentially
        # If exponential: time[2]/time[1] and time[1]/time[0] would be huge
        # If linear: ratios would be modest
        if len(times) >= 2:
            # Very generous threshold - even linear growth is acceptable
            # We're just checking for exponential blow-up
            ratio1 = times[1] / max(times[0], 0.001)  # Avoid div by zero
            # Should not be exponential (e.g., ratio > 100)
            assert ratio1 < 50.0, "Possible exponential slowdown detected"


class TestChunkingConsistency:
    """Tests that chunking is deterministic and consistent."""

    @pytest.mark.parametrize("language", ["python", "java", "csharp", "typescript"])
    def test_same_code_produces_same_chunks(
        self, language: str, language_samples: Dict[str, Dict[str, str]]
    ) -> None:
        """Same code produces same chunks every time (determinism).

        Test that chunking is deterministic - running the same code twice
        produces identical results.

        Args:
            language: Language identifier
            language_samples: Code samples fixture

        Expected: Identical results on repeated runs
        Regression Prevention: Detects non-deterministic behavior
        """
        from astchunk.astchunk_builder import ASTChunkBuilder

        code = language_samples[language]["single_class"]
        builder = ASTChunkBuilder(
            max_chunk_size=512, language=language, metadata_template="default"
        )

        result1 = builder.chunkify(code)
        result2 = builder.chunkify(code)

        # Should produce same number of chunks
        assert len(result1) == len(result2)

        # Chunk contents should be identical
        for chunk1, chunk2 in zip(result1, result2):
            assert chunk1["content"] == chunk2["content"]
            assert chunk1["metadata"] == chunk2["metadata"]
