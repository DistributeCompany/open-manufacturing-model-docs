---
sidebar_position: 1
---

# Basic 1: Toy Car Assembly Line

Welcome to our first tutorial! We'll create a simple assembly line for toy cars. This will show you how different OMM components work together to create a basic manufacturing process.

## What We're Building

Think of this as a small workshop where we:
- Assemble toy cars from parts
- Paint them in different colors
- Get them ready for shipping

## The Components We'll Use

Our toy car assembly line needs:
- **WorkStations** where we'll assemble and paint the cars
- **Parts** like car bodies, wheels, and paint
- **Actions** that define each step in the process
- A **Job** to coordinate everything

## Setting Up Our Assembly Line

Let's start by creating two work areas:

```python
main_assembly = WorkStation(
    name="Main Assembly Station",
    georeference=[1.0, 1.0],
    workstation_type="assembly",
    capabilities=["car_assembly"],
    max_capacity=1
)

decoration_station = WorkStation(
    name="Decoration Station",
    georeference=[2.0, 1.0],
    workstation_type="finishing",
    capabilities=["painting", "detailing"],
    max_capacity=1
)
```

:::tip
Think of WorkStations as dedicated areas where specific tasks happen. Each station has its own purpose and capabilities.
:::

## The Parts We Need

Every toy car needs certain components:

```python
car_parts = [
    Part(
        name="Car Body",
        quantity=50,
        volume=0.001,
        state=ProductionState.NEW,
        part_type=PartType.PURCHASED_COMPONENT,
        cost=2.00,
        min_stock_level=20
    ),
    Part(
        name="Wheels",
        quantity=200,  # We need 4 per car
        volume=0.0002,
        state=ProductionState.NEW,
        part_type=PartType.PURCHASED_COMPONENT,
        cost=0.50,
        min_stock_level=80
    )
]
```

## Creating the Assembly Steps

Now let's define what needs to happen at each station:

```python
assembly_action = Action(
    name="Assemble Car Body",
    action_type=ActionType.ASSEMBLY,
    description="Attach wheels to car body",
    duration=0.25,  # 15 minutes
    sequence_nr=1,
    location=main_assembly
)

# Tell the action what parts it needs
assembly_action.add_requirement("Part", ["Car Body", 1])
assembly_action.add_requirement("Part", ["Wheels", 4])
```

:::tip
Actions are like detailed instructions for each step in the manufacturing process. They specify what needs to happen, where it happens, and what materials are needed.
:::

## Putting It All Together

Finally, we create our product and set up a job to make it:

```python
toy_car = Product(
    name="Red Racing Car",
    volume=0.002,
    production_state=ProductionState.NEW,
    due_date=datetime.now() + timedelta(hours=1)
)

car_job = Job(
    products=[toy_car],
    priority=JobPriority.MEDIUM
)
```

