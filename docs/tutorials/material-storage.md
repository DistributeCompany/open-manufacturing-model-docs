---
sidebar_position: 3
---

# Basic 3: Material Storage

Our final basic tutorial looks at how OMM manages storage and inventory. We'll create a simple storage system that tracks materials and products.

## What We're Building

We're setting up storage areas for:
- Raw materials waiting to be used
- Finished products ready for shipping
- A buffer zone for work in progress

## Storage Areas

Let's create our storage spaces:

```python
raw_materials = Storage(
    name="Raw Materials Warehouse",
    georeference=[0.0, 0.0],
    storage_type=StorageType.WAREHOUSE,
    max_capacity=1000.0  # cubic meters
)

finished_goods = Storage(
    name="Finished Goods Storage",
    georeference=[10.0, 0.0],
    storage_type=StorageType.WAREHOUSE,
    max_capacity=500.0
)
```

:::tip
`Storage` locations keep track of not just what's stored, but also how much space is available and where everything is located.
:::

## Managing Inventory

Here's how we track what's in storage:

```python
# Store a raw material
raw_material = Part(
    name="Aluminum Sheet",
    quantity=100,
    volume=0.5,
    state=ProductionState.RAW,
    part_type=PartType.RAW_MATERIAL,
    cost=50.00,
    min_stock_level=20
)

raw_materials.add_item(raw_material)
```

## Monitoring Storage Levels

We can easily check our storage status:

```python
def check_storage_levels(storage: Storage) -> None:
    """Keep an eye on what's in storage."""
    print(f"Storage {storage.name}:")
    print(f"- Utilization: {storage.utilization}%")
    print(f"- Available space: {storage.available_capacity} cubic meters")
```

## What's Next?

Now that you've completed these basic tutorials, you understand how to:
- Set up simple manufacturing processes
- Create and connect different OMM components
- Handle quality control
- Manage storage and inventory

You're ready to move on to more complex scenarios that combine these basic concepts in new ways. Try modifying these examples to match your own manufacturing needs.