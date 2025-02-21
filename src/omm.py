from dataclasses import dataclass
from typing import List, Optional, TypeVar, ClassVar, Dict, Any, Union, Set, Tuple, get_args
from datetime import datetime
import uuid
from weakref import WeakSet
import logging
from enum import Enum, auto
import pandas as pd 

# Type variables for cross-referencing classes
LocationT = TypeVar('LocationT', bound='Location')
ActorT = TypeVar('ActorT', bound='Actor')
ActionT = TypeVar('ActionT', bound='Action')
ResourceT = TypeVar('ResourceT', bound='Resource')
ConstraintT = TypeVar('ConstraintT', bound='Constraint')
SensorT = TypeVar('SensorT', bound='Sensor')
RouteT = TypeVar('RouteT', bound='Route')
MachineT = TypeVar('MachineT', bound='Machine')
WorkerT = TypeVar('WorkerT', bound='Worker')
ActionLocationT = TypeVar('ActionLocationT', bound=Union['Location', 'Resource'])
ProductT = TypeVar('ProductT',bound='Product')

class LocationType(Enum):
    """Enumeration of valid location types.
    
    Defines the different categories of locations within and outside the manufacturing
    facility to help track and manage material flow and resource positioning.
    """
    INTERNAL = auto()    # Location within the manufacturing facility's boundaries
    EXTERNAL = auto()    # Location outside the facility (suppliers, customers, etc.) 

class ResourceType(Enum):
    """Enumeration of valid resource types.
    
    Defines the different categories of manufacturing resources that can be used
    in production operations. Each type represents a specific kind of equipment
    or asset used in the manufacturing process.
    """
    GENERAL = auto()        # Generic resource without specific categorization
    MACHINE = auto()        # Stationary manufacturing equipment (mills, lathes, etc.)
    WORKSTATION = auto()    # Manual or semi-automated work area for operators
    CONVEYOR = auto()       # Automated material handling system for continuous flow
    ROBOTIC_ARM = auto()    # Programmable robotic manipulator for automated tasks
    VEHICLE = auto()        # Mobile equipment for material transport (AGVs, forklifts)
    TOOL = auto()           # Specialized equipment or implements used in manufacturing

class ActionStatus(Enum):
    """Enumeration of valid action statuses.
    
    Represents the lifecycle states of an Action, from initial creation through completion
    or cancellation. These statuses help track the progress of manufacturing operations
    and enable workflow management.
    """
    
    DRAFT = auto()        # Initial state when action is created but not yet ready for execution
    REQUESTED = auto()    # Action has been submitted for approval or scheduling
    CONFIRMED = auto()    # Action has been approved and scheduled for execution
    IN_PROGRESS = auto()  # Action is currently being executed
    COMPLETED = auto()    # Action has been successfully finished
    CANCELLED = auto()    # Action was terminated before completion or rejected

class ActionType(Enum):
    """Enumeration of valid action types.
    
    Defines the different types of operations that can be performed in a manufacturing
    or logistics environment. Each type represents a specific category of action that
    can be assigned to resources, machines, or jobs.
    """
    STOP = auto()         # Immediately halt current operation for safety or process reasons
    LOAD = auto()         # Transfer materials or products into a machine or workstation
    UNLOAD = auto()       # Remove materials or products from a machine or workstation
    MOVE = auto()         # Transport items between locations in the facility
    ATTACH = auto()       # Connect or join components or sub-assemblies together
    DETACH = auto()       # Separate or disconnect assembled components
    BREAK = auto()        # Scheduled or unscheduled interruption in operations
    WAIT = auto()         # Planned delay or holding period in the process
    PROCESS = auto()      # General manufacturing operation or transformation
    ASSEMBLY = auto()     # Combine multiple components into a larger assembly
    MACHINING = auto()    # Perform specific machining operations on parts
    QUALITY_CHECK = auto()# Inspect products for quality standards compliance
    PACKAGING = auto()    # Prepare products for storage or shipping
    STORAGE = auto()      # Place items in designated storage locations
    SETUP = auto()        # Configure or prepare machines/workstations for operation
    CLEAN = auto()        # Perform cleaning operations on equipment or workspace
    INSPECT = auto()      # Examine equipment or products for issues or maintenance needs
    REPAIR = auto()       # Fix damaged or malfunctioning equipment
    MAINTENANCE = auto()  # Perform preventive or scheduled maintenance tasks

class ResourceStatus(Enum):
    """Enumeration of valid resource statuses.
    
    Defines the possible states a resource can be in during operations, helping track
    resource availability and utilization.
    """
    WAIT = auto()         # Resource is available but waiting for next task
    LOAD = auto()         # Resource is currently loading materials or products
    UNLOAD = auto()       # Resource is currently unloading materials or products
    IDLE = auto()         # Resource is available but not actively working
    WORKING = auto()      # Resource is actively performing an assigned task
    FAILED = auto()       # Resource has encountered an error or malfunction
    CHARGING = auto()     # Resource is recharging or refueling

class VehicleType(Enum):
    """Enumeration of available vehicle types.
    
    Defines the different categories of vehicles that can be used for material
    handling and transportation within the facility.
    """
    GENERIC_AUTOMATED_VEHICLE = auto()  # General-purpose autonomous vehicle
    GENERIC_MANUAL_VEHICLE = auto()     # General-purpose manually operated vehicle
    AUTOMATED_MOBILE_ROBOT = auto()     # Specialized autonomous robot for material handling
    MANUAL_FORKLIFT = auto()            # Traditional operator-driven forklift

class StorageType(Enum):
    """Enumeration of different types of storage locations.
    
    Defines the various storage areas and configurations available in the facility
    for holding materials, work-in-progress, and finished goods.
    """
    GENERAL = auto()      # Multi-purpose storage area without specific designation
    WAREHOUSE = auto()    # Large-scale storage facility for long-term storage
    RACK = auto()         # Structured storage system with multiple levels
    BUFFER = auto()       # Temporary storage area between operations
    QUEUE = auto()        # FIFO storage area for sequential processing

class ProductionState(Enum):
    """Enumeration of different production states for parts and products.
    
    Defines the various stages a part or product can be in during the manufacturing
    process, from raw material to finished product.
    """
    RAW = auto()              # Unprocessed material at start of production
    NEW = auto()              # Newly created or received item
    WORK_IN_PROGRESS = auto() # Partially completed item in production
    FINISHED = auto()         # Completed item ready for delivery
    DEFECTIVE = auto()        # Item that fails quality standards
    ON_HOLD = auto()          # Item temporarily suspended from production

class PartType(Enum):
    """Enumeration of different types of parts.
    
    Defines the categories of parts used in the manufacturing process based on
    their source and nature.
    """
    RAW_MATERIAL = "Raw Material"               # Unprocessed materials used in manufacturing
    PURCHASED_COMPONENT = "Purchased Component" # Pre-made components from external suppliers
    WORK_IN_PROGRESS = "Work-In-Progress"       # Partially completed products

class JobStatus(Enum):
    """Enumeration of manufacturing job statuses.
    
    Defines the possible states of a manufacturing job throughout its lifecycle,
    from planning to completion.
    """
    PLANNED = auto()      # Job is scheduled but not yet started
    IN_PROGRESS = auto()  # Job is currently being executed
    ON_HOLD = auto()      # Job is temporarily suspended
    COMPLETED = auto()    # Job has been successfully finished
    CANCELLED = auto()    # Job was terminated before completion

class JobPriority(Enum):
    """Enumeration of priority levels for jobs.
    
    Defines the urgency levels that can be assigned to manufacturing jobs,
    helping determine processing order and resource allocation.
    """
    LOW = 1              # Routine job with flexible timing
    MEDIUM = 2           # Standard priority job
    HIGH = 3             # Urgent job requiring preferential treatment
    URGENT = 4           # Critical job requiring immediate attention

class RequirementType(Enum):
    """Types of requirements that can be specified for an action."""
    MACHINE = auto()
    WORKSTATION = auto()
    CONVEYER = auto()
    ROBOTIC_ARM = auto()
    VEHICLE = auto()
    PART = auto()
    PRODUCT = auto()
    WORKER = auto()
    TOOL = auto()

class Resource:
    """A class to represent a Resource in the manufacturing system.

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
    """
    # Class variables
    _instances = WeakSet()
    _total_instances = 0
    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        name: str,
        resource_type: ResourceType,
        georeference: List[float],
        id: Optional[str] = None,
        location: Optional[LocationT] = None,
        status: ResourceStatus = ResourceStatus.IDLE,
        power_type: Optional[str] = "manual",  # manual, electric, pneumatic, etc.
        power_consumption: float = 0,   # in kWh
        maintenance_interval: float = 0, # Hours between maintenance
        last_maintenance: Optional[datetime] = None,
        actors: List[ActorT] = None,
        actions: List[ActionT] = None,
        sensors: List[SensorT] = None,
        constraints: Optional[List[ConstraintT]] = None,
    ) -> None:
        """Initialize a Resource instance."""
        self.name = name
        self.resource_type = resource_type
        self._georeference = georeference
        self.id = id if id is not None else str(uuid.uuid4())
        self._actors = actors if actors is not None else []
        self._actions = actions if actions is not None else []
        self._sensors = sensors if sensors is not None else []
        self._constraints = constraints if constraints is not None else []
        self.creation_date = datetime.now()
        self._last_modified = datetime.now()
        self.power_type = power_type
        self.power_consumption = power_consumption
        self.maintenance_interval = maintenance_interval
        self.last_maintenance = last_maintenance
        self._status = status
        self._location = location  
        self._hours_used = 0

        self._validate()
        self._register_instance()
        self._logger.info(f"Created new resource: {self}")

    def __repr__(self) -> str:
        """Return string representation of the Resource instance."""
        return (f"Resource(name='{self.name}', resource_type={self.resource_type}, "
                f"_georeference={self._georeference}, id='{self.id}', "
                f"last_modified={self._last_modified})")

    def __hash__(self):
        """Return hash of the Resource instance."""
        return hash(self.id)
    
    def __eq__(self, other):
        """Compare Resource instances for equality."""
        if not isinstance(other, Resource):
            return NotImplemented
        return self.id == other.id

    def _validate(self) -> None:
        """Validate the resource's attributes."""
        if not self.name or not self.name.strip():
            raise ValueError("Resource name cannot be empty")
        if not isinstance(self._georeference, list) or len(self._georeference) > 3:
            raise ValueError("Georeference must be a list of two floats [x,y] or three floats [x,y,z]")
        if not all(isinstance(x, (int, float)) for x in self._georeference):
            raise ValueError("Georeference coordinates must be numeric")
        if not isinstance(self._actors, list):
            raise ValueError("Actors must be provided as a list")
        if not isinstance(self._sensors, list):
            raise ValueError("Sensors must be provided as a list")
        if self._constraints is not None and not isinstance(self._constraints, list):
            raise ValueError("Constraints must be provided as a list")

    def _register_instance(self) -> None:
        """Register the instance in the WeakSet and increment counter."""
        self.__class__._instances.add(self)
        self.__class__._total_instances += 1

    def _initialize_statistics(self) -> None:
        """Initialize the cumulative statistics DataFrame."""
        self.cum_statistics = pd.DataFrame(columns=[
            'timestamp', 'id', 'name', 'time_in_system', 'working', 'wait',
            'load', 'unload', 'idle', 'failed', 'charging', 'utilization',
            'entries', 'exits', 'energy_consumption', 'distance_traveled'
        ])
        
        # Initialize first statistics record
        start_stats = pd.DataFrame([{
            'timestamp': datetime.now(),
            'id': self.id,
            'name': self.name,
            'time_in_system': 0,
            'working': 0,
            'wait': 0,
            'load': 0,
            'unload': 0,
            'idle': 0,
            'failed': 0,
            'charging': 0,
            'utilization': 0,
            'entries': 0,
            'exits': 0,
            'energy_consumption': 0,
            'distance_traveled': 0
        }])
        self.cum_statistics = pd.concat([self.cum_statistics, start_stats], ignore_index=True)

    @property
    def entries(self) -> int:
        """Return the number of entries for the resource."""
        return self._entries

    @entries.setter
    def entries(self, new_entries: int) -> None:
        """Set the number of entries."""
        if not isinstance(new_entries, int):
            raise TypeError("Number of entries must be an integer")
        if new_entries < self._entries:
            raise ValueError(f"Number of entries cannot decrease. New Value: {new_entries}. Current Value: {self._entries}")
        self._entries = new_entries
        self._update_last_modified()
        self._logger.debug(f"Updated entries for resource {self.id} to {self._entries}")

    @property
    def exits(self) -> int:
        """Return the number of exits for the resource."""
        return self._exits

    @exits.setter
    def exits(self, new_exits: int) -> None:
        """Set the number of exits."""
        if not isinstance(new_exits, int):
            raise TypeError("Number of exits must be an integer")
        if new_exits < self._exits:
            raise ValueError(f"Number of exits cannot decrease. New Value: {new_exits}. Current Value: {self._exits}")
        if new_exits > self._entries:
            raise ValueError(f"Number of exits cannot exceed number of entries. Current entries: {self._entries}. Current exits: {self._exits}. New exits: {new_exits}")        
        self._exits = new_exits
        self._update_last_modified()
        self._logger.debug(f"Updated exits for resource {self.id} to {self._exits}")

    @property
    def status(self) -> ResourceStatus:
        """Return the status of the resource."""
        return self._status
    
    @status.setter
    def status(self, new_status: ResourceStatus) -> None:
        """Set the status of the resource."""
        self._status = new_status
        self._update_last_modified()
        self._logger.info(f"Updated status for resource {self.id} to {new_status}")

    @property
    def actions(self) -> List[ActionT]:
        """Return a copy of the resource's actions."""
        return self._actions.copy()

    @property
    def actors(self) -> List[ActorT]:
        """Return a copy of the resource's actors."""
        return self._actors.copy()

    @property
    def sensors(self) -> List[SensorT]:
        """Return a copy of the resource's sensors."""
        return self._sensors.copy()
    
    @property
    def georeference(self) -> List[float]:
        """Return the resource's georeference."""
        return self._georeference
    
    @georeference.setter
    def georeference(self, georeference: List[float]):
        """Set the resource's georeference."""
        self._validate_georeference(georeference)
        self._georeference = georeference    
        self._update_last_modified()
        self._logger.debug(f"Updated georeference for resource {self.id}")  

    @property
    def constraints(self) -> Optional[List[ConstraintT]]:
        """Return the resource's constraints."""
        return self._constraints
    
    def add_constraint(self, constraint: ConstraintT) -> None:
        """Add a single constraint to the resource's constraints."""
        if not isinstance(constraint, Constraint):
            raise TypeError("constraint must be an instance of Constraint")
        self._constraints.append(constraint)
        self._update_last_modified()
        self._logger.debug(f"Added constraint to resource {self.id}")

    def remove_constraint(self, constraint: ConstraintT) -> None:
        """Remove a specific constraint from the resource's constraints."""
        if not isinstance(constraint, Constraint):
            raise TypeError("constraint must be an instance of Constraint")
        try:
            self._constraints.remove(constraint)
            self._update_last_modified()
            self._logger.debug(f"Deleted constraint from resource {self.id}")
        except ValueError:
            raise ValueError("The specified constraint is not in the constraints list")

    @property
    def last_modified(self) -> datetime:
        """Return the last modified timestamp."""
        return self._last_modified
                         
    def _validate_georeference(self, georeference: List[float]) -> None:
        """Validate georeference coordinates."""
        if not isinstance(georeference, list) or len(georeference) > 3:
            raise ValueError("Georeference must be a list of two floats [x,y] or three floats [x,y,z]")
        if not all(isinstance(x, (int, float)) for x in georeference):
            raise ValueError("Georeference coordinates must be numeric") 
           
    def _update_last_modified(self) -> None:
        """Update the last modified timestamp with logging."""
        self._last_modified = datetime.now()
        self._logger.debug(f"Updated last_modified for resource {self.id} to {self._last_modified}")

    def add_action(self, action: ActionT) -> None:
        """Add a single action to the resource's actions."""
        if not isinstance(action, Action):
            raise TypeError("action must be an instance of Action")
        self._actions.append(action)
        self._update_last_modified()
        self._logger.debug(f"Added action to resource {self.id}")

    def remove_action(self, action: ActionT) -> None:
        """Remove a specific action from the resource's actions."""
        if not isinstance(action, Action):
            raise TypeError("action must be an instance of Action")
        try:
            self._actions.remove(action)
            self._update_last_modified()
            self._logger.debug(f"Deleted action from resource {self.id}")
        except ValueError:
            raise ValueError("The specified action is not in the actions list")

    def get_current_action(self) -> Optional[ActionT]:
        """Get the current in-progress action."""
        return next((action for action in self._actions 
                    if hasattr(action, "status") and 
                    action.status == ActionStatus.IN_PROGRESS), None)
    
    def add_actor(self, actor: ActorT) -> None:
        """Add an actor to the resource."""
        if not isinstance(actor, Actor):
            raise ValueError("An Actor must be an instance of Actor")
        self._actors.append(actor)
        self._update_last_modified()
        self._logger.debug(f"Added actor to resource {self.id}")

    def update_actor(self, old_actor: ActorT, new_actor: ActorT) -> None:
        """Replace an existing actor with a new actor."""
        if not isinstance(old_actor, Actor):
            raise TypeError("old_actor must be an instance of Actor")
        if not isinstance(new_actor, Actor):
            raise TypeError("new_actor must be an instance of Actor")
        try:
            index = self._actors.index(old_actor)
        except ValueError:
            raise ValueError("The specified old actor is not associated with this resource.")
        self._actors[index] = new_actor
        self._update_last_modified()
        self._logger.debug(f"Updated actor in route {self.id}.")

    def remove_actor(self, actor: ActorT) -> None:
        """Remove an actor from the resource."""
        if not isinstance(actor, Actor):
            raise ValueError("An Actor must be an instance of Actor")
        try:
            self._actors.remove(actor)
            self._update_last_modified()
            self._logger.debug(f"Removed actor from resource {self.id}")
        except ValueError:
            raise ValueError("The specified actor is not present in the resource.")

    def operate(self) -> None:
        """Operate Resource."""
        if self._status == 'failed':
            raise ValueError("Cannot operate: resource is in failed state")
        self._logger.info(f"Resource {self.name} ({self.resource_type}) is now operating.")
        self._status = ResourceStatus.WORKING
        self._update_last_modified()

    def needs_maintenance(self) -> bool:
        """Check if tool needs maintenance based on usage hours."""
        if self.maintenance_interval is None:
            return False
        return self._hours_used >= self.maintenance_interval

    def perform_maintenance(self) -> None:
        """Perform maintenance on the tool."""
        self.last_maintenance = datetime.now()
        self._hours_used = 0
        self._update_last_modified()
        self._logger.info(f"Performed maintenance on tool {self.name}")

    @classmethod
    def get_by_id(cls, id: str) -> Optional['Resource']:
        """Retrieve a resource instance by ID."""
        return next((res for res in cls._instances if res.id == id), None)

    @classmethod
    def get_by_type(cls, resource_type: ResourceType) -> List['Resource']:
        """Retrieve all resources of a specific type."""
        return [res for res in cls._instances if res.resource_type == resource_type]

    @classmethod
    def get_by_status(cls, status: str) -> List['Resource']:
        """Get all resource with a specific status."""
        return [equip for equip in cls._instances if equip._status == status]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the resource instance to a dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'resource_type': self.resource_type.name,
            'georeference': self.georeference,
            'creation_date': self.creation_date.isoformat(),
            'last_modified': self.last_modified.isoformat(),
            'total_actions': len(self._actions),
            'status': self._status,
            'location': str(self._location.name) if self._location else None,
            'entries': self._entries,
            'exits': self._exits
        }

