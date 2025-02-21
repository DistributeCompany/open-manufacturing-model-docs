---
sidebar_position: 7
---

# Advanced 1: Thermal Heat Pump Manufacturing

Let's model a complex manufacturing facility that produces thermal heat pumps. This example shows how OMM handles sophisticated manufacturing processes with multiple stages and strict quality requirements. This tutorial is inspired by one of NXTGEN High Tech's partners: [Cooll](https://cooll.com/).

## What We're Building

We're creating a system that:
- Manages multiple production lines
- Coordinates automated and manual processes
- Handles complex assemblies
- Implements quality control at multiple stages
- Manages material flow and storage
- Tracks maintenance schedules

## Setting Up the Production Line

First, let's create our main manufacturing resources:

```python
welding_robot = RoboticArm(
    name="Welding Robot 1",
    georeference=[1.0, 1.0],
    arm_type="6-Axis Industrial Robot",
    reach=2.5,
    payload=50.0,
    degrees_of_freedom=6,
    end_effector_type="Welding Torch",
    sensors=[
        Sensor("temperature"),
        Sensor("position"),
        Sensor("weld_quality")
    ]
)

assembly_line = Conveyor(
    name="Main Assembly Line",
    georeference=[[0.0, 0.0], [20.0, 0.0]],
    speed=0.1,  # meters per second
    capacity=5.0,  # units per meter
    direction="forward",
    sensors=[
        Sensor("speed"),
        Sensor("load"),
        Sensor("temperature")
    ]
)

testing_station = WorkStation(
    name="Final Testing Station",
    georeference=[25.0, 0.0],
    workstation_type="quality_control",
    capabilities=["pressure_test", "performance_test"],
    sensors=[
        Sensor("pressure"),
        Sensor("temperature"),
        Sensor("flow_rate")
    ]
)
```

## Managing Complex Assembly

Create the product structure:

```python
heat_pump = Product(
    name="Thermal Heat Pump Model A",
    volume=1.5,
    production_state=ProductionState.NEW,
    due_date=datetime.now() + timedelta(days=2)
)

components = [
    Part(
        name="Heat Exchanger",
        quantity=1,
        volume=0.3,
        state=ProductionState.NEW,
        part_type=PartType.PURCHASED_COMPONENT,
        cost=500.00,
        min_stock_level=5
    ),
    Part(
        name="Compressor",
        quantity=1,
        volume=0.2,
        state=ProductionState.NEW,
        part_type=PartType.PURCHASED_COMPONENT,
        cost=300.00,
        min_stock_level=5
    )
]

# Create assembly actions
weld_action = Action(
    name="Weld Heat Exchanger",
    action_type=ActionType.WELDING,
    description="Weld heat exchanger connections",
    duration=0.5,  # 30 minutes
    sequence_nr=1,
    location=welding_robot
)

test_action = Action(
    name="Pressure Test",
    action_type=ActionType.QUALITY_CHECK,
    description="Perform pressure and leak tests",
    duration=1.0,  # 1 hour
    sequence_nr=2,
    location=testing_station
)
```