# Python Reference

## Overview

The Open Manufacturing Model provides a general and comprehensive framework for modeling manufacturing operations.  
Below is an overview of the main components and their relationships.

## Python implementation

This section describes the core components of the Open Manufacturing Model together with a Python implementation. We deploy object-oriented programming where we implement the core components using Python `classes`.

:::tip

The Python implementation should be viewed as a *reference architecture*, not as a full Python library able to model, simulate, or control a manufacturing system. At least, not *yet*. We provide starting points for the `attributes` and `methods` of each Python `class` and provide examples on how to create instances of all classes, including their relationships with other classes.

To exemplify that this reference implementation is not a all-in-one solution *yet*, please see the following example. When calling the `start_job` method of the `Job`, the only thing that changes are the attributes `status` and `start_date`. Nothing more and nothing less.

```python
    # Create Job instance
    job = Job(name="An example Job")

    print(job.status)       # 'idle' 
    print(job.start_date)   # 'None'

    # Start job
    job.start_job()

    print(job.status)       # 'in_progress' 
    print(job.start_date)   # 'datetime.now()'
```
:::
### Class Architecture

The following diagram shows the main classes and their inheritance relationships:

```mermaid
classDiagram
    %% Class definitions with grouping
    %% Resources group
    class Part
    class Product
    class Resource
    %% Equipment group
    class Conveyor
    class Machine
    class RoboticArm
    class Tool
    class WorkStation
    %% Actions group
    class Action
    class Actor
    %% Production group
    class Job
    class Requirement
    class Route
    %% Logistics group
    class Location
    class Vehicle
    %% Other group
    class Constraint
    class Sensor
    class Storage
    class Worker
    Resource <|-- Conveyor
    Resource <|-- Machine
    Resource <|-- RoboticArm
    Resource <|-- Tool
    Resource <|-- Vehicle
    Resource <|-- WorkStation
    Location <|-- Storage
    Actor <|-- Worker
```


## Classes

These classes form the core components of the Open Manufacturing Model.

- [Action](./action.md)
- [Actor](./actor.md)
- [Constraint](./constraint.md)
- [Conveyor](./conveyor.md)
- [Job](./job.md)
- [Location](./location.md)
- [Machine](./machine.md)
- [Part](./part.md)
- [Product](./product.md)
- [Requirement](./requirement.md)
- [Resource](./resource.md)
- [RoboticArm](./roboticarm.md)
- [Route](./route.md)
- [Sensor](./sensor.md)
- [Storage](./storage.md)
- [Tool](./tool.md)
- [Vehicle](./vehicle.md)
- [WorkStation](./workstation.md)
- [Worker](./worker.md)

## Enumerations

These enumerations define the valid values for various attributes in the system.

- [ActionStatus](./actionstatus.md)
- [ActionType](./actiontype.md)
- [JobPriority](./jobpriority.md)
- [JobStatus](./jobstatus.md)
- [LocationType](./locationtype.md)
- [PartType](./parttype.md)
- [ProductionState](./productionstate.md)
- [RequirementType](./requirementtype.md)
- [ResourceStatus](./resourcestatus.md)
- [ResourceType](./resourcetype.md)
- [StorageType](./storagetype.md)
- [VehicleType](./vehicletype.md)