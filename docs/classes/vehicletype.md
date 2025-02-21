# VehicleType

Enumeration of available vehicle types.
    
    Defines the different categories of vehicles that can be used for material
    handling and transportation within the facility.


## Values

| Value | Description |
|-------|-------------|
| `GENERIC_AUTOMATED_VEHICLE` | General-purpose autonomous vehicle |
| `GENERIC_MANUAL_VEHICLE` | General-purpose manually operated vehicle |
| `AUTOMATED_MOBILE_ROBOT` | Specialized autonomous robot for material handling |
| `MANUAL_FORKLIFT` | Traditional operator-driven forklift |

## Usage Example

```python
from omm import VehicleType

# Access enum value
value = VehicleType.GENERIC_AUTOMATED_VEHICLE

# Value comparison
if value == VehicleType.GENERIC_AUTOMATED_VEHICLE:
    print(f'Value is GENERIC_AUTOMATED_VEHICLE')
```
