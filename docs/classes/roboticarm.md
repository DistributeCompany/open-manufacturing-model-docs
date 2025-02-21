# RoboticArm

A class to represent a RoboticArm.

    Robotic Arms are specialized Resources that perform precise, programmable manufacturing 
    operations. They represent articulated robotic manipulators used for tasks like assembly, 
    welding, painting, pick-and-place operations, or other automated manufacturing processes. 
    The RoboticArm class extends the Resource class to include robot-specific capabilities 
    and parameters for motion control and end-effector management.

    Robotic Arms are connected to various components in the manufacturing system:
    - Locations they operate in
    - Products they manipulate
    - Parts they handle
    - End-effectors they use
    - Actions they perform
    - Sensors monitoring their status
    - Workers who program and maintain them
    - Machines they interface with

    **Best Practices**:
    - Define accurate workspace boundaries
    - Monitor joint positions and speeds
    - Track payload limits
    - Maintain calibration accuracy
    - Schedule preventive maintenance
    - Ensure safety compliance
    - Monitor collision zones
    - Track tool center point (TCP) accuracy
    - Validate motion paths
    - Monitor energy consumption
    - Verify end-effector operations
    - Maintain emergency stop systems

    **Attributes**:
    | Name                 | Data Type          | Description                                                                           |
    |----------------------|--------------------|---------------------------------------------------------------------------------------|
    | `name`               | `str`              | Human-readable name of the RoboticArm                                                 |
    | `georeference`       | `List[float]`      | Base position coordinates [x, y] or [x, y, z]                                          |
    | `arm_type`           | `str`              | Type/model of the robotic arm                                                         |
    | `reach`              | `float`            | Maximum reach distance in meters                                                      |
    | `payload`            | `float`            | Maximum payload capacity in kg                                                        |
    | `degrees_of_freedom` | `int`              | Number of independent joints/axes                                                     |
    | `end_effector_type`  | `str`              | Type of end-of-arm tooling                                                            |
    | `id`                 | `str`              | Unique identifier                                                                      |
    | `status`             | `ResourceStatus`   | Current operational status. See [ResourceStatus](/docs/classes/resourcestatus)          |
    | `power_type`         | `str`              | Power source                                                                           |
    | `power_consumption`  | `float`            | Power usage in kWh                                                                     |
    | `maintenance_interval`| `int`             | Hours between required maintenance                                                     |
    | `last_maintenance`   | `datetime`         | Timestamp of last maintenance                                                          |
    | `hours_used`         | `float`            | Total hours of use since last maintenance                                              |
    | `actors`             | `List[Actor]`      | Workers authorized to operate/maintain this robot                                      |
    | `sensors`            | `List[Sensor]`     | Sensors monitoring this robot                                                          |
    | `actions`            | `List[Action]`     | Actions associated with this robot                                                     |
    | `constraints`         | `List[constraints]`       | Operating constraints                                                                  |
    | `current_position`   | `List[float]`      | Current angles of each joint                                                           |
    | `home_position`      | `List[float]`      | Default/safe position angles                                                           |
    | `creation_date`      | `datetime`         | Timestamp when robot was created                                                       |
    | `last_modified`      | `datetime`         | Timestamp of last modification                                                         |

    **Example Configuration**:
    ```python
    robotic_arm = RoboticArm(
        name="Assembly Robot 1",
        georeference=[5.0, 3.0, 0.0],
        arm_type="6-Axis Industrial Robot",
        reach=1.8,  # meters
        payload=10.0,  # kg
        degrees_of_freedom=6,
        end_effector_type="2-Finger Gripper",
        power_type="electric",
        power_consumption=3.5  # kWh
        )
    ```
    **Common End-Effector Types**:
    - Grippers (2-finger, 3-finger, vacuum)
    - Welding Torches
    - Paint Sprayers
    - Screwdrivers
    - Inspection Cameras
    - Force/Torque Sensors
    - Tool Changers

    **Common Applications**:
    - Pick and Place Operations
    - Assembly Tasks
    - Welding
    - Painting
    - Material Handling
    - Quality Inspection
    - Packaging
    - Machine Tending
    - Palletizing

    :::note
    The `RoboticArm` class inherits base attributes from the `Resource` class while adding specialized capabilities for robotic manipulation. Use this class for programmable robotic manipulators that perform precise manufacturing operations. The class supports multiple degrees of freedom and various end-effector types to accommodate different manufacturing applications.
    :::


## Inheritance

Inherits from: `Resource`


## Constructor

```python
def __init__(self, name: str, georeference: List[float], arm_type: str, reach: float, payload: float, degrees_of_freedom: int, end_effector_type: str, id: Optional[str] = None, location: Optional[omm.Location] = None, power_type: Optional[str] = 'electric', power_consumption: float = 0, maintenance_interval: float = 0, last_maintenance: Optional[datetime.datetime] = None, actors: Optional[List[~ActorT]] = None, actions: Optional[List[~ActionT]] = None, constraints: Optional[List[~ConstraintT]] = None, sensors: Optional[List[~SensorT]] = None, status: omm.ResourceStatus = <ResourceStatus.IDLE: 4>) -> None:
```

Initialize a RoboticArm instance.


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


### `change_end_effector`

Change the end effector type.

```python
def change_end_effector(self, new_type: str) -> None:
```


### `check_payload`

Check if a given weight is within the arm's payload capacity.

```python
def check_payload(self, weight: float) -> bool:
```


### `get_current_action`

Get the current in-progress action.

```python
def get_current_action(self) -> Optional[~ActionT]:
```


### `get_current_position`

Get the current joint positions of the robotic arm.

```python
def get_current_position(self) -> List[float]:
```


### `home`

Move the robotic arm to its home position.

```python
def home(self) -> None:
```


### `move_to_position`

Move the robotic arm to a specific joint configuration.

```python
def move_to_position(self, position: List[float]) -> None:
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
# Example: Setting up a sophisticated robotic arm
robot_arm = RoboticArm(
    name='Robot_01',
    georeference=[12.0, 8.0, 0.0],
    arm_type='6-axis',
    reach=1.8,  # meters
    payload=15.0,  # kg
    degrees_of_freedom=6,
    end_effector_type='multi_purpose_gripper',
    sensors=[
        Sensor('joint_position'),
        Sensor('torque'),
        Sensor('gripper_force'),
        Sensor('collision_detection')
    ]
)

# Program robotic movement
pick_position = [0.0, 45.0, 90.0, 0.0, 45.0, 0.0]  # Joint angles
if robot_arm.check_payload(5.0):  # Check if weight is within limits
    robot_arm.move_to_position(pick_position)
    print(f'Robot at position: {robot_arm.get_current_position()}')

# Change end effector for different task
robot_arm.change_end_effector('precision_welder')
print(f'Current end effector: {robot_arm.end_effector_type}')

# Return to safe position
robot_arm.home()
print('Robot returned to home position')
```
