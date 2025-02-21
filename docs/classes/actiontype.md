# ActionType

Enumeration of valid action types.
    
    Defines the different types of operations that can be performed in a manufacturing
    or logistics environment. Each type represents a specific category of action that
    can be assigned to resources, machines, or jobs.


## Values

| Value | Description |
|-------|-------------|
| `STOP` | Immediately halt current operation for safety or process reasons |
| `LOAD` | Transfer materials or products into a machine or workstation |
| `UNLOAD` | Remove materials or products from a machine or workstation |
| `MOVE` | Transport items between locations in the facility |
| `ATTACH` | Connect or join components or sub-assemblies together |
| `DETACH` | Separate or disconnect assembled components |
| `BREAK` | Scheduled or unscheduled interruption in operations |
| `WAIT` | Planned delay or holding period in the process |
| `PROCESS` | General manufacturing operation or transformation |
| `ASSEMBLY` | Combine multiple components into a larger assembly |
| `MACHINING` | Perform specific machining operations on parts |
| `QUALITY_CHECK` | Inspect products for quality standards compliance |
| `PACKAGING` | Prepare products for storage or shipping |
| `STORAGE` | Place items in designated storage locations |
| `SETUP` | Configure or prepare machines/workstations for operation |
| `CLEAN` | Perform cleaning operations on equipment or workspace |
| `INSPECT` | Examine equipment or products for issues or maintenance needs |
| `REPAIR` | Fix damaged or malfunctioning equipment |
| `MAINTENANCE` | Perform preventive or scheduled maintenance tasks |

## Usage Example

```python
from omm import ActionType

# Access enum value
value = ActionType.STOP

# Value comparison
if value == ActionType.STOP:
    print(f'Value is STOP')
```