class Location:
    """A class to represent a geographical Location in (or outside) the manufacturing system.

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
    """
    # Class variables
    _instances = WeakSet()
    _total_instances = 0
    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        name: str,
        georeference: List[float],
        location_type: LocationType = LocationType.EXTERNAL,
        id: Optional[str] = None,
        actors: List[ActorT] = None,
        actions: List[ActionT] = None,
        constraints: Optional[List[ConstraintT]] = None,
    ) -> None:
        """Initialize a Location instance."""
        self.name = name
        self._georeference = georeference
        self.location_type = location_type
        self.id = id if id is not None else str(uuid.uuid4())
        self._actors = actors if actors is not None else []
        self._actions = actions if actions is not None else []
        self._constraints = constraints if constraints is not None else []
        self.creation_date = datetime.now()
        self._last_modified = datetime.now()
        
        self._validate()
        self._register_instance()
        self._logger.info(f"Created new location: {self}")

    def __repr__(self) -> str:
        """Return string representation of the Location instance."""
        return (f"Location(name='{self.name}', georeference={self._georeference}, "
                f"location_type={self.location_type.name}, id='{self.id}', "
                f"actors={self._actors}, last_modified={self._last_modified})")

    def _validate(self) -> None:
        """Validate the location's attributes."""
        if not self.name or not self.name.strip():
            raise ValueError("Location name cannot be empty")
        if not isinstance(self._georeference, list) or len(self._georeference) > 3:
            raise ValueError("Georeference must be a list of two floats [x,y] or three floats [x,y,z]")
        if not all(isinstance(x, (int, float)) for x in self._georeference):
            raise ValueError("Georeference coordinates must be numeric")
        if not isinstance(self._actors, list):
            raise ValueError("Actors must be provided as a list")
        if not all(isinstance(actor, Actor) for actor in self._actors):
            raise ValueError("Actors must be an instance of Actor")
        if not isinstance(self._actions, list):
            raise ValueError("Actions must be provided as a list")
        if not all(isinstance(action, Action) for action in self._actions):
            raise ValueError("Actions must be an instance of Action")
        if self._constraints is not None and not isinstance(self._constraints, list):
            raise ValueError("Constraints must be provided as a list")

    def __hash__(self):
        """Return hash of the Location instance."""
        return hash(self.id)
    
    def __eq__(self, other):
        """Compare Location instances for equality."""
        if not isinstance(other, Location):
            return NotImplemented
        return self.id == other.id

    def _register_instance(self) -> None:
        """Register the instance in the WeakSet and increment counter."""
        self.__class__._instances.add(self)
        self.__class__._total_instances += 1

    @property
    def actors(self) -> List[ActorT]:
        """Return a copy of the location's actors."""
        return self._actors.copy()

    @property
    def actions(self) -> List[ActionT]:
        """Return a copy of the location's actions."""
        return self._actions.copy()

    @property
    def georeference(self) -> List[float]:
        """Return the resource's georeference."""
        return self._georeference
    
    @georeference.setter
    def georeference(self, georeference: List[float]):
        """Set the resource's georeference."""
        self._validate_georeference(georeference)
        self._georeference = georeference    
        self._update_last_modified()
        self._logger.debug(f"Updated georeference for location {self.id}")

    @property
    def constraints(self) -> Optional[List[ConstraintT]]:
        """Return the location's constraints."""
        return self._constraints

    def add_constraint(self, constraint: ConstraintT) -> None:
        """Add a single constraint to the resource's constraints."""
        if not isinstance(constraint, Constraint):
            raise TypeError("constraint must be an instance of Constraint")
        self._constraints.append(constraint)
        self._update_last_modified()
        self._logger.debug(f"Added constraint to resource {self.id}")

    def remove_constraint(self, constraint: ConstraintT) -> None:
        """Remove a specific constraint from the resource's constraints."""
        if not isinstance(constraint, Constraint):
            raise TypeError("constraint must be an instance of Constraint")
        try:
            self._constraints.remove(constraint)
            self._update_last_modified()
            self._logger.debug(f"Deleted constraint from resource {self.id}")
        except ValueError:
            raise ValueError("The specified constraint is not in the constraints list")

    @property
    def last_modified(self) -> datetime:
        """Return the last modified timestamp."""
        return self._last_modified

    def _validate_georeference(self, georeference: List[float]) -> None:
        """Validate georeference coordinates."""
        if not isinstance(georeference, list) or len(georeference) != 2:
            raise ValueError("Georeference must be a list of two floats [latitude, longitude]")
        if not all(isinstance(x, (int, float)) for x in georeference):
            raise ValueError("Georeference coordinates must be numeric")

    def _update_last_modified(self) -> None:
        """Update the last modified timestamp with logging."""
        self._last_modified = datetime.now()
        self._logger.debug(f"Updated last_modified for location {self.id} to {self._last_modified}")

    def add_action(self, action: ActionT) -> None:
        """Add a single action to the location's actions."""
        if not isinstance(action, Action):
            raise TypeError("action must be an instance of Action")
        self._actions.append(action)
        self._update_last_modified()
        self._logger.debug(f"Added action to location {self.id}")

    def update_action(self, old_action: ActionT, new_action: ActionT) -> None:
        """Replace an existing action with a new action."""
        if not isinstance(old_action, Action):
            raise TypeError("old_action must be an instance of Action")
        if not isinstance(new_action, Action):
            raise TypeError("new_action must be an instance of Action")
        try:
            index = self.actions.index(old_action)
        except ValueError:
            raise ValueError("The specified old action is not associated with this location.")
        self._actions[index] = new_action
        self._update_last_modified()
        self._logger.debug(f"Updated action of location {self.id}.")

    def remove_action(self, action: ActionT) -> None:
        """Remove a specific action from the location's actions."""
        if not isinstance(action, Action):
            raise TypeError("action must be an instance of Action")
        try:
            self._actions.remove(action)
            self._update_last_modified()
            self._logger.debug(f"Deleted action from location {self.id}")
        except ValueError:
            raise ValueError("The specified action is not in the actions list")

    def get_current_action(self) -> Optional[ActionT]:
        """Get the current in-progress action."""
        return next((action for action in self._actions 
                    if hasattr(action, "status") and 
                    action.status == ActionStatus.IN_PROGRESS), None)
    
    def add_actor(self, actor: ActorT) -> None:
        """Add an actor to the location."""
        if not isinstance(actor, Actor):
            raise ValueError("An Actor must be an instance of Actor")
        self._actors.append(actor)
        self._update_last_modified()
        self._logger.debug(f"Added actor to location {self.id}")

    def update_actor(self, old_actor: ActorT, new_actor: ActorT) -> None:
        """Replace an existing actor with a new actor."""
        if not isinstance(old_actor, Actor):
            raise TypeError("old_actor must be an instance of Actor")
        if not isinstance(new_actor, Actor):
            raise TypeError("new_actor must be an instance of Actor")
        try:
            index = self.actors.index(old_actor)
        except ValueError:
            raise ValueError("The specified old actor is not associated with this location.")
        self._actors[index] = new_actor
        self._update_last_modified()
        self._logger.debug(f"Updated actor of location {self.id}.")

    def remove_actor(self, actor: ActorT) -> None:
        """Remove an actor from the location."""
        if not isinstance(actor, Actor):
            raise ValueError("An Actor must be an instance of Actor")
        try:
            self._actors.remove(actor)
            self._update_last_modified()
            self._logger.debug(f"Removed actor from location {self.id}")
        except ValueError:
            raise ValueError("The specified actor is not present in the location.")

    @classmethod
    def get_by_id(cls, id: str) -> Optional[LocationT]:
        """Retrieve a location instance by ID."""
        return next((loc for loc in cls._instances if loc.id == id), None)

    @classmethod
    def get_by_name(cls, name: str) -> Optional[LocationT]:
        """Retrieve a location instance by name."""
        return next((loc for loc in cls._instances if loc.name == name), None)

    @classmethod
    def get_by_type(cls, location_type: LocationType) -> List[LocationT]:
        """Retrieve all location instances of a specific type."""
        return [loc for loc in cls._instances if loc.location_type == location_type]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the location instance to a dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'georeference': self.georeference,
            'location_type': self.location_type.name if hasattr(self.location_type, 'name') else self.location_type,
            'creation_date': self.creation_date.isoformat(),
            'last_modified': self._last_modified.isoformat()
        }
     
class Actor:
    """A class to represent an Actor in the manufacturing system.

    Actors are entities that participate in the manufacturing environment without directly 
    performing manufacturing operations. They represent stakeholders such as customers, 
    suppliers, service providers, and other external or internal parties that interact 
    with the manufacturing system.

    Actors establish relationships with manufacturing processes through:
        - Business relationships (customer orders, supplier deliveries)
        - Service agreements (maintenance providers, logistics partners)
        - Resource ownership (equipment providers, facility owners)
        - Process oversight (quality inspectors, auditors)

    The Actor class serves as a base class for more specialized actor types:
        - `Worker`: Performs actual manufacturing operations
        - `Customer`: Places orders and receives finished products (not yet implemented)
        - `Supplier`: Provides raw materials and components (not yet implemented)
        - `Service Provider`: Offers maintenance and support services (not yet implemented)

    **Best Practices**:
    - Associate Actors with specific locations where they operate
    - Use meaningful names that describe the Actor's role

    **Attributes**:
    | Name            | Data Type       | Description                                               |
    |-----------------|-----------------|-----------------------------------------------------------|
    | `name`          | `str`           | Human-readable name of the Actor                          |
    | `id`            | `str`           | Unique identifier                                         |
    | `locations`     | `List[Location]`| List of locations associated with this actor              |
    | `creation_date` | `datetime`      | Timestamp when the actor was created                      |
    | `last_modified` | `datetime`      | Timestamp of last modification       

    **Example Configuration**
    ```python
    actor = Actor(
        name="Acme Corporation",
        locations=[main_warehouse, shipping_dock], # instances of Location class
        id="SUPPLIER_001"
        )
    ```

    :::note
    For actors who actively perform manufacturing operations (operators, technicians, maintenance staff), use the `Worker` subclass instead of the `Actor` base class.
    :::
    """
    # Class variables
    _instances = WeakSet()
    _total_instances = 0
    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        name: str,
        id: Optional[str] = None,
        locations: List[LocationT] = None,
    ) -> None:
        """Initialize an Actor instance."""
        self.name = name
        self.id = id if id is not None else str(uuid.uuid4())
        self._locations = locations if locations is not None else []
        self.creation_date = datetime.now()
        self._last_modified = datetime.now()
        
        self._validate()
        self._register_instance()
        self._logger.info(f"Created new actor: {self}")

    def __repr__(self) -> str:
        """Return string representation of the Actor instance."""
        return f"Actor(name='{self.name}', id='{self.id}', locations={self._locations}, last_modified={self._last_modified})"

    def __hash__(self):
        """Return hash of the Actor instance."""
        return hash(self.id)
    
    def __eq__(self, other):
        """Compare Actor instances for equality."""
        if not isinstance(other, Actor):
            return NotImplemented
        return self.id == other.id

    def _validate(self) -> None:
        """Validate the actor's attributes."""
        if not self.name or not self.name.strip():
            raise ValueError("Actor name cannot be empty")
        if self._locations is not None and not isinstance(self._locations, list):
            raise ValueError("Locations must be provided as a list or left as the default empty list.")

    def _register_instance(self) -> None:
        """Register the instance in the WeakSet and increment counter."""
        self.__class__._instances.add(self)
        self.__class__._total_instances += 1

    @property
    def locations(self) -> List[LocationT]:
        """Return a copy of the actor's locations."""
        return self._locations.copy()

    @property
    def last_modified(self) -> datetime:
        """Return the last modified timestamp."""
        return self._last_modified

    def _update_last_modified(self) -> None:
        """Update the last modified timestamp with logging."""
        self._last_modified = datetime.now()
        self._logger.debug(f"Updated last_modified for actor {self.id} to {self._last_modified}")

    def add_location(self, location: LocationT) -> None:
        """Add a location to the actor."""
        if not isinstance(location, Location):
            raise TypeError("location must be an instance of Location")
        if location in self._locations:
            self._logger.debug(f"Location already exists for actor {self.id}")
            return
        self._locations.append(location)
        self._update_last_modified()
        self._logger.debug(f"Added location to actor {self.id}")

    def update_location(self, old_location: LocationT, new_location: LocationT) -> None:
        """Replace an existing location with a new location."""
        if not isinstance(old_location, Location):
            raise TypeError("old_location must be an instance of Location")
        if not isinstance(new_location, Location):
            raise TypeError("new_location must be an instance of Location")
        try:
            index = self._locations.index(old_location)
        except ValueError:
            raise ValueError("The specified old location is not associated with this actor.")
        self._locations[index] = new_location
        self._update_last_modified()
        self._logger.debug(f"Updated location for actor {self.id}")

    def remove_location(self, location: LocationT) -> None:
        """Remove a location from the actor."""
        if not isinstance(location, Location):
            raise TypeError("location must be an instance of Location")
        try:
            self._locations.remove(location)
            self._update_last_modified()
            self._logger.debug(f"Removed location from actor {self.id}")
        except ValueError:
            raise ValueError("The specified location is not associated with this actor.")

    @classmethod
    def get_by_id(cls, id: str) -> Optional[ActorT]:
        """Retrieve an actor instance by ID."""
        return next((actor for actor in cls._instances if actor.id == id), None)

    @classmethod
    def get_by_name(cls, name: str) -> List[ActorT]:
        """Retrieve all actor instances with the given name."""
        return [actor for actor in cls._instances if actor.name == name]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the actor instance to a dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'locations': [str(loc) for loc in self._locations],
            'creation_date': self.creation_date.isoformat(),
            'last_modified': self._last_modified.isoformat()
        }
    
