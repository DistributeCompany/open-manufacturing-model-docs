---
sidebar_position: 2
---

# Basic 2: Quality Control Station

In this tutorial, we'll set up a quality control station for checking electronic components. This will show you how OMM handles quality inspection and worker assignments.

## What We're Building

We're creating a quality control area where:
- Workers inspect electronic components
- Both visual and functional tests are performed
- Products are marked as passed or defective

## The Key Players

Our quality control system needs:
- A **WorkStation** for testing
- A **Worker** to perform inspections

## Setting Up the Station

First, let's create our testing area:

```python
qc_station = WorkStation(
    name="Electronics QC Station",
    georeference=[1.0, 1.0],
    workstation_type="quality_control",
    capabilities=["visual_inspection", "functional_testing"],
    max_capacity=1
)
```

## Adding Our Inspector

Every quality control station needs skilled workers. Let's create one.

```python
qc_inspector = Worker(
    name="Sarah Johnson",
    roles={
        # This allows our Worker to work on all WorkStations of type quality_control
        "QC Inspector": ["quality_control"]
    }
)

# Verify whether Worker can work with WorkStation
if qc_inspector.can_work_with(qc_station):
    print(f'{qc_inspector.name} can work with {qc_station.name}')
    # Sarah Johnson can work with Electronics QC Station
```

:::note
`Workers` are specialized `Actors` who actively perform tasks. They have specific roles and capabilities that determine what they can do.
:::

## What's Next?
Now that you've completed this quality control tutorial, you understand how to:

* Set up a specialized WorkStation for quality control procedures
* Create Workers with specific roles and permissions
* Verify Worker-WorkStation compatibility using the can_work_with method
* Establish basic quality control capabilities

This foundation will help you explore more advanced concepts like:
* Creating multi-stage quality control processes
* Implementing quality metrics and reporting
* Managing multiple inspectors and shifts

Try extending this example by:

* Adding different types of quality tests (stress testing, safety checks)
* Creating a repair WorkStation for failed items

:::tip
Quality control is a critical part of any manufacturing process. As you build more complex systems, you can use these basic concepts to create comprehensive quality management systems.
:::

