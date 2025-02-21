# Conveyor

A class to represent a Conveyor.

    Conveyors are specialized Resources that facilitate continuous material flow and transport 
    within the manufacturing environment. They represent fixed material handling systems like 
    belt conveyors, roller conveyors, chain conveyors, or other automated transport systems. 
    The Conveyor class extends the Resource class to include conveyor-specific capabilities 
    and parameters for material flow management.

    Conveyors are connected to various components in the manufacturing system:
    - Locations they connect (start and end points)
    - Products and Parts they transport
    - Actions they perform
    - Sensors monitoring their status
    - Workers who maintain them
    - Machines they interface with

    **Best Practices**:
    - Define accurate path coordinates for the entire conveyor length
    - Monitor material flow rates and congestion
    - Track energy consumption and efficiency
    - Maintain proper load distribution
    - Schedule preventive maintenance
    - Ensure safety compliance
    - Monitor speed and capacity utilization
    - Track system bottlenecks

    **Attributes**:
    | Name                   | Data Type          | Description                                                                           |
    |------------------------|--------------------|---------------------------------------------------------------------------------------|
    | `name`                 | `str`              | Human-readable name of the Conveyor                                                   |
    | `georeference`         | `List[float]`      | Coordinates [x, y] or [x, y, z] describing the entire conveyor                         |
    | `speed`                | `float`            | Operating speed in meters per second                                                  |
    | `capacity`             | `float`            | Maximum items per meter of conveyor length                                             |
    | `direction`            | `str`              | Direction of movement ("forward" or "reverse")                                        |
    | `id`                   | `str`              | Unique identifier                                                                      |
    | `status`               | `ResourceStatus`   | Current operational status. See [ResourceStatus](/docs/classes/resourcestatus)          |
    | `power_type`           | `str`              | Power source                                                                           |
    | `power_consumption`    | `float`            | Power usage in kWh                                                                     |
    | `maintenance_interval` | `int`              | Hours between required maintenance                                                     |
    | `last_maintenance`     | `datetime`         | Timestamp of last maintenance                                                          |
    | `hours_used`           | `float`            | Total hours of use since last maintenance                                              |
    | `actors`               | `List[Actor]`      | Workers authorized to maintain this conveyor                                           |
    | `sensors`              | `List[Sensor]`     | Sensors monitoring this conveyor                                                       |
    | `actions`              | `List[Action]`     | Actions associated with this conveyor                                                  |
    | `constraints`           | `List[constraints]`       | Operating constraints                                                                  |
    | `creation_date`        | `datetime`         | Timestamp when conveyor was created                                                    |
    | `last_modified`        | `datetime`         | Timestamp of last modification                                                         |

    **Example Configuration**:
    ```python
    conveyor = Conveyor(
        name="Main Assembly Line",
        georeference=[[0.0, 0.0, 0.0], [10.0, 0.0, 2.0]], # a Conveyor with only two coordinates
        speed=0.5,  # meters per second
        capacity=2.0,  # items per meter
        direction="forward",
        power_type="electric",
        power_consumption=5.0  # kWh
        )
    ```
    :::note
    The `Conveyor` class inherits base attributes from the `Resource` class while adding specialized capabilities for continuous material flow. Use this class for any fixed material handling systems that enable continuous product or part movement through the manufacturing facility.
    :::
    :::info
    The `georeference` attribute for `Conveyors` differs from other classes as it contains the coordinates describing the entire conveyor system, not just a single point. The format depends on the implementation but typically includes a list of coordinate pairs or a more complex path description (e.g., with z-dimension).
    :::


## Inheritance

Inherits from: `Resource`


## Constructor

```python
def __init__(self, name: str, georeference: List[float], speed: float, capacity: float, direction: str = 'forward', id: Optional[str] = None, location: Optional[omm.Location] = None, power_type: Optional[str] = 'electric', power_consumption: float = 0, maintenance_interval: float = 0, last_maintenance: Optional[datetime.datetime] = None, actors: Optional[List[~ActorT]] = None, actions: Optional[List[~ActionT]] = None, constraints: Optional[List[~ConstraintT]] = None, sensors: Optional[List[~SensorT]] = None, status: omm.ResourceStatus = <ResourceStatus.IDLE: 4>) -> None:
```

Initialize a Conveyor instance.


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


### `add_items`

Add items to the conveyor.

```python
def add_items(self, count: float) -> None:
```


### `get_current_action`

Get the current in-progress action.

```python
def get_current_action(self) -> Optional[~ActionT]:
```


### `get_total_capacity`

Calculate total capacity of the conveyor.

```python
def get_total_capacity(self) -> float:
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


### `remove_items`

Remove items from the conveyor.

```python
def remove_items(self, count: float) -> None:
```


### `reverse_direction`

Reverse the direction of the conveyor.

```python
def reverse_direction(self) -> None:
```


### `to_dict`

Convert the resource instance to a dictionary representation.

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
# Example: Setting up a smart conveyor system
main_conveyor = Conveyor(
    name='MainLine_01',
    georeference=[0.0, 0.0, 0.0],
    polyline=[[0,0], [10,0], [10,10], [20,10]],  # Conveyor path
    speed=0.5,  # meters per second
    capacity=10.0,  # items per meter
    direction='forward',
    sensors=[
        Sensor('motor_temperature'),
        Sensor('belt_tension'),
        Sensor('item_counter')
    ]
)

# Manage conveyor operations
main_conveyor.add_items(5)  # Add 5 items

# Calculate utilization
total_capacity = main_conveyor.get_total_capacity()
available_space = total_capacity - main_conveyor._current_load
print(f'Conveyor utilization: {(main_conveyor._current_load/total_capacity)*100:.1f}%')

# Reverse direction for return line
main_conveyor.reverse_direction()
print(f'Conveyor direction: {main_conveyor.direction}')
```
