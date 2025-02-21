# Machine

A class to represent a Machine in the manufacturing system.

    Machines are specialized Resources that perform specific manufacturing operations.
    They represent stationary manufacturing equipment such as CNC machines, 3D printers,
    assembly stations, or any other automated or semi-automated production equipment.
    The Machine class extends the Resource class to include machine-specific capabilities
    and operational parameters.

    Machines are connected to various components in the manufacturing system:
    - Workers authorized to operate them
    - Products they can manufacture
    - Parts they can process
    - Tools they can use
    - Actions they should perform
    - Sensors monitoring their status

    Machines can have multiple capabilities:
    - Manufacturing operations (milling, turning, printing)
    - Assembly operations (welding, fastening, bonding)
    - Processing operations (heating, cooling, curing)
    - Quality control operations (measuring, testing, inspecting)
    - Material handling operations (loading, unloading, positioning)

    **Best Practices**:
    - Define clear machine capabilities
    - Maintain accurate status tracking
    - Monitor performance metrics
    - Schedule maintenance according to maintenance interval
    - Track operational parameters
    - Update capabilities as needed

    **Attributes**:
    | Name                 | Data Type         | Description                                                      |
    |----------------------|-------------------|------------------------------------------------------------------|
    | `name`               | `str`             | Human-readable name of the Machine                               |
    | `machine_type`       | `str`             | Specific type of machine                                           |
    | `georeference`       | `List[float]`     | Physical location coordinates                                      |
    | `id`                 | `str`             | Unique identifier                                                  |
    | `location`           | `Location`        | Location where the machine is installed                            |
    | `capabilities`       | `List[str]`       | List of operations this machine can perform                        |
    | `power_type`         | `str`             | Power source                                                       |
    | `power_consumption`  | `float`           | Power usage in kWh                                                 |
    | `maintenance_interval`| `int`            | Hours between required maintenance                                 |
    | `last_maintenance`   | `datetime`        | Timestamp of last maintenance                                      |
    | `actors`             | `List[Actor]`     | Workers authorized to operate this machine                         |
    | `actions`            | `List[Action]`    | Actions associated with this machine                               |
    | `constraints`         | `List[constraints]`      | Operating constraints                                              |
    | `sensors`            | `List[Sensor]`    | Sensors monitoring this machine                                    |
    | `status`             | `ResourceStatus`  | Current operational status. See [ResourceStatus](/docs/classes/resourcestatus)                                         |
    | `creation_date`      | `datetime`        | Timestamp when the machine was created                             |
    | `last_modified`      | `datetime`        | Timestamp of last modification    

    **Example capabilities configuration**:
    ```python
    capabilities = [
        "cnc_milling",
        "surface_finishing",
        "precision_drilling"
        ]
    ```
    :::note
    The `Machine `class inherits base attributes from the `Resource` class while adding specialized capabilities for manufacturing operations. Use this class for any stationary manufacturing equipment in the production system.
    :::


## Inheritance

Inherits from: `Resource`


## Constructor

```python
def __init__(self, name: str, machine_type: str, georeference: List[float], id: Optional[str] = None, location: Optional[~LocationT] = None, capabilities: Optional[List[str]] = None, power_type: Optional[str] = 'electric', power_consumption: float = 0, maintenance_interval: float = 0, last_maintenance: Optional[datetime.datetime] = None, actors: Optional[List[~ActorT]] = None, actions: Optional[List[~ActionT]] = None, constraints: Optional[List[~ConstraintT]] = None, sensors: Optional[List[~SensorT]] = None, status: omm.ResourceStatus = <ResourceStatus.IDLE: 4>) -> None:
```

Initialize a Machine instance.


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


### `add_capability`

Add a new capability to the machine.

```python
def add_capability(self, capability: str) -> None:
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


### `remove_capability`

Remove a capability from the machine.

```python
def remove_capability(self, capability: str) -> None:
```


### `remove_constraint`

Remove a specific constraint from the resource's constraints.

```python
def remove_constraint(self, constraint: ~ConstraintT) -> None:
```


### `start_capability`

Start a specific capability if available on the machine.

```python
def start_capability(self, capability: str) -> None:
```


### `to_dict`

Convert the machine instance to a dictionary representation.

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
# Example: Creating a CNC machine resource with sensors and operators.
cnc_machine = Machine(
    name='CNC_Mill_01',
    machine_type=5-Axis Mill,
    georeference=[10.5, 20.0, 0.0],  # Machine location in the factory
    capabilities=['precision_milling', 'drilling', 'threading', 'engraving'],
    sensors=[
        Sensor('spindle_speed'),
        Sensor('coolant_level'),
        Sensor('tool_wear')
    ],
    status=ResourceStatus.IDLE,
    power_consumption=7.5,  # kW
    maintenance_interval=2000  # Hours
)

# Assign workers and start operation
operator = Worker('Berry Gerrits', roles={'CNC Operator': ['5-Axis Mill']})
cnc_machine.add_actor(operator)

if operator.can_work_with(cnc_machine):
    operator.work_on(cnc_machine, 'engraving')
    print(f'{operator.name} operating {cnc_machine.name}')
# Monitor machine condition
for sensor in cnc_machine.sensors:
    print(f'{sensor.name}: {sensor.get_reading()}')
```
