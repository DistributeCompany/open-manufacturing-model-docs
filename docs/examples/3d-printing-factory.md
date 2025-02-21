# Intermediate: 3D Printing Factory

## Create a 3D printing job for a miniature Pikachu.

We start by creating a `Job` instance. The `Job` resembles the manufacturing actions required to satisfy a customer order. This job contains a single `Product`. The customer is an instance of the `Actor` class. In this way, we establish a relationship between a `Job` and an `Actor`.
```python
pikachu_print_job = Job(
    products=[
        Product(
            name='Miniature Pikachu',
            volume=0.125,  # Approximate volume in cubic meters
            production_state=ProductionState.NEW,
            due_date=datetime.now() + timedelta(hours=8)  # Expected print time
        )
    ],
    priority=JobPriority.MEDIUM,
    customer=Actor(
        name="Pokemon Collector",
        ),
)
```

:::tip
Optional: for additional clarity, we may add the customer's name to the `Product`. In this way, we have a human-readible description of the customer on the `Product` level. 

```python
for product in pickachu_print_job.products:
    product.customer = pickachu_print_job.customer.name
    print(product.customer) # prints "Pokemon Collector"
```
:::
## Create a Location
The shipping department would probably interested in where to send the `Product` when the `Job` is finished. Let's add a `Location` to the `Actor`.

```python
customer_location =
    Location(
        name="Home Office of Pokemon Collector",
        georeference=[52.23767045493833, 6.848023899076972],
        location_type=LocationType.EXTERNAL
        )

# Establish a relationship between the customer and the location
pikachu_print.customer.add_location([customer_location]) # an Actor can have multiple Locations, so we provide it as a list. 
```

## Create the 3D printer resource
We have a 3D printer in our manufacturing facility. Let's create an OMM-compliant representation. 

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
:::note
Notice that we do not set the `location` attribute. Let's just assume that in this use case, we only have one facility, so a bit overkill to create a seperate `Location` for our `Machine`, especially because we already have a `georeference` attribute to represent where the `Machine` is located in our facility. 
:::

## Create printing action
This `Product` only requires a single `Action`. Let's create it. 
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
:::note
By default, `Actions` are intialized with the attribute `status` set to `ActionType.DRAFT`. 
:::

## Create required parts (filaments)
To execute this `Action` we need several `Parts`.
```python
filaments = [
    Part(
        name='PolyTerra PLA Savannah Yellow',
        quantity=100,  # grams
        volume=0.00008,  # cubic meters
        state=ProductionState.NEW,
        part_type=PartType.RAW_MATERIAL,
        cost=24.99,
        min_stock_level=50  # minimum grams
    ),
    Part(
        name='PolyTerra PLA Lava Red',
        quantity=25,
        volume=0.00002,
        state=ProductionState.NEW,
        part_type=PartType.RAW_MATERIAL,
        cost=24.99,
        min_stock_level=50
    ),
    Part(
        name='PolyTerra PLA Charcoal Black',
        quantity=15,
        volume=0.000012,
        state=ProductionState.NEW,
        part_type=PartType.RAW_MATERIAL,
        cost=24.99,
        min_stock_level=50
    ),
    Part(
        name='PolyTerra PLA Cotton White',
        quantity=10,
        volume=0.000008,
        state=ProductionState.NEW,
        part_type=PartType.RAW_MATERIAL,
        cost=24.99,
        min_stock_level=50
    ),
    Part(
        name='PolyTerra PLA Wood Brown',
        quantity=5,
        volume=0.000004,
        state=ProductionState.NEW,
        part_type=PartType.RAW_MATERIAL,
        cost=24.99,
        min_stock_level=50
    )
]
```

## Add requirements to the action
Let's connect the `Parts` to the `Action` using the `requirements` attribute of the `Action`. We also add a requirement to determine which instances of `Machine` are allowed to perform this `Action`.
```python
for filament in filaments:
    print_action.add_requirement('Part', [filament.name, filament.quantity])

# Add the requirement that this Action can only be performed on a specific Machine. 
print_action.add_requirement('Machine', ['Bambu Lab X1C 3D Printer'])
```
## Add action to job and start
Finally we add the `Action` to the `Job` and hit start!
```python
pikachu_print.add_action(print_action)
pikachu_print.start_job()
```

:::info
Using `add_action()` we add the `Action` to `Job.actions`. You may wonder, that the `Action` is also related once a  `Machine` performs the `Action`. That is correct! So once we've determined which `Machine` is going to perform the `Action`, it is also added to `Machine.actions`. In this way, we have a clear view of all `Actions` related to a `Job`, but we also know all the `Actions` performed on a `Machine`.
:::
## Monitor progress
If we are modelling a Digital Twin, we can now kick back and relax and watch the print come to life! To monitor the process, we may use the following commands. Note that we can also simulate this process, and use the same commands. 
```python
print(f'Job progress: {pikachu_print.get_progress()}%')
print(f'Estimated completion time: {pikachu_print.get_estimated_completion_time()} hours')
print(f'Current status: {pikachu_print.status}')
```
## Check if any filaments need restocking
During printing, we may run out of filament. 
```python
for filament in filaments:
    if filament.is_below_min_stock():
        print(f'Low stock alert: {filament.name}')
```

:::tip
You can also chose to check whether the filament level(s) will run out at the `Machine` (or possibly you run out of filament in the entire factory!) before starting the `Action`. You would then probably create a *set-up* `Action` that makes sure the `Machine` has sufficient filament, before the `print_action` is allowed to start. Or you may create an `Action` of type `replenish stock` (not implemented!).
:::