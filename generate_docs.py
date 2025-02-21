import os
import inspect
import importlib.util
import ast
from typing import Any, Dict, List
import logging
from pathlib import Path
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_module(file_path: str, module_name: str = "omm") -> Any:
    """Load a Python module from file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_classes(module: Any) -> List[type]:
    """Get all classes defined in the module."""
    return [obj for name, obj in inspect.getmembers(module)
            if inspect.isclass(obj) and obj.__module__ == module.__name__]

def get_enum_comments(enum_class: type, source_file: Path) -> Dict[str, str]:
    """Extract inline comments for enum members by parsing the source file directly."""
    member_comments = {}
    
    try:
        # Read the entire source file
        with open(source_file, 'r', encoding='utf-8') as f:
            source = f.read()
            
        # Parse the source code into an AST
        tree = ast.parse(source)
        
        # Find the class definition that matches our enum
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == enum_class.__name__:
                logger.info(f"Found class definition for {node.name}")
                # Look for assignments (enum members) in the class body
                for item in node.body:
                    if isinstance(item, ast.Assign):
                        # Get the member name
                        for target in item.targets:
                            if isinstance(target, ast.Name):
                                member_name = target.id
                                if member_name in enum_class.__members__:
                                    # Get the line from source
                                    line = source.splitlines()[item.lineno - 1]
                                    comment_start = line.find('#')
                                    if comment_start != -1:
                                        comment = line[comment_start + 1:].strip()
                                        member_comments[member_name] = comment
                                        logger.info(f"Added comment for {member_name}: {comment}")
        
        logger.info(f"Final member_comments dictionary: {member_comments}")
        return member_comments
        
    except Exception as e:
        logger.warning(f"Error processing enum {enum_class.__name__}: {str(e)}")
        return {}

def generate_enum_doc(enum_class: type, source_file: Path) -> str:
    """Generate markdown documentation for an Enum class."""
    doc_parts = []
    
    # Get comments for enum members and log them
    member_comments = get_enum_comments(enum_class, source_file)
    logger.info(f"Comments for {enum_class.__name__}: {member_comments}")
    
    # Enum name and description
    doc_parts.append(f"# {enum_class.__name__}\n")
    if enum_class.__doc__:
        doc_parts.append(f"{enum_class.__doc__.strip()}\n")
    
    # Enum values
    doc_parts.append("\n## Values\n")
    
    # Create a table of enum values
    doc_parts.append("| Value | Description |")
    doc_parts.append("|-------|-------------|")
    
    # Add each enum member with its comment and log each entry
    for name, member in enum_class.__members__.items():
        description = member_comments.get(name, 'No description available')
        logger.info(f"Generating doc for {name}: {description}")
        doc_parts.append(f"| `{name}` | {description} |")
    
    # Usage Example
    doc_parts.append("\n## Usage Example\n")
    doc_parts.append("```python")
    doc_parts.append(f"from omm import {enum_class.__name__}")
    doc_parts.append("")
    first_value = next(iter(enum_class.__members__))
    doc_parts.append(f"# Access enum value")
    doc_parts.append(f"value = {enum_class.__name__}.{first_value}")
    doc_parts.append("")
    doc_parts.append("# Value comparison")
    doc_parts.append(f"if value == {enum_class.__name__}.{first_value}:")
    doc_parts.append(f"    print(f'Value is {first_value}')")
    doc_parts.append("```\n")
    
    # Log the final documentation
    final_doc = '\n'.join(doc_parts)
    logger.info(f"Generated documentation for {enum_class.__name__}:")
    logger.info(final_doc)
    
    return final_doc

def generate_class_doc(cls: type) -> str:
    """Generate markdown documentation for a regular class."""
    doc_parts = []
    
    # Class name and description
    doc_parts.append(f"# {cls.__name__}\n")
    if cls.__doc__:
        doc_parts.append(f"{cls.__doc__.strip()}\n")
    
    # Inheritance
    if cls.__bases__ and cls.__bases__[0] != object:
        base_classes = ', '.join(base.__name__ for base in cls.__bases__)
        doc_parts.append(f"\n## Inheritance\n")
        doc_parts.append(f"Inherits from: `{base_classes}`\n")
    
    # Constructor
    if hasattr(cls, '__init__'):
        init_doc = inspect.getdoc(cls.__init__)
        signature = str(inspect.signature(cls.__init__))
        doc_parts.append(f"\n## Constructor\n")
        doc_parts.append(f"```python\ndef __init__{signature}:\n```\n")
        if init_doc:
            doc_parts.append(f"{init_doc}\n")
    
    # Properties
    properties = inspect.getmembers(cls, lambda x: isinstance(x, property))
    if properties:
        doc_parts.append("\n## Properties\n")
        for name, prop in properties:
            doc_parts.append(f"\n### `{name}`\n")
            if prop.__doc__:
                doc_parts.append(f"{prop.__doc__.strip()}\n")
            
            # Add property code example
            doc_parts.append("```python")
            doc_parts.append(f"@property")
            doc_parts.append(f"def {name}(self):")
            doc_parts.append(f"    # Returns {prop.fget.__annotations__.get('return', 'Any')}")
            doc_parts.append("```\n")
    
    # Methods
    methods = [m for m in inspect.getmembers(cls, predicate=inspect.isfunction)
              if not m[0].startswith('_') or m[0] == '__init__']
    if methods:
        doc_parts.append("\n## Methods\n")
        for name, method in methods:
            if name == '__init__':
                continue
            doc_parts.append(f"\n### `{name}`\n")
            if method.__doc__:
                doc_parts.append(f"{method.__doc__.strip()}\n")
            
            # Add method signature
            signature = str(inspect.signature(method))
            doc_parts.append("```python")
            doc_parts.append(f"def {name}{signature}:")
            doc_parts.append("```\n")
    
    # Usage Example
    doc_parts.append("\n## Example Usage\n")
    doc_parts.append("```python")
    doc_parts.append(generate_example_usage(cls))
    
    doc_parts.append("```\n")
    
    return '\n'.join(doc_parts)

def generate_example_usage(cls: type) -> str:
    """Generate human-friendly example usage for a class."""
    examples = []
    class_name = cls.__name__

    # Class-specific examples

    # Machine examples
    if class_name == "Machine":
        examples.extend([
            "# Example: Creating a CNC machine resource with sensors and operators.",
            "cnc_machine = Machine(",
            "    name='CNC_Mill_01',",
            "    machine_type=5-Axis Mill,",
            "    georeference=[10.5, 20.0, 0.0],  # Machine location in the factory",
            "    capabilities=['precision_milling', 'drilling', 'threading', 'engraving'],",
            "    sensors=[",
            "        Sensor('spindle_speed'),",
            "        Sensor('coolant_level'),",
            "        Sensor('tool_wear')",
            "    ],",
            "    status=ResourceStatus.IDLE,",
            "    power_consumption=7.5,  # kW",
            "    maintenance_interval=2000  # Hours",
            ")",
            "",
            "# Assign workers and start operation",
            "operator = Worker('Berry Gerrits', roles={'CNC Operator': ['5-Axis Mill']})",
            "cnc_machine.add_actor(operator)",
            "",
            "if operator.can_work_with(cnc_machine):",
            "    operator.work_on(cnc_machine, 'engraving')",
            "    print(f'{operator.name} operating {cnc_machine.name}')"
            "",
            "# Monitor machine condition",
            "for sensor in cnc_machine.sensors:",
            "    print(f'{sensor.name}: {sensor.get_reading()}')"
        ])
    # Job examples
    elif class_name == "Job":
        examples.extend([
            "# Example: Creating a manufacturing job for a custom order",
            "custom_cabinet = Job(",
            "    name='Custom Cabinet Assembly',",
            "    job_type='ASSEMBLY',",
            "    priority=JobPriority.HIGH,",
            "    deadline=datetime.now() + timedelta(days=2),",
            "    required_resources=[",
            "        'CNC_Router_01',  # For cutting panels",
            "        'Assembly_Station_3',  # For assembly",
            "        'Paint_Booth_02'  # For finishing",
            "    ]",
            ")",
            "",
            "# Add job requirements",
            "custom_cabinet.add_requirement(",
            "    Requirement('Wood panels', quantity=12)",
            ")",
            "",
            "# Track job progress",
            "custom_cabinet.update_status(JobStatus.IN_PROGRESS)",
            "custom_cabinet.update_completion(45)  # 45% complete"
        ])
    # Location examples
    elif class_name == "Location":
        examples.extend([
            "# Example: Creating a manufacturing assembly line location",
            "assembly_line = Location(",
            "    name='Assembly Line A',",
            "    georeference=[50.2, 30.5],  # Location coordinates in factory",
            "    location_type=LocationType.INTERNAL,",
            "    actors=[",
            "        Worker('Emma Chen', roles={'Assembler': ['Workstation']}),",
            "        Worker('James Wilson', roles={'QC': ['Inspection']})",
            "    ],",
            "    actions=[",
            "        Action('Assembly', ActionType.ASSEMBLY, duration=45),",
            "        Action('Quality Check', ActionType.QUALITY_CHECK, duration=15)",
            "    ]",
            ")",
            "",
            "# Track current activities",
            "current_action = assembly_line.get_current_action()",
            "if current_action:",
            "    print(f'Current activity: {current_action.name} ({current_action.progress}% complete)')",
            "",
            "# Manage workers at the location",
            "new_worker = Worker('Maria Garcia', roles={'Assembler': ['Workstation']})",
            "assembly_line.add_actor(new_worker)",
            "print(f'Workers at location: {[w.name for w in assembly_line.actors]}')"
        ])

    # Actor examples
    elif class_name == "Actor":
        examples.extend([
            "# Example: Creating and managing an actor in the system",
            "supplier = Actor(",
            "    name='Precision Parts Ltd',",
            "    locations=[",
            "        Location('Warehouse A', [45.5, 23.7], LocationType.EXTERNAL),",
            "        Location('Loading Dock B', [45.6, 23.8], LocationType.EXTERNAL)",
            "    ]",
            ")",
            "",
            "# Add a new delivery location",
            "new_location = Location('Distribution Center', [46.0, 24.0], LocationType.EXTERNAL)",
            "supplier.add_location(new_location)",
            "",
            "# Track supplier's delivery points",
            "print(f'Delivery locations for {supplier.name}:')",
            "for loc in supplier.locations:",
            "    print(f'  - {loc.name} at {loc.georeference}')"
        ])

    # Worker examples
    elif class_name == "Worker":
        examples.extend([
            "# Example: Setting up a skilled manufacturing worker",
            "skilled_worker = Worker(",
            "    name='David Miller',",
            "    roles={",
            "        'Machine Operator': ['CNC', 'Lathe', 'Mill'],",
            "        'Quality Inspector': ['Assembly', 'Final Product'],",
            "        'Maintenance': ['Preventive', 'Repair']",
            "    },",
            "    locations=[",
            "        Location('Machining Area', [10.0, 20.0], LocationType.INTERNAL),",
            "        Location('QC Station', [15.0, 20.0], LocationType.INTERNAL)",
            "    ]",
            ")",
            "",
            "# Assign new role and verify qualifications",
            "skilled_worker.add_role('Trainer', ['New Operators', 'Safety'])",
            "",
            "# Start work on a machine",
            "cnc_machine = Machine('CNC_01', 'CNC', [10.0, 20.0])",
            "if skilled_worker.can_work_with(cnc_machine):",
            "    skilled_worker.work_on(cnc_machine, 'precision_cutting')",
            "    print(f'{skilled_worker.name} operating {cnc_machine.name}')"
        ])

    # Machine examples
    elif class_name == "Machine":
        examples.extend([
            "# Example: Setting up a sophisticated CNC machine",
            "cnc_machine = Machine(",
            "    name='CNC_Mill_01',",
            "    machine_type='5-Axis Mill',",
            "    georeference=[10.5, 20.0, 0.0],",
            "    capabilities=['precision_milling', 'drilling', 'threading', 'engraving'],",
            "    sensors=[",
            "        Sensor('spindle_speed'),",
            "        Sensor('coolant_level'),",
            "        Sensor('tool_wear')",
            "    ],",
            "    status=ResourceStatus.IDLE,",
            "    power_consumption=7.5,  # kW",
            "    maintenance_interval=2000  # Hours",
            ")",
            "",
            "# Assign workers and start operation",
            "operator = Worker('Sarah Chen', roles={'CNC Operator': ['5-Axis Mill']})",
            "cnc_machine.add_actor(operator)",
            "",
            "# Start specific machining operation",
            "cnc_machine.start_capability('precision_milling')",
            "print(f'Machine status: {cnc_machine.status}')",
            "",
            "# Monitor machine condition",
            "for sensor in cnc_machine.sensors:",
            "    print(f'{sensor.name}: {sensor.get_reading()}')"
        ])

    # Vehicle examples
    elif class_name == "Vehicle":
        examples.extend([
            "# Example: Creating an automated guided vehicle (AGV)",
            "agv = Vehicle(",
            "    name='AGV_01',",
            "    vehicle_type=VehicleType.AUTOMATED_MOBILE_ROBOT,",
            "    georeference=[0.0, 0.0, 0.0],",
            "    average_speed=1.5,  # meters/second",
            "    battery_capacity=24.0,  # kWh",
            "    battery_threshold=20.0,  # Minimum battery percentage",
            "    battery_charging_rate=4.0,  # kW",
            "    load_capacities={'max_weight': 500},  # kg",
            "    sensors=[",
            "        Sensor('battery_level'),",
            "        Sensor('proximity'),",
            "        Sensor('path_detection')",
            "    ],",
            "    energy_consumption_moving=0.5,  # kWh per hour while moving",
            "    energy_consumption_idling=0.1   # kWh per hour while idle",
            ")",
            "",
            "# Monitor vehicle status and start charging if needed",
            "if agv.battery_threshold > 20:",
            "    agv.start_charging()",
            "    print(f'Charging vehicle at {agv.battery_charging_rate}kW')",
            "",
            "# Adjust speed based on load",
            "agv.speed = agv.average_speed * 0.8  # Reduce speed to 80% for heavy load",
            "print(f'Current speed: {agv.speed} m/s')"
        ])

    # WorkStation examples
    elif class_name == "WorkStation":
        examples.extend([
            "# Example: Creating an advanced assembly workstation",
            "assembly_station = WorkStation(",
            "    name='Assembly_Station_01',",
            "    georeference=[15.0, 25.0, 0.0],",
            "    workstation_type='electronics_assembly',",
            "    capabilities=[",
            "        'circuit_board_assembly',",
            "        'component_soldering',",
            "        'quality_inspection'",
            "    ],",
            "    max_capacity=3,  # Number of simultaneous assemblies",
            "    actors=[",
            "        Worker('Emma Thompson', roles={'Electronics Assembler': ['PCB']})",
            "    ],",
            "    sensors=[",
            "        Sensor('temperature'),",
            "        Sensor('humidity')",
            "    ]",
            ")",
            "",
            "# Update station capacity and status",
            "assembly_station.update_capacity(2)",
            "print(f'Current occupation: {assembly_station.current_capacity}/{assembly_station.max_capacity}')",
            "",
            "# Check environmental conditions",
            "for sensor in assembly_station.sensors:",
            "    print(f'{sensor.name}: {sensor.get_reading()}')"
        ])

    # Tool examples
    elif class_name == "Tool":
        examples.extend([
            "# Example: Setting up a precision power tool",
            "power_drill = Tool(",
            "    name='Industrial_Drill_01',",
            "    tool_type='precision_drill',",
            "    georeference=[5.0, 10.0, 0.0],",
            "    power_type='electric',",
            "    maintenance_interval=200,  # Hours between maintenance",
            "    location=Location('Tool Storage', [5.0, 10.0], LocationType.INTERNAL),",
            "    sensors=[",
            "        Sensor('temperature'),",
            "        Sensor('vibration')",
            "    ]",
            ")",
            "",
            "# Track tool usage and maintenance",
            "power_drill.use_tool(duration=2.5)  # Hours",
            "",
            "if power_drill.needs_maintenance():",
            "    power_drill.perform_maintenance()",
            "    print(f'Maintenance completed on {power_drill.name}')",
            "",
            "# Monitor tool condition",
            "for sensor in power_drill.sensors:",
            "    print(f'{sensor.name}: {sensor.get_reading()}')"
        ])

    # Conveyor examples
    elif class_name == "Conveyor":
        examples.extend([
            "# Example: Setting up a smart conveyor system",
            "main_conveyor = Conveyor(",
            "    name='MainLine_01',",
            "    georeference=[0.0, 0.0, 0.0],",
            "    polyline=[[0,0], [10,0], [10,10], [20,10]],  # Conveyor path",
            "    speed=0.5,  # meters per second",
            "    capacity=10.0,  # items per meter",
            "    direction='forward',",
            "    sensors=[",
            "        Sensor('motor_temperature'),",
            "        Sensor('belt_tension'),",
            "        Sensor('item_counter')",
            "    ]",
            ")",
            "",
            "# Manage conveyor operations",
            "main_conveyor.add_items(5)  # Add 5 items",
            "",
            "# Calculate utilization",
            "total_capacity = main_conveyor.get_total_capacity()",
            "available_space = total_capacity - main_conveyor._current_load",
            "print(f'Conveyor utilization: {(main_conveyor._current_load/total_capacity)*100:.1f}%')",
            "",
            "# Reverse direction for return line",
            "main_conveyor.reverse_direction()",
            "print(f'Conveyor direction: {main_conveyor.direction}')"
        ])

    # RoboticArm examples
    elif class_name == "RoboticArm":
        examples.extend([
            "# Example: Setting up a sophisticated robotic arm",
            "robot_arm = RoboticArm(",
            "    name='Robot_01',",
            "    georeference=[12.0, 8.0, 0.0],",
            "    arm_type='6-axis',",
            "    reach=1.8,  # meters",
            "    payload=15.0,  # kg",
            "    degrees_of_freedom=6,",
            "    end_effector_type='multi_purpose_gripper',",
            "    sensors=[",
            "        Sensor('joint_position'),",
            "        Sensor('torque'),",
            "        Sensor('gripper_force'),",
            "        Sensor('collision_detection')",
            "    ]",
            ")",
            "",
            "# Program robotic movement",
            "pick_position = [0.0, 45.0, 90.0, 0.0, 45.0, 0.0]  # Joint angles",
            "if robot_arm.check_payload(5.0):  # Check if weight is within limits",
            "    robot_arm.move_to_position(pick_position)",
            "    print(f'Robot at position: {robot_arm.get_current_position()}')",
            "",
            "# Change end effector for different task",
            "robot_arm.change_end_effector('precision_welder')",
            "print(f'Current end effector: {robot_arm.end_effector_type}')",
            "",
            "# Return to safe position",
            "robot_arm.home()",
            "print('Robot returned to home position')"
        ])

    # Part examples
    elif class_name == "Part":
        examples.extend([
            "# Example: Managing manufacturing parts inventory",
            "aluminum_block = Part(",
            "    name='Aluminum_Block_6061',",
            "    quantity=50,",
            "    volume=0.008,  # cubic meters",
            "    state=ProductionState.NEW,",
            "    part_type=PartType.RAW_MATERIAL,",
            "    cost=15.0,  # cost per unit",
            "    supplier=Actor('MetalsRUs'),",
            "    min_stock_level=10",
            ")",
            "",
            "# Track inventory movements",
            "aluminum_block.adjust_quantity(-5)  # Use 5 units",
            "",
            "# Check inventory status",
            "if aluminum_block.is_below_min_stock():",
            "    print(f'Low stock alert for {aluminum_block.name}!')",
            "    print(f'Current quantity: {aluminum_block.quantity}')",
            "    print(f'Minimum level: {aluminum_block.min_stock_level}')",
            "",
            "# Calculate inventory value",
            "total_value = aluminum_block.calculate_value()",
            "print(f'Total inventory value: ${total_value:.2f}')"
        ])
    else:
        # Generic example for other classes
        examples.extend([
            f"# Create a new {class_name} instance"
        ])
        
        # Get constructor parameters
        if hasattr(cls, '__init__'):
            params = inspect.signature(cls.__init__).parameters
            param_examples = []
            for name, param in params.items():
                if name == 'self':
                    continue
                if param.default is inspect.Parameter.empty:
                    param_examples.append(f"    {name}=<{param.annotation.__name__ if hasattr(param.annotation, '__name__') else 'Any'}>")
            if param_examples:
                examples.append(f"{class_name}(")
                examples.extend(param_examples)
                examples.append(")")

    return "\n".join(examples)

def get_inheritance_tree(classes: List[type]) -> Dict[str, List[str]]:
    """Build inheritance relationships between classes."""
    inheritance_map = {}
    for cls in classes:
        for base in cls.__bases__:
            if base != object and base.__name__ != 'Enum':
                if base.__name__ not in inheritance_map:
                    inheritance_map[base.__name__] = []
                inheritance_map[base.__name__].append(cls.__name__)
    return inheritance_map

def generate_class_groups(classes: List[type]) -> Dict[str, List[str]]:
    """Group classes by their primary functionality."""
    groups = {
        "Resources": [],
        "Equipment": [],
        "Actions": [],
        "Production": [],
        "Logistics": [],
        "Other": []
    }
    
    for cls in classes:
        name = cls.__name__
        if name.endswith(('Resource', 'Part', 'Product')):
            groups["Resources"].append(name)
        elif name.endswith(('Machine', 'WorkStation', 'Conveyor', 'RoboticArm', 'Tool', 'Equipment')):
            groups["Equipment"].append(name)
        elif name.startswith(('Action', 'Actor')):
            groups["Actions"].append(name)
        elif name in ['Job', 'Route', 'ProductionState', 'Requirement']:
            groups["Production"].append(name)
        elif name in ['Location', 'Vehicle', 'Inventory']:
            groups["Logistics"].append(name)
        else:
            groups["Other"].append(name)
    
    # Remove empty groups
    return {k: v for k, v in groups.items() if v}

def generate_mermaid_class_diagram(inheritance_map: Dict[str, List[str]], groups: Dict[str, List[str]]) -> str:
    """Generate a Mermaid class diagram showing inheritance and grouping."""
    mermaid_parts = [
        "```mermaid",
        "classDiagram",
        "    %% Class definitions with grouping"
    ]
    
    # Add class definitions with subgraphs
    for group, classes in groups.items():
        mermaid_parts.append(f"    %% {group} group")
        for cls in classes:
            mermaid_parts.append(f"    class {cls}")
    
    # Add inheritance relationships
    for base, derived in inheritance_map.items():
        for child in derived:
            mermaid_parts.append(f"    {base} <|-- {child}")
    
    mermaid_parts.append("```\n")
    return '\n'.join(mermaid_parts)

def generate_index_content(enum_classes: List[type], regular_classes: List[type]) -> str:
    """Generate the complete index.md content with overview."""
    # Start with title and introduction
    content = [
        "# Python Reference\n",
        "## Overview\n",
        "The Open Manufacturing Model provides a general and comprehensive framework for modeling manufacturing operations.  ",
        "Below is an overview of the main components and their relationships.\n",
        
        "## Python implementation\n",
        "This section describes the core components of the Open Manufacturing Model together with a Python implementation. We deploy object-oriented programming where we implement the core components using Python `classes`.\n",
        
        ":::tip\n",
        "The Python implementation should be viewed as a *reference architecture*, not as a full Python library able to model, simulate, or control a manufacturing system. At least, not *yet*. We provide starting points for the `attributes` and `methods` of each Python `class` and provide examples on how to create instances of all classes, including their relationships with other classes.\n",
        
        "To exemplify that this reference implementation is not a all-in-one solution *yet*, please see the following example. When calling the `start_job` method of the `Job`, the only thing that changes are the attributes `status` and `start_date`. Nothing more and nothing.\n",
        
        "```python",
        "    # Create Job instance",
        "    job = Job(name=\"An example Job\")",
        "",
        "    print(job.status)       # 'idle' ",
        "    print(job.start_date)   # 'None'",
        "",
        "    # Start job",
        "    job.start_job()",
        "",
        "    print(job.status)       # 'in_progress' ",
        "    print(job.start_date)   # 'datetime.now()'",
        "```",
        ":::\n"

        "### Class Architecture\n",
        "The following diagram shows the main classes and their inheritance relationships:\n",
    ]
    
    # Generate inheritance tree and class groups
    inheritance_map = get_inheritance_tree(regular_classes)
    groups = generate_class_groups(regular_classes)
    
    # Add class diagram
    content.append(generate_mermaid_class_diagram(inheritance_map, groups))
    
     # Add Classes section
    if regular_classes:
        content.extend([
            "\n## Classes\n",
            "These classes form the core components of the Open Manufacturing Model.\n"
        ])
        for cls in sorted(regular_classes, key=lambda x: x.__name__):
            content.append(f"- [{cls.__name__}](./{cls.__name__.lower()}.md)")

    # Add Enumerations section
    if enum_classes:
        content.extend([
            "\n## Enumerations\n",
            "These enumerations define the valid values for various attributes in the system.\n"
        ])
        for enum_class in sorted(enum_classes, key=lambda x: x.__name__):
            content.append(f"- [{enum_class.__name__}](./{enum_class.__name__.lower()}.md)")
    

    
    return '\n'.join(content)

def main():
    # Configure paths
    src_dir = Path("src")
    docs_dir = Path("docs/classes")
    source_file = src_dir / "omm.py"
    
    logger.info(f"Processing source file: {source_file.absolute()}")
    if not source_file.exists():
        logger.error(f"Could not find omm.py at {source_file.absolute()}")
        return
        
    # Create docs directory if it doesn't exist
    docs_dir.mkdir(parents=True, exist_ok=True)
    
    # Load the module
    logger.info("Loading module...")
    module = load_module(str(source_file))
    
    # Get all classes
    classes = get_classes(module)
    logger.info(f"Found classes: {[cls.__name__ for cls in classes]}")
    
    # Sort classes into enums and regular classes
    enum_classes = [cls for cls in classes if issubclass(cls, Enum)]
    regular_classes = [cls for cls in classes if cls not in enum_classes]
    
    # Generate documentation for enums
    for enum_class in enum_classes:
        logger.info(f"\nProcessing enum class: {enum_class.__name__}")
        doc_content = generate_enum_doc(enum_class, source_file)
        doc_file = docs_dir / f"{enum_class.__name__.lower()}.md"
        
        logger.info(f"Writing documentation to: {doc_file}")
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write(doc_content)
        
        logger.info(f"Generated enum documentation for {enum_class.__name__}")
    
    # Generate documentation for regular classes
    for cls in regular_classes:
        doc_content = generate_class_doc(cls)
        doc_file = docs_dir / f"{cls.__name__.lower()}.md"
        
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write(doc_content)
        
        logger.info(f"Generated class documentation for {cls.__name__}")
    
    # Generate index file with overview
    index_content = generate_index_content(enum_classes, regular_classes)
    with open(docs_dir / "index.md", 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    logger.info("Generated API index with class overview")

if __name__ == "__main__":
    main()