class Route:
    """A class to represent a Route.

    Routes define paths that connect different Locations within and outside the manufacturing
    environment. They are primarily used for planning and executing movement Actions of 
    mobile Resources like Vehicles, and typically include multiple waypoints.

    Routes are connected to various components in the manufacturing system:
    - Locations that the route connects
    - Vehicles that can traverse the route
    - Actions that use the route (i.e, 'move' actions)

    **Best Practices**:
    - Define accurate georeference coordinates for the entire path
    - Calculate and maintain correct route lengths

    **Attributes**:
    | Name              | Data Type         | Description                                               |
    |-------------------|-------------------|-----------------------------------------------------------|
    | `name`            | `str`             | Human-readable name of the Route                          |
    | `georeference`    | `List[List[float]]`| Coordinates describing the entire route path             |
    | `length`          | `float`           | Total length of the route in meters                       |
    | `id`              | `str`             | Unique identifier                                         |
    | `actors`          | `List[Actor]`     | Actors associated with the route                          |
    | `creation_date`   | `datetime`        | Timestamp when route was created                          |
    | `last_modified`   | `datetime`        | Timestamp of last modification       

    **Example Configuration**
    ```python
    route = Route(
        name="Machine A to WorkStation B",
        georeference=[[0.0, 0.0], [5.0, 0.0], [5.0, 5.0]],
        length=10.0,  # meters
        nodes=[1, 2, 3]  # waypoint IDs
        )
    ```
    :::info
    The georeference attribute for `Routes` differs from other classes as it contains the coordinates for the entire path, not just a single point. The format depends on the implementation but typically includes a list of coordinate pairs or a more complex path description.
    :::
    """
    # Class variables for instance tracking and logging
    _instances = WeakSet()
    _total_instances = 0
    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        name: str,
        georeference: List[List[float]],  # the georeference describes the coordinates of entire route, not just the start and end coordinates
        length: float,
        id: Optional[str] = None,
        actors: List[Actor] = None,
    ) -> None:
        """Initialize a Route instance."""
        self.name = name
        self._georeference = georeference
        self.length = length
        self.id = id if id is not None else str(uuid.uuid4())
        self._actors = actors if actors is not None else []
        self.creation_date = datetime.now()
        self._last_modified = datetime.now()
        
        self._validate()
        self._register_instance()
        self._logger.info(f"Created new route: {self}")

    def __repr__(self) -> str:
        """Return string representation of the Route instance."""
        return (f"Route(name='{self.name}', georeference={self._georeference}, "
                f"length={self.length}, "
                f"id='{self.id}', last_modified={self._last_modified})")

    def __hash__(self):
        """Return hash of the Route instance."""
        return hash(self.id)
    
    def __eq__(self, other):
        """Compare Route instances for equality."""
        if not isinstance(other, Route):
            return NotImplemented
        return self.id == other.id

    def _validate(self) -> None:
        """Validate the route's attributes."""
        if not self.name or not self.name.strip():
            raise ValueError("Route name cannot be empty.")
        if not isinstance(self.georeference, list) or len(self.georeference) < 2:
            raise ValueError("Georeference must be a list with at least two coordinate points.")
        if not all(isinstance(coord, (int, float)) for point in self.georeference for coord in (point if isinstance(point, list) else [point])):
            raise ValueError("Each coordinate in georeference must be numeric.")
        if not isinstance(self.length, (int, float)) or self.length < 0:
            raise ValueError("Route length must be a non-negative number.")

    def _register_instance(self) -> None:
        """Register the instance and increment the total instance count."""
        self.__class__._instances.add(self)
        self.__class__._total_instances += 1

    @property
    def actors(self) -> List[Actor]:
        """Return a copy of the route's associated actors."""
        return self._actors.copy()

    @property
    def georeference(self) -> List[float]:
        """Return the route's georeference."""
        return self._georeference

    @property
    def last_modified(self) -> datetime:
        """Return the last modified timestamp."""
        return self._last_modified

    def _update_last_modified(self) -> None:
        """Update the last modified timestamp and log the change."""
        self._last_modified = datetime.now()
        self._logger.debug(f"Updated last_modified for route {self.id} to {self._last_modified}")

    def update_georeference(self, new_georeference: List[float]) -> None:
        """Update the route's entire georeference."""
        self._validate_georeference(new_georeference)
        self._georeference = new_georeference
        self._update_last_modified()
        self._logger.debug(f"Updated georeference for resource {self.id}")

    def _validate_georeference(self, georeference: List[float]) -> None:
        """Validate georeference coordinates."""
        if not isinstance(georeference, list) or len(georeference) < 2:
            raise ValueError("Georeference must be a list with at least two coordinate points.")
        if not all(isinstance(x, (int, float)) for x in georeference):
            raise ValueError("Georeference coordinates must be numeric")

    def add_actor(self, actor: Actor) -> None:
        """Add an actor to the route."""
        if not isinstance(actor, Actor):
            raise ValueError("An Actor must be an instance of Actor")
        if actor in self._actors:
            self._logger.debug(f"Actor already associated with route {self.id}.")
            return
        self._actors.append(actor)
        self._update_last_modified()
        self._logger.debug(f"Added actor to route {self.id}.")

    def remove_actor(self, actor: Actor) -> None:
        """Remove an actor from the route."""
        if not isinstance(actor, Actor):
            raise ValueError("An Actor must be an instance of Actor")
        try:
            self._actors.remove(actor)
            self._update_last_modified()
            self._logger.debug(f"Removed actor from route {self.id}.")
        except ValueError:
            raise ValueError("The specified actor is not associated with this route.")

    def update_actor(self, old_actor: Actor, new_actor: Actor) -> None:
        """Replace an existing actor with a new one."""
        if not isinstance(old_actor, Actor):
            raise ValueError("An Actor must be an instance of Actor")
        if not isinstance(new_actor, Actor):
            raise ValueError("An Actor must be an instance of Actor")
        try:
            index = self._actors.index(old_actor)
        except ValueError:
            raise ValueError("The specified old actor is not associated with this route.")
        self._actors[index] = new_actor
        self._update_last_modified()
        self._logger.debug(f"Updated actor in route {self.id}.")

    @classmethod
    def get_by_id(cls, id: str) -> List[RouteT]:
        """Retrieve a list of route instances that match the given id."""
        return [route for route in cls._instances if route.id == id]

    def to_dict(self) -> dict:
        """Convert the route instance to a dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'georeference': self._georeference,
            'length': self.length,
            'actors': [str(actor) for actor in self._actors],
            'creation_date': self.creation_date.isoformat(),
            'last_modified': self._last_modified.isoformat()
        }

class Worker(Actor):
    """A class to represent a Worker in the manufacturing system.

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
    """
    # Class variables
    _instances = WeakSet()
    _total_instances = 0
    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        name: str,
        id: Optional[str] = None,
        roles: Dict[str, List[str]] = None,
        locations: List[LocationT] = None,
    ) -> None:
        """Initialize a Worker instance."""

        # Worker-specific attributes
        self._roles = roles if roles is not None else {}

        # Initialize parent Actor class
        super().__init__(
            name=name,
            id=id,
            locations=locations
        )
        
        self._validate_worker()
        self._register_instance()
        self._logger.info(f"Created new worker: {self}")

    def __repr__(self) -> str:
        """Return string representation of the Worker instance."""
        return f"Worker(id='{self.id}', name='{self.name}', roles={self._roles})"

    def _validate_worker(self) -> None:
        """Validate worker-specific attributes."""
        if not isinstance(self._roles, dict):
            raise ValueError("Roles must be provided as a dictionary")
        for role, allowed_types in self._roles.items():
            if not isinstance(role, str):
                raise ValueError("Role names must be strings")
            if not isinstance(allowed_types, list):
                raise ValueError("Allowed resource types must be provided as a list")
            if not all(isinstance(t, str) for t in allowed_types):
                raise ValueError("Resource types must be strings")

    def add_role(self, role: str, allowed_resource_types: List[str]) -> None:
        """
        Add or update a role with its allowed resource types.
        
        Example: worker.add_role("Operator", ["Machine"])
        """
        if not isinstance(role, str):
            raise ValueError("Role must be a string")
        if not isinstance(allowed_resource_types, list):
            raise ValueError("Allowed resource types must be provided as a list")
        if not all(isinstance(t, str) for t in allowed_resource_types):
            raise ValueError("Resource types must be strings")

        if role in self._roles:
            # Merge allowed resource types (avoid duplicates)
            self._roles[role] = list(set(self._roles[role]).union(allowed_resource_types))
        else:
            self._roles[role] = allowed_resource_types

        self._update_last_modified()
        self._logger.info(f"{self.name} now has role '{role}' with allowed types: {self._roles[role]}")

    def remove_role(self, role: str) -> None:
        """Remove a role from the worker."""
        if not isinstance(role, str):
            raise ValueError("Role must be a string")
        
        if role not in self._roles:
            raise ValueError(f"Role '{role}' not found for worker {self.name}")
        
        del self._roles[role]
        self._update_last_modified()
        self._logger.info(f"Removed role '{role}' from {self.name}")

    def can_work_with(self, resource: Resource) -> bool:
        """Check if any of the worker's roles allow them to work with the given resource type."""
        if not isinstance(resource, Resource):
            raise TypeError("Resource must be an instance of Resource")
        
        return any(resource.resource_type in allowed_types 
                  for allowed_types in self._roles.values())

    def work_on(self, machine: MachineT, capability: Optional[str] = None) -> None:
        """
        Attempt to work on the machine. If a capability is provided,
        start that capability if it is available.
        """
        if not isinstance(machine, Machine):
            raise TypeError("Machine must be an instance of Machine")
        if capability is not None and not isinstance(capability, str):
            raise ValueError("Capability must be a string if provided")

        if not self.can_work_with(machine):
            self._logger.warning(
                f"{self.name} is not authorized to work on {machine.name} [{machine.resource_type}]"
            )
            return

        if capability:
            if capability in machine.capabilities:
                self._logger.info(f"{self.name} is starting the '{capability}' capability on {machine.name}")
                machine.start_capability(capability)
            else:
                self._logger.warning(f"{machine.name} does not support the capability '{capability}'")
        else:
            self._logger.info(f"{self.name} is now working on {machine.name}")
            machine.operate()

        self._update_last_modified()

    @property
    def roles(self) -> Dict[str, List[str]]:
        """Return a copy of the worker's roles."""
        return self._roles.copy()

    @classmethod
    def get_by_role(cls, role: str) -> List['Worker']:
        """Retrieve all worker instances that have the given role."""
        return [worker for worker in cls._instances if role in worker.roles]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the worker instance to a dictionary representation."""
        base_dict = super().to_dict()
        worker_dict = {
            'roles': self._roles
        }
        return {**base_dict, **worker_dict}

class Machine(Resource):
    """A class to represent a Machine in the manufacturing system.

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
    """
    # Class variables
    _instances = WeakSet()
    _total_instances = 0
    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        name: str,
        machine_type: str,
        georeference: List[float],
        id: Optional[str] = None,
        location: Optional[LocationT] = None,
        capabilities: Optional[List[str]] = None,
        power_type: Optional[str] = "electric",
        power_consumption: float = 0,
        maintenance_interval: float = 0,
        last_maintenance: Optional[datetime] = None,
        actors: Optional[List[ActorT]] = None,
        actions: Optional[List[ActionT]] = None,
        constraints: Optional[List[ConstraintT]] = None,
        sensors: Optional[List[SensorT]] = None,
        status: ResourceStatus = ResourceStatus.IDLE,
    ) -> None:
        """Initialize a Machine instance."""

        # Machine-specific attributes
        self.machine_type = machine_type
        self.capabilities = capabilities if capabilities is not None else []

        # Call Resource initializer with resource_type set to "Machine"
        super().__init__(
            name=name,
            resource_type=ResourceType.MACHINE,
            id=id,
            georeference=georeference,
            location=location,
            power_type=power_type,
            power_consumption=power_consumption,
            maintenance_interval=maintenance_interval,
            last_maintenance=last_maintenance,
            actors=actors,
            actions=actions,
            constraints=constraints,
            sensors=sensors,
            status=status,
        )

        self._validate_machine()
        self._register_instance()
        self._logger.info(f"Created new machine: {self}")

    def __repr__(self) -> str:
        """Return string representation of the Machine instance."""
        return (f"Machine(name='{self.name}', machine_type='{self.machine_type}', "
                f"capabilities={self.capabilities}, status='{self.status}')")

    def __str__(self) -> str:
        """Return human-readable string representation of the Machine instance."""
        cap_str = ", ".join(self.capabilities) if self.capabilities else "No capabilities"
        return f"Machine({self.id}): {self.name} [{self.machine_type}] | Capabilities: {cap_str}"

    def _validate_machine(self) -> None:
        """Validate machine-specific attributes."""
        if not self.machine_type or not isinstance(self.machine_type, str):
            raise ValueError("Machine type must be a non-empty string")
        if not isinstance(self.capabilities, list):
            raise ValueError("Capabilities must be provided as a list")
        if not all(isinstance(cap, str) for cap in self.capabilities):
            raise ValueError("All capabilities must be strings")

    def _register_instance(self) -> None:
        """Register the instance in the WeakSet and increment counter."""
        self.__class__._instances.add(self)
        self.__class__._total_instances += 1

    def start_capability(self, capability: str) -> None:
        """Start a specific capability if available on the machine."""
        if not isinstance(capability, str):
            raise ValueError("Capability must be a string")

        if capability in self.capabilities:
            self._logger.info(f"Machine {self.name} is executing capability '{capability}'.")
            self.status = ResourceStatus.WORKING
            self._update_last_modified()
        else:
            self._logger.warning(f"Capability '{capability}' is not available on machine {self.name}.")
            raise ValueError(f"Capability '{capability}' not available")

    def add_capability(self, capability: str) -> None:
        """Add a new capability to the machine."""
        if not isinstance(capability, str):
            raise ValueError("Capability must be a string")
        
        if capability not in self.capabilities:
            self.capabilities.append(capability)
            self._update_last_modified()
            self._logger.info(f"Added capability '{capability}' to machine {self.name}")

    def remove_capability(self, capability: str) -> None:
        """Remove a capability from the machine."""
        if not isinstance(capability, str):
            raise ValueError("Capability must be a string")
        
        try:
            self.capabilities.remove(capability)
            self._update_last_modified()
            self._logger.info(f"Removed capability '{capability}' from machine {self.name}")
        except ValueError:
            raise ValueError(f"Capability '{capability}' not found on machine {self.name}")

    @classmethod
    def get_by_machine_type(cls, machine_type: str) -> List['Machine']:
        """Get all machines of a specific type."""
        return [machine for machine in cls._instances if machine.machine_type == machine_type]

    @classmethod
    def get_by_capability(cls, capability: str) -> List['Machine']:
        """Get all machines that have a specific capability."""
        return [machine for machine in cls._instances if capability in machine.capabilities]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the machine instance to a dictionary representation."""
        base_dict = super().to_dict()
        machine_dict = {
            'machine_type': self.machine_type,
            'capabilities': self.capabilities,
        }
        return {**base_dict, **machine_dict}

