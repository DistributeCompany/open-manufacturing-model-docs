from enum import Enum, auto

class LocationType(Enum):
    """Enumeration of valid location types."""
    
    INTERNAL = auto() # Location within the manufacturing facility
    EXTERNAL = auto() # Location outside the manufacturing facility
    INVENTORY = auto() # Storage or warehouse location
    

import ast
import inspect
from enum import Enum
from typing import Dict

def get_enum_comments(enum_class: type) -> Dict[str, str]:
    """Extract inline comments for enum members using AST."""
    # Get the source code of the enum class
    try:
        source = inspect.getsource(enum_class)
    except (TypeError, OSError):
        return {}
    
    # Parse the source code into an AST
    tree = ast.parse(source)
    
    # Dictionary to store member comments
    member_comments = {}
    
    # Find the class definition
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Look for assignments (enum members) in the class body
            for item in node.body:
                if isinstance(item, ast.Assign):
                    # Get the member name
                    for target in item.targets:
                        if isinstance(target, ast.Name):
                            member_name = target.id
                            # Get the inline comment if it exists
                            if (hasattr(item, 'end_lineno') and 
                                hasattr(item, 'end_col_offset')):
                                # Extract comment from the same line
                                line = source.splitlines()[item.lineno - 1]
                                comment_start = line.find('#')
                                if comment_start != -1:
                                    comment = line[comment_start + 1:].strip()
                                    member_comments[member_name] = comment
    
    return member_comments

def generate_enum_doc(enum_class: type) -> str:
    """Generate markdown documentation for an Enum class."""
    doc_parts = []
    
    # Get comments for enum members
    member_comments = get_enum_comments(enum_class)
    
    # Enum name and description
    doc_parts.append(f"# {enum_class.__name__}\n")
    if enum_class.__doc__:
        doc_parts.append(f"{enum_class.__doc__.strip()}\n")
    
    # Enum values
    doc_parts.append("\n## Values\n")
    
    # Create a table of enum values
    doc_parts.append("| Value | Description |")
    doc_parts.append("|-------|-------------|")
    
    # Add each enum member with its comment
    for name, member in enum_class.__members__.items():
        description = member_comments.get(name, 'No description available')
        doc_parts.append(f"| `{name}` | {description} |")
    
    # Usage Example
    doc_parts.append("\n## Usage Example\n")
    doc_parts.append("```python")
    doc_parts.append(f"from omm import {enum_class.__name__}")
    doc_parts.append("")
    first_value = next(iter(enum_class.__members__))
    doc_parts.append(f"# Access enum value")
    doc_parts.append(f"value = {enum_class.__name__}.{first_value}")
    doc_parts.append("")
    doc_parts.append("# Value comparison")
    doc_parts.append(f"if value == {enum_class.__name__}.{first_value}:")
    doc_parts.append(f"    print(f'Value is {first_value}')")
    doc_parts.append("```\n")
    
    return '\n'.join(doc_parts)

# Test the documentation generation
print("\nTesting enum documentation through _member_map_:")
for name, member in LocationType._member_map_.items():
    doc = getattr(member, '__doc__', None)
    if doc and doc != LocationType.__doc__:
        print(f"\n{name}: {doc.strip()}")
    else:
        print(f"\n{name}: No description available")

# Generate full documentation as a test
print("\nGenerated documentation:")
print(generate_enum_doc(LocationType))