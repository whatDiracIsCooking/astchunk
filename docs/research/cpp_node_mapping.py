#!/usr/bin/env python3
"""Generate exact node type mappings for C++ in astchunk."""

import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser

CPP_LANGUAGE = Language(tscpp.language())
parser = Parser(CPP_LANGUAGE)

def get_node_type(code):
    """Parse code and return the type of the first named node."""
    tree = parser.parse(bytes(code, "utf8"))
    for child in tree.root_node.children:
        if child.is_named:
            return child.type
    return None

def find_node_by_type(node, target_type):
    """Recursively find first node of target type."""
    if node.type == target_type:
        return node
    for child in node.children:
        result = find_node_by_type(child, target_type)
        if result:
            return result
    return None

# Test constructs
tests = {
    "CLASS_NODE": "class MyClass {};",
    "STRUCT_NODE": "struct MyStruct {};",
    "NAMESPACE_NODE": "namespace MyNamespace {}",
    "FUNCTION_NODE": "void myFunction() {}",
    "TEMPLATE_CLASS_NODE": "template<typename T> class MyTemplate {};",
    "TEMPLATE_FUNCTION_NODE": "template<typename T> void myFunc() {}",
    "ENUM_NODE": "enum MyEnum { A, B };",
    "UNION_NODE": "union MyUnion { int a; float b; };",
}

print("=" * 80)
print("TREE-SITTER-CPP NODE TYPE MAPPINGS FOR ASTCHUNK")
print("=" * 80)
print()

for const_name, code in tests.items():
    node_type = get_node_type(code)
    print(f"{const_name:30} = '{node_type}'")

print()
print("=" * 80)
print("NESTED CONSTRUCTS (for identifying methods/functions)")
print("=" * 80)
print()

# Check what node types are used for methods inside classes
class_with_method = """
class MyClass {
public:
    void myMethod() {}
    MyClass() {}
    ~MyClass() {}
};
"""

tree = parser.parse(bytes(class_with_method, "utf8"))
class_node = find_node_by_type(tree.root_node, "class_specifier")
if class_node:
    field_list = find_node_by_type(class_node, "field_declaration_list")
    if field_list:
        print("Inside class_specifier > field_declaration_list:")
        for child in field_list.children:
            if child.is_named and child.type not in ['access_specifier', '{', '}']:
                text = child.text.decode('utf8').replace('\n', ' ')[:50]
                print(f"  {child.type:30} [{text}...]")

print()

# Check namespace contents
namespace_with_content = """
namespace MyNamespace {
    void func() {}
    class MyClass {};
}
"""

tree = parser.parse(bytes(namespace_with_content, "utf8"))
ns_node = find_node_by_type(tree.root_node, "namespace_definition")
if ns_node:
    decl_list = find_node_by_type(ns_node, "declaration_list")
    if decl_list:
        print("Inside namespace_definition > declaration_list:")
        for child in decl_list.children:
            if child.is_named and child.type not in ['{', '}']:
                text = child.text.decode('utf8').replace('\n', ' ')[:50]
                print(f"  {child.type:30} [{text}...]")

print()
print("=" * 80)
print("IDENTIFIER NODES")
print("=" * 80)
print()

# Check identifier node types
identifier_tests = {
    "class name": ("class MyClass {};", "class_specifier"),
    "struct name": ("struct MyStruct {};", "struct_specifier"),
    "namespace name": ("namespace MyNamespace {}", "namespace_definition"),
    "function name": ("void myFunc() {}", "function_definition"),
}

for desc, (code, parent_type) in identifier_tests.items():
    tree = parser.parse(bytes(code, "utf8"))
    parent_node = find_node_by_type(tree.root_node, parent_type)
    if parent_node:
        # Find the identifier child
        for child in parent_node.children:
            if child.is_named and 'identifier' in child.type:
                print(f"{desc:30} uses: {child.type:30} [value: {child.text.decode('utf8')}]")
                break

print()
print("=" * 80)
print("COMPARISON WITH OTHER LANGUAGES")
print("=" * 80)
print()

comparisons = """
Python:
  CLASS_NODE       = 'class_definition'
  FUNCTION_NODE    = 'function_definition'
  
Java:
  CLASS_NODE       = 'class_declaration'
  INTERFACE_NODE   = 'interface_declaration'
  METHOD_NODE      = 'method_declaration'
  FUNCTION_NODE    = 'method_declaration'
  
C++:
  CLASS_NODE       = 'class_specifier'
  STRUCT_NODE      = 'struct_specifier'
  NAMESPACE_NODE   = 'namespace_definition'
  FUNCTION_NODE    = 'function_definition'
  TEMPLATE_*_NODE  = 'template_declaration'
"""

print(comparisons)

print()
print("=" * 80)
print("CRITICAL FINDINGS FOR ASTCHUNK")
print("=" * 80)
print()

findings = """
1. CLASSES: Use 'class_specifier' (NOT 'class_declaration')
2. STRUCTS: Use 'struct_specifier'
3. NAMESPACES: Use 'namespace_definition' (confirmed!)
4. FUNCTIONS: Use 'function_definition'
5. TEMPLATES: Use 'template_declaration' (wraps class/function)
6. METHODS: Same as functions - 'function_definition' inside class
7. CONSTRUCTORS: Also 'function_definition'
8. DESTRUCTORS: Also 'function_definition'

IDENTIFIER EXTRACTION:
- class_specifier uses: type_identifier
- struct_specifier uses: type_identifier
- namespace_definition uses: namespace_identifier
- function_definition uses: identifier (inside function_declarator)

BODY EXTRACTION:
- class/struct body: field_declaration_list
- namespace body: declaration_list
- function body: compound_statement
"""

print(findings)