@dataclass
class Requirement:
    """A class to represent Requirements for manufacturing Actions.

    Requirements define the specific resources, components, tools, or personnel needed
    to execute an Action. Each Requirement specifies a type (e.g., Machine, Part, Worker)
    and detailed specifications for that type.

    The Requirement types are defined by the [RequirementType](/docs/classes/requirementtype):
    - *Machine*: Manufacturing equipment requirements
    - *Workstation:* Workstation requirements
    - *Conveyor*: Conveyor system requirements
    - *Robotic Arm*: Robotic Arm requirements
    - *Vehicle*: Transport requirements
    - *Part*: Part/Material requirements
    - *Product*: Product requirements
    - *Worker*: Personnel requirements
    - *Tool*: Equipment requirements

    **Best Practices**:
    - Specify requirements at the appropriate level of detail
    - Include quantity information for parts and products
    - Clearly define skill requirements for workers
    - Specify exact machine types when necessary
    - Use generic types when flexibility is possible

    **Attributes**:
    | Name   | Data Type         | Description                                                                                     |
    |--------|-------------------|-------------------------------------------------------------------------------------------------|
    | `type` | `RequirementType` | Type of requirement. See [RequirementType](/docs/classes/requirementtype)                        |
    | `specs`| `List[Any]`       | Specifications for the requirement, format depends on type                                      |
    
    **Example Requirements**:

    * Specific machine requirement  
    ```python
    Requirement(type=RequirementType.MACHINE, specs=["CNC Mill"])
    ```
    * Part requirement with quantity  
    ```python
    Requirement(type=RequirementType.PART, specs=["Steel Plate", 5])
    ```
    * Generic worker requirement  
    ```python
    * Requirement(type=RequirementType.WORKER, specs=[])
    ```python
    * Specific worker role requirement  
    ```python
    Requirement(type=RequirementType.WORKER, specs=["Technician"])
    ```
    :::note
    The format of the specs list varies depending on the requirement type. Always validate the specs format against the requirement type's expectations.
    :::
    """
    type: RequirementType
    specs: List[Any]

    def __post_init__(self):
        self._validate()

    def _validate(self):
        """Validate the requirement specifications based on type."""
        if self.type in [RequirementType.MACHINE, RequirementType.VEHICLE]:
            if len(self.specs) > 1:
                raise ValueError(f"{self.type.value} requirement should have 0 or 1 specification")
                
        elif self.type == RequirementType.PART:
            if len(self.specs) == 0:
                raise ValueError("Part requirement must specify at least the part name")
            if len(self.specs) > 2:
                raise ValueError("Part requirement should have 1 (name) or 2 (name, quantity) specifications")
            if len(self.specs) == 2 and not isinstance(self.specs[1], (int, float)):
                raise ValueError("Part quantity must be a number")
                
        elif self.type in [RequirementType.WORKER, RequirementType.TOOL]:
            if len(self.specs) > 1:
                raise ValueError(f"{self.type.value} requirement should have 0 or 1 specification")

    def __str__(self):
        if self.type == RequirementType.PART and len(self.specs) == 2:
            return f"{self.type.value}({self.specs[0]}, {self.specs[1]} units)"
        elif self.specs:
            return f"{self.type.value}({', '.join(map(str, self.specs))})"
        return f"{self.type.value}(any)"

class Action:
    """A class to represent manufacturing and logistics Actions.

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
    """

    # Class variables
    _instances = WeakSet()
    _total_instances = 0
    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        name: str,
        action_type: ActionType,
        description: Optional[str],
        duration: Optional[float],  # Duration in hours
        job_id: Optional[str] = None,
        status: ActionStatus = ActionStatus.DRAFT,
        requirements: Dict[str, List[str]] = None, 
        id: Optional[str] = None,
        sequence_nr: Optional[int] = None,
        location: Optional[ActionLocationT] = None,
        worker: Optional[WorkerT] = None,
        origin: Optional[Union[ActionLocationT]] = None,
        destination: Optional[ActionLocationT] = None,
        route: Optional[RouteT] = None,
        constraints: Optional[List[ConstraintT]] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        progress: float = 0,
    ) -> None:
        """Initialize an Action instance."""
        self.name = name
        self._action_type = action_type
        self._status = status
        self.description = description
        self.duration = duration
        self.job_id = job_id  # Reference to the job this action belongs to
        self.id = id if id is not None else str(uuid.uuid4())
        self.sequence_nr = sequence_nr
        self.requirements: List[Requirement] = requirements if requirements else []
        self._location = location
        self._worker = worker
        self._origin = origin               # for 'move' actions
        self._destination = destination     # for 'move' actions
        self._route = route                 # for 'move' actions
        self._constraints = constraints if constraints is not None else []
        self._progress = progress
        self._start_time = start_time
        self._end_time = end_time
        self.creation_date = datetime.now()
        self._last_modified = datetime.now()

        self._validate()
        self._register_instance()
        self._logger.info(f"Created new action: {self}")

    def __repr__(self) -> str:
        """Return string representation of the Action instance."""
        return (f"Action(name='{self.name}', sequence_nr={self.sequence_nr}, "
                f"type='{self.action_type}', status='{self.status}', "
                f"_from={self._from}, _to={self._to}, location={self.location}, "
                f"route={self.route}, duration={self.duration}, "
                f"start_time={self.start_time})")

    def __hash__(self):
        """Return hash of the Action instance."""
        return hash(self.id)
    
    def __eq__(self, other):
        """Compare Action instances for equality."""
        if not isinstance(other, Action):
            return NotImplemented
        return self.id == other.id

    def _validate(self) -> None:
        """Validate the action's attributes."""
        if not isinstance(self.name, str):
            raise ValueError("Action name must be a string")
        if self.sequence_nr is not None and not isinstance(self.sequence_nr, int):
            raise ValueError("Sequence number must be an integer if provided")
        if not isinstance(self.progress, (int, float)) or not 0 <= self.progress <= 100:
            raise ValueError("Progress must be a number between 0 and 100") 
        if self._origin is not None and not isinstance(self._origin, get_args(ActionLocationT.__bound__)):
            raise ValueError("Origin must be an instance of Location or Resource, if provided") 
        if self._destination is not None and not isinstance(self._destination, get_args(ActionLocationT.__bound__)):
            raise ValueError("Destination must be an instance of Location or Resource, if provided")  
        if self._location is not None and not isinstance(self._location, get_args(ActionLocationT.__bound__)):
            raise ValueError("Location must be an instance of Location or Resource, if provided")
        if self._worker is not None and not isinstance(self._worker, get_args(WorkerT.__bound__)):
            raise ValueError("Worker must be an instance of Worker, if provided")

    def _register_instance(self) -> None:
        """Register the instance in the WeakSet and increment counter."""
        self.__class__._instances.add(self)
        self.__class__._total_instances += 1

    @property
    def last_modified(self) -> datetime:
        """Return the last modified timestamp."""
        return self._last_modified

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, new_status: ActionStatus) -> None:
        """Set the status of the action."""
        self._status = new_status
        self._update_last_modified()
        self._logger.info(f"Updated status for action {self.id} to {new_status}")

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, new_location: ActionLocationT) -> None:
        if self._location is not None and not isinstance(self._location, get_args(ActionLocationT.__bound__)):
            raise ValueError("Location must be an instance of Location or Resource, if provided")
        self._location = new_location
        self._update_last_modified()
        self._logger.info(f"Updated location for action {self.id} to {new_location}")
       
    @property
    def worker(self):
        return self._worker

    @worker.setter
    def worker(self, new_worker: WorkerT) -> None:
        if self._worker is not None and not isinstance(self._worker, get_args(WorkerT.__bound__)):
            raise ValueError("Worker must be an instance of Worker, if provided")
        self._worker = new_worker
        self._update_last_modified()
        self._logger.info(f"Updated worker for action {self.id} to {new_worker}")  

    @property
    def origin(self) -> ActionLocationT:
        return self._origin

    @origin.setter
    def origin(self, new_origin: ActionLocationT) -> None:
        if self._origin is not None and not isinstance(self._origin, get_args(ActionLocationT.__bound__)):
            raise ValueError("Origin must be an instance of Location or Resource, if provided")
        self._origin = new_origin
        self._update_last_modified()
        self._logger.info(f"Updated origin for action {self.id} to {new_origin}")

    @property
    def destination(self) -> ActionLocationT:
        return self._destination

    @destination.setter
    def destination(self, new_destination: ActionLocationT) -> None:
        if self._destination is not None and not isinstance(self._destination, get_args(ActionLocationT.__bound__)):
            raise ValueError("Destination must be an instance of Location or Resource, if provided")
        self._destination = new_destination
        self._update_last_modified()
        self._logger.info(f"Updated destination for action {self.id} to {new_destination}")

    @property
    def constraints(self) -> Optional[List[ConstraintT]]:
        """Return the action's constraints."""
        return self._constraints
    
    def add_constraint(self, constraint: ConstraintT) -> None:
        """Add a single constraint to the resource's constraints."""
        if not isinstance(constraint, Constraint):
            raise TypeError("constraint must be an instance of Constraint")
        self._constraints.append(constraint)
        self._update_last_modified()
        self._logger.debug(f"Added constraint to resource {self.id}")

    def remove_constraint(self, constraint: ConstraintT) -> None:
        """Remove a specific constraint from the action's constraints."""
        if not isinstance(constraint, Constraint):
            raise TypeError("constraint must be an instance of Constraint")
        try:
            self._constraints.remove(constraint)
            self._update_last_modified()
            self._logger.debug(f"Deleted constraint from action {self.id}")
        except ValueError:
            raise ValueError("The specified constraint is not in the constraints list")

    @property
    def start_time(self) -> datetime:
        return self._start_time

    @start_time.setter
    def start_time(self, new_start_time: datetime) -> None:
        if not isinstance(new_start_time, datetime):
            raise ValueError("new_end_time must be an instance of datetime.")
        self._start_time = new_start_time
        self._update_last_modified()
        self._logger.debug(f"Updated start_time for action {self.id}")   

    @property
    def end_time(self) -> datetime:
        return self._end_time

    @end_time.setter
    def end_time(self, new_end_time: datetime) -> None:
        if not isinstance(new_end_time, datetime):
            raise ValueError("new_end_time must be an instance of datetime.")
        self._end_time = new_end_time
        self._update_last_modified()
        self._logger.debug(f"Updated end_time for action {self.id}")   

    @property
    def progress(self):
        return self.progress
    
    @progress.setter
    def progress(self, new_progress: Union[float, int]) -> None:
        if not isinstance(new_progress, (int, float)) or not 0 <= new_progress <= 100:
            raise ValueError("Progress must be a number between 0 and 100")
        self._progress = new_progress
        self._update_last_modified()
        self._logger.info(f"Updated progress for action {self.id} to {new_progress}")        

    @classmethod
    def get_job_actions(cls, job_id: str) -> List['Action']:
        """Get all actions associated with a specific job."""
        return [action for action in cls._all_actions.values() 
                if action.job_id == job_id]

    def set_job(self, job_id: str) -> None:
        """Associate this action with a job."""
        self.job_id = job_id
        self._logger.info(f"Associated action {self.id} with job {job_id}")

    def remove_job(self) -> None:
        """Remove this action's association with a job."""
        self.job_id = None
        self._logger.info(f"Removed job association from action {self.id}")

    @classmethod
    def cleanup_job(cls, job_id: str) -> None:
        """Remove all actions associated with a specific job."""
        actions = cls.get_job_actions(job_id)
        for action in actions:
            action.remove_job()

    def add_requirement(self, req_type: Union[str, RequirementType], specs: Optional[List[Any]]=None) -> None:
        """
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
        """
        # Convert string to RequirementType if necessary
        if isinstance(req_type, str):
            try:
                req_type = RequirementType[req_type.upper()]
            except KeyError:
                raise ValueError(f"Invalid requirement type: {req_type}")

        # Create and validate the requirement
        specs = specs if specs is not None else []
        requirement = Requirement(req_type, specs)
        self.requirements.append(requirement)
        self._logger.info(f"Added requirement to {self.name}: {requirement}")

    def remove_requirement(self, req_type: Union[str, RequirementType], specs: Optional[List[Any]] = None) -> None:
        """
        Remove a requirement from the action.
        
        Args:
        *   `req_type`: Type of requirement to remove
        *   `specs`: Specific specs to match (or None to remove all of type)
        """
        if isinstance(req_type, str):
            try:
                req_type = RequirementType[req_type.upper()]
            except KeyError:
                raise ValueError(f"Invalid requirement type: {req_type}")

        initial_count = len(self.requirements)
        if specs is None:
            # Remove all requirements of the specified type
            self.requirements = [r for r in self.requirements if r.type != req_type]
        else:
            # Remove specific requirement
            self.requirements = [r for r in self.requirements 
                               if not (r.type == req_type and r.specs == specs)]

        removed_count = initial_count - len(self.requirements)
        self._logger.info(f"Removed {removed_count} requirements of type {req_type.value} from {self.name}")

    def get_requirements(self, req_type: Optional[Union[str, RequirementType]] = None) -> List[Requirement]:
        """
        Get all requirements or requirements of a specific type.
        
        Args:
        *   `req_type`: Type of requirements to get (or None for all)
            
        Returns:
        *   List of matching requirements
        """
        if req_type is None:
            return self.requirements.copy()

        if isinstance(req_type, str):
            try:
                req_type = RequirementType[req_type.upper()]
            except KeyError:
                raise ValueError(f"Invalid requirement type: {req_type}")

        return [r for r in self.requirements if r.type == req_type]

    def check_requirements_satisfied(self, location: 'Location') -> Tuple[bool, List[str]]:
        """
        Check if all requirements are satisfied at the given location.
        
        Args:
        *   `location`: Location to check requirements against
            
        Returns:
        *   `Tuple` of `(satisfied: bool, missing_requirements: List[str])`
        """
        satisfied = True
        missing = []

        for req in self.requirements:
            if req.type == RequirementType.MACHINE:
                if not self._check_machine_requirement(req, location):
                    satisfied = False
                    missing.append(str(req))
                    
            elif req.type == RequirementType.VEHICLE:
                if not self._check_vehicle_requirement(req, location):
                    satisfied = False
                    missing.append(str(req))
                    
            elif req.type == RequirementType.PART:
                if not self._check_part_requirement(req, location):
                    satisfied = False
                    missing.append(str(req))
                    
            elif req.type == RequirementType.WORKER:
                if not self._check_worker_requirement(req, location):
                    satisfied = False
                    missing.append(str(req))
                    
            elif req.type == RequirementType.TOOL:
                if not self._check_tool_requirement(req, location):
                    satisfied = False
                    missing.append(str(req))

        return satisfied, missing

    def _update_last_modified(self) -> None:
        """Update the last modified timestamp with logging."""
        self._last_modified = datetime.now()
        self._logger.debug(f"Updated last_modified for action {self.id} to {self._last_modified}")

    def _check_machine_requirement(self, req: Requirement, location: 'Location') -> bool:
        """Check if a machine requirement is satisfied."""
        machines = [r for r in location.resources if isinstance(r, Machine)]
        if not machines:
            return False
        if not req.specs:  # Any machine is acceptable
            return True
        return any(m.machine_type == req.specs[0] for m in machines)

    def _check_vehicle_requirement(self, req: Requirement, location: 'Location') -> bool:
        """Check if a vehicle requirement is satisfied."""
        vehicles = [r for r in location.resources if isinstance(r, Vehicle)]
        if not vehicles:
            return False
        if not req.specs:  # Any vehicle is acceptable
            return True
        return any(v.vehicle_type == req.specs[0] for v in vehicles)

    def _check_part_requirement(self, req: Requirement, location: 'Location') -> bool:
        """Check if a part requirement is satisfied."""
        parts = [r for r in location.resources if isinstance(r, Part)]
        matching_parts = [p for p in parts if p.name == req.specs[0]]
        if not matching_parts:
            return False
        if len(req.specs) == 1:  # Only name specified, any quantity is acceptable
            return True
        return sum(p.quantity for p in matching_parts) >= req.specs[1]

    def _check_worker_requirement(self, req: Requirement, location: 'Location') -> bool:
        """Check if a worker requirement is satisfied."""
        people = [r for r in location.resources if isinstance(r, Worker)]
        if not people:
            return False
        if not req.specs:  # Any worker is acceptable
            return True
        return any(p.role == req.specs[0] for p in people)

    def _check_tool_requirement(self, req: Requirement, location: 'Location') -> bool:
        """Check if a tool requirement is satisfied."""
        tools = [r for r in location.resources if isinstance(r, Tool)]
        if not tools:
            return False
        if not req.specs:  # Any tool is acceptable
            return True
        return any(t.tool_type == req.specs[0] for t in tools)


    @classmethod
    def get_by_id(cls, id: str) -> Optional[ActionT]:
        """Retrieve an action instance by ID."""
        return next((action for action in cls._instances if action.id == id), None)

    @classmethod
    def get_by_status(cls, status: str) -> List[ActionT]:
        """Retrieve all actions with a specific status."""
        return [action for action in cls._instances if action._status == status]

    @classmethod
    def get_by_action_type(cls, action_type: str) -> List[ActionT]:
        """Retrieve all actions of a specific type."""
        return [action for action in cls._instances if action.action_type == action_type]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the action instance to a dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'action_type': self._action_type,
            'status': self._status,
            'sequence_nr': self.sequence_nr,
            'location': str(self._location.name) if self._location else None,
            'origin': str(self._origin.name) if self._origin else None,
            'destination': str(self._destination.name) if self._destination else None,
            'progress': self._progress,
            'start_time': self._start_time.isoformat() if self._start_time else None,
            'end_time': self._end_time.isoformat() if self._end_time else None,
            'creation_date': self.creation_date.isoformat(),
            'last_modified': self._last_modified.isoformat()
        }

