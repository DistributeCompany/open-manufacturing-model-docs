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
- **Actions** for different types of tests
- A system to track inspection results

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

Every quality control station needs skilled workers:

```python
qc_inspector = Worker(
    name="Sarah Johnson",
    roles={
        "QC Inspector": ["visual_inspection", "functional_testing"]
    }
)

qc_station.add_actor(qc_inspector)
```

:::note
Workers are specialized Actors who actively perform tasks. They have specific roles and capabilities that determine what they can do.
:::

