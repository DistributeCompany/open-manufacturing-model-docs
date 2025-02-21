# JobPriority

Enumeration of priority levels for jobs.
    
    Defines the urgency levels that can be assigned to manufacturing jobs,
    helping determine processing order and resource allocation.


## Values

| Value | Description |
|-------|-------------|
| `LOW` | Routine job with flexible timing |
| `MEDIUM` | Standard priority job |
| `HIGH` | Urgent job requiring preferential treatment |
| `URGENT` | Critical job requiring immediate attention |

## Usage Example

```python
from omm import JobPriority

# Access enum value
value = JobPriority.LOW

# Value comparison
if value == JobPriority.LOW:
    print(f'Value is LOW')
```
