# Vehicle

A class to represent a Vehicle.

Vehicles are specialized Resources used for material transport and logistics operations.
They represent mobile equipment such as automated guided vehicles (AGVs), forklifts,
manual transport vehicles, or any other mobile equipment used for moving parts and products.
The Vehicle class extends the Resource class to include vehicle-specific capabilities
and parameters for movement, energy management, and load handling.

Vehicles are connected to various components in the manufacturing system:
- Routes they can traverse
- Locations they move between
- Products or Parts they can transport
- Actions they should perform
- Sensors monitoring their status
- Workers authorized to operate them

**Best Practices**:
- Monitor battery levels and charging status
- Track vehicle location in real-time
- Maintain load capacity constraints
- Schedule preventive maintenance
- Monitor environmental impact
- Optimize route selection
- Ensure safety compliance

**Attributes**:
| Name                      | Data Type               | Description                                                                |
|---------------------------|-------------------------|----------------------------------------------------------------------------|
| `name`                    | `str`                   | Human-readable name of the Vehicle                                         |
| `vehicle_type`            | `VehicleType`           | Type of vehicle. See [VehicleType](/docs/classes/vehicletype)                |
| `georeference`            | `List[float]`           | Current location coordinates [x, y] or [x, y, z]                           |
| `id`                      | `str`                   | Unique identifier                                                          |
| `status`                  | `ResourceStatus`        | Current operational status. See [ResourceStatus](/docs/classes/resourcestatus)|
| `power_type`              | `str`                   | Power source                                                               |
| `power_consumption`       | `float`                 | Power usage in kWh                                                         |
| `maintenance_interval`    | `int`                   | Hours between required maintenance                                         |
| `last_maintenance`        | `datetime`              | Timestamp of last maintenance                                              |
| `hours_used`              | `float`                 | Total hours of use since last maintenance                                  |
| `actors`                  | `List[Actor]`           | Workers authorized to operate this vehicle                                 |
| `sensors`                 | `List[Sensor]`          | Sensors on-board this vehicle                                              |
| `actions`                 | `List[Action]`          | Actions associated with this vehicle                                       |
| `constraints`              | `List[constraints]`            | Operating constraints                                                      |
| `fuel`                    | `str`                   | Type of fuel or power source                                               |
| `average_fuel_consumption`| `float`                 | Average fuel consumption rate                                              |
| `emission_standard`       | `str`                   | Applicable emission standard                                               |
| `load_capacities`         | `dict`                  | Maximum load capacity specifications                                       |
| `length`                  | `float`                 | Vehicle length in meters                                                   |
| `height`                  | `float`                 | Vehicle height in meters                                                   |
| `width`                   | `float`                 | Vehicle width in meters                                                    |
| `license_plate`           | `str`                   | Vehicle identification plate                                               |
| `empty_weight`            | `float`                 | Weight without load in kg                                                  |
| `average_speed`           | `float`                 | Normal operating speed in meters/second                                  |
| `speed`                   | `float`                 | Current actual speed in meters/second                                      |
| `co2_emission`            | `float`                 | CO2 emissions in g/km                                                      |
| `nox_emission`            | `float`                 | NOx emissions in g/km                                                      |
| `noise_pollution`         | `float`                 | Noise level in dB                                                          |
| `land_use`                | `float`                 | Space requirement in m²                                                    |
| `battery_capacity`        | `float`                 | Total battery capacity in kWh                                              |
| `battery_threshold`       | `float`                 | Minimum battery level for operation                                        |
| `battery_charging_rate`   | `float`                 | Charging rate in kW                                                        |
| `energy_consumption_moving`| `float`                 | Energy use while moving in kWh/km                                          |
| `energy_consumption_idling`| `float`                 | Energy use while idle in kWh/h                                             |
| `creation_date`           | `datetime`              | Timestamp when vehicle was created                                         |
| `last_modified`           | `datetime`              | Timestamp of last modification                                             |

**Example Configuration**:
```python
vehicle = Vehicle(
    name="AGV-001",
    vehicle_type=VehicleType.AUTOMATED_MOBILE_ROBOT,
    average_speed=1.0,  # m/s
    battery_capacity=10.0,  # kWh
    battery_threshold=0.2,  # 20%
    load_capacities={"weight": 150}  # kg
    )
```
:::note
The `Vehicle` class inherits base attributes from the `Resource` class while adding specialized capabilities for transport operations. Use this class for any mobile equipment used in material handling and logistics.
    :::


## Inheritance

Inherits from: `Resource`


## Constructor

