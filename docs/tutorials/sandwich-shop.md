---
sidebar_position: 5
---

# Intermediate 2: Sandwich Shop Delivery

Let's model a sandwich shop that takes custom orders and delivers them to customers. This example shows how OMM can handle food service operations with time-sensitive deliveries. Let's call that a manufacturing system. That's how flexible OMM is! 

## What We're Building

We're creating a system that:
- Takes customer orders for sandwiches and burgers
- Manages ingredient inventory
- Coordinates food preparation
- Handles delivery scheduling
- Tracks order status

## The Components We Need

Our sandwich shop needs:
- **WorkStations** for food preparation
- **Storage** for ingredients
- **Vehicles** for delivery
- **Workers** for preparation and delivery
- **Routes** for deliveries
- **Products** (sandwiches and burgers)
- **Parts** (ingredients)

## Setting Up the Kitchen

First, let's create our food preparation areas:

```python
prep_station = WorkStation(
    name="Prep Station 1",
    georeference=[1.0, 1.0],
    workstation_type="food_prep",
    capabilities=["sandwich_assembly", "burger_assembly"],
    max_capacity=3  # Can prepare 3 orders simultaneously
)

grill_station = WorkStation(
    name="Grill Station",
    georeference=[2.0, 1.0],
    workstation_type="cooking",
    capabilities=["grilling", "toasting"],
    max_capacity=10  # Can grill or toast 3 orders simultaneously
)
```

## Managing Ingredients

Let's set up our ingredient storage and stock:

```python
cold_storage = Storage(
    name="Cold Storage",
    georeference=[0.0, 0.0],
    storage_type=StorageType.WAREHOUSE,
    max_capacity=10.0  # cubic meters
)

ingredients = [
    Part(
        name="Bread",
        quantity=200, # slices
        volume=0.01,
        state=ProductionState.NEW,
        part_type=PartType.RAW_MATERIAL,
        cost=0.15,
        min_stock_level=30
    ),
    Part(
        name="Burger Patty",
        quantity=50,
        volume=0.002,
        state=ProductionState.NEW,
        part_type=PartType.RAW_MATERIAL,
        cost=1.50,
        min_stock_level=10
    )
]

for ingredient in ingredients:
    cold_storage.add_item(ingredient)
```

## Setting Up Delivery

Create our delivery system:

```python
delivery_vehicle = Vehicle(
    name="Delivery Bike 1",
    vehicle_type=VehicleType.GENERIC_MANUAL_VEHICLE,
    georeference=[10.0, 10.0],
    average_speed=10.0,  # km/h
    energy_consumption_moving=0.1,  # kWh/km
    load_capacities={"weight": 10.0}  # kg
)

delivery_driver = Worker(
    name="Yoran",
    roles={
        "Delivery Driver": ["bike_delivery"]
    }
)
```

## Creating Orders

Handle a customer order:

```python
# Create the sandwich product
club_sandwich = Product(
    name="Club Sandwich",
    volume=0.001,
    production_state=ProductionState.NEW,
    due_date=datetime.now() + timedelta(minutes=45)
)

# Create prep actions
prep_action = Action(
    name="Prepare Club Sandwich",
    action_type=ActionType.ASSEMBLY,
    description="Assemble club sandwich with toasted bread",
    duration=0.05,  # 3 minutes
    sequence_nr=1,
    location=prep_station
)

# Add requirements
prep_action.add_requirement("Part", ["Bread", 3])
prep_action.add_requirement("Part", ["Turkey", 1])
prep_action.add_requirement("Part", ["Lettuce", 1])

# Create delivery action
delivery_action = Action(
    name="Deliver Sandwich",
    action_type=ActionType.MOVE,
    description="Deliver to customer address",
    duration=0.25,  # 15 minutes
    sequence_nr=2,
    worker=delivery_driver,
    origin=prep_station,
    destination=customer_location
)

# Add actions to product
club_sandwich.add_action(prep_action)
club_sandwich.add_action(delivery_action)

# Create the job
sandwich_order = Job(
    products=[club_sandwich],
    priority=JobPriority.MEDIUM,
    customer=customer
)
```

## Start Job

Let's make and deliver a sandwich. 

```python
# Start the job (assumption: this also starts the first action)
sandwich_order.start_job()

# Monitor action status
print(f"Prep action status: {prep_action.status}")  # in_progress

'''
Through the miracle of time, 3 minutes have gone by...
''' 

# Start delivery action after prep is complete
if prep_action.status == ActionStatus.COMPLETED:
    delivery_action.start_action() #  note: this method is currently not yet in OMM
    print(f"Delivery action started at {delivery_action.start_time)}")
else:
    print("Cannot start delivery - preparation not complete")

# Monitor action status
print(f"Prep action status: {prep_action.status}")  # completed
print(f"Delivery action status: {delivery_action.status}") # in_progress

# Track delivery every minute
while delivery_action.status != ActionStatus.COMPLETED:
    print(f"Delivery action progress: {delivery_action.progress}" ) # e.g., 35 %
    time.sleep(60)
```

:::tip
For food service, timing is crucial. Use the Job's priority system to ensure orders are prepared and delivered in the right sequence.
:::

## What's Next?
Now that you've seen how to create a sandwich shop delivery system with OMM, try extending this example with::

- Add menu item variations with branching preparation workflows (like special dietary requirements or custom toppings)
- Implement quality checks and temperature monitoring during preparation and delivery
- Set up automated ingredient reordering based on min_stock_level triggers
- Add real-time delivery route optimization based on multiple pending orders
- Implement parallel preparation workflows when orders contain multiple items
- Add scheduling systems for worker shifts and delivery zone management

:::tip
Remember that OMM's flexibility means you can start simple and gradually add more sophisticated features as your operation grows.
:::