class Vehicle(Resource):
    """A class to represent a Vehicle.

    Vehicles are specialized Resources used for material transport and logistics operations.
    They represent mobile equipment such as automated guided vehicles (AGVs), forklifts,
    manual transport vehicles, or any other mobile equipment used for moving parts and products.
    The Vehicle class extends the Resource class to include vehicle-specific capabilities
    and parameters for movement, energy management, and load handling.

    Vehicles are connected to various components in the manufacturing system:
    - Routes they can traverse
    - Locations they move between
    - Products or Parts they can transport
    - Actions they should perform
    - Sensors monitoring their status
    - Workers authorized to operate them

    **Best Practices**:
    - Monitor battery levels and charging status
    - Track vehicle location in real-time
    - Maintain load capacity constraints
    - Schedule preventive maintenance
    - Monitor environmental impact
    - Optimize route selection
    - Ensure safety compliance

    **Attributes**:
    | Name                      | Data Type               | Description                                                                |
    |---------------------------|-------------------------|----------------------------------------------------------------------------|
    | `name`                    | `str`                   | Human-readable name of the Vehicle                                         |
    | `vehicle_type`            | `VehicleType`           | Type of vehicle. See [VehicleType](/docs/classes/vehicletype)                |
    | `georeference`            | `List[float]`           | Current location coordinates [x, y] or [x, y, z]                           |
    | `id`                      | `str`                   | Unique identifier                                                          |
    | `status`                  | `ResourceStatus`        | Current operational status. See [ResourceStatus](/docs/classes/resourcestatus)|
    | `power_type`              | `str`                   | Power source                                                               |
    | `power_consumption`       | `float`                 | Power usage in kWh                                                         |
    | `maintenance_interval`    | `int`                   | Hours between required maintenance                                         |
    | `last_maintenance`        | `datetime`              | Timestamp of last maintenance                                              |
    | `hours_used`              | `float`                 | Total hours of use since last maintenance                                  |
    | `actors`                  | `List[Actor]`           | Workers authorized to operate this vehicle                                 |
    | `sensors`                 | `List[Sensor]`          | Sensors on-board this vehicle                                              |
    | `actions`                 | `List[Action]`          | Actions associated with this vehicle                                       |
    | `constraints`              | `List[constraints]`            | Operating constraints                                                      |
    | `fuel`                    | `str`                   | Type of fuel or power source                                               |
    | `average_fuel_consumption`| `float`                 | Average fuel consumption rate                                              |
    | `emission_standard`       | `str`                   | Applicable emission standard                                               |
    | `load_capacities`         | `dict`                  | Maximum load capacity specifications                                       |
    | `length`                  | `float`                 | Vehicle length in meters                                                   |
    | `height`                  | `float`                 | Vehicle height in meters                                                   |
    | `width`                   | `float`                 | Vehicle width in meters                                                    |
    | `license_plate`           | `str`                   | Vehicle identification plate                                               |
    | `empty_weight`            | `float`                 | Weight without load in kg                                                  |
    | `average_speed`           | `float`                 | Normal operating speed in meters/second                                  |
    | `speed`                   | `float`                 | Current actual speed in meters/second                                      |
    | `co2_emission`            | `float`                 | CO2 emissions in g/km                                                      |
    | `nox_emission`            | `float`                 | NOx emissions in g/km                                                      |
    | `noise_pollution`         | `float`                 | Noise level in dB                                                          |
    | `land_use`                | `float`                 | Space requirement in m²                                                    |
    | `battery_capacity`        | `float`                 | Total battery capacity in kWh                                              |
    | `battery_threshold`       | `float`                 | Minimum battery level for operation                                        |
    | `battery_charging_rate`   | `float`                 | Charging rate in kW                                                        |
    | `energy_consumption_moving`| `float`                 | Energy use while moving in kWh/km                                          |
    | `energy_consumption_idling`| `float`                 | Energy use while idle in kWh/h                                             |
    | `creation_date`           | `datetime`              | Timestamp when vehicle was created                                         |
    | `last_modified`           | `datetime`              | Timestamp of last modification                                             |

    **Example Configuration**:
    ```python
    vehicle = Vehicle(
        name="AGV-001",
        vehicle_type=VehicleType.AUTOMATED_MOBILE_ROBOT,
        average_speed=1.0,  # m/s
        battery_capacity=10.0,  # kWh
        battery_threshold=0.2,  # 20%
        load_capacities={"weight": 150}  # kg
        )
    ```
    :::note
    The `Vehicle` class inherits base attributes from the `Resource` class while adding specialized capabilities for transport operations. Use this class for any mobile equipment used in material handling and logistics.
        :::
    """
    # Class variables
    _instances = WeakSet()
    _total_instances = 0
    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        name: str,
        vehicle_type: VehicleType,
        georeference: List[float],
        status: ResourceStatus = ResourceStatus.IDLE,
        id: Optional[str] = None,
        power_type: Optional[str] = "electric",
        power_consumption: float = 0,
        maintenance_interval: float = 0,
        last_maintenance: Optional[datetime] = None,
        actors: Optional[List[ActorT]] = None,
        sensors: Optional[List[SensorT]] = None,
        actions: Optional[List[ActionT]] = None,
        constraints: Optional[List[ConstraintT]] = None,
        fuel: Optional[str] = None,
        average_fuel_consumption: Optional[float] = None,
        emission_standard: Optional[str] = None,
        load_capacities: Optional[dict] = None,
        length: Optional[float] = None,
        height: Optional[float] = None,
        width: Optional[float] = None,
        license_plate: Optional[str] = None,
        empty_weight: Optional[float] = None,
        average_speed: float = 1.0, # meters/second
        co2_emission: float = 0,
        nox_emission: float = 0,
        noise_pollution: float = 0,
        land_use: float = 0,
        battery_capacity: float = 0,
        battery_threshold: float = 0,
        battery_charging_rate: float = 0,
        energy_consumption_moving: float = 0,
        energy_consumption_idling: float = 0,

    ) -> None:
        """Initialize a Vehicle instance."""

        # Vehicle-specific attributes
        self.vehicle_type = vehicle_type
        self.fuel = fuel
        self.average_fuel_consumption = average_fuel_consumption
        self.emission_standard = emission_standard
        self.load_capacities = load_capacities if load_capacities is not None else {}
        self.length = length
        self.height = height
        self.width = width
        self.license_plate = license_plate
        self.empty_weight = empty_weight
        self.average_speed = average_speed
        self._speed = average_speed
        self.co2_emission = co2_emission
        self.nox_emission = nox_emission
        self.noise_pollution = noise_pollution
        self.land_use = land_use
        self.battery_capacity = battery_capacity
        self.energy_consumption_moving = energy_consumption_moving
        self.energy_consumption_idling = energy_consumption_idling
        self.battery_charging_rate = battery_charging_rate
        self._battery_threshold = battery_threshold

        # Call Resource initializer
        super().__init__(
            name=name,
            resource_type=ResourceType.VEHICLE,
            georeference=georeference,
            id=id,
            location=None,  # Vehicles are mobile, initial location is None
            power_type=power_type,
            power_consumption=power_consumption,
            maintenance_interval=maintenance_interval,
            last_maintenance=last_maintenance,
            actors=actors,
            actions=actions,
            constraints=constraints,
            sensors=sensors,
            status=status,
        )
        
        self._validate_vehicle()
        self._register_instance()
        self._logger.info(f"Created new vehicle: {self}")

    def __repr__(self) -> str:
        """Return string representation of the Vehicle instance."""
        return (f"Vehicle(name='{self.name}', vehicle_type='{self.vehicle_type}', "
                f"status='{self.status}', average_speed={self.average_speed}m/s, speed={self._speed}m/s "
                f"georeference={self._georeference})")

    def _validate_vehicle(self) -> None:
        """Validate vehicle-specific attributes."""
        if not isinstance(self.vehicle_type, VehicleType):
            raise ValueError("Vehicle type must be an instance of VehicleType")
        if not isinstance(self.average_speed, (int, float)) or self.average_speed < 0:
            raise ValueError("Average speed must be a non-negative number")
        if self.license_plate is not None and not isinstance(self.license_plate, str):
            raise ValueError("License plate must be a string if provided")
        if self.length is not None and (not isinstance(self.length, (int, float)) or self.length <= 0):
            raise ValueError("Length must be a positive number if provided")
        if self.height is not None and (not isinstance(self.height, (int, float)) or self.height <= 0):
            raise ValueError("Height must be a positive number if provided")
        if self.width is not None and (not isinstance(self.width, (int, float)) or self.width <= 0):
            raise ValueError("Width must be a positive number if provided")

    @property
    def battery_threshold(self) -> float:
        """Return the vehicle's battery threshold."""
        return self._battery_threshold

    @battery_threshold.setter
    def battery_threshold(self, value: float) -> None:
        """Set the vehicle's battery threshold."""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Battery threshold must be a non-negative number")
        self._battery_threshold = value
        self._update_last_modified()
        self._logger.debug(f"Updated battery threshold for vehicle {self.id} to {value}")

    @property
    def speed(self) -> float:
        """Return the vehicle's actual speed."""
        return self._speed
    
    @speed.setter
    def speed(self, new_speed: float) -> None:
        """Set the vehicle's actual speed."""
        if not isinstance(new_speed, (int, float)) or new_speed < 0:
            raise ValueError("Speed must be a non-negative number")
        self._speed = new_speed
        self._update_last_modified()
        self._logger.debug(f"Updated actual speed for vehicle {self.id} to {new_speed}")

    def start_charging(self) -> None:
        """Start charging the vehicle."""
        if self.status != ResourceStatus.IDLE:
            raise ValueError("Vehicle must be idle to start charging")
        self.status = ResourceStatus.CHARING
        self._update_last_modified()
        self._logger.info(f"Started charging vehicle {self.id}")

    def stop_charging(self) -> None:
        """Stop charging the vehicle."""
        if self.status != ResourceStatus.CHARING:
            raise ValueError("Vehicle is not currently charging")
        self.status = ResourceStatus.IDLE
        self._update_last_modified()
        self._logger.info(f"Stopped charging vehicle {self.id}")

    @classmethod
    def get_by_vehicle_type(cls, vehicle_type: VehicleType) -> List['Vehicle']:
        """Retrieve all vehicles of a specific type."""
        return [vehicle for vehicle in cls._instances if vehicle.vehicle_type == vehicle_type]

    @classmethod
    def get_by_license_plate(cls, license_plate: str) -> Optional['Vehicle']:
        """Retrieve a vehicle by its license plate."""
        return next((vehicle for vehicle in cls._instances if vehicle.license_plate == license_plate), None)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the vehicle instance to a dictionary representation."""
        base_dict = super().to_dict()
        vehicle_dict = {
            'vehicle_type': self.vehicle_type.name,
            'average_speed': self.average_speed,
            'speed': self._speed,
            'fuel': self.fuel,
            'average_fuel_consumption': self.average_fuel_consumption,
            'emission_standard': self.emission_standard,
            'load_capacities': self.load_capacities,
            'dimensions': {
                'length': self.length,
                'height': self.height,
                'width': self.width
            },
            'license_plate': self.license_plate,
            'empty_weight': self.empty_weight,
            'emissions': {
                'co2': self.co2_emission,
                'nox': self.nox_emission,
                'noise': self.noise_pollution
            },
            'energy': {
                'battery_capacity': self.battery_capacity,
                'battery_threshold': self._battery_threshold,
                'battery_charging_rate': self.battery_charging_rate,
                'consumption_moving': self.energy_consumption_moving,
                'consumption_idling': self.energy_consumption_idling
            }
        }
        return {**base_dict, **vehicle_dict}

class WorkStation(Resource):
    """A class to represent a WorkStation.

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
    """
    # Class variables
    _instances = WeakSet()
    _total_instances = 0
    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        name: str,
        georeference: List[float],
        id: Optional[str] = None,
        location: Optional[Location] = None,
        workstation_type: Optional[str] = "general",
        capabilities: Optional[List[str]] = None,
        max_capacity: Optional[int] = None,
        power_type: Optional[str] = "manual",
        power_consumption: float = 0,
        maintenance_interval: float = 0,
        last_maintenance: Optional[datetime] = None,
        actors: Optional[List[ActorT]] = None,
        actions: Optional[List[ActionT]] = None,
        constraints: Optional[List[ConstraintT]] = None,
        sensors: Optional[List[SensorT]] = None,
        status: ResourceStatus = ResourceStatus.IDLE,
    ) -> None:
        """Initialize a WorkStation instance."""

        # WorkStation-specific attributes
        self.workstation_type = workstation_type
        self.capabilities = capabilities if capabilities is not None else []
        self.max_capacity = max_capacity
        self._current_capacity = 0

        # Call Resource initializer
        super().__init__(
            name=name,
            resource_type=ResourceType.WORKSTATION,
            georeference=georeference,
            id=id,
            location=location,
            power_type=power_type,
            power_consumption=power_consumption,
            maintenance_interval=maintenance_interval,
            last_maintenance=last_maintenance,
            actors=actors,
            actions=actions,
            constraints=constraints,
            sensors=sensors,
            status=status,
        )

        self._validate_workstation()
        self._register_instance()
        self._logger.info(f"Created new workstation: {self}")

    def __repr__(self) -> str:
        """Return string representation of the WorkStation instance."""
        return (f"WorkStation(name='{self.name}', type='{self.workstation_type}', "
                f"status='{self.status}', location={self._location})")

    def _validate_workstation(self) -> None:
        """Validate workstation-specific attributes."""
        if not isinstance(self.workstation_type, str):
            raise ValueError("Workstation type must be a string")
        if not isinstance(self.capabilities, list):
            raise ValueError("Capabilities must be a list")
        if not all(isinstance(cap, str) for cap in self.capabilities):
            raise ValueError("All capabilities must be strings")
        if self.max_capacity is not None and not isinstance(self.max_capacity, int):
            raise ValueError("Maximum capacity must be an integer if provided")
        if self.max_capacity is not None and self.max_capacity <= 0:
            raise ValueError("Maximum capacity must be positive")

    @property
    def current_capacity(self) -> int:
        """Return the current capacity utilization."""
        return self._current_capacity

    def add_capability(self, capability: str) -> None:
        """Add a new capability to the workstation."""
        if not isinstance(capability, str):
            raise ValueError("Capability must be a string")
            
        if capability not in self.capabilities:
            self.capabilities.append(capability)
            self._update_last_modified()
            self._logger.info(f"Added capability '{capability}' to workstation {self.name}")

    def remove_capability(self, capability: str) -> None:
        """Remove a capability from the workstation."""
        if not isinstance(capability, str):
            raise ValueError("Capability must be a string")
            
        try:
            self.capabilities.remove(capability)
            self._update_last_modified()
            self._logger.info(f"Removed capability '{capability}' from workstation {self.name}")
        except ValueError:
            raise ValueError(f"Capability '{capability}' not found in workstation {self.name}")

    def update_capacity(self, new_capacity: int) -> None:
        """Update the current capacity utilization."""
        if not isinstance(new_capacity, int):
            raise ValueError("Capacity must be an integer")
            
        if self.max_capacity is not None and new_capacity > self.max_capacity:
            raise ValueError(f"New capacity exceeds maximum capacity of {self.max_capacity}")
            
        self._current_capacity = new_capacity
        self._update_last_modified()
        self._logger.debug(f"Updated capacity for workstation {self.id} to {new_capacity}")

    @classmethod
    def get_by_type(cls, workstation_type: str) -> List['WorkStation']:
        """Retrieve all workstations of a specific type."""
        return [ws for ws in cls._instances if ws.workstation_type == workstation_type]

    @classmethod
    def get_by_capability(cls, capability: str) -> List['WorkStation']:
        """Retrieve all workstations that have a specific capability."""
        return [ws for ws in cls._instances if capability in ws.capabilities]

    @classmethod
    def get_available_workstations(cls, workstation_type: Optional[str] = None) -> List['WorkStation']:
        """
        Retrieve all idle workstations, optionally filtered by type.
        
        Parameters
        ----------
        workstation_type : str, optional
            If provided, only return idle workstations of this type.
            
        Returns
        -------
        List[WorkStation]
            List of idle workstations, filtered by type if specified.
        """
        if workstation_type is not None:
            return [ws for ws in cls._instances 
                    if ws.status == ResourceStatus.IDLE 
                    and ws.workstation_type == workstation_type]
        
        return [ws for ws in cls._instances if ws.status == ResourceStatus.IDLE]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the workstation instance to a dictionary representation."""
        base_dict = super().to_dict()
        workstation_dict = {
            'workstation_type': self.workstation_type,
            'capabilities': self.capabilities,
            'max_capacity': self.max_capacity,
            'current_capacity': self._current_capacity,
            'location': str(self.location) if self.location else None
        }
        return {**base_dict, **workstation_dict}

