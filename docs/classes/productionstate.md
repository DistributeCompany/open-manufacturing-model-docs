# ProductionState

Enumeration of different production states for parts and products.
    
    Defines the various stages a part or product can be in during the manufacturing
    process, from raw material to finished product.


## Values

| Value | Description |
|-------|-------------|
| `RAW` | Unprocessed material at start of production |
| `NEW` | Newly created or received item |
| `WORK_IN_PROGRESS` | Partially completed item in production |
| `FINISHED` | Completed item ready for delivery |
| `DEFECTIVE` | Item that fails quality standards |
| `ON_HOLD` | Item temporarily suspended from production |

## Usage Example

```python
from omm import ProductionState

# Access enum value
value = ProductionState.RAW

# Value comparison
if value == ProductionState.RAW:
    print(f'Value is RAW')
```
