# Job

A class to represent a Job in the manufacturing system.

Jobs are the core scheduling and execution units that manage the production of customer-ordered 
Products. They coordinate the sequence of Actions, allocation of Resources, and tracking of 
progress required to manufacture Products. The Job class manages the complete lifecycle of 
manufacturing orders from receipt through completion.

Jobs are connected to various components in the manufacturing system:
- Products being manufactured
- Actions required for production
- Resources allocated to the job
- Workers assigned to tasks
- Customers who ordered products
- Parts required for production
- Storage locations used

Jobs can exist in different states:
- **Planned**: Scheduled but not yet started
- **In Progress**: Currently being executed
- **On Hold**: Temporarily suspended
- **Completed**: Successfully finished
- **Cancelled**: Terminated before completion

Priority levels:
- **Low** (1): Routine jobs with flexible timing
- **Medium** (2): Standard priority jobs
- **High** (3): Urgent jobs requiring preferential treatment
- **Urgent** (4): Critical jobs requiring immediate attention

**Best Practices**:
- Monitor job progress
- Track resource allocation
- Maintain due date compliance
- Update job status accurately
- Monitor priority levels
- Track completion times
- Document job changes
- Monitor resource utilization
- Track quality metrics
- Maintain customer communication
- Document delays or issues

**Attributes**:
| Name | Data Type | Description |
|------|-----------|-------------|
| `id` | `str` | Unique identifier for the job |
| `customer` | `Optional[Actor]` | Customer who placed the order |
| `products` | `Optional[List[Product]]` | Products to be manufactured |
| `due_date` | `Optional[datetime]` | Required completion date |
| `priority` | `Optional[JobPriority]` | Priority level of the job |
| `status` | `JobStatus` | Current status of the job |
| `creation_date` | `datetime` | When the job was created |
| `start_date` | `Optional[datetime]` | When production began |
| `completion_date` | `Optional[datetime]` | When production finished |
| `allocated_resources` | `Dict[str, str]` | Map of Action IDs to Resource IDs |
| `last_modified` | `datetime` | Last modification timestamp |

**Example Configuration**:
```python
job = Job(
    products=[electric_motor, control_panel], # instances of Product class
    customer=industrial_customer, # instance of Actor class
    due_date=datetime(2025, 3, 15),
    priority=JobPriority.HIGH
    )
```
Allocate resources
```python
job.allocate_resource(assembly_action, robot_arm_1)
job.allocate_resource(testing_action, test_station_2)
```
Start production
```python
job.start_job()
```
:::note
`Jobs` are the primary workflow management entities in the manufacturing system. They coordinate all aspects of product manufacture including resource allocation, action sequencing, and progress tracking. Each job maintains its relationship with customer orders, manages resource allocations, and tracks the progress of manufacturing operations through completion.
:::


## Constructor

```python
def __init__(self, products: Optional[List[~ProductT]] = None, customer: Optional[~ActorT] = None, due_date: Optional[datetime.datetime] = None, priority: Optional[omm.JobPriority] = None, id: Optional[str] = None):
```

Initialize a Job instance.


## Properties


### `actions`

Get all actions associated with this job.

```python
@property
def actions(self):
    # Returns typing.List[~ActionT]
```


### `products`

Get all products associated with this job.

```python
@property
def products(self):
    # Returns typing.List[ForwardRef('Product')]
```


## Methods


### `add_action`

Add a new action to this job.

```python
def add_action(self, action: ~ActionT) -> None:
```


### `add_product`

```python
def add_product(self, new_product) -> None:
```


### `allocate_resource`

Allocate resources to a specific action.

```python
def allocate_resource(self, action: ~ActionT, resource: ~ResourceT) -> None:
```


### `cancel_job`

Cancel the job.

```python
def cancel_job(self, reason: str) -> None:
```


### `complete_job`

Mark the job as completed.

```python
def complete_job(self) -> None:
```


### `get_estimated_completion_time`

Calculate estimated completion time in hours.

```python
def get_estimated_completion_time(self) -> float:
```


### `get_in_progress_actions`

Get actions that are currently in progress.

```python
def get_in_progress_actions(self) -> List[~ActionT]:
```


### `get_incomplete_actions`

Get all actions that haven't been completed.

```python
def get_incomplete_actions(self) -> List[~ActionT]:
```


### `get_progress`

Calculate job progress as a percentage.

```python
def get_progress(self) -> float:
```


### `get_ready_actions`

Get actions that are ready to be executed.

```python
def get_ready_actions(self) -> List[~ActionT]:
```


### `is_overdue`

Check if the job is overdue.

```python
def is_overdue(self) -> bool:
```


### `put_on_hold`

Put the job on hold.

```python
def put_on_hold(self, reason: str) -> None:
```


### `remove_action`

Remove an action from this job.

```python
def remove_action(self, action: ~ActionT) -> None:
```


### `remove_product`

Remove a specific product from the job's products.

```python
def remove_product(self, product: 'Product') -> None:
```


### `resume_job`

Resume a job that was on hold.

```python
def resume_job(self) -> None:
```


### `start_job`

Start the manufacturing job.

```python
def start_job(self) -> None:
```


### `to_dict`

Convert the job instance to a dictionary representation.

```python
def to_dict(self) -> Dict[str, Any]:
```


## Example Usage

```python
# Example: Creating a manufacturing job for a custom order
custom_cabinet = Job(
    name='Custom Cabinet Assembly',
    job_type='ASSEMBLY',
    priority=JobPriority.HIGH,
    deadline=datetime.now() + timedelta(days=2),
    required_resources=[
        'CNC_Router_01',  # For cutting panels
        'Assembly_Station_3',  # For assembly
        'Paint_Booth_02'  # For finishing
    ]
)

# Add job requirements
custom_cabinet.add_requirement(
    Requirement('Wood panels', quantity=12)
)

# Track job progress
custom_cabinet.update_status(JobStatus.IN_PROGRESS)
custom_cabinet.update_completion(45)  # 45% complete
```
