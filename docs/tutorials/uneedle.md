---
sidebar_position: 8
---

# Advanced 2: Medical Device Manufacturing (U-Needle)

This tutorial models a highly regulated cleanroom manufacturing facility with multiple cleanliness zones, strict environmental controls, and comprehensive process validation. This tutorial is inspired by one of the partners of NXTGEN High Tech Factory 2030: [U-Needle](https://www.uneedle.com/)

## What We're Building

We're creating a state-of-the-art cleanroom facility that:
- Uses different cleanliness zones (ISO 7 and ISO 5)
- Implements environmental monitoring and contamination control
- Tracks worker certifications and access rights

Think of this as a complete medical device manufacturing facility where different zones, systems, and controls work together seamlessly to produce medical devices under strict regulatory requirements. We'll set up everything from material handling through airlocks to final inspection, with validated processes throughout.

## Set Up the Manufacturing Facility

First, let's create our cleanroom facility and its cleanliness zones:

```python
cleanroom_facility = Location(
    name="Medical Device Facility",
    georeference=[52.23767045493833, 6.848023899076972],
    location_type=LocationType.INTERNAL,
    constraints=[
        Constraint("particle_count", max_value=10000),
        Constraint("pressure_differential", min_value=0.02),
        Constraint("air_changes", min_value=20)
    ]
)

# Create zones with increasing cleanliness requirements
iso_7_zone = Location(
    name="ISO 7 Manufacturing Zone",
    georeference=[1.0, 1.0],
    location_type=LocationType.INTERNAL,
    constraints=[
        Constraint("particle_count", max_value=352000),
        Constraint("temperature", min_value=20, max_value=22),
        Constraint("humidity", min_value=45, max_value=55),
        Constraint("pressure_differential", min_value=0.02)
    ]
)

iso_5_zone = Location(
    name="ISO 5 Assembly Zone",
    georeference=[2.0, 1.0],
    location_type=LocationType.INTERNAL,
    constraints=[
        Constraint("particle_count", max_value=3520),
        Constraint("temperature", min_value=20, max_value=22),
        Constraint("humidity", min_value=45, max_value=55),
        Constraint("pressure_differential", min_value=0.03)
    ]
)
```

## Create Material Transfer System

Set up airlocks and controlled material movement:

```python
entrance_airlock = Location(
    name="Main Airlock",
    georeference=[0.5, 1.0],
    location_type=LocationType.INTERNAL,
    constraints=[
        Constraint("door_interlock", type="exclusive"),
        Constraint("pressure_differential", min_value=0.015),
        Constraint("particle_count", max_value=50000)
    ]
)

material_transfer = Route(
    name="Clean Transfer Route",
    georeference=[[1.0, 1.0], [1.0, 2.0], [2.0, 2.0], [2.0, 1.0]],
    length=4.0,
    constraints=[
        Constraint("route_validation", type="unidirectional"),
        Constraint("cross_contamination", type="prevention")
    ]
)

clean_storage = Storage(
    name="Clean Component Storage",
    georeference=[0.0, 0.0],
    storage_type=StorageType.CLEANROOM,
    max_capacity=500.0,
    constraints=[
        Constraint("particle_count", max_value=352000),
        Constraint("temperature", min_value=20, max_value=22),
        Constraint("humidity", min_value=45, max_value=55)
    ]
)
```

:::tip
Material transfers between different ISO classes must always go through appropriate airlocks with validated cleaning procedures.
:::

## Set Up Manufacturing Equipment

Create precision manufacturing equipment with validation controls:

```python
precision_machine = Machine(
    name="Precision_CNC",
    machine_type="Ultra-Precision CNC",
    georeference=[1.5, 1.0],
    capabilities=[
        "micro_machining",
        "surface_finishing",
        "dimensional_inspection"
    ],
    constraints=[
        Constraint("calibration_interval", max_hours=168),
        Constraint("validation_status", required=True),
        Constraint("environmental_monitoring", active=True)
    ],
    sensors=[
        Sensor("spindle_vibration"),
        Sensor("tool_wear"),
        Sensor("dimensional_accuracy"),
        Sensor("surface_roughness")
    ]
)

inspection_system = Machine(
    name="Vision_System_1",
    machine_type="Vision System",
    georeference=[2.5, 1.0],
    capabilities=[
        "surface_inspection",
        "dimensional_verification",
        "defect_detection"
    ],
    constraints=[
        Constraint("measurement_accuracy", min_value=0.001),
        Constraint("calibration_status", valid=True)
    ],
    sensors=[
        Sensor("camera_calibration"),
        Sensor("lighting_intensity"),
        Sensor("measurement_uncertainty")
    ]
)
```

## Create Worker Roles

Set up workers with appropriate certifications:

```python
cleanroom_operator = Worker(
    name="Cleanroom_Operator_1",
    roles={
        "Production": [
            "cleanroom_operation",
            "gowning_procedure",
            "material_handling"
        ],
        "Quality": [
            "in_process_inspection",
            "documentation",
            "environmental_monitoring"
        ]
    },
    constraints=[
        Constraint("certification_status", valid=True),
        Constraint("medical_clearance", required=True),
        Constraint("gowning_qualification", level=2)
    ]
)

quality_specialist = Worker(
    name="Quality_Specialist_1",
    roles={
        "Quality": [
            "quality_inspection",
            "process_validation",
            "documentation_review"
        ],
        "Compliance": [
            "regulatory_compliance",
            "audit_support"
        ]
    },
    constraints=[
        Constraint("certification_status", valid=True),
        Constraint("cleanroom_certification", level=3)
    ]
)

# Associate workers with zones
iso_7_zone.add_actor(cleanroom_operator)
iso_5_zone.add_actor(quality_specialist)
```

## Define Manufacturing Process

Create actions for medical device manufacturing:

```python
material_prep = Action(
    name="Material Preparation",
    action_type=ActionType.PREPARATION,
    sequence_nr=1,
    location=entrance_airlock,
    requirements=[
        Requirement(RequirementType.WORKER, ["cleanroom_operation"]),
        Requirement(RequirementType.CERTIFICATION, ["gowning_level_2"])
    ]
)

machining_action = Action(
    name="Precision Machining",
    action_type=ActionType.MANUFACTURING,
    sequence_nr=2,
    location=precision_machine,
    requirements=[
        Requirement(RequirementType.WORKER, ["Production"]),
        Requirement(RequirementType.MACHINE, ["Precision_CNC"]),
        Requirement(RequirementType.VALIDATION, ["process_validation"])
    ]
)

inspection_action = Action(
    name="Quality Inspection",
    action_type=ActionType.QUALITY_CHECK,
    sequence_nr=3,
    location=inspection_system,
    requirements=[
        Requirement(RequirementType.WORKER, ["Quality"]),
        Requirement(RequirementType.MACHINE, ["Vision_System"]),
        Requirement(RequirementType.DOCUMENTATION, ["inspection_record"])
    ]
)
```

## Set Up Process Monitoring

Create monitoring functions:

```python
def monitor_cleanroom_status():
    """Monitor cleanroom environmental conditions."""
    conditions = {
        'iso_7': [sensor.get_reading() for sensor in iso_7_zone.sensors],
        'iso_5': [sensor.get_reading() for sensor in iso_5_zone.sensors],
        'airlock': [sensor.get_reading() for sensor in entrance_airlock.sensors]
    }
    
    equipment = {
        'cnc': precision_machine.status,
        'vision': inspection_system.status
    }
    
    compliance = {
        'particle_counts': check_particle_counts(),
        'pressure_differentials': check_pressure_differentials(),
        'temperature_humidity': check_environmental_conditions()
    }
    
    return conditions, equipment, compliance

def validate_process(process_id: str, measurements: Dict):
    """Validate process parameters against specifications."""
    validation_point = ValidationPoint(
        name=f"Process_{process_id}",
        parameters={
            "temperature": (20, 22, "C"),
            "humidity": (45, 55, "%"),
            "particle_count": (0, 3520, "particles/m3")
        }
    )
    
    return validation_point.check_parameters(measurements)
```

## Create Production Job

Finally, let's create a job to manufacture a medical device:

```python
medical_device = Product(
    name="Medical Device Type A",
    production_state=ProductionState.NEW,
    due_date=datetime.now() + timedelta(days=1),
    constraints=[
        Constraint("cleanliness_class", value="ISO_5"),
        Constraint("sterilization", required=True)
    ]
)

# Add actions to product
medical_device.add_action(material_prep)
medical_device.add_action(machining_action)
medical_device.add_action(inspection_action)

# Create manufacturing job
production_job = Job(
    products=[medical_device],
    priority=JobPriority.HIGH,
    constraints=[
        Constraint("validation_required", True),
        Constraint("documentation_required", True)
    ]
)

# Start production
production_job.start_job()
```

:::note
Medical device manufacturing requires complete traceability. Every job must maintain detailed records of environmental conditions, operator actions, and process parameters.
:::

## What's Next?

Now that you've seen how to create a medical device manufacturing facility with OMM, try extending this example with:

- Implementation of electronic batch records
- Integration with quality management systems
- Advanced environmental monitoring and alerting