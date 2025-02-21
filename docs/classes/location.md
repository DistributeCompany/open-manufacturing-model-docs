# Location

A class to represent a geographical Location in (or outside) the manufacturing system.

Locations define physical areas. They can represent
both internal areas within a facility and external locations such as supplier or customer sites.
Each Location has specific coordinates and can contain Resources, Actions, and Actors.

Locations are connected to various components in the manufacturing system:
- Resources positioned at the location
- Actions that occur at the location
- Actors that are associated with the location
- Routes that connect different locations

The Location class serves as a base class for more specialized location types:
- `Storage`: Dedicated areas for storing parts and products

**Best Practices**:
- Define accurate georeference coordinates for precise positioning
- Specify appropriate location type (internal/external)
- Associate relevant actors and resources
- Maintain clear relationships with connected locations
- Track all actions performed at the location

**Attributes**:
| Name              | Data Type         | Description                                                 |
|-------------------|-------------------|-------------------------------------------------------------|
| `name`            | `str`             | Human-readable name of the Location                         |
| `georeference`    | `List[float]`     | Physical location coordinates [x, y] or [x, y, z]           |
| `location_type`   | `LocationType`    | Type of location. See [LocationType](/docs/classes/locationtype)                       |
| `id`              | `str`             | Unique identifier                                           |
| `actors`          | `List[Actor]`     | Actors associated with this location                        |
| `actions`         | `List[Action]`    | Actions that can be performed at this location              |
| `constraints`      | `List[constraints]`      | Operating constraints                                       |
| `creation_date`   | `datetime`        | Timestamp when location was created                         |
| `last_modified`   | `datetime`        | Timestamp of last modification  

**Example Configuration**
```python
location = Location(
    name="Production Facility",
    georeference=[52.23769997661302, 6.848124696630017],
    location_type=LocationType.INTERNAL,
    actors=[assembly_supervisor, technician_1, grumpy_manager_4] # instances of Actor class
)
```
:::note
For `Locations` specifically designed for storing `Parts` and `Products`, use the `Storage` subclass instead of the base Location class.
:::
:::warning
**Developer Note**: Might be smarter to define one *internal* `Location` for all `Resources` in the same factory, instead of a dedicated instance of `Location` per `Resource`. **TODO**: Add `resources` attribute to `Location` class to track all `Resources` link to this `Location. 
:::


## Constructor

```python
def __init__(self, name: str, georeference: List[float], location_type: omm.LocationType = <LocationType.EXTERNAL: 2>, id: Optional[str] = None, actors: List[~ActorT] = None, actions: List[~ActionT] = None, constraints: Optional[List[~ConstraintT]] = None) -> None:
```

Initialize a Location instance.


## Properties


### `actions`

Return a copy of the location's actions.

```python
@property
def actions(self):
    # Returns typing.List[~ActionT]
```


### `actors`

Return a copy of the location's actors.

```python
@property
def actors(self):
    # Returns typing.List[~ActorT]
```


### `constraints`

Return the location's constraints.

```python
@property
def constraints(self):
    # Returns typing.Optional[typing.List[~ConstraintT]]
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


## Methods


### `add_action`

Add a single action to the location's actions.

```python
def add_action(self, action: ~ActionT) -> None:
```


### `add_actor`

Add an actor to the location.

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


### `remove_action`

Remove a specific action from the location's actions.

```python
def remove_action(self, action: ~ActionT) -> None:
```


### `remove_actor`

Remove an actor from the location.

```python
def remove_actor(self, actor: ~ActorT) -> None:
```


### `remove_constraint`

Remove a specific constraint from the resource's constraints.

```python
def remove_constraint(self, constraint: ~ConstraintT) -> None:
```


### `to_dict`

Convert the location instance to a dictionary representation.

```python
def to_dict(self) -> Dict[str, Any]:
```


### `update_action`

Replace an existing action with a new action.

```python
def update_action(self, old_action: ~ActionT, new_action: ~ActionT) -> None:
```


### `update_actor`

Replace an existing actor with a new actor.

```python
def update_actor(self, old_actor: ~ActorT, new_actor: ~ActorT) -> None:
```


## Example Usage

```python
# Example: Creating a manufacturing assembly line location
assembly_line = Location(
    name='Assembly Line A',
    georeference=[50.2, 30.5],  # Location coordinates in factory
    location_type=LocationType.INTERNAL,
    actors=[
        Worker('Emma Chen', roles={'Assembler': ['Workstation']}),
        Worker('James Wilson', roles={'QC': ['Inspection']})
    ],
    actions=[
        Action('Assembly', ActionType.ASSEMBLY, duration=45),
        Action('Quality Check', ActionType.QUALITY_CHECK, duration=15)
    ]
)

# Track current activities
current_action = assembly_line.get_current_action()
if current_action:
    print(f'Current activity: {current_action.name} ({current_action.progress}% complete)')

# Manage workers at the location
new_worker = Worker('Maria Garcia', roles={'Assembler': ['Workstation']})
assembly_line.add_actor(new_worker)
print(f'Workers at location: {[w.name for w in assembly_line.actors]}')
```
