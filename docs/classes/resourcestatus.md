# ResourceStatus

Enumeration of valid resource statuses.
    
    Defines the possible states a resource can be in during operations, helping track
    resource availability and utilization.


## Values

| Value | Description |
|-------|-------------|
| `WAIT` | Resource is available but waiting for next task |
| `LOAD` | Resource is currently loading materials or products |
| `UNLOAD` | Resource is currently unloading materials or products |
| `IDLE` | Resource is available but not actively working |
| `WORKING` | Resource is actively performing an assigned task |
| `FAILED` | Resource has encountered an error or malfunction |
| `CHARGING` | Resource is recharging or refueling |

## Usage Example

```python
from omm import ResourceStatus

# Access enum value
value = ResourceStatus.WAIT

# Value comparison
if value == ResourceStatus.WAIT:
    print(f'Value is WAIT')
```
