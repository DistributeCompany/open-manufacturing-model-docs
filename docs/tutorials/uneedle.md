---
sidebar_position: 8
---

# Advanced 2: Medical Device Manufacturing

This tutorial demonstrates advanced OMM features for highly regulated manufacturing with complex routing, strict environmental controls, and detailed process validation. It is inspired by one of the partners of NXTGEN High Tech Factory 2030: [U-Needle](https://www.uneedle.com/)

## What We're Building

We're creating a state-of-the-art cleanroom facility that:
- Maintains different cleanliness zones (ISO 7 and ISO 5)
- Controls contamination through airlocks and material transfers
- Tracks worker certifications and access rights
- Validates processes in real-time
- Monitors environmental conditions continuously
- Ensures regulatory compliance
- Manages product serialization and traceability

This facility represents a highly controlled manufacturing environment where medical devices can be produced under strict regulatory requirements. Every aspect of the operation, from worker access to material movement, is carefully monitored and controlled.

## Create the Cleanroom Facility

First, let's set up our cleanroom with different cleanliness zones:

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

## Create Airlocks and Material Transfer

Set up controlled material movement between zones:

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
```

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

## Create Certified Workers

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
```

## Implement Process Validation

Create validation checkpoints:

```python
class ValidationPoint:
    def __init__(self, name: str, parameters: Dict[str, tuple]):
        self.name = name
        self.parameters = parameters  # parameter: (min, max, unit)
        self.measurements = []
    
    def check_parameters(self, measurements: Dict[str, float]) -> bool:
        """Verify measurements against parameters."""
        for param, value in measurements.items():
            min_val, max_val, _ = self.parameters[param]
            if not min_val <= value <= max_val:
                return False
        return True
    
    def record_measurement(self, measurements: Dict[str, float]) -> None:
        """Record a set of measurements."""
        self.measurements.append({
            'timestamp': datetime.now(),