class Tool(Resource):
    """A class to represent a Tool.

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
    """
    _instances = WeakSet()
    _total_instances = 0
    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        name: str,
        georeference: List[float],
        tool_type: str,
        id: Optional[str] = None,
        power_type: Optional[str] = "manual",
        power_consumption: float = 0,
        maintenance_interval: float = 0,
        last_maintenance: Optional[datetime] = None,
        location: Optional[Location] = None,
        actors: Optional[List[ActorT]] = None,
        actions: Optional[List[ActionT]] = None,
        constraints: Optional[List[ConstraintT]] = None,
        sensors: Optional[List[SensorT]] = None,
        status: ResourceStatus = ResourceStatus.IDLE,
    ) -> None:
        """Initialize a Tool instance."""
        self.tool_type = tool_type

        super().__init__(
            name=name,
            resource_type=ResourceType.TOOL,
            georeference=georeference,
            id=id,
            location=location,
            power_type=power_type,
            power_consumption=power_consumption,
            maintenance_interval=maintenance_interval,
            last_maintenance=last_maintenance,
            actors=actors,
            actions=actions,
            constraints=constraints,
            sensors=sensors,
            status=status,
        )

        self._validate_tool()
        self._register_instance()
        self._logger.info(f"Created new tool: {self}")

    def __repr__(self) -> str:
        """Return string representation of the Tool instance."""
        return (f"Tool(name='{self.name}', type='{self.tool_type}', "
                f"power='{self.power_type}', status='{self.status}')")

    def _validate_tool(self) -> None:
        """Validate tool-specific attributes."""
        if not isinstance(self.tool_type, str):
            raise ValueError("Tool type must be a string")
        if not isinstance(self.power_type, str):
            raise ValueError("Power type must be a string")
        if self.maintenance_interval is not None and not isinstance(self.maintenance_interval, int):
            raise ValueError("Maintenance interval must be an integer if provided")
        if self.maintenance_interval is not None and self.maintenance_interval <= 0:
            raise ValueError("Maintenance interval must be positive")

    def use_tool(self, duration: float) -> None:
        """Record usage of the tool."""
        if self.needs_maintenance():
            raise ValueError(f"Tool {self.name} requires maintenance before use")
        
        self._hours_used += duration
        self.status = ResourceStatus.WORKING
        self._update_last_modified()
        self._logger.debug(f"Tool {self.name} used for {duration} hours")

class Conveyor(Resource):
    """A class to represent a Conveyor.

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
    """
    _instances = WeakSet()
    _total_instances = 0
    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        name: str,
        georeference: List[float],
        speed: float,  # meters per second
        capacity: float,  # items per meter
        direction: str = "forward",  # forward or reverse
        id: Optional[str] = None,
        location: Optional[Location] = None,
        power_type: Optional[str] = "electric",
        power_consumption: float = 0,
        maintenance_interval: float = 0,
        last_maintenance: Optional[datetime] = None,
        actors: Optional[List[ActorT]] = None,
        actions: Optional[List[ActionT]] = None,
        constraints: Optional[List[ConstraintT]] = None,
        sensors: Optional[List[SensorT]] = None,
        status: ResourceStatus = ResourceStatus.IDLE,
    ) -> None:
        """Initialize a Conveyor instance."""
        self.speed = speed
        self.capacity = capacity
        self.direction = direction
        self._current_load = 0
        self._length = self._calculate_length()

        super().__init__(
            name=name,
            resource_type=ResourceType.CONVEYOR,
            georeference=georeference,
            id=id,
            location=location,
            power_type=power_type,
            power_consumption=power_consumption,
            maintenance_interval=maintenance_interval,
            last_maintenance=last_maintenance,
            actors=actors,
            actions=actions,
            constraints=constraints,
            sensors=sensors,
            status=status,
        )

        self._validate_conveyor()
        self._register_instance()
        self._logger.info(f"Created new conveyor: {self}")

    def __repr__(self) -> str:
        """Return string representation of the Conveyor instance."""
        return (f"Conveyor(name='{self.name}', length={self._length:.2f}m, "
                f"speed={self.speed}m/s, status='{self.status}')")

    def _validate_conveyor(self) -> None:
        """Validate conveyor-specific attributes."""
        if not isinstance(self.speed, (int, float)) or self.speed <= 0:
            raise ValueError("Speed must be a positive number")
        if not isinstance(self.capacity, (int, float)) or self.capacity <= 0:
            raise ValueError("Capacity must be a positive number")
        if self.direction not in ["forward", "reverse"]:
            raise ValueError("Direction must be either 'forward' or 'reverse'")

    def _calculate_length(self) -> float:
        """Calculate the total length of the conveyor system."""
        length = 0
        for i in range(len(self.georeference) - 1):
            p1 = self.georeference[i]
            p2 = self.georeference[i + 1]
            length += ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)**0.5
        return length

    def get_total_capacity(self) -> float:
        """Calculate total capacity of the conveyor."""
        return self._length * self.capacity

    def add_items(self, count: float) -> None:
        """Add items to the conveyor."""
        new_load = self._current_load + count
        if new_load > self.get_total_capacity():
            raise ValueError("Adding items would exceed conveyor capacity")
        self._current_load = new_load
        self._update_last_modified()

    def remove_items(self, count: float) -> None:
        """Remove items from the conveyor."""
        new_load = self._current_load - count
        if new_load < 0:
            raise ValueError("Cannot remove more items than currently on conveyor")
        self._current_load = new_load
        self._update_last_modified()

    def reverse_direction(self) -> None:
        """Reverse the direction of the conveyor."""
        self.direction = "reverse" if self.direction == "forward" else "forward"
        self._update_last_modified()
        self._logger.info(f"Reversed conveyor {self.name} direction to {self.direction}")

class RoboticArm(Resource):
    """A class to represent a RoboticArm.

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
    """
    _instances = WeakSet()
    _total_instances = 0
    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        name: str,
        georeference: List[float],
        arm_type: str,
        reach: float,
        payload: float,
        degrees_of_freedom: int,
        end_effector_type: str,
        id: Optional[str] = None,
        location: Optional[Location] = None,
        power_type: Optional[str] = "electric",
        power_consumption: float = 0,
        maintenance_interval: float = 0,
        last_maintenance: Optional[datetime] = None,
        actors: Optional[List[ActorT]] = None,
        actions: Optional[List[ActionT]] = None,
        constraints: Optional[List[ConstraintT]] = None,
        sensors: Optional[List[SensorT]] = None,
        status: ResourceStatus = ResourceStatus.IDLE,
    ) -> None:
        """Initialize a RoboticArm instance."""
        self.arm_type = arm_type                                # Type/model of the robotic arm
        self.reach = reach                                      # Maximum reach distance in meters
        self.payload = payload                                  # Maximum weight capacity in kg
        self.degrees_of_freedom = degrees_of_freedom            # Number of independent joints/axes
        self.end_effector_type = end_effector_type              # Type of end-of-arm tooling (gripper, welder, etc.)
        self._current_position = [0.0] * degrees_of_freedom     # Current angles of each joint
        self._home_position = [0.0] * degrees_of_freedom        # Default/safe position angles

        super().__init__(
            name=name,
            resource_type=ResourceType.ROBOTIC_ARM,
            georeference=georeference,
            id=id,
            location=location,
            power_type=power_type,
            power_consumption=power_consumption,
            maintenance_interval=maintenance_interval,
            last_maintenance=last_maintenance,
            actors=actors,
            actions=actions,
            constraints=constraints,
            sensors=sensors,
            status=status,
        )

        self._validate_robotic_arm()
        self._register_instance()
        self._logger.info(f"Created new robotic arm: {self}")

    def __repr__(self) -> str:
        """Return string representation of the RoboticArm instance."""
        return (f"RoboticArm(name='{self.name}', type='{self.arm_type}', "
                f"DoF={self.degrees_of_freedom}, status='{self.status}')")

    def _validate_robotic_arm(self) -> None:
        """Validate robotic arm-specific attributes."""
        if not isinstance(self.arm_type, str):
            raise ValueError("Arm type must be a string")
        if not isinstance(self.reach, (int, float)) or self.reach <= 0:
            raise ValueError("Reach must be a positive number")
        if not isinstance(self.payload, (int, float)) or self.payload <= 0:
            raise ValueError("Payload must be a positive number")
        if not isinstance(self.degrees_of_freedom, int) or self.degrees_of_freedom <= 0:
            raise ValueError("Degrees of freedom must be a positive integer")
        if not isinstance(self.end_effector_type, str):
            raise ValueError("End effector type must be a string")

    def move_to_position(self, position: List[float]) -> None:
        """Move the robotic arm to a specific joint configuration."""
        if len(position) != self.degrees_of_freedom:
            raise ValueError(f"Position must have {self.degrees_of_freedom} values")
        
        self._current_position = position.copy()
        self.status = ResourceStatus.WORKING
        self._update_last_modified()
        self._logger.debug(f"Moving arm {self.name} to position {position}")

    def home(self) -> None:
        """Move the robotic arm to its home position."""
        self.move_to_position(self._home_position)
        self._logger.info(f"Arm {self.name} returned to home position")

    def change_end_effector(self, new_type: str) -> None:
        """Change the end effector type."""
        self.end_effector_type = new_type
        self._update_last_modified()
        self._logger.info(f"Changed end effector of {self.name} to {new_type}")

    def get_current_position(self) -> List[float]:
        """Get the current joint positions of the robotic arm."""
        return self._current_position.copy()

    def check_payload(self, weight: float) -> bool:
        """Check if a given weight is within the arm's payload capacity."""
        return weight <= self.payload

