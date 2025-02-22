---
sidebar_position: 1
---

# Basic 1: Toy Car Assembly Line

Welcome to our first tutorial! We'll create a simple assembly line for toy cars. This will show you how different OMM components work together to create a basic manufacturing process.

## What We're Building

Think of this as a small workshop where we:
- Assemble toy cars from parts
- Get them ready for shipping

## The Components We'll Use

Our toy car assembly line needs:
- **WorkStations** where we'll assemble the cars
- **Parts** like car bodies and wheels
- **Actions** that define each step in the process
- A **Job** to coordinate everything

## Setting Up Our Assembly Line

Our assembly line only consists of one station. Let's start by creating a work area:

```python
main_assembly = WorkStation(
    name="Main Assembly Station",
    georeference=[1.0, 1.0], # A reference to where the WorkStation is in our model/simulation/factory
    workstation_type="assembly",
    capabilities=["car_assembly"],
    max_capacity=2 # Two toy cars can be assembled in parallel 
)
```

:::tip
Think of `WorkStations` as dedicated areas where specific tasks happen. Each station has its own purpose and capabilities.
:::

## The Parts We Need

Every toy car needs two types of parts:

```python
car_parts = [
    Part(
        name="Car Body",
        quantity=50, # We now have 50 car bodies availabe
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

Now let's define what needs to happen:

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
`Actions` are like detailed instructions for each step in the manufacturing process. They specify what needs to happen, where it happens, and what materials are needed.
:::

## Putting It All Together

Finally, we create our product and set up a job to make it:

```python
toy_car = Product(
    name="Red Bull Racing Car",
    volume=0.002,
    production_state=ProductionState.NEW,
    due_date=datetime.now() + timedelta(hours=1)
)

# Add the required Parts to the Product
toy_car.add_part(car_parts[0], quantity=1)
toy_car.add_part(car_parts[1], quantiy=4)

# Create the Job
car_job = Job(
    products=[toy_car],
    priority=JobPriority.MEDIUM
)

# Add the required Action to the Job
car_job.add_action(assembly_action)
```

## What's Next?

Now that you've completed this basic tutorial, you understand how to:
* Create a WorkStation with specific capabilities and capacity for your manufacturing process
* Define Parts with properties like quantity, cost, and minimum stock levels
* Set up Actions that specify assembly steps, including their duration and resource requirements
* Build a complete Job by combining Products, Parts, and Actions into a working assembly line

This foundation will help you explore more advanced concepts like:
* Adding multiple WorkStations to create complex assembly lines
* Implementing quality control checks between production steps
* Managing part inventory and automated reordering
* Creating parallel assembly processes for increased efficiency

Try modifying this example by:
* Adding a second WorkStation for painting the toy cars

:::tip
Remember that every manufacturing process starts with these basic building blocks. As you get comfortable with them, you can create increasingly sophisticated production lines.
:::