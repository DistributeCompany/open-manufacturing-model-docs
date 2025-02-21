# JobStatus

Enumeration of manufacturing job statuses.

Defines the possible states of a manufacturing job throughout its lifecycle,
from planning to completion.


## Values

| Value | Description |
|-------|-------------|
| `PLANNED` | Job is scheduled but not yet started |
| `IN_PROGRESS` | Job is currently being executed |
| `ON_HOLD` | Job is temporarily suspended |
| `COMPLETED` | Job has been successfully finished |
| `CANCELLED` | Job was terminated before completion |

## Usage Example

```python
from omm import JobStatus

# Access enum value
value = JobStatus.PLANNED

# Value comparison
if value == JobStatus.PLANNED:
    print(f'Value is PLANNED')
```
