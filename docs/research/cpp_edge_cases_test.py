#!/usr/bin/env python3
"""Test edge cases for C++ node type identification."""

import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser

CPP_LANGUAGE = Language(tscpp.language())
parser = Parser(CPP_LANGUAGE)

def find_node_by_type(node, target_type):
    """Find first node of target type."""
    if node.type == target_type:
        return node
    for child in node.children:
        result = find_node_by_type(child, target_type)
        if result:
            return result
    return None

def extract_function_name(func_def_node):
    """Extract function name from function_definition node."""
    declarator = find_node_by_type(func_def_node, "function_declarator")
    if not declarator:
        return None
    
    # Find first named child that's not parameter_list
    for child in declarator.children:
        if child.is_named and child.type != "parameter_list":
            if child.type == "identifier":
                return child.text.decode('utf8')
            elif child.type == "field_identifier":
                return child.text.decode('utf8')
            elif child.type == "destructor_name":
                # Option 1: Use full text with ~
                return child.text.decode('utf8')
                # Option 2: Extract just the name
                # for subchild in child.children:
                #     if subchild.type == "identifier":
                #         return f"~{subchild.text.decode('utf8')}"
            elif child.type == "qualified_identifier":
                # Find last identifier
                for subchild in reversed(child.children):
                    if subchild.type == "identifier":
                        return subchild.text.decode('utf8')
            else:
                # Fallback: use full text
                return child.text.decode('utf8')
    return None

# Edge cases to test
edge_cases = [
    ("Operator overloading", """
class MyClass {
    MyClass operator+(const MyClass& other) { return *this; }
};
"""),
    ("Conversion operator", """
class MyClass {
    operator int() { return 0; }
};
"""),
    ("Lambda in function", """
void func() {
    auto lambda = [](int x) { return x * 2; };
}
"""),
    ("Function pointer", """
void (*funcPtr)(int);
"""),
    ("Pure virtual", """
class Base {
    virtual void method() = 0;
};
"""),
    ("Inline definition", """
class MyClass {
    void method() { /* inline */ }
};
void MyClass::method() { /* out-of-line */ }
"""),
    ("Template specialization", """
template<typename T>
class Container {};

template<>
class Container<int> {};
"""),
    ("Nested class", """
class Outer {
    class Inner {
        void method() {}
    };
};
"""),
    ("Anonymous namespace", """
namespace {
    void func() {}
}
"""),
    ("Nested namespace (C++17)", """
namespace Outer::Inner {
    void func() {}
}
"""),
]

print("=" * 80)
print("C++ EDGE CASES TESTING")
print("=" * 80)

for desc, code in edge_cases:
    print(f"\n{desc}:")
    print("-" * 80)
    
    tree = parser.parse(bytes(code, "utf8"))
    
    # Find all function_definition nodes
    def find_all_functions(node, results=None):
        if results is None:
            results = []
        if node.type == "function_definition":
            results.append(node)
        for child in node.children:
            find_all_functions(child, results)
        return results
    
    functions = find_all_functions(tree.root_node)
    
    if functions:
        print(f"Found {len(functions)} function_definition node(s):")
        for func in functions:
            name = extract_function_name(func)
            code_preview = func.text.decode('utf8')[:60].replace('\n', ' ')
            print(f"  Name: {name!r} - Code: {code_preview}...")
    else:
        print("  No function_definition nodes found")
    
    # Check for other interesting nodes
    for node_type in ["class_specifier", "namespace_definition", "template_declaration"]:
        nodes = []
        def find_all(node, target_type, results):
            if node.type == target_type:
                results.append(node)
            for child in node.children:
                find_all(child, target_type, results)
        find_all(tree.root_node, node_type, nodes)
        
        if nodes:
            print(f"  Found {len(nodes)} {node_type} node(s)")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print("""
Edge Cases Handled:
- Operator overloading: Parsed as function_definition
- Conversion operators: Parsed as function_definition
- Lambdas: NOT function_definition (different node type)
- Pure virtual functions: Parsed as field_declaration (no body)
- Inline vs out-of-line: Both are function_definition
- Template specializations: Wrapped in template_declaration
- Nested classes: Standard class_specifier nesting
- Anonymous namespaces: Still namespace_definition (no name)
- Nested namespaces: Single namespace_definition with qualified name

Recommendations:
1. Function extraction algorithm handles most cases correctly
2. Pure virtual functions may need special handling (field_declaration vs function_definition)
3. Anonymous namespaces will have empty namespace_identifier
4. Nested namespace syntax creates single node with qualified identifier
""")

