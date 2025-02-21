# Worker

A class to represent a Worker in the manufacturing system.

    Workers are specialized Actors that actively perform manufacturing operations in the system.
    They represent human operators, technicians, maintenance staff, and other personnel who
    directly interact with Resources and execute Actions. The Worker class extends the Actor
    class to include role-based capabilities and authorizations.

    Workers are connected to various components in the manufacturing system:
    - Resources they are authorized to operate
    - Locations where they can work
    - Actions they should perform
    - Tools they can use
    - Jobs they are assigned to

    Workers can have multiple roles with specific authorizations:
    - Machine operators for specific equipment
    - Maintenance technicians for certain resource types
    - Quality inspectors for specific processes
    - Material handlers for logistics operations
    - Process specialists for particular manufacturing steps

    **Best Practices**:
    - Clearly define worker roles and authorizations
    - Associate workers with their qualified resources
    - Maintain accurate certification and training records
    - Track worker locations and assignments
    - Update skill sets and capabilities regularly
    - Monitor work hours and schedules (not yet implemented)

    **Attributes**:
    | Name            | Data Type         | Description                                               |
    |-----------------|-------------------|-----------------------------------------------------------|
    | `name`          | `str`             | Human-readable name of the Worker                         |
    | `id`            | `str`             | Unique identifier                                         |
    | `roles`         | `Dict[str, List[str]]` | Dictionary mapping roles to allowed resource types   |
    | `locations`     | `List[Location]`  | Locations where the worker can operate                    |
    | `creation_date` | `datetime`        | Timestamp when the worker was created                     |
    | `last_modified` | `datetime`        | Timestamp of last modification        

    **Example roles configuration**:
    ```
    roles = {
        "Operator": ["Machine", "Workstation"],
        "Technician": ["RoboticArm", "Conveyor"],
        "Inspector": ["QualityStation"],
        }
    ```
    :::note
    The `Worker` class inherits base attributes from the `Actor` class while adding specialized capabilities for manufacturing operations. Use this class for any personnel who actively perform operations in the manufacturing system.
    :::


## Inheritance

Inherits from: `Actor`


## Constructor

```python
def __init__(self, name: str, id: Optional[str] = None, roles: Dict[str, List[str]] = None, locations: List[~LocationT] = None) -> None:
```

Initialize a Worker instance.


## Properties


### `last_modified`

Return the last modified timestamp.

```python
@property
def last_modified(self):
    # Returns <class 'datetime.datetime'>
```


### `locations`

Return a copy of the actor's locations.

```python
@property
def locations(self):
    # Returns typing.List[~LocationT]
```


### `roles`

Return a copy of the worker's roles.

```python
@property
def roles(self):
    # Returns typing.Dict[str, typing.List[str]]
```


## Methods


### `add_location`

Add a location to the actor.

```python
def add_location(self, location: ~LocationT) -> None:
```


### `add_role`

Add or update a role with its allowed resource types.
        
        Example: worker.add_role("Operator", ["Machine"])

```python
def add_role(self, role: str, allowed_resource_types: List[str]) -> None:
```


### `can_work_with`

Check if any of the worker's roles allow them to work with the given resource type.

```python
def can_work_with(self, resource: omm.Resource) -> bool:
```


### `remove_location`

Remove a location from the actor.

```python
def remove_location(self, location: ~LocationT) -> None:
```


### `remove_role`

Remove a role from the worker.

```python
def remove_role(self, role: str) -> None:
```


### `to_dict`

Convert the worker instance to a dictionary representation.

```python
def to_dict(self) -> Dict[str, Any]:
```


### `update_location`

Replace an existing location with a new location.

```python
def update_location(self, old_location: ~LocationT, new_location: ~LocationT) -> None:
```


### `work_on`

Attempt to work on the machine. If a capability is provided,
        start that capability if it is available.

```python
def work_on(self, machine: ~MachineT, capability: Optional[str] = None) -> None:
```


## Example Usage

```python
# Example: Setting up a skilled manufacturing worker
skilled_worker = Worker(
    name='David Miller',
    roles={
        'Machine Operator': ['CNC', 'Lathe', 'Mill'],
        'Quality Inspector': ['Assembly', 'Final Product'],
        'Maintenance': ['Preventive', 'Repair']
    },
    locations=[
        Location('Machining Area', [10.0, 20.0], LocationType.INTERNAL),
        Location('QC Station', [15.0, 20.0], LocationType.INTERNAL)
    ]
)

# Assign new role and verify qualifications
skilled_worker.add_role('Trainer', ['New Operators', 'Safety'])

# Start work on a machine
cnc_machine = Machine('CNC_01', 'CNC', [10.0, 20.0])
if skilled_worker.can_work_with(cnc_machine):
    skilled_worker.work_on(cnc_machine, 'precision_cutting')
    print(f'{skilled_worker.name} operating {cnc_machine.name}')
```
