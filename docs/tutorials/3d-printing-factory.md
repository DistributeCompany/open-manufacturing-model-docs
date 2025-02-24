---
sidebar_position: 4
---

# Intermediate 1: 3D Printing Factory

Welcome to this hands-on tutorial where we'll create a complete 3D printing workflow using OMM! We'll walk through creating a manufacturing job for a miniature Pikachu figure, demonstrating how different OMM components work together in a real-world scenario.

![Pika, Pika!](@site/static/img/pikachu.png)  
[Source: Makerworld](https://makerworld.com/en/models/388565?from=search#profileId-289389)

## What We're Building

In this tutorial, we'll:
- Set up a manufacturing job for a custom 3D printed product
- Create and connect a customer profile
- Configure a 3D printer as a manufacturing resource
- Define the required materials and actions
- Monitor the printing process

## The Manufacturing Flow

Here's how our 3D printing process will work:
1. Create a job for the customer's order
2. Set up the product specifications
3. Configure the 3D printer resource
4. Define the printing action
5. Specify required materials
6. Start and monitor the manufacturing process

## Creating the Job

Let's start by creating a Job that represents our customer's order. Jobs in OMM coordinate the production of Products and connect them to customers (Actors).

```python
pikachu_print_job = Job(
    products=[
        Product(
            name='Miniature Pikachu',
            volume=0.125,  # Approximate volume in cubic meters
            production_state=ProductionState.NEW,
            due_date=datetime.now() + timedelta(hours=8)  # Production due date
        )
    ],
    priority=JobPriority.MEDIUM,
    customer=Actor(
        name="Pokemon Collector",
    ),
)
```

:::tip
For better traceability, you can add the customer's name directly to the Product:

```python
for product in pikachu_print_job.products:
    product.customer = pikachu_print_job.customer.name
```
:::

## Adding a Customer Location

Every customer lives somewhere. Let's add the customer's information using OMM's Location class:

```python
customer_location = Location(
    name="Home Office of Pokemon Collector",
    georeference=[52.23767045493833, 6.848023899076972],
    location_type=LocationType.EXTERNAL
)

# Link the location to our customer
pikachu_print_job.customer.add_location([customer_location]) # As an Actor can have multiple Locations, we provide it as a list
```

## Setting Up the 3D Printer

Now let's configure our 3D printer as a Resource. In OMM, machines are specialized resources that can have capabilities and sensors:

```python
printer = Machine(
    name='Bambu_X1C_01',
    machine_type='Bambu Lab X1C 3D Printer',
    georeference=[10.0, 20.0, 0.0],
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
```

## Defining the Printing Action

Every manufacturing job needs Actions that describe what needs to be done. For our 3D print, we'll create a single printing action:

```python
print_action = Action(
    name='Print Pikachu',
    action_type=ActionType.PROCESS,
    description='3D print miniature Pikachu with multiple colors',
    duration=8.0,  # 8 hours estimated print time
    sequence_nr=1,
    location=printer
)
```

## Specifying Required Materials

Our Pikachu needs different colored filaments. In OMM, these are represented as Parts:

```python
filaments = [
    Part(
        name='PolyTerra PLA Savannah Yellow',
        quantity=100,  # grams
        volume=0.00008,  # cubic meters
        state=ProductionState.NEW,
        part_type=PartType.RAW_MATERIAL,
        cost=24.99,
        min_stock_level=50
    ),
    # Additional filaments...
]
```

## Connecting Everything Together

Now we'll link our materials to the action and specify machine requirements:

```python
# Connect filaments to the action
for filament in filaments:
    print_action.add_requirement('Part', [filament.name, filament.quantity])

# Specify machine requirements
print_action.add_requirement('Machine', ['Bambu Lab X1C 3D Printer'])

# Add the action to our job
pikachu_print_job.add_action(print_action)
```

## Starting and Monitoring Production

With everything set up, we can start our job and monitor its progress:

```python
# Start the manufacturing process
pikachu_print_job.start_job()

# Monitor progress
print(f'Job progress: {pikachu_print_job.get_progress()}%')
print(f'Estimated completion time: {pikachu_print_job.get_estimated_completion_time()} hours')
print(f'Current status: {pikachu_print_job.status}')
```

## Managing Inventory

We can check if any materials need restocking:

```python
for filament in filaments:
    if filament.is_below_min_stock():
        print(f'Low stock alert: {filament.name}')
```

:::tip
Consider checking material levels before starting the job to avoid interruptions. You might want to add an additional Action to the Job that checks if the Resource is properly setup and satisfies all Part requirements. In this way, `print_action` should not fail or be put on-hold due to missing Parts. 
:::

## What's Next?

Now that you've seen how to create a 3D printing workflow with OMM, you can:
- Experiment with different product configurations
- Add quality control actions
- Implement more complex multi-machine workflows
- Create automated material restocking systems