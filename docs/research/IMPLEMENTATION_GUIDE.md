# C++ Implementation Guide for astchunk

## Overview
This guide provides implementation details for adding C++ support to astchunk based on verified tree-sitter-cpp node types.

## Node Type Configuration

### Basic Configuration
```python
from astchunk.languages.base import LanguageConfig

class CPPLanguageConfig(LanguageConfig):
    """Language configuration for C++."""
    
    # Primary chunk types
    CHUNK_TYPES = {
        "class_specifier",
        "struct_specifier",
        "namespace_definition",
        "function_definition",
        "enum_specifier",
        # Optional: "union_specifier", "template_declaration"
    }
    
    # Identifier node mappings (simple cases)
    IDENTIFIER_NODES = {
        "class_specifier": "type_identifier",
        "struct_specifier": "type_identifier",
        "namespace_definition": "namespace_identifier",
        "enum_specifier": "type_identifier",
        "union_specifier": "type_identifier",
    }
    
    # Body node mappings
    BODY_NODES = {
        "class_specifier": "field_declaration_list",
        "struct_specifier": "field_declaration_list",
        "namespace_definition": "declaration_list",
        "function_definition": "compound_statement",
        "enum_specifier": "enumerator_list",
        "union_specifier": "field_declaration_list",
    }
```

## Function Name Extraction (Required Custom Logic)

Function names in C++ require special handling because the identifier type varies by context:

```python
def extract_function_name(self, node):
    """Extract function name from function_definition node.
    
    Returns the function name or None if it cannot be determined.
    Handles: regular functions, methods, constructors, destructors,
    operator overloading, and qualified names.
    """
    # Find function_declarator child
    declarator = None
    for child in node.children:
        if child.type == "function_declarator":
            declarator = child
            break
    
    if not declarator:
        return None
    
    # Find the name node (first named child before parameter_list)
    for child in declarator.children:
        if not child.is_named or child.type == "parameter_list":
            continue
            
        # Regular function or constructor
        if child.type == "identifier":
            return child.text.decode('utf8')
        
        # Class method
        elif child.type == "field_identifier":
            return child.text.decode('utf8')
        
        # Destructor
        elif child.type == "destructor_name":
            return child.text.decode('utf8')  # Includes ~ prefix
        
        # Qualified method (MyClass::method)
        elif child.type == "qualified_identifier":
            # Extract the final identifier (method name)
            for subchild in reversed(child.children):
                if subchild.type == "identifier":
                    return subchild.text.decode('utf8')
        
        # Operator overloading (operator+, operator[])
        elif child.type == "operator_name":
            return child.text.decode('utf8')
        
        # Fallback: use full text
        else:
            return child.text.decode('utf8')
    
    return None
```

## Override extract_identifier Method

```python
def extract_identifier(self, node):
    """Extract identifier from a node.
    
    Overrides base class to handle function_definition specially.
    """
    # Special handling for functions
    if node.type == "function_definition":
        return self.extract_function_name(node)
    
    # Standard handling for other types
    if node.type in self.IDENTIFIER_NODES:
        identifier_type = self.IDENTIFIER_NODES[node.type]
        for child in node.children:
            if child.type == identifier_type:
                return child.text.decode('utf8')
    
    return None
```

## Edge Cases to Handle

### 1. Anonymous Namespaces
```cpp
namespace {
    void func() {}
}
```
- Node type: `namespace_definition`
- No `namespace_identifier` child
- Handle by returning empty string or placeholder like "<anonymous>"

### 2. Conversion Operators
```cpp
operator int() { return 0; }
```
- Node type: `function_definition`
- function_declarator has no simple identifier child
- May need to check for `primitive_type` or other type nodes
- Fallback to full text: "operator int"

### 3. Pure Virtual Functions
```cpp
virtual void method() = 0;
```
- Node type: `field_declaration` (NOT `function_definition`)
- No body present
- May want to skip these or handle separately

### 4. Template Declarations
```cpp
template<typename T>
class Container {};
```
- Node type: `template_declaration`
- Wraps inner `class_specifier` or `function_definition`
- **Decision required**: 
  - Option A: Skip template_declaration, extract inner node
  - Option B: Treat template_declaration as chunk type
  - Option C: Extract both as separate chunks

### 5. Nested Namespaces (C++17)
```cpp
namespace Outer::Inner {
    void func() {}
}
```
- Creates single `namespace_definition` 
- `namespace_identifier` contains qualified name "Outer::Inner"
- No need for special handling

