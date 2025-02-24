---
sidebar_position: 6
---

# Intermediate 3: Custom Guitar Workshop

Welcome to our custom guitar workshop tutorial. Here we'll explore how OMM can help manage a workshop that creates customized guitars. This example shows how to handle both automated and hand-crafted manufacturing processes.

## What We're Building

We're creating a system that:
- Takes custom guitar orders with specific requirements
- Manages wood selection and aging
- Coordinates both machine work and hand crafting
- Tracks quality at every stage
- Handles final setup and testing
- Manages specialized workers and their skills

## The Components We Need

Our guitar workshop needs:
- **Storage** for wood and materials
- **Machines** for precision cutting and shaping
- **WorkStations** for hand crafting
- **Workers** with different skills
- **Quality Control** stations
- **Products** (different guitar models)
- **Parts** (woods, hardware, electronics)

## Setting Up the Workshop

Let's create our main work areas first:

```python
# CNC machine for precision cutting
cnc_station = Machine(
    name="CNC Router",
    machine_type="CNC Router",
    georeference=[1.0, 1.0],
    capabilities=[
        "neck_cutting",
        "body_routing",
        "fret_slots",
        "inlay_routing"
    ],
    sensors=[
        Sensor("spindle_speed"),
        Sensor("temperature"),
        Sensor("tool_wear")
    ]
)

# Workbench for hand crafting
luthier_bench = WorkStation(
    name="Luthier Workbench 1",
    georeference=[2.0, 1.0],
    workstation_type="crafting",
    capabilities=[
        "body_shaping",
        "neck_carving",
        "fret_installation",
        "setup_adjustment",
        "finish_work"
    ],
    max_capacity=1  # One guitar at a time
)

# Final setup and testing area
setup_station = WorkStation(
    name="Setup and Testing",
    georeference=[3.0, 1.0],
    workstation_type="quality_control",
    capabilities=[
        "string_setup",
        "action_adjustment",
        "electronics_testing",
        "playability_testing"
    ],
    max_capacity=2
)
```

## Managing Materials

Set up storage for our precious woods and parts:

```python
wood_storage = Storage(
    name="Wood Storage Room",
    georeference=[0.0, 0.0],
    storage_type=StorageType.WAREHOUSE,
    max_capacity=100.0,  # cubic meters
    constraints=[
        Constraint("humidity", min_value=45, max_value=55),
        Constraint("temperature", min_value=20, max_value=22)
    ]
)

hardware_storage = Storage(
    name="Hardware and Electronics",
    georeference=[0.0, 2.0],
    storage_type=StorageType.RACK,
    max_capacity=20.0
)

# Define our materials
materials = [
    Part(
        name="Mahogany Body Blank",
        quantity=6,
        volume=0.02,
        state=ProductionState.RAW,
        part_type=PartType.RAW_MATERIAL,
        cost=200.00,
        min_stock_level=3
    ),
    Part(
        name="Maple Neck Blank",
        quantity=10,
        volume=0.01,
        state=ProductionState.RAW,
        part_type=PartType.RAW_MATERIAL,
        cost=150.00,
        min_stock_level=5
    ),
    Part(
        name="Rosewood Fretboard",
        quantity=8,
        volume=0.005,
        state=ProductionState.RAW,
        part_type=PartType.RAW_MATERIAL,
        cost=80.00,
        min_stock_level=4
    ),
    Part(
        name="Humbucker Pickup Set",
        quantity=15,
        volume=0.001,
        state=ProductionState.NEW,
        part_type=PartType.PURCHASED_COMPONENT,
        cost=120.00,
        min_stock_level=5
    )
]

for material in materials:
    if material.name.startswith(("Maple", "Rosewood")):
        wood_storage.add_item(material)
    else:
        hardware_storage.add_item(material)
```

## Creating Skilled Workers

Define our craftspeople and their skills:

```python
master_luthier = Worker(
    name="Stef Klomp",
    roles={
        "Master Luthier": [
            "neck_carving",
            "fret_work",
            "final_setup",
            "quality_inspection"
        ]
    }
)

cnc_operator = Worker(
    name="Teun",
    roles={
        "CNC Operator": [
            "cnc_programming",
            "tool_setup",
            "precision_machining"
        ]
    }
)
```

## Defining the Manufacturing Process

Create actions for building a custom guitar:

```python
# Body shaping and routing
body_shaping = Action(
    name="CNC Body Shaping",
    action_type=ActionType.MACHINING,
    description="Cut and shape guitar body from blank, route pickup cavities",
    duration=2.0,  # 2 hours
    sequence_nr=1,  # Make this first
    location=cnc_station,
    worker=cnc_operator,
    requirements=[
        Requirement("Part", ["Mahogany Body Blank", 1]),
        Requirement("Tool", ["Body Template", 1])
    ]
)

# CNC cutting of neck profile
neck_cutting = Action(
    name="CNC Neck Profile",
    action_type=ActionType.MACHINING,
    description="Cut basic neck profile and fret slots",
    duration=1.0,  # 1 hour
    sequence_nr=2,
    location=cnc_station,
    worker=cnc_operator
)

# Hand carving of neck
neck_carving = Action(
    name="Hand Carve Neck",
    action_type=ActionType.PROCESS,
    description="Fine carving and shaping of neck profile",
    duration=3.0,  # 3 hours
    sequence_nr=3,
    location=luthier_bench,
    worker=master_luthier
)

# Final setup
final_setup = Action(
    name="Final Setup",
    action_type=ActionType.ASSEMBLY,
    description="String installation and playing adjustment",
    duration=2.0,  # 2 hours
    sequence_nr=4,
    location=setup_station,
    worker=master_luthier
)

# Quality check
quality_check = Action(
    name="Quality Check",
    action_type=ActionType.QUALITY_CHECK,
    description="Final inspection and playability test",
    duration=1.0,  # 1 hour
    sequence_nr=5,
    location=setup_station,
    worker=master_luthier
)
```

## Creating a Custom Guitar Order

Handle a customer's order:

```python
custom_guitar = Product(
    name="Custom Electric Guitar #2025-001",
    volume=0.1,
    production_state=ProductionState.NEW,
    due_date=datetime.now() + timedelta(days=30)
)

# Add our actions to the product
custom_guitar.add_action(body_shaping) 
custom_guitar.add_action(neck_cutting)
custom_guitar.add_action(neck_carving)
custom_guitar.add_action(final_setup)
custom_guitar.add_action(quality_check)

# Create the manufacturing job
guitar_job = Job(
    products=[custom_guitar],
    priority=JobPriority.MEDIUM,
    customer=customer
)
```

:::tip
Custom guitar building requires careful tracking of materials, especially wood. Use the Storage constraints to maintain proper environmental conditions for wood storage.
:::

## Monitoring Build Progress

Track the guitar's progress through the workshop:

```python
def check_build_progress(job: Job) -> None:
    """Monitor the progress of a guitar build."""
    print(f"Guitar build progress: {job.get_progress()}%")
    current_action = None
    for action in job.actions:
        if action.status == ActionStatus.IN_PROGRESS:
            current_action = action
            break
    
    if current_action:
        print(f"Current stage: {current_action.name}")
        print(f"Being worked on by: {current_action.worker.name}")
        print(f"Location: {current_action.location.name}")
```

:::note
Quality checks are crucial at every stage of guitar building. Use Action status updates to ensure each step meets quality standards before proceeding.
:::

## What's Next?
Now that you've seen how to create a guitar workshop with OMM, try extending this example with:
- Multiple guitar models
- Different wood combinations
- Custom hardware options
- Finish selection and application
- Production schedule optimization
- Worker skill tracking