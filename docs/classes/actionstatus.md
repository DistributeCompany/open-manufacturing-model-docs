# ActionStatus

Enumeration of valid action statuses.

Represents the lifecycle states of an Action, from initial creation through completion
or cancellation. These statuses help track the progress of manufacturing operations
and enable workflow management.


## Values

| Value | Description |
|-------|-------------|
| `DRAFT` | Initial state when action is created but not yet ready for execution |
| `REQUESTED` | Action has been submitted for approval or scheduling |
| `CONFIRMED` | Action has been approved and scheduled for execution |
| `IN_PROGRESS` | Action is currently being executed |
| `COMPLETED` | Action has been successfully finished |
| `CANCELLED` | Action was terminated before completion or rejected |

## Usage Example

```python
from omm import ActionStatus

# Access enum value
value = ActionStatus.DRAFT

# Value comparison
if value == ActionStatus.DRAFT:
    print(f'Value is DRAFT')
```
