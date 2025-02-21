# Action

A class to represent manufacturing and logistics Actions.

Actions are fundamental building blocks that 
encapsulate steps required to manufacture a `Product`. They represent discrete 
operations that can be performed by `Resources`, `Machines`, or other entities in the 
manufacturing process.

Actions are associated with various entities through their respective `actions` attributes,
establishing relationships between Actions and classes like `Resource`, `Machine`, `Product`, 
and `Job`. For example:
    - A machine might have actions: `['Setup Machine', 'Drill Hole']`
    - A vehicle might have actions: `['Move Product from Machine A to Resource B', 'Charge Vehicle']`
    - A job might have actions: `['Quality Check', 'Package Product']`

Best Practices:
    - Associate Actions directly with their primary executing entity
    - Assign general or cross-entity Actions to the parent Job
    - Use clear, specific action names that describe the operation
    - Validate all Actions against the ActionType enumeration

Supported Action Types:
* The **Stop** action halts an ongoing operation or process
* The **Load** action transfers parts or products, e.g., into a machine or onto a vehicle
* The **Unload** action removes parts or products, from a machine or vehicle
* The **Move** action transports items between locations in (or outside) the facility
* The **Attach** action connects resources, e.g., an robotic arm onto an AGV
* The **Detach** action separates or disconnects resources
* The **Break** action indicates a scheduled or unscheduled interruption, e.g., lunch break for a worker
* The **Wait** action represents waiting
* The **Process** action executes general manufacturing operations
* The **Assembly** action combines parts into products
* The **Machining** actione executes specific machining operations
* The **Quality Check** action performs quality control inspections
* The **Packinging** action prepares products for storage or shipping
* The **Storage** action places parts or products in designated storage locations
* The **Setup** action configures machines or other resources before operations
* The **Clean** action performs cleaning operations
* The **Inspect** action performs inspection of e.g., resources, locations, parts, or products
* The **Repair** action repairs a resource
* The **Maintenance** action Conducts equipment maintenance tasks

**Attributes**:
| Name            | Data Type                         | Description                                                                           |
|-----------------|-----------------------------------|---------------------------------------------------------------------------------------|
| `name`          | `str`                             | Human-readable name of the Action                                                     |
| `action_type`   | `ActionType`                      | Type of action. See [ActionType](/docs/classes/actiontype)                            |
| `description`   | `str`                             | Detailed description of the action                                                    |
| `duration`      | `float`                           | Expected duration in hours                                                            |
| `job_id`        | `str`                             | ID of the associated job                                                               |
| `status`        | `ActionStatus`                    | Current status. See [ActionStatus](/docs/classes/actionstatus)                          |
| `requirements`  | `List[Requirement]`               | List of requirements for this action                                                   |
| `id`            | `str`                             | Unique identifier                                                                      |
| `sequence_nr`   | `int`                             | Sequence number in the job                                                             |
| `location`      | `Union[Location, Resource]`       | Location or resource where action is performed                                         |
| `worker`        | `Worker`                          | Worker performing the action                                                           |
| `origin`        | `Union[Location, Resource]`       | Starting location for move actions                                                     |
| `destination`   | `Union[Location, Resource]`       | End location for move actions                                                          |
| `route`         | `Route`                           | Route for move actions                                                                 |
| `constraints`    | `List[constraints]`                      | Operating constraints                                                                  |
| `start_time`    | `datetime`                        | Actual start time                                                                      |
| `end_time`      | `datetime`                        | Actual end time                                                                        |
| `progress`      | `float`                           | Completion progress (0-100)                                                            |
| `creation_date` | `datetime`                        | Timestamp when action was created                                                      |
| `last_modified` | `datetime`                        | Timestamp of last modification                                                         |

**Example Configuration**:
```python
action = Action(
    name="Assemble Motor Housing",
    action_type=ActionType.ASSEMBLY,
    description="Attach motor housing to base plate",
    duration=0.5,  # hours
    sequence_nr=1,
    location=assembly_station_1, # instance of Location class
    worker=technician_1, # instance of Worker class
    status=ActionStatus.PLANNED
    )
```


## Constructor

