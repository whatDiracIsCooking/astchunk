# C++ Node Types - Quick Reference

## Essential Node Types for astchunk

### Primary Chunk Types
```python
CHUNK_TYPES = {
    "class_specifier",       # class MyClass {};
    "struct_specifier",      # struct MyStruct {};
    "namespace_definition",  # namespace MyNamespace {}
    "function_definition",   # void func() {}, methods, constructors, destructors
    "enum_specifier",        # enum MyEnum {};
    "union_specifier",       # union MyUnion {};
}
```

### Identifier Extraction

| Node Type | Identifier Child Node | Example |
|-----------|----------------------|---------|
| `class_specifier` | `type_identifier` | `Calculator` |
| `struct_specifier` | `type_identifier` | `Point` |
| `namespace_definition` | `namespace_identifier` | `Math` |
| `enum_specifier` | `type_identifier` | `Color` |
| `union_specifier` | `type_identifier` | `Data` |
| `function_definition` | **COMPLEX** - see below | varies |

### Function Name Extraction (Special Handling Required!)

For `function_definition`, find `function_declarator` child, then check first named child:

| First Child Type | Extract Name From | Example |
|-----------------|-------------------|---------|
| `identifier` | Direct text | `myFunction` |
| `field_identifier` | Direct text | `method` (in class) |
| `destructor_name` | Full text or `identifier` child | `~MyClass` |
| `qualified_identifier` | Last `identifier` child | `MyClass::method` → `method` |

### Body Extraction

| Node Type | Body Child Node |
|-----------|-----------------|
| `class_specifier` | `field_declaration_list` |
| `struct_specifier` | `field_declaration_list` |
| `namespace_definition` | `declaration_list` |
| `function_definition` | `compound_statement` |
| `enum_specifier` | `enumerator_list` |
| `union_specifier` | `field_declaration_list` |

## Critical Differences from Other Languages

### DO NOT CONFUSE!
- ❌ `class_declaration` → **WRONG** (Java uses this)
- ✅ `class_specifier` → **CORRECT** (C++ uses this)

### Python Comparison
- Python: `class_definition`, `function_definition`
- C++: `class_specifier`, `function_definition`

### Java Comparison
- Java: `class_declaration`, `method_declaration`
- C++: `class_specifier`, `function_definition`

## Template Declarations

Templates wrap other declarations:
```
template_declaration
├── template_parameter_list
└── class_specifier / function_definition
```

**Decision needed**: Extract inner node or use template_declaration as chunk?

## Verification

Verified with:
- tree-sitter-cpp version 0.23.4
- Test scripts in `/docs/research/`
- Run: `python3 docs/research/cpp_node_research.py`

## Implementation Notes

1. Function names require custom extraction logic (not just `identifier`)
2. Namespaces are first-class chunks (unique to C++)
3. Constructors and destructors are `function_definition` (not separate types)
4. Template handling strategy TBD
5. Consider preserving qualified names for context

---

For complete details, see: `CPP_NODE_TYPE_REFERENCE.md`
