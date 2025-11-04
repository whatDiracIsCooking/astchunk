# Tree-Sitter-CPP Node Type Reference for astchunk

## Executive Summary

This document provides verified node type names from tree-sitter-cpp for implementing C++ language support in astchunk.

### Critical Node Types

| Construct | Node Type | Identifier Type | Body Type |
|-----------|-----------|-----------------|-----------|
| Class | `class_specifier` | `type_identifier` | `field_declaration_list` |
| Struct | `struct_specifier` | `type_identifier` | `field_declaration_list` |
| Namespace | `namespace_definition` | `namespace_identifier` | `declaration_list` |
| Function | `function_definition` | See Function Names | `compound_statement` |
| Template | `template_declaration` | (wraps inner type) | (wraps inner type) |
| Enum | `enum_specifier` | `type_identifier` | `enumerator_list` |
| Union | `union_specifier` | `type_identifier` | `field_declaration_list` |

### Key Differences from Other Languages

| Language | Class Node | Namespace Node | Function Node |
|----------|------------|----------------|---------------|
| Python | `class_definition` | N/A | `function_definition` |
| Java | `class_declaration` | N/A | `method_declaration` |
| C++ | `class_specifier` | `namespace_definition` | `function_definition` |

**CRITICAL**: C++ uses `class_specifier` (NOT `class_declaration`!)

---

## Detailed Node Type Specifications

### 1. Class Declarations

**Node Type**: `class_specifier`

**Structure**:
```
class_specifier
├── type_identifier           # Class name
└── field_declaration_list    # Body
    ├── access_specifier      # public, private, protected
    ├── field_declaration     # Member variables
    └── function_definition   # Methods, constructors, destructors
```

**Example**:
```cpp
class Calculator {
public:
    int add(int a, int b) { return a + b; }
    Calculator() {}
    ~Calculator() {}
};
```

**Verified**:
- Top-level node: `class_specifier`
- Name: `type_identifier` child
- Body: `field_declaration_list` child
- Methods inside are `function_definition` nodes

---

### 2. Struct Declarations

**Node Type**: `struct_specifier`

**Structure**:
```
struct_specifier
├── type_identifier           # Struct name
└── field_declaration_list    # Body
    ├── field_declaration     # Member variables
    └── function_definition   # Member functions
```

**Example**:
```cpp
struct Point {
    int x, y;
    void method() {}
};
```

**Verified**:
- Top-level node: `struct_specifier`
- Name: `type_identifier` child
- Body: `field_declaration_list` child
- Same structure as class_specifier

---

### 3. Namespace Declarations

**Node Type**: `namespace_definition`

**Structure**:
```
namespace_definition
├── namespace_identifier      # Namespace name
└── declaration_list          # Body
    ├── function_definition   # Free functions
    ├── class_specifier       # Classes
    └── namespace_definition  # Nested namespaces
```

**Example**:
```cpp
namespace Math {
    int add(int a, int b) { return a + b; }
    class Calculator {};
}
```

**Verified**:
- Top-level node: `namespace_definition`
- Name: `namespace_identifier` child
- Body: `declaration_list` child
- Can be nested

---

### 4. Function Definitions

**Node Type**: `function_definition`

**Structure**:
```
function_definition
├── <return_type>            # primitive_type, type_identifier, etc.
├── function_declarator      # Function signature
│   ├── <name_node>          # See "Function Name Extraction" below
│   └── parameter_list       # Parameters
└── compound_statement       # Function body
```

**Example**:
```cpp
int add(int a, int b) {
    return a + b;
}
```

**Verified**:
- Top-level node: `function_definition`
- Name: Complex (see Function Name Extraction section)
- Body: `compound_statement` child

---

### 5. Function Name Extraction (COMPLEX!)

Function names in C++ require different extraction strategies depending on context:

| Context | Declarator Child Type | Name Extraction |
|---------|----------------------|-----------------|
| Free function | `identifier` | Direct text |
| Class method | `field_identifier` | Direct text |
| Constructor | `identifier` | Direct text (matches class name) |
| Destructor | `destructor_name` | `identifier` child (with `~` prefix in full text) |
| Qualified method | `qualified_identifier` | `identifier` child (last part) |
| Template function | `identifier` | Direct text (template wraps function) |

**Example Structures**:

```
Regular function:
function_declarator
├── identifier ["myFunction"]
└── parameter_list

Class method:
function_declarator
├── field_identifier ["method"]
└── parameter_list

Destructor:
function_declarator
├── destructor_name ["~C"]
│   └── identifier ["C"]
└── parameter_list

Qualified method (out-of-class definition):
function_declarator
├── qualified_identifier ["MyClass::method"]
│   ├── namespace_identifier ["MyClass"]
│   └── identifier ["method"]
└── parameter_list
```