```python
def __init__(self, name: str, action_type: omm.ActionType, description: Optional[str], duration: Optional[float], job_id: Optional[str] = None, status: omm.ActionStatus = <ActionStatus.DRAFT: 1>, requirements: Dict[str, List[str]] = None, id: Optional[str] = None, sequence_nr: Optional[int] = None, location: Optional[~ActionLocationT] = None, worker: Optional[~WorkerT] = None, origin: Optional[~ActionLocationT] = None, destination: Optional[~ActionLocationT] = None, route: Optional[~RouteT] = None, constraints: Optional[List[~ConstraintT]] = None, start_time: Optional[datetime.datetime] = None, end_time: Optional[datetime.datetime] = None, progress: float = 0) -> None:
```

Initialize an Action instance.


## Properties


### `constraints`

Return the action's constraints.

```python
@property
def constraints(self):
    # Returns typing.Optional[typing.List[~ConstraintT]]
```


### `destination`

```python
@property
def destination(self):
    # Returns ~ActionLocationT
```


### `end_time`

```python
@property
def end_time(self):
    # Returns <class 'datetime.datetime'>
```


### `last_modified`

Return the last modified timestamp.

```python
@property
def last_modified(self):
    # Returns <class 'datetime.datetime'>
```


### `location`

```python
@property
def location(self):
    # Returns Any
```


### `origin`

```python
@property
def origin(self):
    # Returns ~ActionLocationT
```


### `progress`

```python
@property
def progress(self):
    # Returns Any
```


### `start_time`

```python
@property
def start_time(self):
    # Returns <class 'datetime.datetime'>
```


### `status`

```python
@property
def status(self):
    # Returns Any
```


### `worker`

```python
@property
def worker(self):
    # Returns Any
```


## Methods


### `add_constraint`

Add a single constraint to the resource's constraints.

```python
def add_constraint(self, constraint: ~ConstraintT) -> None:
```


### `add_requirement`

Add a requirement to the action.

Args:
*   `req_type`: Type of requirement (as string or RequirementType)
*   `specs`: Specifications for the requirement
    
Examples:
*   Action requires a Machine of type Bambu Lab X1C 3D Printer  
```action.add_requirement("Machine", ["Bambu Lab X1C 3D Printer"])``` 
*   Action requires a Vehicle, any type  
```action.add_requirement("Vehicle", [])```
*   Action requires 250 units of Blue Filament  
```action.add_requirement("Part", ["Blue Filament", 250])```
*   Action requires a Worker, any type  
```action.add_requirement("Worker", [])```

```python
def add_requirement(self, req_type: Union[str, omm.RequirementType], specs: Optional[List[Any]] = None) -> None:
```


### `check_requirements_satisfied`

Check if all requirements are satisfied at the given location.

Args:
*   `location`: Location to check requirements against
    
Returns:
*   `Tuple` of `(satisfied: bool, missing_requirements: List[str])`

```python
def check_requirements_satisfied(self, location: 'Location') -> Tuple[bool, List[str]]:
```


### `get_requirements`

Get all requirements or requirements of a specific type.

Args:
*   `req_type`: Type of requirements to get (or None for all)
    
Returns:
*   List of matching requirements

```python
def get_requirements(self, req_type: Union[str, omm.RequirementType, NoneType] = None) -> List[omm.Requirement]:
```


### `remove_constraint`

Remove a specific constraint from the action's constraints.

```python
def remove_constraint(self, constraint: ~ConstraintT) -> None:
```


### `remove_job`

Remove this action's association with a job.

```python
def remove_job(self) -> None:
```


### `remove_requirement`

Remove a requirement from the action.

Args:
*   `req_type`: Type of requirement to remove
*   `specs`: Specific specs to match (or None to remove all of type)

```python
def remove_requirement(self, req_type: Union[str, omm.RequirementType], specs: Optional[List[Any]] = None) -> None:
```


### `set_job`

Associate this action with a job.

```python
def set_job(self, job_id: str) -> None:
```


### `to_dict`

Convert the action instance to a dictionary representation.

```python
def to_dict(self) -> Dict[str, Any]:
```


## Example Usage

```python
# Create a new Action instance
Action(
    name=<str>
    action_type=<ActionType>
    description=<Optional>
    duration=<Optional>
)
```
