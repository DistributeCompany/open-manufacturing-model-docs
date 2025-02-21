# ResourceType

Enumeration of valid resource types.

Defines the different categories of manufacturing resources that can be used
in production operations. Each type represents a specific kind of equipment
or asset used in the manufacturing process.


## Values

| Value | Description |
|-------|-------------|
| `GENERAL` | Generic resource without specific categorization |
| `MACHINE` | Stationary manufacturing equipment (mills, lathes, etc.) |
| `WORKSTATION` | Manual or semi-automated work area for operators |
| `CONVEYOR` | Automated material handling system for continuous flow |
| `ROBOTIC_ARM` | Programmable robotic manipulator for automated tasks |
| `VEHICLE` | Mobile equipment for material transport (AGVs, forklifts) |
| `TOOL` | Specialized equipment or implements used in manufacturing |

## Usage Example

```python
from omm import ResourceType

# Access enum value
value = ResourceType.GENERAL

# Value comparison
if value == ResourceType.GENERAL:
    print(f'Value is GENERAL')
```
