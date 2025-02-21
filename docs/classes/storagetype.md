# StorageType

Enumeration of different types of storage locations.

Defines the various storage areas and configurations available in the facility
for holding materials, work-in-progress, and finished goods.


## Values

| Value | Description |
|-------|-------------|
| `GENERAL` | Multi-purpose storage area without specific designation |
| `WAREHOUSE` | Large-scale storage facility for long-term storage |
| `RACK` | Structured storage system with multiple levels |
| `BUFFER` | Temporary storage area between operations |
| `QUEUE` | FIFO storage area for sequential processing |

## Usage Example

```python
from omm import StorageType

# Access enum value
value = StorageType.GENERAL

# Value comparison
if value == StorageType.GENERAL:
    print(f'Value is GENERAL')
```