**Name Extraction Algorithm**:
1. Find `function_declarator` child of `function_definition`
2. Look for first named child (before `parameter_list`)
3. Extract based on type:
   - `identifier` → use directly
   - `field_identifier` → use directly
   - `destructor_name` → use full text OR extract `identifier` child
   - `qualified_identifier` → extract last `identifier` child
   - Other → use full text

---

### 6. Template Declarations

**Node Type**: `template_declaration`

**Structure**:
```
template_declaration
├── template_parameter_list   # <typename T, ...>
└── <inner_declaration>       # class_specifier, function_definition, etc.
```

**Examples**:
```cpp
template<typename T>
class Container {
    T value;
};

template<typename T>
T max(T a, T b) {
    return a > b ? a : b;
}
```

**Verified**:
- Top-level node: `template_declaration`
- Templates wrap the actual declaration (class/function)
- For astchunk: May want to treat the inner declaration as the chunk
- Alternative: Treat template_declaration itself as the chunk

---

### 7. Enum Declarations

**Node Type**: `enum_specifier`

**Examples**:
```cpp
enum Color { RED, GREEN, BLUE };
enum class Status { OK, ERROR };
```

**Structure**:
```
enum_specifier
├── type_identifier          # Enum name
└── enumerator_list          # Values
```

---

### 8. Union Declarations

**Node Type**: `union_specifier`

**Example**:
```cpp
union MyUnion {
    int a;
    float b;
};
```

**Structure**:
```
union_specifier
├── type_identifier          # Union name
└── field_declaration_list   # Members
```

---

## Implementation Recommendations for astchunk

### Suggested CHUNK_TYPES Configuration

```python
CHUNK_TYPES = {
    "class_specifier",       # Classes
    "struct_specifier",      # Structs
    "namespace_definition",  # Namespaces
    "function_definition",   # Functions, methods, constructors, destructors
    "enum_specifier",        # Enums
    "union_specifier",       # Unions
    # Consider: "template_declaration" or extract inner node
}
```

### Suggested IDENTIFIER_EXTRACTION

```python
IDENTIFIER_NODES = {
    "class_specifier": "type_identifier",
    "struct_specifier": "type_identifier",
    "namespace_definition": "namespace_identifier",
    "enum_specifier": "type_identifier",
    "union_specifier": "type_identifier",
    # function_definition requires custom logic
}
```

### Special Handling Required

1. **function_definition names**: Requires examining function_declarator child types
2. **template_declaration**: May want to extract inner node instead
3. **Qualified identifiers**: May want to preserve full qualification for context

### Body Extraction

```python
BODY_NODES = {
    "class_specifier": "field_declaration_list",
    "struct_specifier": "field_declaration_list",
    "namespace_definition": "declaration_list",
    "function_definition": "compound_statement",
    "enum_specifier": "enumerator_list",
    "union_specifier": "field_declaration_list",
}
```

---

## Verification Scripts

All findings in this document were verified using tree-sitter-cpp 0.23.4 with the following test scripts:

1. `/tmp/cpp_node_research.py` - Comprehensive AST analysis
2. `/tmp/cpp_node_mapping.py` - Node type mapping verification
3. `/tmp/cpp_function_name_extraction.py` - Function name extraction patterns

To reproduce:
```bash
pip install tree-sitter-cpp
python3 /tmp/cpp_node_research.py
python3 /tmp/cpp_node_mapping.py
python3 /tmp/cpp_function_name_extraction.py
```

---

## Comparison with Existing Language Configs

### Python (`tree-sitter-python`)
```python
CHUNK_TYPES = {"class_definition", "function_definition"}
```
- Simple, straightforward
- Both use `identifier` for names

### Java (`tree-sitter-java`)
```python
CHUNK_TYPES = {
    "class_declaration",
    "interface_declaration",
    "method_declaration",
    "constructor_declaration",
}
```
- More granular (separate method/constructor)
- Uses `identifier` for names

### C++ (proposed)
```python
CHUNK_TYPES = {
    "class_specifier",      # Note: NOT class_declaration
    "struct_specifier",
    "namespace_definition",
    "function_definition",  # Unified for all function types
}
```
- Must handle multiple identifier types
- Function names require complex extraction

---

## Critical Notes for Implementation

1. **"specifier" vs "declaration"**: C++ tree-sitter uses `class_specifier` not `class_declaration`

2. **Namespace support**: Critical for C++ - uses `namespace_definition`

3. **Function name complexity**: Cannot use simple `identifier` extraction - must implement special logic

4. **Template handling**: Decision needed on whether to chunk template_declaration or inner node

5. **Struct/Class equivalence**: Both use same body structure (`field_declaration_list`)

6. **Methods are functions**: No separate `method_definition` - all use `function_definition`

---

## Next Steps

1. Implement `CPPLanguageConfig` class
2. Add special function name extraction logic
3. Test on real C++ codebases
4. Decide on template_declaration handling strategy
5. Test with nested namespaces and complex hierarchies