class Part:
    """A class to represent a Part.

    Parts are fundamental components used in manufacturing processes. They represent raw 
    materials, purchased components, or intermediate items that are used to create finished 
    products. The Part class manages inventory tracking, state transitions, and supply chain 
    relationships for manufacturing components.

    Parts are connected to various components in the manufacturing system:
    - Products they are used in
    - Storage locations where they are kept
    - Suppliers who provide them
    - Actions that process them
    - Resources that handle them
    - Jobs that require them

    Parts can be categorized into different types:
    - Raw Materials: Unprocessed materials used in manufacturing
    - Purchased Components: Pre-made components from external suppliers
    - Work-in-Progress: Partially completed components

    **Best Practices**:
    - Maintain accurate inventory levels
    - Track minimum stock thresholds
    - Monitor part states
    - Record supplier information
    - Track cost and value
    - Monitor quality metrics
    - Manage batch/lot numbers
    - Track expiration dates
    - Document specifications
    - Monitor usage patterns
    - Track reorder points

    **Attributes**:
    | Name              | Data Type         | Description                                                     |
    |-------------------|-------------------|-----------------------------------------------------------------|
    | `name`            | `str`             | Human-readable name of the Part                                 |
    | `quantity`        | `int`             | Current quantity in stock                                       |
    | `volume`          | `float`           | Physical volume of one unit                                     |
    | `state`           | `ProductionState` | Current state. See [ProductionState](/docs/classes/productionstate) |
    | `part_type`       | `PartType`        | Category of part. See [PartType](/docs/classes/parttype)          |
    | `cost`            | `float`           | Cost per unit                                                   |
    | `supplier`        | `Actor`           | Supplier providing this part                                    |
    | `min_stock_level` | `int`             | Minimum quantity to maintain                                    |
    | `id`              | `str`             | Unique identifier                                               |
    | `creation_date`   | `datetime`        | Timestamp when part was created                                 |
    | `last_modified`   | `datetime`        | Timestamp of last modification                                  |

    **States include**:
    - **Raw**: Unprocessed material
    - **New**: Newly received item
    - **Work in Progress**: In production
    - **Finished**: Complete and ready
    - **Defective**: Failed quality check
    - **On Hold**: Suspended from use

    **Example Configuration**:
    ```python
    part = Part(
        name="Steel Bracket",
        quantity=100,
        volume=0.5,  # cubic meters
        state=ProductionState.NEW,
        part_type=PartType.PURCHASED_COMPONENT,
        cost=25.50,
        min_stock_level=50
        )
    ```
    :::note
    `Parts` are components in the manufacturing process that get transformed into finished products and can be analogous to Materials. They typically require inventory management and state tracking throughout their lifecycle in the manufacturing system.
    :::
    """
    _instances = WeakSet()
    _total_instances = 0
    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        name: str,
        quantity: int,
        volume: float,
        state: ProductionState = ProductionState.NEW,
        part_type: PartType = PartType.RAW_MATERIAL,
        cost: float = 0.0,
        supplier: Optional[ActorT] = None,
        min_stock_level: int = 0,
        id: Optional[str] = None
    ) -> None:
        """Initialize a Part instance."""
        self.id = id if id is not None else str(uuid.uuid4())
        self.name = name
        self.quantity = quantity
        self.volume = volume
        self.state = state if part_type != PartType.PURCHASED_COMPONENT else ProductionState.FINISHED
        self.part_type = part_type
        self.cost = cost
        self.supplier = supplier
        self.min_stock_level = min_stock_level
        self.creation_date = datetime.now()
        self._last_modified = datetime.now()
        
        self._validate()
        self._register_instance()
        self._logger.info(f"Created new part: {self}")

    def _validate(self) -> None:
        """Validate the part's attributes."""
        if not self.name or not self.name.strip():
            raise ValueError("Name cannot be empty")
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if self.volume < 0:
            raise ValueError("Volume cannot be negative")
        if self.cost < 0:
            raise ValueError("Cost cannot be negative")
        if self.min_stock_level < 0:
            raise ValueError("Minimum stock level cannot be negative")
        
    def _register_instance(self) -> None:
        """Register the instance in the WeakSet and increment counter."""
        self.__class__._instances.add(self)
        self.__class__._total_instances += 1

    def _update_last_modified(self) -> None:
        """Update the last modified timestamp with logging."""
        self._last_modified = datetime.now()
        self._logger.debug(f"Updated last_modified for resource {self.id} to {self._last_modified}")

    @property
    def last_modified(self) -> datetime:
        """Return the last modified timestamp."""
        return self._last_modified
    
    def update_state(self, new_state: ProductionState) -> None:
        """
        Update the production state of the part.
        
        Args:
            new_state: New ProductionState to set
            
        Raises:
            ValueError: If state transition is invalid
        """
        if self.part_type == PartType.PURCHASED_COMPONENT and new_state != ProductionState.FINISHED:
            raise ValueError("Purchased components must remain in FINISHED state")
            
        old_state = self.state
        self.state = new_state
        self._update_last_modified()
        
        self._logger.info(f"Updated {self.name} state from {old_state.value} to {new_state.value}")

    def adjust_quantity(self, amount: int) -> None:
        """
        Adjust the quantity of the part by the given amount.
        
        Args:
            amount: Amount to adjust (positive or negative)
            
        Raises:
            ValueError: If resulting quantity would be negative
        """
        new_quantity = self.quantity + amount
        if new_quantity < 0:
            raise ValueError("Cannot reduce quantity below 0")
            
        self.quantity = new_quantity
        self._update_last_modified()
        self._logger.info(f"Adjusted {self.name} quantity by {amount} to {new_quantity}")

    def is_below_min_stock(self) -> bool:
        """Check if current quantity is below minimum stock level."""
        return self.quantity < self.min_stock_level

    def calculate_value(self) -> float:
        """Calculate total value of part based on quantity and cost."""
        return self.quantity * self.cost

    def to_dict(self) -> Dict[str, Any]:
        """Convert the part instance to a dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'volume': self.volume,
            'state': self.state.value,
            'part_type': self.part_type.value,
            'cost': self.cost,
            'supplier': self.supplier,
            'min_stock_level': self.min_stock_level,
            'creation_date': self.creation_date.isoformat(),
            'last_modified': self.last_modified.isoformat()
        }

    def __eq__(self, other: object) -> bool:
        """Compare Part instances for equality."""
        if not isinstance(other, Part):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        """Return hash of the Part instance."""
        return hash(self.id)

    def __str__(self) -> str:
        """Return string representation of the Part instance."""
        return (f"Part({self.id}): {self.name}, Qty: {self.quantity}, "
                f"State: {self.state.value}, Type: {self.part_type.value}")

class Product:
    """A class to represent a Product.

    Products are the finished goods that result from manufacturing processes. They represent 
    completed items that are ready for delivery to customers. The Product class manages the 
    bill of materials, manufacturing processes, and product lifecycle states for finished goods.

    Products are connected to various components in the manufacturing system:
    - Parts they are made from
    - Actions required to produce them
    - Jobs that require them
    - Customers who order them
    - Storage locations where they are kept
    - Resources used in their production
    - Workers involved in their manufacture

    **Best Practices**:
    - Maintain accurate bill of materials
    - Track production states
    - Monitor quality metrics
    - Record customer requirements
    - Track manufacturing costs
    - Document production processes
    - Monitor completion dates
    - Track product variants
    - Maintain revision history
    - Document specifications
    - Track serialization

    **Attributes**:
    | Name                | Data Type                         | Description                                                                          |
    |---------------------|-----------------------------------|--------------------------------------------------------------------------------------|
    | `name`              | `str`                             | Human-readable name of the Product                                                   |
    | `volume`            | `float`                           | Physical volume of the product                                                       |
    | `production_state`  | `ProductionState`                 | Current state. See [ProductionState](/docs/classes/productionstate)                   |
    | `customer`          | `str`                             | Customer who ordered the product                                                     |
    | `due_date`          | `datetime`                        | Required completion date                                                             |
    | `id`                | `str`                             | Unique identifier                                                                    |
    | `actions`           | `List[Action]`                    | Manufacturing steps required                                                         |
    | `parts`             | `Dict[str, tuple[Part, int]]`      | Bill of materials with quantities                                                    |
    | `creation_date`     | `datetime`                        | Timestamp when product was created                                                   |
    | `last_modified`     | `datetime`                        | Timestamp of last modification                                                       |

    **States include**:
    - **New**: Product order received
    - **Work in Progress**: In production
    - **Finished**: Complete and ready
    - **Defective**: Failed quality check
    - **On Hold**: Production suspended

    ***Example Configuration**:
    ```python
    product = Product(
        name="Electric Motor Assembly",
        volume=2.5,  # cubic meters
        production_state=ProductionState.NEW,
        customer="Acme Industries",
        due_date=datetime(2025, 3, 15)
        )
    ```
    Add required parts:
    ```python
    product.add_part(motor_housing, 1)
    product.add_part(rotor_assembly, 1)
    product.add_part(stator_assembly, 1)
    product.add_part(mounting_brackets, 4)
    ```

    :::note
    `Products` represent the output of manufacturing processes and require careful management of their components, production steps, and quality requirements. Each product maintains its bill of materials through `Parts` and associated manufacturing actions to ensure proper production.
    :::
    """
    _instances = WeakSet()
    _total_instances = 0
    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        name: str,
        volume: float,
        production_state: ProductionState = ProductionState.WORK_IN_PROGRESS,
        customer: Optional[str] = None,
        due_date: Optional[datetime] = None,
        id: Optional[str] = None,
        actions: List[ActionT] = None
    ) -> None:
        """Initialize a Product instance."""
        self.id = id if id is not None else str(uuid.uuid4())
        self.name = name
        self.volume = volume
        self._production_state = production_state
        self._customer = customer #TODO: Move to Job?
        self._due_date = due_date #TODO: Move to Job?
        self._parts: Dict[str, tuple[Part, int]] = {}  # Dict of part_id: (Part, quantity)
        self._actions = actions if actions is not None else []
        self.creation_date = datetime.now()
        self._last_modified = datetime.now()
        
        self._validate()
        self._register_instance()
        self._logger.info(f"Created new product: {self}")

    def _validate(self) -> None:
        """Validate the product's attributes."""
        if not self.name or not self.name.strip():
            raise ValueError("Name cannot be empty")
        if self.volume < 0:
            raise ValueError("Volume cannot be negative")
        if self.due_date and self.due_date < datetime.now():
            raise ValueError("Due date cannot be in the past")
        
    def _register_instance(self) -> None:
        """Register the instance in the WeakSet and increment counter."""
        self.__class__._instances.add(self)
        self.__class__._total_instances += 1

    def _update_last_modified(self) -> None:
        """Update the last modified timestamp with logging."""
        self._last_modified = datetime.now()
        self._logger.debug(f"Updated last_modified for resource {self.id} to {self._last_modified}")

    @property
    def actions(self) -> List[ActionT]:
        """Return a copy of the Product's actions."""
        return self._actions.copy()

    @property
    def customer(self) -> ActorT:
        """Return a copy of the Products customer."""
        return self._customer.copy()
    
    @property
    def last_modified(self) -> datetime:
        """Return the last modified timestamp."""
        return self._last_modified    
    
    def add_part(self, part: Part, quantity: int = 1) -> None:
        """
        Add a part to the product's bill of materials.
        
        Args:
            part: Part to add
            quantity: Quantity of the part needed
            
        Raises:
            ValueError: If quantity is invalid
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
            
        self._parts[part.id] = (part, quantity)
        self._update_last_modified()
        
        self._logger.info(f"Added {quantity}x {part.name} to {self.name}'s bill of materials")

    def remove_part(self, part_id: str) -> None:
        """
        Remove a part from the product's bill of materials.
        
        Args:
            part_id: ID of part to remove
            
        Raises:
            KeyError: If part is not found
        """
        if part_id not in self._parts:
            raise KeyError(f"Part {part_id} not found in bill of materials")
            
        part, _ = self._parts.pop(part_id)
        self._update_last_modified()
        self._logger.info(f"Removed {part.name} from {self.name}'s bill of materials")

    def update_part_quantity(self, part_id: str, new_quantity: int) -> None:
        """
        Update the quantity of a part in the bill of materials.
        
        Args:
            part_id: ID of part to update
            new_quantity: New quantity to set
            
        Raises:
            KeyError: If part is not found
            ValueError: If new quantity is invalid
        """
        if part_id not in self._parts:
            raise KeyError(f"Part {part_id} not found in bill of materials")
        if new_quantity <= 0:
            raise ValueError("Quantity must be positive")
            
        part, _ = self._parts[part_id]
        self._parts[part_id] = (part, new_quantity)
        self._update_last_modified()
        self._logger.info(f"Updated {part.name} quantity to {new_quantity} in {self.name}'s BOM")

    def add_action(self, action: Action) -> None:
        """Add an action to the product's process."""
        if not isinstance(action, Action):
            raise TypeError("action must be an instance of Action")
        self._actions.append(action)
        self._actions.sort(key=lambda a: a.sequence_nr)
        self._update_last_modified()
        self._logger.info(f"Added action '{action.name}' to {self.name}'s process")

    def remove_action(self, action: Action) -> None:
        """Remove an action from the product's process."""
        if not isinstance(action, Action):
            raise TypeError("action must be an instance of Action")
        try:
            self._actions.remove(action)
            self._update_last_modified()
            self._logger.info(f"Removed action '{action.name}' from {self.name}'s process")
        except ValueError:
            raise ValueError(f"Action '{action.name}' not found in process")

    def update_state(self, new_state: ProductionState) -> None:
        """Update the production state of the product."""
        old_state = self.production_state
        self.production_state = new_state
        self._update_last_modified()
        self._logger.info(f"Updated {self.name} state from {old_state.value} to {new_state.value}")

    def calculate_total_cost(self) -> float:
        """Calculate total cost of product based on parts and quantities."""
        return sum(part.cost * quantity for part, quantity in self._parts.values())

    def is_overdue(self) -> bool:
        """Check if product is overdue based on due date."""
        return bool(self._due_date and datetime.now() > self._due_date)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the product instance to a dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'volume': self.volume,
            'production_state': self.production_state.value,
            'customer': self._customer,
            'due_date': self._due_date.isoformat() if self._due_date else None,
            'parts_count': len(self._parts),
            'actions_count': len(self._actions),
            'creation_date': self.creation_date.isoformat(),
            'last_modified': self._last_modified.isoformat()
        }

    def __eq__(self, other: object) -> bool:
        """Compare Product instances for equality."""
        if not isinstance(other, Product):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        """Return hash of the Product instance."""
        return hash(self.id)

    def __str__(self) -> str:
        """Return string representation of the Product instance."""
        return (f"Product({self.id}): {self.name}, "
                f"State: {self.production_state.value}, "
                f"Parts: {len(self._parts)}, Actions: {len(self._actions)}")
      
