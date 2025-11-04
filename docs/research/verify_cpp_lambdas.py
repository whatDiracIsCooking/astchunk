#!/usr/bin/env python3
"""
Verification script for C++ lambda_expression node detection.

This script verifies that tree-sitter-cpp correctly identifies lambda_expression
nodes in various C++ lambda scenarios. The output is structured JSON format that
can be imported by automated tests.

Output Format:
    {
        "timestamp": "ISO 8601 timestamp",
        "parser_version": "tree-sitter-cpp version",
        "test_results": [
            {
                "name": "scenario name",
                "code": "C++ code snippet",
                "expected_node": "lambda_expression",
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


class CppLambdaVerifier:
    """Verifies C++ lambda_expression node detection."""

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

    def test_lambda_scenario(self, name: str, code: str) -> Dict[str, Any]:
        """Test a single lambda scenario and return results."""
        try:
            # Parse the code
            tree = self.parser.parse(code.encode())

            # Find lambda_expression nodes
            lambda_nodes = self.find_nodes_of_type(tree.root_node, "lambda_expression")

            # Get all node types for debugging
            all_nodes = self.find_all_node_types(tree.root_node)

            status = "PASS" if lambda_nodes else "FAIL"

            return {
                "name": name,
                "code": code.strip(),
                "expected_node": "lambda_expression",
                "found_nodes": lambda_nodes if lambda_nodes else list(all_nodes),
                "status": status,
                "parse_error": False,
            }
        except Exception as e:
            return {
                "name": name,
                "code": code.strip(),
                "expected_node": "lambda_expression",
                "found_nodes": [],
                "status": "FAIL",
                "parse_error": True,
                "error": str(e),
            }

    def run_verification(self) -> Dict[str, Any]:
        """Run all lambda verification tests and return structured results."""

        # 9 lambda scenarios from the plan
        test_scenarios = {
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

        # Run tests
        results = []
        for name, code in test_scenarios.items():
            result = self.test_lambda_scenario(name, code)
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
    """Run lambda verification and output JSON results."""
    verifier = CppLambdaVerifier()
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
