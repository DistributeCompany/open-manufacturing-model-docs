# RequirementType

Types of requirements that can be specified for an action.


## Values

| Value | Description |
|-------|-------------|
| `MACHINE` | No description available |
| `WORKSTATION` | No description available |
| `CONVEYER` | No description available |
| `ROBOTIC_ARM` | No description available |
| `VEHICLE` | No description available |
| `PART` | No description available |
| `PRODUCT` | No description available |
| `WORKER` | No description available |
| `TOOL` | No description available |

## Usage Example

```python
from omm import RequirementType

# Access enum value
value = RequirementType.MACHINE

# Value comparison
if value == RequirementType.MACHINE:
    print(f'Value is MACHINE')
```
