---
sidebar_position: 8
---

# Advanced 2: Intradermic Needle Manufacturing

Our most complex example models a cleanroom facility producing medical devices. This showcases how OMM handles highly regulated manufacturing with strict environmental and quality requirements. This tutorial is inspired by one of NXTGEN High Tech's partners: [U-Needle](https://www.uneedle.com/).

## What We're Building

We're creating a system that:
- Maintains cleanroom conditions
- Tracks environmental parameters
- Manages sterile processing
- Handles product serialization
- Ensures regulatory compliance
- Controls worker access
- Monitors quality at every stage

## Setting Up the Cleanroom

```python
cleanroom = Location(
    name="ISO 7 Cleanroom",
    georeference=[0.0, 0.0],
    location_type=LocationType.INTERNAL,
    constraints=[
        Constraint("particle_count", max_value=10000),  # particles per m³
        Constraint("temperature", min_value=20, max_value=22),
        Constraint("humidity", min_value=45, max_value=55)
    ]
)

grinding_machine = Machine(
    name="Precision Grinder",
    machine_type="CNC Grinding",
    georeference=[1.0, 1.0],
    location=cleanroom,
    capabilities=["precision_grinding", "surface_finishing"],
    sensors=[
        Sensor("vibration"),
        Sensor("temperature"),
        Sensor("particle_count")
    ]
)

inspection_system = Machine(
    name="Optical Inspection System",
    machine_type="Vision System",
    georeference=[2.0, 1.0],
    location=cleanroom,
    capabilities=["dimensional_inspection", "surface_inspection"],
    sensors=[
        Sensor("camera"),
        Sensor("laser_measurement")
    ]
)
```

## Managing Sterile Processing

```python
needle_batch = Product(
    name="Intradermic Needle Batch A123",
    volume=0.001,
    production_state=ProductionState.NEW,
    due_date=datetime.now() + timedelta(days=1)
)

sterilization_action = Action(
    name="Sterilize Batch",
    action_type=ActionType.PROCESS,
    description="Autoclave sterilization cycle",
    duration=2.0,  # 2 hours
    sequence_nr=1,
    location=sterilization_unit
)

packaging_action = Action(
    name="Sterile Packaging",
    action_type=ActionType.PACKAGING,
    description="Package in sterile barrier system",
    duration=0.5,  # 30 minutes
    sequence_nr=2,
    location=packaging_station
)
```

:::note
Medical device manufacturing requires complete traceability. Use OMM's relationship tracking to maintain a full history of each product's manufacturing process.
:::

## What's Next?

These advanced tutorials demonstrate how OMM can handle complex manufacturing scenarios. Key takeaways:

- Use Sensors to monitor critical parameters
- Implement Constraints for process control
- Create detailed Action sequences
- Track complex product assemblies
- Manage advanced resource capabilities
- Monitor environmental conditions
- Ensure regulatory compliance

Try extending these examples with additional features like:
- Maintenance scheduling
- Quality data analysis
- Resource optimization
- Environmental monitoring
- Regulatory reporting

Remember that OMM is flexible and can be adapted to match your specific manufacturing requirements, no matter how complex they may be.