## Recommended Implementation Strategy

### Phase 1: Basic Support
1. Implement basic chunk types:
   - `class_specifier`
   - `struct_specifier`
   - `function_definition`
   - `namespace_definition`

2. Implement function name extraction with these cases:
   - Regular functions (`identifier`)
   - Class methods (`field_identifier`)
   - Constructors (`identifier`)
   - Destructors (`destructor_name`)

3. Test on simple C++ files

### Phase 2: Extended Support
1. Add qualified name handling:
   - Out-of-class method definitions (`qualified_identifier`)

2. Add operator overloading support:
   - Check for `operator_name` node type

3. Handle anonymous namespaces

4. Add enum and union support

### Phase 3: Advanced Features
1. Template handling strategy
2. Conversion operator support
3. Consider pure virtual functions
4. Optimize for nested structures

## Testing Strategy

### Test Files Provided
1. `cpp_node_research.py` - Comprehensive AST exploration
2. `cpp_node_mapping.py` - Node type verification
3. `cpp_function_name_extraction.py` - Function name patterns
4. `cpp_edge_cases_test.py` - Edge case handling

### Suggested Test Cases
```cpp
// Test file: test_cpp_chunks.cpp

// 1. Simple class
class Calculator {
public:
    int add(int a, int b) { return a + b; }
};

// 2. Struct
struct Point {
    int x, y;
    void move(int dx, int dy) { x += dx; y += dy; }
};

// 3. Namespace
namespace Math {
    int multiply(int a, int b) { return a * b; }
}

// 4. Free function
void globalFunction() {}

// 5. Constructor/Destructor
class MyClass {
    MyClass() {}
    ~MyClass() {}
};

// 6. Out-of-class definition
class MyClass {
    void method();
};
void MyClass::method() {}

// 7. Nested namespace
namespace Outer {
    namespace Inner {
        void func() {}
    }
}

// 8. Template (if supported)
template<typename T>
class Container {
    T value;
};
```

### Expected Chunks
```python
expected_chunks = [
    {"type": "class_specifier", "name": "Calculator"},
    {"type": "function_definition", "name": "add"},
    {"type": "struct_specifier", "name": "Point"},
    {"type": "function_definition", "name": "move"},
    {"type": "namespace_definition", "name": "Math"},
    {"type": "function_definition", "name": "multiply"},
    {"type": "function_definition", "name": "globalFunction"},
    {"type": "class_specifier", "name": "MyClass"},
    {"type": "function_definition", "name": "MyClass"},  # constructor
    {"type": "function_definition", "name": "~MyClass"},  # destructor
    {"type": "function_definition", "name": "method"},  # out-of-class
    {"type": "namespace_definition", "name": "Outer"},
    {"type": "namespace_definition", "name": "Inner"},
    {"type": "function_definition", "name": "func"},
]
```

## Integration with Existing Code

### File Location
Create: `astchunk/languages/cpp.py`

### Language Registration
Update `astchunk/languages/__init__.py`:
```python
from .cpp import CPPLanguageConfig

LANGUAGE_CONFIGS = {
    "python": PythonLanguageConfig,
    "java": JavaLanguageConfig,
    "cpp": CPPLanguageConfig,
    "c++": CPPLanguageConfig,  # Alias
}
```

### Tree-sitter Integration
Ensure tree-sitter-cpp is available:
```python
# In language config
def get_language(self):
    import tree_sitter_cpp as tscpp
    from tree_sitter import Language
    return Language(tscpp.language())
```

## Performance Considerations

1. **Caching**: Function name extraction may be called frequently - consider caching
2. **Node traversal**: Function extraction requires finding function_declarator - optimize if needed
3. **Large files**: Namespace chunks may be very large - consider max size limits

## Known Limitations

1. **Conversion operators**: May not extract name correctly in all cases
2. **Pure virtual functions**: Not identified as function_definition
3. **Template specializations**: Complex template syntax may need special handling
4. **Macros**: Preprocessor macros not handled by tree-sitter
5. **Multiple declarations**: `int a, b, c;` style declarations may need special handling

## References

- Complete documentation: `CPP_NODE_TYPE_REFERENCE.md`
- Quick reference: `CPP_QUICK_REFERENCE.md`
- Verification scripts: `cpp_*.py` files
- tree-sitter-cpp: https://github.com/tree-sitter/tree-sitter-cpp

