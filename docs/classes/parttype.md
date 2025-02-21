# PartType

Enumeration of different types of parts.

Defines the categories of parts used in the manufacturing process based on
their source and nature.


## Values

| Value | Description |
|-------|-------------|
| `RAW_MATERIAL` | Unprocessed materials used in manufacturing |
| `PURCHASED_COMPONENT` | Pre-made components from external suppliers |
| `WORK_IN_PROGRESS` | Partially completed products |

## Usage Example

```python
from omm import PartType

# Access enum value
value = PartType.RAW_MATERIAL

# Value comparison
if value == PartType.RAW_MATERIAL:
    print(f'Value is RAW_MATERIAL')
```
