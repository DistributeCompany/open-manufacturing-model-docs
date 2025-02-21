# Resource

A class to represent a Resource in the manufacturing system.

    Resources are physical entities in the manufacturing environment that are used to perform
    manufacturing operations. They include machines, workstations, vehicles and other 
    assets required for production processes.

    Resources are connected to various other classes in the manufacturing system:
        - Locations where they are positioned
        - Actions they perform
        - Actors who can operate them
        - Jobs they are assigned to
        - Sensors that monitor their status

    The Resource class serves as a base class for more specialized resource types:
        - `Machine`: Manufacturing equipment like CNC, laser cutters, 3D printers
        - `WorkStation`: Manual or semi-automated work areas
        - `Conveyor`: Material handling systems for continuous flow
        - `RoboticArm`: Programmable robotic manipulators
        - `Vehicle`: Mobile equipment for material transport, e.g., AGVs, AMRs, or forklifts
        - `Tool`: Specialized (non-stationary) equipment, e.g., a drill or pH meter

    **Best Practices**:
        - Define clear georeference coordinates for resource positioning
        - Track real-time georeference of mobile resources (i.e., Vehicles)
        - Maintain accurate status tracking
        - Associate appropriate actors with each resource
        - Track resource utilization and performance
        - Monitor power consumption and maintenance intervals

    **Attributes**:
    | Name                  | Data Type           | Description                                                        |
    |-----------------------|---------------------|--------------------------------------------------------------------|
    | `name`                | `str`               | Human-readable name of the Resource                                |
    | `resource_type`       | `ResourceType`      | Category of the resource. See [ResourceType](/docs/classes/resourcetype)  |
    | `georeference`        | `List[float]`       | Physical location coordinates                                      |
    | `id`                 | `str`               | Unique identifier                                                  |
    | `location`            | `Location`          | Associated location instance                                       |
    | `status`              | `ResourceStatus`    | Current operational status. See [ResourceStatus](/docs/classes/resourcestatus)                                         |
    | `power_type`          | `str`               | Power source (e.g., "manual", "electric")                          |
    | `power_consumption`   | `float`             | Power usage in kWh                                                 |
    | `maintenance_interval`| `int`               | Hours between required maintenance                                 |
    | `last_maintenance`    | `datetime`          | Timestamp of last maintenance                                      |
    | `hours_used`          | `float`             | Total hours of use since last maintenance                          |
    | `actors`              | `List[Actor]`       | Actors who can operate this resource                               |
    | `actions`             | `List[Action]`      | Actions of this resource                                           |
    | `sensors`             | `List[Sensor]`      | Sensors monitoring this resource                                   |
    | `constraints`          | `List[constraints]`        | Operating constraints   

    **Example Configuration**
    ```python
    resource = Resource(
        name="Assembly Tool Kit",
        resource_type=ResourceType.TOOL,
        georeference=[1.5, 2.0],
        power_type="manual",
        maintenance_interval=168,  # hours (1 week)
        status=ResourceStatus.IDLE
        )
    ```
    :::warning
    **Developer notes**: `Workers` authorized to work on `Resource` should be added to `actions` attribute. **TODO**: Integrate this in `Worker.add_role()` and `Worker.remove_role()`.
    :::


## Constructor

```python
def __init__(self, name: str, resource_type: omm.ResourceType, georeference: List[float], id: Optional[str] = None, location: Optional[~LocationT] = None, status: omm.ResourceStatus = <ResourceStatus.IDLE: 4>, power_type: Optional[str] = 'manual', power_consumption: float = 0, maintenance_interval: float = 0, last_maintenance: Optional[datetime.datetime] = None, actors: List[~ActorT] = None, actions: List[~ActionT] = None, sensors: List[~SensorT] = None, constraints: Optional[List[~ConstraintT]] = None) -> None:
```

Initialize a Resource instance.


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


## Example Usage

```python
# Create a new Resource instance
Resource(
    name=<str>
    resource_type=<ResourceType>
    georeference=<List>
)
```
