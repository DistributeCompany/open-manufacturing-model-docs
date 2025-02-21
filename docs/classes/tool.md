# Tool

A class to represent a Tool.

Tools are specialized Resources that are used to perform specific manufacturing
operations. They represent equipment like drills, hammers, wrenches, measuring devices,
or any other non-stationary tooling used in production processes. The Tool class extends the
Resource class to include tool-specific types.

Tools are connected to various components in the manufacturing system:
- Workers authorized to use them
- Workstations where they are used
- Actions they are used for
- Locations where they are stored
- Machines they are used with (optional)

**Best Practices**:
- Record tool locations
- Track worker authorizations

**Attributes**:
| Name                 | Data Type         | Description                                                                           |
|----------------------|-------------------|---------------------------------------------------------------------------------------|
| `name`               | `str`             | Human-readable name of the Tool                                                       |
| `georeference`       | `List[float]`     | Physical location coordinates [x, y] or [x, y, z]                                     |
| `tool_type`          | `str`             | Type of tool (e.g., "drill", "wrench")                                                  |
| `id`                 | `str`             | Unique identifier                                                                     |
| `location`           | `Location`        | Current storage location                                                              |
| `power_type`         | `str`             | Power source                                                                          |
| `power_consumption`  | `float`           | Power usage in kWh                                                                    |
| `maintenance_interval`| `int`            | Hours between required maintenance                                                    |
| `last_maintenance`   | `datetime`        | Timestamp of last maintenance                                                         |
| `hours_used`         | `float`           | Total hours of use since last maintenance                                             |
| `actors`             | `List[Actor]`     | Workers authorized to use this tool                                                   |
| `actions`            | `List[Action]`    | Actions associated with this tool                                                     |
| `constraints`         | `List[constraints]`      | Operating constraints                                                                 |
| `sensors`            | `List[Sensor]`    | Sensors monitoring this tool                                                          |
| `status`             | `ResourceStatus`  | Current operational status. See [ResourceStatus](/docs/classes/resourcestatus)         |
| `creation_date`      | `datetime`        | Timestamp when tool was created                                                       |
| `last_modified`      | `datetime`        | Timestamp of last modification                                                        |

**Example Configuration**:
```python
tool = Tool(
    name="Power Drill #1",
    tool_type="drill",
    power_type="electric",
    maintenance_interval=100  # hours
    )
```
:::note
The `Tool` class inherits base attributes from the `Resource` class while only adding a tool_type attribute. Use this class for non-stationary resources, that can be used by `Workers`.
:::


## Inheritance

Inherits from: `Resource`


## Constructor

```python
def __init__(self, name: str, georeference: List[float], tool_type: str, id: Optional[str] = None, power_type: Optional[str] = 'manual', power_consumption: float = 0, maintenance_interval: float = 0, last_maintenance: Optional[datetime.datetime] = None, location: Optional[omm.Location] = None, actors: Optional[List[~ActorT]] = None, actions: Optional[List[~ActionT]] = None, constraints: Optional[List[~ConstraintT]] = None, sensors: Optional[List[~SensorT]] = None, status: omm.ResourceStatus = <ResourceStatus.IDLE: 4>) -> None:
```

Initialize a Tool instance.


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


### `use_tool`

Record usage of the tool.

```python
def use_tool(self, duration: float) -> None:
```


## Example Usage

```python
# Example: Setting up a precision power tool
power_drill = Tool(
    name='Industrial_Drill_01',
    tool_type='precision_drill',
    georeference=[5.0, 10.0, 0.0],
    power_type='electric',
    maintenance_interval=200,  # Hours between maintenance
    location=Location('Tool Storage', [5.0, 10.0], LocationType.INTERNAL),
    sensors=[
        Sensor('temperature'),
        Sensor('vibration')
    ]
)

# Track tool usage and maintenance
power_drill.use_tool(duration=2.5)  # Hours

if power_drill.needs_maintenance():
    power_drill.perform_maintenance()
    print(f'Maintenance completed on {power_drill.name}')

# Monitor tool condition
for sensor in power_drill.sensors:
    print(f'{sensor.name}: {sensor.get_reading()}')
```
