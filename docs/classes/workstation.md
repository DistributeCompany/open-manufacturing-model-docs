# WorkStation

A class to represent a WorkStation.

WorkStations are specialized Resources that provide designated areas for manufacturing
operations. They represent manual or semi-automated work areas where operators perform
specific tasks such as assembly, inspection, or processing operations. The WorkStation
class extends the Resource class to include workspace-specific capabilities and
capacity management.

WorkStations are connected to various components in the manufacturing system:
- Workers assigned to the station
- Tools used at the station
- Products processed at the station
- Parts handled at the station
- Actions performed at the station
- Sensors monitoring the station

WorkStations support various operation types:
- Assembly operations
- Quality control and inspection
- Material preparation
- Packaging and labeling
- Testing and verification
- Manual processing tasks

**Best Practices**:
- Define clear workstation capabilities
- Track station capacity and utilization
- Monitor worker assignments
- Ensure proper tool availability

**Attributes**:
| Name                | Data Type              | Description                                                                              |
|---------------------|------------------------|------------------------------------------------------------------------------------------|
| `name`              | `str`                  | Human-readable name of the WorkStation                                                   |
| `georeference`      | `List[float]`          | Physical location coordinates [x, y] or [x, y, z]                                        |
| `id`                | `str`                  | Unique identifier                                                                        |
| `location`          | `Location`             | Location where the workstation is installed                                              |
| `workstation_type`  | `str`                  | Type of workstation (e.g., "assembly", "inspection")                                     |
| `capabilities`      | `List[str]`            | List of operations this workstation supports                                             |
| `max_capacity`      | `int`                  | Maximum number of simultaneous operations                                                |
| `current_capacity`  | `int`                  | Current number of operations in progress                                                 |
| `power_type`        | `str`                  | Power source                                                                             |
| `power_consumption` | `float`                | Power usage in kWh                                                                       |
| `maintenance_interval` | `int`              | Hours between required maintenance                                                       |
| `last_maintenance`  | `datetime`             | Timestamp of last maintenance                                                            |
| `hours_used`        | `float`                | Total hours of use since last maintenance                                                |
| `actors`            | `List[Actor]`          | Workers assigned to this workstation                                                     |
| `actions`           | `List[Action]`         | Actions associated with this station                                                     |
| `constraints`        | `List[constraints]`           | Operating constraints                                                                    |
| `sensors`           | `List[Sensor]`         | Sensors monitoring this workstation                                                      |
| `status`            | `ResourceStatus`       | Current operational status. See [ResourceStatus](/docs/classes/resourcestatus)            |
| `creation_date`     | `datetime`             | Timestamp when workstation was created                                                   |
| `last_modified`     | `datetime`             | Timestamp of last modification                                                           |

**Example Configuration**:
```python
workstation = WorkStation(
    name="Assembly Station 1",
    workstation_type="assembly",
    capabilities=["manual_assembly", "testing"],
    max_capacity=2
    )
 ```
:::note
The `WorkStation` class inherits base attributes from the `Resource` class while adding specialized capabilities for manual and semi-automated operations. Use this class for designated work areas where operators perform specific manufacturing tasks.
:::


## Inheritance

Inherits from: `Resource`


## Constructor

```python
def __init__(self, name: str, georeference: List[float], id: Optional[str] = None, location: Optional[omm.Location] = None, workstation_type: Optional[str] = 'general', capabilities: Optional[List[str]] = None, max_capacity: Optional[int] = None, power_type: Optional[str] = 'manual', power_consumption: float = 0, maintenance_interval: float = 0, last_maintenance: Optional[datetime.datetime] = None, actors: Optional[List[~ActorT]] = None, actions: Optional[List[~ActionT]] = None, constraints: Optional[List[~ConstraintT]] = None, sensors: Optional[List[~SensorT]] = None, status: omm.ResourceStatus = <ResourceStatus.IDLE: 4>) -> None:
```

Initialize a WorkStation instance.


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


### `current_capacity`

Return the current capacity utilization.

```python
@property
def current_capacity(self):
    # Returns <class 'int'>
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

Add a new capability to the workstation.

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

Remove a capability from the workstation.

```python
def remove_capability(self, capability: str) -> None:
```


### `remove_constraint`

Remove a specific constraint from the resource's constraints.

```python
def remove_constraint(self, constraint: ~ConstraintT) -> None:
```


### `to_dict`

Convert the workstation instance to a dictionary representation.

```python
def to_dict(self) -> Dict[str, Any]:
```


### `update_actor`

Replace an existing actor with a new actor.

```python
def update_actor(self, old_actor: ~ActorT, new_actor: ~ActorT) -> None:
```


### `update_capacity`

Update the current capacity utilization.

```python
def update_capacity(self, new_capacity: int) -> None:
```


## Example Usage

```python
# Example: Creating an advanced assembly workstation
assembly_station = WorkStation(
    name='Assembly_Station_01',
    georeference=[15.0, 25.0, 0.0],
    workstation_type='electronics_assembly',
    capabilities=[
        'circuit_board_assembly',
        'component_soldering',
        'quality_inspection'
    ],
    max_capacity=3,  # Number of simultaneous assemblies
    actors=[
        Worker('Emma Thompson', roles={'Electronics Assembler': ['PCB']})
    ],
    sensors=[
        Sensor('temperature'),
        Sensor('humidity')
    ]
)

# Update station capacity and status
assembly_station.update_capacity(2)
print(f'Current occupation: {assembly_station.current_capacity}/{assembly_station.max_capacity}')

# Check environmental conditions
for sensor in assembly_station.sensors:
    print(f'{sensor.name}: {sensor.get_reading()}')
```