class Storage(Location):
    """A class to represent a Storage location.

    Storage locations are specialized Location instances that manage the storage of Parts and 
    Products within the manufacturing facility. They represent dedicated areas like warehouses, 
    buffer zones, racks, or queues where materials and finished goods are stored. The Storage 
    class extends the Location class to include inventory management capabilities and capacity 
    tracking.

    Storage locations are connected to various components in the manufacturing system:
    - Parts stored within them
    - Products stored within them
    - Workers who manage them
    - Vehicles that access them
    - Actions performed in them
    - Resources used to manage them
    - Jobs that require items from them

    Storage locations can be categorized into different types:
    - **General**: Multi-purpose storage area without specific designation
    - **Warehouse**: Large-scale storage facility
    - **Rack**: Structured storage system with multiple levels
    - **Buffer**: Temporary storage area between operations
    - **Queue**: FIFO storage area for sequential processing

    **Best Practices**:
    - Monitor capacity utilization
    - Track item locations
    - Maintain inventory accuracy
    - Implement proper storage conditions
    - Manage access control
    - Monitor environmental conditions
    - Implement FIFO/LIFO as needed
    - Track storage duration
    - Maintain safety clearances
    - Monitor storage conditions
    - Implement zone organization
    - Track item movements

    **Attributes**:
    | Name               | Data Type                         | Description                                                                           |
    |--------------------|-----------------------------------|---------------------------------------------------------------------------------------|
    | `name`             | `str`                             | Human-readable name of the Storage                                                    |
    | `georeference`     | `List[float]`                     | Physical location coordinates [x, y] or [x, y, z]                                      |
    | `storage_type`     | `StorageType`                     | Type of storage. See [StorageType](/docs/classes/storagetype)                         |
    | `max_capacity`     | `float`                           | Maximum storage capacity in volume units                                              |
    | `id`               | `str`                             | Unique identifier                                                                      |
    | `actors`           | `List[Actor]`                     | Workers who manage this storage                                                        |
    | `actions`          | `List[Action]`                    | Actions performed in this storage                                                      |
    | `constraints`       | `List[constraints]`                      | Operating constraints                                                                  |
    | `storage`          | `Dict[str, Union[Product, Part]]` | Dictionary of stored items by ID                                                       |
    | `current_capacity` | `float`                           | Current used capacity                                                                  |
    | `creation_date`    | `datetime`                        | Timestamp when storage was created                                                     |
    | `last_modified`    | `datetime`                        | Timestamp of last modification                                                         |

    **Storage Operations**:
    - Add items to storage
    - Remove items from storage
    - Query stored items
    - Track capacity utilization
    - Monitor storage conditions
    - Manage item locations
    - Track inventory levels
    - Handle item retrievals

    **Example Configuration**:
    ```python
    storage = Storage(
        name="Main Warehouse",
        georeference=[52.2376489846171, 6.847945014035459],
        storage_type=StorageType.WAREHOUSE,
        max_capacity=1000.0,  # cubic meters
        actors=[warehouse_manager, inventory_clerk], # instances of Actor class
        constraints=[temperature_constraint] # instance of Constraint class
        )
    ```

    Add items to storage
    ```python
    storage.add_item(raw_material_batch)
    storage.add_item(finished_product)
    ```

    Check utilization
    ```python
    print(f"Storage utilization: {storage.utilization}%")
    ```

    :::note
    The `Storage` class inherits base attributes from the `Location` class while adding specialized capabilities for inventory management. Use this class for any areas dedicated to storing `Parts` or `Products`, whether temporary or long-term. The class supports different storage types and maintains accurate capacity tracking to prevent overflow conditions.
    :::
    """
    def __init__(
        self,
        name: str,
        georeference: List[float],
        storage_type: StorageType,
        max_capacity: float,
        id: Optional[str] = None,
        actors: List[ActorT] = None,
        actions: List[ActionT] = None,
        constraints: Optional[List[ConstraintT]] = None,
    ) -> None:
        
        """Initialize an Storage location."""
        self.storage_type = storage_type
        self.max_capacity = max_capacity
        self._storage: Dict[str, Union[Product, Part]] = {}  # Dictionary to store items by their IDs
        self._current_capacity = 0.0

        super().__init__(
            name=name,
            georeference=georeference,
            location_type=LocationType.INTERNAL,  # Inventories are always internal
            id=id,
            actors=actors,
            actions=actions,
            constraints=constraints
        )

        self._logger.info(f"Created new storage location: {self}")

    def __repr__(self) -> str:
        """Return string representation of the Storage instance."""
        return (f"Storage(name='{self.name}', type={self.storage_type.value}, "
                f"capacity={self._current_capacity}/{self.max_capacity}, "
                f"items={len(self._storage)})")

    def add_item(self, item: Union[Product, Part]) -> None:
        """
        Add a Product or Part to the storage.
        
        Args:
            item: The Product or Part to add
            
        Raises:
            TypeError: If item is not a Product or Part
            ValueError: If adding the item would exceed capacity
        """
        if not isinstance(item, (Product, Part)):
            raise TypeError("Only Products and Parts can be stored in storage")
            
        new_capacity = self._current_capacity + item.volume
        if new_capacity > self.max_capacity:
            raise ValueError(f"Adding item would exceed max capacity of {self.max_capacity}")
            
        self._storage[item.id] = item
        self._current_capacity = new_capacity
        self._update_last_modified()
        self._logger.debug(f"Added item {item.id} to storage {self.id}")

    def remove_item(self, item_id: str) -> Union[Product, Part]:
        """
        Remove and return an item from storage by its ID.
        
        Args:
            item_id: The ID of the item to remove
            
        Returns:
            The removed Product or Part
            
        Raises:
            KeyError: If item_id is not found in storage
        """
        if item_id not in self._storage:
            raise KeyError(f"Item {item_id} not found in storage")
            
        item = self._storage.pop(item_id)
        self._current_capacity -= item.volume
        self._update_last_modified()
        self._logger.debug(f"Removed item {item_id} from storage {self.id}")
        return item

    def get_item(self, item_id: str) -> Union[Product, Part]:
        """
        Get an item from storage by its ID without removing it.
        
        Args:
            item_id: The ID of the item to get
            
        Returns:
            The Product or Part
            
        Raises:
            KeyError: If item_id is not found in storage
        """
        if item_id not in self._storage:
            raise KeyError(f"Item {item_id} not found in storage")
        return self._storage[item_id]

    def list_items(self) -> List[Union[Product, Part]]:
        """Return a list of all items in the storage."""
        return list(self._storage.values())

    def get_items_by_type(self, item_type: type) -> List[Union[Product, Part]]:
        """
        Get all items of a specific type (Product or Part).
        
        Args:
            item_type: The type to filter by (Product or Part)
            
        Returns:
            List of items matching the specified type
        """
        return [item for item in self._storage.values() if isinstance(item, item_type)]

    @property
    def available_capacity(self) -> float:
        """Return the remaining available capacity."""
        return self.max_capacity - self._current_capacity

    @property
    def utilization(self) -> float:
        """Return the current utilization as a percentage."""
        return (self._current_capacity / self.max_capacity) * 100 if self.max_capacity > 0 else 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert the storage instance to a dictionary representation."""
        base_dict = super().to_dict()
        storage_dict = {
            'storage_type': self.storage_type.value,
            'max_capacity': self.max_capacity,
            'current_capacity': self._current_capacity,
            'utilization': self.utilization,
            'item_count': len(self._storage)
        }
        return {**base_dict, **storage_dict}

class Job:
    """A class to represent a Job in the manufacturing system.

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
    | `products` | `List[Product]` | Products to be manufactured |
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
    """
    _instances = WeakSet()
    _total_instances = 0
    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        products: List[ProductT],
        customer: Optional[ActorT] = None,
        due_date: Optional[datetime] = None,
        priority: Optional[JobPriority] = None,
        id: Optional[str] = None
    ):
        """Initialize a Job instance."""
        self.id = id if id is not None else str(uuid.uuid4())
        self.customer = customer
        self.products = products
        self.due_date = due_date
        self.priority = priority
        self.status = JobStatus.PLANNED
        
        # Timestamps
        self.creation_date = datetime.now()
        self.start_date: Optional[datetime] = None
        self.completion_date: Optional[datetime] = None
        self._last_modified = datetime.now()
        
        # Resource allocation
        self.allocated_resources: Dict[str, str] = {}  # Action ID to Resource IDs
        
        # Initialize by associating all product actions with this job
        self._initialize_actions()

        self._validate()
        self._logger.info(f"Created new job: {self}")

    def _validate(self) -> None:
        """Validate job attributes."""
        if self.customer is not None and not isinstance(self.customer, get_args(ActorT.__bound__)):
            raise ValueError("Customer must be an instance of Actor, if given")
        if not self.products:
            raise ValueError("Job must have at least one product")
        if self.due_date < datetime.now():
            raise ValueError("Due date cannot be in the past")

    def _update_last_modified(self) -> None:
        """Update the last modified timestamp with logging."""
        self._last_modified = datetime.now()
        self._logger.debug(f"Updated last_modified for location {self.id} to {self._last_modified}")

    def _register_instance(self) -> None:
        """Register the instance in the WeakSet and increment counter."""
        self.__class__._instances.add(self)
        self.__class__._total_instances += 1

    def _initialize_actions(self) -> None:
        """Initialize by associating relevant actions with this job."""
        # Associate product actions
        for product in self.products:
            for action in product.actions:
                action.set_job(self.id)
        
    def allocate_resource(self, action: ActionT, resource: ResourceT) -> None:
        """Allocate resources to a specific action."""
        if action not in self.actions:
            raise ValueError(f"Action {action.id} not found in job")
        self.allocated_resources[action.id] = resource.id
        self._update_last_modified()
        self._logger.info(f"Allocated resource {resource.id} to action {action.id}")

    @property
    def actions(self) -> List[ActionT]:
        """Get all actions associated with this job."""
        return Action.get_job_actions(self.id)

    def add_action(self, action: ActionT) -> None:
        """Add a new action to this job."""
        action.set_job(self.id)
        self._logger.info(f"Added action {action.id} to job {self.id}")

    def remove_action(self, action: ActionT) -> None:
        """Remove an action from this job."""
        if action.job_id == self.id:
            action.remove_job()
            self._logger.info(f"Removed action {action.id} from job {self.id}")

    def get_incomplete_actions(self) -> List[ActionT]:
        """Get all actions that haven't been completed."""
        return [action for action in self.actions 
                if action.status != ProductionState.FINISHED]

    def get_ready_actions(self) -> List[ActionT]:
        """Get actions that are ready to be executed."""
        return [action for action in self.actions 
                if action.status == ProductionState.PLANNED]

    def get_in_progress_actions(self) -> List[ActionT]:
        """Get actions that are currently in progress."""
        return [action for action in self.actions 
                if action.status == ProductionState.WORK_IN_PROGRESS]

    def start_job(self) -> None:
        """Start the manufacturing job."""
        if self.status != JobStatus.PLANNED:
            raise ValueError(f"Cannot start job in {self.status.value} status")
            
        self.status = JobStatus.IN_PROGRESS
        self.start_date = datetime.now()
        self._update_last_modified()
        self._logger.info(f"Started job {self.id}")
 
    def complete_job(self) -> None:
        """Mark the job as completed."""
        self.status = JobStatus.COMPLETED
        self.completion_date = datetime.now()
        self._update_last_modified()
        self._logger.info(f"Completed job {self.id}")

    def put_on_hold(self, reason: str) -> None:
        """Put the job on hold."""
        self.status = JobStatus.ON_HOLD
        self._update_last_modified()
        self._logger.info(f"Put job {self.id} on hold: {reason}")

    def resume_job(self) -> None:
        """Resume a job that was on hold."""
        if self.status != JobStatus.ON_HOLD:
            raise ValueError(f"Cannot resume job in {self.status.value} status")
            
        self.status = JobStatus.IN_PROGRESS
        self._update_last_modified()
        self._logger.info(f"Resumed job {self.id}")

    def cancel_job(self, reason: str) -> None:
        """Cancel the job."""
        self.status = JobStatus.CANCELLED
        self._update_last_modified()
        self._logger.info(f"Cancelled job {self.id}: {reason}")

    def get_progress(self) -> float:
        """Calculate job progress as a percentage."""
        total_actions = len(self.actions)
        if total_actions == 0:
            return 0.0
        completed = sum(1 for action in self.actions 
                       if action.status == ProductionState.FINISHED)
        return (completed / total_actions) * 100

    def get_estimated_completion_time(self) -> float:
        """Calculate estimated completion time in hours."""
        return sum(action.duration for action in self.actions)

    def is_overdue(self) -> bool:
        """Check if the job is overdue."""
        return datetime.now() > self.due_date

    def to_dict(self) -> Dict[str, Any]:
        """Convert the job instance to a dictionary representation."""
        return {
            'id': self.id,
            'customer_name': self.customer.name,
            'products': [product.id for product in self.products],
            'status': self.status.value,
            'priority': self.priority.value,
            'progress': self.get_progress(),
            'due_date': self.due_date.isoformat(),
            'creation_date': self.creation_date.isoformat(),
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'action_count': len(self.actions),
            'estimated_completion_time': self.get_estimated_completion_time()
        }

    def __str__(self) -> str:
        return (f"Job({self.id}): Customer: {self.customer_name}, "
                f"Products: {len(self.products)}, Status: {self.status.value}, "
                f"Progress: {self.get_progress():.1f}%")

class Constraint:
    '''
    Not Yet Implemented. 
    '''
    pass

class Sensor:
    """A class to represent a Sensor in the manufacturing system.

    Sensors are devices that monitor and collect data about Resources, Locations, or other 
    manufacturing system components. They provide real-time or periodic measurements of 
    various parameters like temperature, pressure, position, speed, etc.

    Sensors are connected to various components in the manufacturing system:
    - Resources they monitor (machines, tools, conveyors)
    - Locations they observe
    - Products they inspect
    - Parts they measure

    **Best Practices**:
    - Define clear measurement ranges and units
    - Set appropriate sampling frequencies
    - Maintain calibration schedules
    - Monitor sensor health
    - Handle measurement errors
    - Track data history
    - Set alert thresholds
    - Validate measurements

    **Attributes**:
    | Name                  | Data Type           | Description                                                        |
    |-----------------------|---------------------|--------------------------------------------------------------------|
    | `name`                | `str`               | Human-readable name of the Sensor                                  |
    | `sensor_type`         | `str`               | Type of sensor (temperature, pressure, etc.)                       |
    | `measurement_unit`    | `str`               | Unit of measurement (°C, bar, mm, etc.)                           |
    | `range_min`           | `float`             | Minimum measurable value                                          |
    | `range_max`           | `float`             | Maximum measurable value                                          |
    | `accuracy`            | `float`             | Measurement accuracy (± value)                                     |
    | `sampling_rate`       | `float`             | Measurements per second                                           |
    | `last_reading`        | `float`             | Most recent measurement                                           |
    | `last_reading_time`   | `datetime`          | Timestamp of last measurement                                     |
    | `alert_min`           | `float`             | Lower threshold for alerts                                        |
    | `alert_max`           | `float`             | Upper threshold for alerts                                        |
    | `status`              | `str`               | Current sensor status (active, fault, etc.)                       |
    | `calibration_date`    | `datetime`          | Last calibration timestamp                                        |
    | `calibration_due`     | `datetime`          | Next calibration due date                                         |
    | `id`                  | `str`               | Unique identifier                                                 |
    | `location`            | `Location` or `Resource`         | Physical location of the sensor                                   |
    | `creation_date`       | `datetime`          | Timestamp when sensor was created                                 |
    | `last_modified`       | `datetime`          | Timestamp of last modification                                    |

    **Example Configuration**:
    ```python
    # Temperature sensor for a CNC machine
    temp_sensor = Sensor(
        name="CNC-1 Spindle Temperature",
        sensor_type="temperature",
        measurement_unit="°C",
        range_min=0.0,
        range_max=150.0,
        accuracy=0.1,
        sampling_rate=1.0,  # Hz (readings per second)
        alert_min=10.0,     # alert if below 10°C
        alert_max=120.0,    # alert if above 120°C
        resource=cnc_machine_1
    )

    # Vibration sensor for predictive maintenance
    vib_sensor = Sensor(
        name="Robot-2 Vibration Monitor",
        sensor_type="vibration",
        measurement_unit="mm/s",
        range_min=0.0,
        range_max=50.0,
        accuracy=0.01,
        sampling_rate=100.0,  # 100 Hz sampling
        alert_max=30.0,       # alert if vibration too high
        resource=robot_arm_2
    )

    # Position sensor for an AGV
    pos_sensor = Sensor(
        name="AGV-1 Position Tracker",
        sensor_type="position",
        measurement_unit="m",
        range_min=0.0,
        range_max=100.0,
        accuracy=0.005,
        sampling_rate=10.0,  # 10 Hz position updates
        resource=agv_1
    )
    ```

    :::note
    Sensors are used for monitoring manufacturing processes.
    :::
    """
    pass  # Implementation details would go here