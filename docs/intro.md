---
sidebar_position: 1
---

# Introduction to Open Manufacturing Model (OMM)

Welcome to the Open Manufacturing Model (OMM) documentation! OMM is a standardized data model designed to facilitate communication within and between manufacturing systems. It provides a lightweight, flexible framework for representing manufacturing entities, processes, and relationships. OMM also provides a standardized approach to model manufacturing systems for Digital Twins, as exemplified by our object-oriented reference implementation in Python.

## What is OMM?

The Open Manufacturing Model (OMM) is a data modeling framework that enables:

- Standardized representation of manufacturing entities and processes
- Easy integration of different manufacturing components
- Enables full transparancy and traceability of the manufacturing system
- Foundation for building Digital Models, Digital Shadows, and Digital Twins.
- Lightweight and flexible implementation

Heavily inspired by the [Open Trip Model](https://www.opentripmodel.org/) used in logistics, OMM adapts similar principles to address the specific needs of manufacturing systems.

## Core Concepts

OMM is built around several key concepts that represent different aspects of a manufacturing system:

### Physical Entities
- **Resources**: Physical assets used in manufacturing (machines, tools, vehicles)
- **Locations**: Physical spaces where manufacturing activities occur
- **Products**: Items being manufactured
- **Parts**: Components and materials used in manufacturing

### Operational Entities
- **Actions**: Manufacturing operations and processes
- **Jobs**: Scheduled manufacturing tasks
- **Workers**: Human operators and technicians
- **Routes**: Paths for material and resource movement

For further details on the entities in OMM, please see [OMM in 5 Minutes](/docs/getting_started.md).

For technical details about specific components, refer to the [Python Reference](/docs/classes/index.md) section.

## Getting Started

To start using OMM in modeling, simulating, or controling your manufacturing system:

1. **Understand the Model**: Review the documentation to understand OMM's core concepts
2. **Identify Components**: Map your manufacturing system's components to OMM entities
3. **Implement Classes**: Use the provided Python implementation or create your own
4. **Define Relationships**: Establish connections between different entities
5. **Monitor States**: Track and update entity states through data-exchange with the (simulated) manufacturing system

## Python Implementation

OMM includes a [Python Reference Implementation](/docs/classes/index.md) that demonstrates how to implement the model:

```python
# Create a manufacturing location
manufacturing_site = Location(
    name="Fraunhofer Innovation Platform at the University of Twente",
    georeference=[52.23766202998197, 6.848024162213785],
    location_type=LocationType.EXTERNAL
)

# Create a manufacturing resource
printer = Machine(
    name='Bambu_X1C_01',
    machine_type='Bambu Lab X1C 3D Printer',
    georeference=[10.0, 20.0, 0.0], # internal coordinates
    capabilities=[
        'multi_material_printing',
        'abs_printing',
        'pla_printing',
        'petg_printing'
    ],
    sensors=[
        Sensor('nozzle_temperature'),
        Sensor('bed_temperature'),
        Sensor('chamber_temperature'),
        Sensor('filament_flow')
    ]
)

# Define a manufacturing action
print_action = Action(
    name='Print Pikachu',
    action_type=ActionType.PROCESS,
    description='3D print miniature Pikachu with multiple colors',
    duration=8.0,  # 8 hours estimated print time
    sequence_nr=1,
    location=printer # location where action is performed
)
```

## Benefits of Using OMM

- **Standardization**: Common language for describing manufacturing systems
- **Interoperability**: Easy integration between different systems
- **Flexibility**: Adaptable to various manufacturing scenarios
- **Digital Twin Ready**: Reference implementation in Python to model or simulate real-world systems
- **Maintainability**: Clear structure and relationships
- **Scalability**: Can represent both simple and complex systems

## Learn by Example
[Various tutorials](/docs/category/tutorials/) are provided to learn how to use OMM.

## Next Steps

The Open Manufacturing Model, the accompying Python implementation, and this documentation is still very much under active development. If you want to be involved, please contact [Berry Gerrits](mailto::b.gerrits@distribute.company).

Moreover, to fully appreciate the standardized data model of OMM, a standardized API based on OMM should be developed. This is currently not yet available. A first hint on how a (json-formatted) response of a `Get` request could look like, is demonstrated in the `to_dict` methods of the various classes in the [Python Reference Implementation](/docs/classes/index.md). 



## Acknowledgments 

The Open Manufacturing Model is being developed by [dr. ir. Berry Gerrits](https://nl.linkedin.com/in/berry-gerrits). The development of OMM is part of the [NXTGEN Hightech](https://nxtgenhightech.nl/) Growth Fund, financed by the Dutch Government. More specially, the Open Manufacturing Model is the result of activities carred out in the **Smart Industry 02 Autonomous Factory - Industrieel Cluster Oost**. Or for brevity, **Factory2030**. 