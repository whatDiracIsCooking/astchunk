#!/usr/bin/env python3
"""Test how to extract function names from function_definition nodes."""

import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser

CPP_LANGUAGE = Language(tscpp.language())
parser = Parser(CPP_LANGUAGE)

def print_node_details(node, indent=0):
    """Print node with children."""
    prefix = "  " * indent
    text = node.text.decode('utf8')[:40].replace('\n', '\\n')
    print(f"{prefix}{node.type} [{text}...]")
    for child in node.children:
        if child.is_named:
            print_node_details(child, indent + 1)

def find_node_by_type(node, target_type):
    """Find first node of target type."""
    if node.type == target_type:
        return node
    for child in node.children:
        result = find_node_by_type(child, target_type)
        if result:
            return result
    return None

# Test different function types
test_cases = [
    ("Regular function", "void myFunction() {}"),
    ("Class method", "class C { void method() {} };"),
    ("Constructor", "class C { C() {} };"),
    ("Destructor", "class C { ~C() {} };"),
    ("Qualified method", "void MyClass::method() {}"),
    ("Template function", "template<typename T> void func() {}"),
]

print("=" * 80)
print("FUNCTION NAME EXTRACTION PATTERNS")
print("=" * 80)
print()

for desc, code in test_cases:
    print(f"\n{desc}: {code}")
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
    
    for func in functions:
        print(f"\nfunction_definition structure:")
        print_node_details(func, 0)
        
        # Find function_declarator
        declarator = find_node_by_type(func, "function_declarator")
        if declarator:
            print(f"\nName extraction path:")
            for child in declarator.children:
                if child.is_named:
                    text = child.text.decode('utf8')
                    print(f"  declarator child: {child.type:30} = '{text}'")
                    
                    # If it's a destructor_name, show its structure
                    if child.type == "destructor_name":
                        for subchild in child.children:
                            if subchild.is_named:
                                print(f"    destructor_name child: {subchild.type:20} = '{subchild.text.decode('utf8')}'")
                    
                    # If it's qualified_identifier, show its structure
                    if child.type == "qualified_identifier":
                        for subchild in child.children:
                            if subchild.is_named:
                                print(f"    qualified_identifier child: {subchild.type:20} = '{subchild.text.decode('utf8')}'")

