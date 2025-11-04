#!/usr/bin/env python3
"""
Verification script for C++ template_declaration node detection.

This script verifies that tree-sitter-cpp correctly identifies template_declaration
nodes in various C++ template scenarios. The output is structured JSON format that
can be imported by automated tests.

Output Format:
    {
        "timestamp": "ISO 8601 timestamp",
        "parser_version": "tree-sitter-cpp version",
        "test_results": [
            {
                "name": "scenario name",
                "code": "C++ code snippet",
                "expected_node": "template_declaration",
                "found_nodes": ["node types found"],
                "status": "PASS" or "FAIL"
            },
            ...
        ],
        "summary": {
            "total": count,
            "passed": count,
            "failed": count,
            "all_pass": boolean
        }
    }
"""

import json
import sys
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

# Try to import tree-sitter
try:
    import tree_sitter as ts
    import tree_sitter_cpp as tscpp
except ImportError:
    print("ERROR: tree-sitter or tree-sitter-cpp not installed", file=sys.stderr)
    sys.exit(1)


class CppTemplateVerifier:
    """Verifies C++ template_declaration node detection."""

    def __init__(self):
        """Initialize the tree-sitter C++ parser."""
        try:
            self.parser = ts.Parser(ts.Language(tscpp.language()))
        except Exception as e:
            print(f"ERROR: Failed to initialize C++ parser: {e}", file=sys.stderr)
            sys.exit(1)

    def get_parser_version(self) -> str:
        """Get tree-sitter-cpp parser version string."""
        try:
            import tree_sitter_cpp
            # Try to get version from module
            return getattr(tree_sitter_cpp, "__version__", "unknown")
        except Exception:
            return "unknown"

    def find_nodes_of_type(
        self, node: Any, node_type: str, results: Optional[List[str]] = None
    ) -> List[str]:
        """Recursively find all nodes of a given type in the AST."""
        if results is None:
            results = []

        if node.type == node_type:
            results.append(node_type)

        for child in node.children:
            self.find_nodes_of_type(child, node_type, results)

        return results

    def find_all_node_types(self, node: Any, types_set: Optional[set] = None) -> set:
        """Recursively find all node types in the AST."""
        if types_set is None:
            types_set = set()

        types_set.add(node.type)

        for child in node.children:
            self.find_all_node_types(child, types_set)

        return types_set

    def test_template_scenario(self, name: str, code: str) -> Dict[str, Any]:
        """Test a single template scenario and return results."""
        try:
            # Parse the code
            tree = self.parser.parse(code.encode())

            # Find template_declaration nodes
            template_nodes = self.find_nodes_of_type(tree.root_node, "template_declaration")

            # Get all node types for debugging
            all_nodes = self.find_all_node_types(tree.root_node)

            status = "PASS" if template_nodes else "FAIL"

            return {
                "name": name,
                "code": code.strip(),
                "expected_node": "template_declaration",
                "found_nodes": template_nodes if template_nodes else list(all_nodes),
                "status": status,
                "parse_error": False,
            }
        except Exception as e:
            return {
                "name": name,
                "code": code.strip(),
                "expected_node": "template_declaration",
                "found_nodes": [],
                "status": "FAIL",
                "parse_error": True,
                "error": str(e),
            }

    def run_verification(self) -> Dict[str, Any]:
        """Run all template verification tests and return structured results."""

        # 9 template scenarios from the plan
        test_scenarios = {
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

        # Run tests
        results = []
        for name, code in test_scenarios.items():
            result = self.test_template_scenario(name, code)
            results.append(result)

        # Calculate summary
        passed = sum(1 for r in results if r["status"] == "PASS")
        failed = len(results) - passed

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "parser_version": f"tree-sitter-cpp ({self.get_parser_version()})",
            "test_results": results,
            "summary": {
                "total": len(results),
                "passed": passed,
                "failed": failed,
                "all_pass": failed == 0,
            },
        }


def main():
    """Run template verification and output JSON results."""
    verifier = CppTemplateVerifier()
    results = verifier.run_verification()

    # Output JSON (must be valid JSON for automated consumption)
    print(json.dumps(results, indent=2))

    # Return exit code based on all_pass
    if results["summary"]["all_pass"]:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
