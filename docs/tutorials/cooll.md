---
sidebar_position: 7
---

# Advanced 1: Thermal Heat Pump Manufacturing (Cooll)

This tutorial models a complex manufacturing facility with multiple production lines, automated material handling, detailed monitoring, and sophisticated resource management. This tutorial is inspired by one of the partners of NXTGEN High Tech Factory 2030: [Cooll](https://cooll.com/)

## What We're Building

We're creating a sophisticated manufacturing facility that:
- Uses automated material handling with AGVs and conveyors
- Implements environmental monitoring and controls
- Tracks detailed worker authorizations
- Monitors production in real-time

Think of this as a complete factory where different components and systems work together seamlessly to produce thermal heat pumps. We'll set up everything from the initial material storage to final testing, with automated systems moving materials between stations.

## Set Up the Manufacturing Facility

First, let's create our main facility and its internal zones:

```python
main_facility = Location(
    name="Heat Pump Factory",
    georeference=[52.2376489846171, 6.847945014035459],
    location_type=LocationType.INTERNAL
)

# Create internal zones
assembly_zone = Location(
    name="Assembly Zone",
    georeference=[1.0, 1.0],
    location_type=LocationType.INTERNAL
)

testing_zone = Location(
    name="Testing Zone",
    georeference=[2.0, 1.0],
    location_type=LocationType.INTERNAL
)
```

## Create Storage Systems

Next, we'll set up our storage areas with environmental controls:

```python
component_storage = Storage(
    name="Component Warehouse",
    georeference=[0.0, 0.0],
    storage_type=StorageType.WAREHOUSE,
    max_capacity=1000.0,
    constraints=[
        Constraint("temperature", min_value=18, max_value=24),
        Constraint("humidity", min_value=40, max_value=60)
    ]
)

finished_goods = Storage(
    name="Finished Products",
    georeference=[10.0, 0.0],
    storage_type=StorageType.WAREHOUSE,
    max_capacity=50.0
)
```

:::tip
Storage areas need different environmental controls based on the materials they hold. Use Constraints to enforce these requirements.
:::

## Set Up Material Handling

Create an automated material handling network:

```python
# Main conveyor system
main_conveyor = Conveyor(
    name="Assembly to Testing Conveyor",
    georeference=[[1.0, 1.0], [2.0, 2.0]],
    speed=0.2,
    capacity=10.0,
    direction="forward",
    sensors=[
        Sensor("speed"),
        Sensor("load"),
        Sensor("position")
    ]
)

# Create AGV for flexible material movement
agv = Vehicle(
    name="AGV_1",
    vehicle_type=VehicleType.AUTOMATED_MOBILE_ROBOT,
    georeference=[0.0, 0.0],
    average_speed=1.5,
    load_capacities={"weight": 250.0},
    sensors=[
        Sensor("battery"),
        Sensor("position"),
        Sensor("obstacle_detection")
    ]
)
```

## Define Material Routes

Create routes for material movement that the AGV can use:

```python
storage_to_assembly = Route(
    name="Storage to Assembly",
    georeference=[[0.0, 0.0], [5.0, 0.0], [5.0, 2.0]],
    origin=component_storage,
    destination=assembly_zone,
    length=7.0,
    constraints=[
        Constraint("path_clearance", min_value=2.0),
        Constraint("speed_limit", max_value=1.0)
    ]
)

assembly_to_testing = Route(
    name="Assembly to Testing",
    georeference=[[5.0, 2.0], [5.0, 5.0], [8.0, 5.0]],
    origin=assembly_zone,
    destination=testing_zone
    length=6.0
)
```

## Set Up Production Resources

Create our manufacturing resources with detailed capabilities:

```python
assembly_robot = RoboticArm(
    name="Assembly_Robot_1",
    arm_type="6-Axis Industrial Robot",
    reach=2.5,
    payload=100.0,
    degrees_of_freedom=6,
    end_effector_type="Multi-Tool",
    constraints=[
        Constraint("workspace_boundary", shape="cylinder", radius=2.5, height=3.0),
        Constraint("collision_avoidance", min_distance=0.5)
    ],
    sensors=[
        Sensor("joint_position"),
        Sensor("force_torque"),
        Sensor("tool_temperature")
    ],
    location=assembly_zone
)

test_station = WorkStation(
    name="Test_Station_1",
    workstation_type="quality_control",
    capabilities=[
        "pressure_test",
        "performance_test",
        "leak_detection"
    ],
    constraints=[
        Constraint("air_pressure", min_value=6.0, max_value=8.0),
        Constraint("temperature", min_value=20, max_value=22)
    ],
    sensors=[
        Sensor("pressure"),
        Sensor("temperature"),
        Sensor("flow_rate")
    ],
    location=testing_zone
)
```

## Create Worker Roles

Set up workers with different authorization levels:

```python
senior_tech = Worker(
    name="Senior Technician",
    roles={
        "Assembly": ["robot_operation", "quality_control"],
        "Maintenance": ["robot_repair", "preventive_maintenance"],
        "Supervision": ["process_approval", "team_leadership"]
    }
)

quality_inspector = Worker(
    name="Quality Inspector",
    roles={
        "Quality": ["testing", "certification", "documentation"],
        "Process": ["calibration", "data_analysis"]
    }
)

# Associate workers with resources
assembly_robot.add_actor(senior_tech)
test_station.add_actor(quality_inspector)
```

## Define Manufacturing Process

Create actions for heat pump assembly:

```python
# An AGV retreives a heat exchanger from storage. 
prep_action = Action(
    name="Retreive Components",
    action_type=ActionType.MOVE,
    sequence_nr=1,
    origin=component_storage,
    destination=asssembly_zone
    requirements=[
        Requirement(RequirementType.PART, ["Heat Exchanger", 1]),
        Requirement(RequirementType.VEHICLE, ["AGV"])
    ]
)

# A robotic arm does some assembly, and requires a worker to monitor the arm and use a torque wrench.  
assembly_action = Action(
    name="Robot Assembly",
    action_type=ActionType.ASSEMBLY,
    sequence_nr=2,
    location=assembly_robot,
    requirements=[
        Requirement(RequirementType.WORKER, ["Assembly"]),
        Requirement(RequirementType.TOOL, ["Torque_Wrench"])
    ]
)

assembly_to_test_action = Action(
    name="Move heat pump from assembly to testing",
    action_type=ActionType.MOVE,
    sequence_nr=3,
    origin=assembly_zone,
    destination=testing_zone,
    requirements=[
        Requirement(RequirementType.CONVEYOR, []) # Any type of Conveyor. We also could have used the AGV
    ]

)
test_action = Action(
    name="Performance Testing",
    action_type=ActionType.QUALITY_CHECK,
    sequence_nr=4,
    location=test_station,
    requirements=[
        Requirement(RequirementType.WORKER, ["Quality"]),
        Requirement(RequirementType.MACHINE, ["Test_Station"])
    ]
)
```

## Set Up Production Monitoring

Create monitoring functions:

```python
def monitor_production_status():
    """Monitor overall production status."""
    # Check resource utilization
    resources = {
        'robot': assembly_robot.status,
        'agv': agv.status,
        'test_station': test_station.status,
        'conveyor': main_conveyor.status
    }
    
    # Monitor environmental conditions
    environment = {
        'assembly': [sensor.get_reading() for sensor in assembly_zone.sensors],
        'testing': [sensor.get_reading() for sensor in testing_zone.sensors],
        'storage': [sensor.get_reading() for sensor in component_storage.sensors]
    }
    
    # Track material movements
    materials = {
        'incoming': component_storage.entries,
        'outgoing': component_storage.exits
    }
    
    return resources, environment, materials

def check_worker_assignments(job: Job):
    """Monitor worker assignments and authorizations."""
    assignments = {
        worker.name: [
            action.name for action in job.actions 
            if action.worker == worker and 
            action.status == ActionStatus.IN_PROGRESS
        ]
        for worker in [senior_tech, quality_inspector]
    }
    return assignments
```

## Create Production Job

Finally, let's create a job to manufacture a heat pump:

```python
heat_pump = Product(
    name="Thermal Heat Pump Model A",
    volume=1.5,
    production_state=ProductionState.NEW,
    due_date=datetime.now() + timedelta(days=2)
)

# Add actions to product
heat_pump.add_action(prep_action)
heat_pump.add_action(assembly_action)
heat_pump.add_action(assembly_to_test_action)
heat_pump.add_action(test_action)

# Create manufacturing job
production_job = Job(
    products=[heat_pump],
    priority=JobPriority.HIGH,
)

# Start production
production_job.start_job()
```

:::note
We did not set the `customer` attribute of the `Job`. Hence, it could be interpreted as  *make-to-stock*.
:::

## What's Next?

Now that you've seen how to create a heat pump manufacturing facility with OMM, try extending this example with:

- Conveyor speed control to avoid clogging
- Advanced AGV fleet management and routing optimization
- Predictive maintenance systems using sensor data
- Energy consumption monitoring and optimization
- Integration with supplier inventory systems for just-in-time delivery
