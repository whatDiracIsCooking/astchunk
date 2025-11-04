# C++ Language Support Research for astchunk

This directory contains comprehensive research on tree-sitter-cpp node types for implementing C++ language support in astchunk.

## Documents

### 1. CPP_QUICK_REFERENCE.md
**Quick reference guide** - Start here!
- Essential node types at a glance
- Comparison with Python and Java
- One-page reference for implementation

### 2. CPP_NODE_TYPE_REFERENCE.md
**Complete technical reference** - Comprehensive documentation
- Detailed node type specifications
- AST structure diagrams
- Function name extraction algorithms
- Edge case documentation
- Comparison with other languages

### 3. IMPLEMENTATION_GUIDE.md
**Implementation guide** - Step-by-step instructions
- Code templates for CPPLanguageConfig
- Phased implementation strategy
- Testing strategy with test cases
- Integration instructions
- Performance considerations

## Verification Scripts

All findings have been verified using tree-sitter-cpp 0.23.4:

### cpp_node_research.py
Comprehensive AST analysis of all C++ constructs:
- Classes, structs, namespaces, functions
- Templates, enums, unions
- Detailed tree structure output

**Run**: `python3 cpp_node_research.py`

### cpp_node_mapping.py
Node type mapping verification:
- Confirms exact node type names
- Identifies identifier and body nodes
- Compares with Python and Java

**Run**: `python3 cpp_node_mapping.py`

### cpp_function_name_extraction.py
Function name extraction patterns:
- Regular functions vs methods
- Constructors and destructors
- Qualified names (MyClass::method)
- Shows exact AST structure for name extraction

**Run**: `python3 cpp_function_name_extraction.py`

### cpp_edge_cases_test.py
Edge case testing:
- Operator overloading
- Conversion operators
- Pure virtual functions
- Template specializations
- Anonymous namespaces
- Nested namespaces

**Run**: `python3 cpp_edge_cases_test.py`

## Key Findings Summary

### Critical Node Types
```python
CHUNK_TYPES = {
    "class_specifier",       # NOT "class_declaration"!
    "struct_specifier",
    "namespace_definition",  # Unique to C++
    "function_definition",   # Used for all function types
    "enum_specifier",
}
```

### Identifier Extraction
| Node Type | Identifier Node |
|-----------|----------------|
| class_specifier | type_identifier |
| struct_specifier | type_identifier |
| namespace_definition | namespace_identifier |
| function_definition | **COMPLEX** - see guides |

### Function Name Extraction (Special Handling Required!)
Function names require examining the function_declarator child:
- Regular function: `identifier`
- Class method: `field_identifier`
- Destructor: `destructor_name`
- Qualified method: `qualified_identifier`
- Operator: `operator_name`

## Quick Start

1. Read: `CPP_QUICK_REFERENCE.md`
2. Verify: Run all verification scripts
3. Implement: Follow `IMPLEMENTATION_GUIDE.md`
4. Reference: Use `CPP_NODE_TYPE_REFERENCE.md` for details

## Installation

```bash
pip install tree-sitter-cpp
```

## Dependencies

- tree-sitter >= 0.25.2
- tree-sitter-cpp >= 0.23.4

## Next Steps

1. Create `astchunk/languages/cpp.py`
2. Implement `CPPLanguageConfig` class
3. Add function name extraction logic
4. Register language in `__init__.py`
5. Add tests for C++ support
6. Update documentation

## Critical Warnings

⚠️ **C++ uses `class_specifier` NOT `class_declaration`**
- Python uses: `class_definition`
- Java uses: `class_declaration`
- C++ uses: `class_specifier` ← Different!

⚠️ **Function name extraction is complex**
- Cannot use simple identifier lookup
- Must check function_declarator child type
- See IMPLEMENTATION_GUIDE.md for algorithm

⚠️ **Namespaces are first-class chunks**
- C++ has namespace support
- Python and Java don't
- Use `namespace_definition` node type

## Verification

All research verified using:
- tree-sitter-cpp: 0.23.4
- tree-sitter: 0.25.2
- Python: 3.9+
- Date: 2025-11-04

To verify yourself:
```bash
cd docs/research
python3 cpp_node_research.py
python3 cpp_node_mapping.py
python3 cpp_function_name_extraction.py
python3 cpp_edge_cases_test.py
```

## Contact

For questions about this research, refer to:
- Implementation issues: See IMPLEMENTATION_GUIDE.md
- Node type questions: See CPP_NODE_TYPE_REFERENCE.md
- Quick lookups: See CPP_QUICK_REFERENCE.md

---

**Status**: Research complete, ready for implementation
**Last Updated**: 2025-11-04
**Version**: 1.0