```python
def __init__(self, name: str, vehicle_type: omm.VehicleType, georeference: List[float], status: omm.ResourceStatus = <ResourceStatus.IDLE: 4>, id: Optional[str] = None, power_type: Optional[str] = 'electric', power_consumption: float = 0, maintenance_interval: float = 0, last_maintenance: Optional[datetime.datetime] = None, actors: Optional[List[~ActorT]] = None, sensors: Optional[List[~SensorT]] = None, actions: Optional[List[~ActionT]] = None, constraints: Optional[List[~ConstraintT]] = None, fuel: Optional[str] = None, average_fuel_consumption: Optional[float] = None, emission_standard: Optional[str] = None, load_capacities: Optional[dict] = None, length: Optional[float] = None, height: Optional[float] = None, width: Optional[float] = None, license_plate: Optional[str] = None, empty_weight: Optional[float] = None, average_speed: float = 1.0, co2_emission: float = 0, nox_emission: float = 0, noise_pollution: float = 0, land_use: float = 0, battery_capacity: float = 0, battery_threshold: float = 0, battery_charging_rate: float = 0, energy_consumption_moving: float = 0, energy_consumption_idling: float = 0) -> None:
```

Initialize a Vehicle instance.


## Properties


### `actions`

Return a copy of the resource's actions.

```python
@property
def actions(self):
    # Returns typing.List[~ActionT]
```


### `actors`

Return a copy of the resource's actors.

```python
@property
def actors(self):
    # Returns typing.List[~ActorT]
```


### `battery_threshold`

Return the vehicle's battery threshold.

```python
@property
def battery_threshold(self):
    # Returns <class 'float'>
```


### `constraints`

Return the resource's constraints.

```python
@property
def constraints(self):
    # Returns typing.Optional[typing.List[~ConstraintT]]
```


### `entries`

Return the number of entries for the resource.

```python
@property
def entries(self):
    # Returns <class 'int'>
```


### `exits`

Return the number of exits for the resource.

```python
@property
def exits(self):
    # Returns <class 'int'>
```


### `georeference`

Return the resource's georeference.

```python
@property
def georeference(self):
    # Returns typing.List[float]
```


### `last_modified`

Return the last modified timestamp.

```python
@property
def last_modified(self):
    # Returns <class 'datetime.datetime'>
```


### `sensors`

Return a copy of the resource's sensors.

```python
@property
def sensors(self):
    # Returns typing.List[~SensorT]
```


### `speed`

Return the vehicle's actual speed.

```python
@property
def speed(self):
    # Returns <class 'float'>
```


### `status`

Return the status of the resource.

```python
@property
def status(self):
    # Returns <enum 'ResourceStatus'>
```


## Methods


### `add_action`

Add a single action to the resource's actions.

```python
def add_action(self, action: ~ActionT) -> None:
```


### `add_actor`

Add an actor to the resource.

```python
def add_actor(self, actor: ~ActorT) -> None:
```


### `add_constraint`

Add a single constraint to the resource's constraints.

```python
def add_constraint(self, constraint: ~ConstraintT) -> None:
```


### `get_current_action`

Get the current in-progress action.

```python
def get_current_action(self) -> Optional[~ActionT]:
```


### `needs_maintenance`

Check if tool needs maintenance based on usage hours.

```python
def needs_maintenance(self) -> bool:
```


### `operate`

Operate Resource.

```python
def operate(self) -> None:
```


### `perform_maintenance`

Perform maintenance on the tool.

```python
def perform_maintenance(self) -> None:
```


### `remove_action`

Remove a specific action from the resource's actions.

```python
def remove_action(self, action: ~ActionT) -> None:
```


### `remove_actor`

Remove an actor from the resource.

```python
def remove_actor(self, actor: ~ActorT) -> None:
```


### `remove_constraint`

Remove a specific constraint from the resource's constraints.

```python
def remove_constraint(self, constraint: ~ConstraintT) -> None:
```


### `start_charging`

Start charging the vehicle.

```python
def start_charging(self) -> None:
```


### `stop_charging`

Stop charging the vehicle.

```python
def stop_charging(self) -> None:
```


### `to_dict`

Convert the vehicle instance to a dictionary representation.

```python
def to_dict(self) -> Dict[str, Any]:
```


### `update_actor`

Replace an existing actor with a new actor.

```python
def update_actor(self, old_actor: ~ActorT, new_actor: ~ActorT) -> None:
```


## Example Usage

```python
# Example: Creating an automated guided vehicle (AGV)
agv = Vehicle(
    name='AGV_01',
    vehicle_type=VehicleType.AUTOMATED_MOBILE_ROBOT,
    georeference=[0.0, 0.0, 0.0],
    average_speed=1.5,  # meters/second
    battery_capacity=24.0,  # kWh
    battery_threshold=20.0,  # Minimum battery percentage
    battery_charging_rate=4.0,  # kW
    load_capacities={'max_weight': 500},  # kg
    sensors=[
        Sensor('battery_level'),
        Sensor('proximity'),
        Sensor('path_detection')
    ],
    energy_consumption_moving=0.5,  # kWh per hour while moving
    energy_consumption_idling=0.1   # kWh per hour while idle
)

# Monitor vehicle status and start charging if needed
if agv.battery_threshold > 20:
    agv.start_charging()
    print(f'Charging vehicle at {agv.battery_charging_rate}kW')

# Adjust speed based on load
agv.speed = agv.average_speed * 0.8  # Reduce speed to 80% for heavy load
print(f'Current speed: {agv.speed} m/s')
```
