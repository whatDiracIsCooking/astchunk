#!/usr/bin/env python3
"""Research script to identify tree-sitter-cpp node type names."""

import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser

# Initialize parser
CPP_LANGUAGE = Language(tscpp.language())
parser = Parser(CPP_LANGUAGE)

# Sample C++ constructs to analyze
test_cases = {
    "simple_class": """
class Calculator {
public:
    int add(int a, int b) { return a + b; }
    Calculator() {}
    ~Calculator() {}
};
""",
    "struct": """
struct Point {
    int x, y;
    void method() {}
};
""",
    "namespace": """
namespace Math {
    int add(int a, int b) { return a + b; }
}
""",
    "nested_namespace": """
namespace Outer {
    namespace Inner {
        class Nested {};
    }
}
""",
    "template_class": """
template<typename T>
class Container {
    T value;
public:
    void set(T v) { value = v; }
};
""",
    "function": """
int add(int a, int b) {
    return a + b;
}
""",
    "template_function": """
template<typename T>
T max(T a, T b) {
    return a > b ? a : b;
}
""",
    "enum": """
enum Color { RED, GREEN, BLUE };
""",
    "enum_class": """
enum class Status { OK, ERROR };
""",
    "typedef": """
typedef int Integer;
typedef struct { int x, y; } Point;
""",
    "using_declaration": """
using Integer = int;
""",
    "method_definition": """
class MyClass {
    void method();
};
void MyClass::method() {}
""",
    "access_specifiers": """
class Test {
private:
    int x;
protected:
    int y;
public:
    int z;
};
""",
}

def print_tree(node, indent=0, max_depth=6):
    """Print the syntax tree."""
    if indent > max_depth:
        return
    
    prefix = "  " * indent
    node_info = f"{prefix}{node.type}"
    
    # Add text for leaf nodes or small nodes
    if node.child_count == 0 or len(node.text) < 50:
        text = node.text.decode('utf8').replace('\n', '\\n')
        node_info += f" [{text}]"
    
    print(node_info)
    
    for child in node.children:
        print_tree(child, indent + 1, max_depth)

def find_nodes_of_type(node, node_type, results=None):
    """Find all nodes of a specific type."""
    if results is None:
        results = []
    
    if node.type == node_type:
        results.append(node)
    
    for child in node.children:
        find_nodes_of_type(child, node_type, results)
    
    return results

def analyze_construct(name, code):
    """Analyze a C++ construct and print its AST."""
    print(f"\n{'=' * 80}")
    print(f"Analyzing: {name}")
    print(f"{'=' * 80}")
    print("Code:")
    print(code)
    print("\nAST:")
    
    tree = parser.parse(bytes(code, "utf8"))
    print_tree(tree.root_node)
    
    # Find key node types
    print("\n--- Key Node Types ---")
    for child in tree.root_node.children:
        if child.type != 'comment':
            print(f"Top-level: {child.type}")
            # Print first level children
            for grandchild in child.children:
                if grandchild.is_named:
                    print(f"  Child: {grandchild.type}")

# Run analysis on all test cases
for name, code in test_cases.items():
    analyze_construct(name, code)

# Summary of critical node types
print("\n" + "=" * 80)
print("SUMMARY: Critical Node Types for astchunk")
print("=" * 80)

summary_tests = {
    "class_specifier": "class Test {};",
    "struct_specifier": "struct Test {};",
    "namespace_definition": "namespace Test {}",
    "function_definition": "void func() {}",
    "template_declaration": "template<typename T> class Test {};",
    "field_declaration": "class Test { int x; };",
    "constructor": "class Test { Test() {} };",
    "destructor": "class Test { ~Test() {} };",
}

print("\nNode type verification:")
for expected_type, code in summary_tests.items():
    tree = parser.parse(bytes(code, "utf8"))
    root = tree.root_node
    # Find the first named child
    for child in root.children:
        if child.is_named:
            actual_type = child.type
            match = "✓" if expected_type in code else "?"
            print(f"  {expected_type}: actual={actual_type} {match}")
            break

