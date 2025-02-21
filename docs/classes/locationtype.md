# LocationType

Enumeration of valid location types.
    
    Defines the different categories of locations within and outside the manufacturing
    facility to help track and manage material flow and resource positioning.


## Values

| Value | Description |
|-------|-------------|
| `INTERNAL` | Location within the manufacturing facility's boundaries |
| `EXTERNAL` | Location outside the facility (suppliers, customers, etc.) |

## Usage Example

```python
from omm import LocationType

# Access enum value
value = LocationType.INTERNAL

# Value comparison
if value == LocationType.INTERNAL:
    print(f'Value is INTERNAL')
```
