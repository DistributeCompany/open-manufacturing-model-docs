# Part

A class to represent a Part.

    Parts are fundamental components used in manufacturing processes. They represent raw 
    materials, purchased components, or intermediate items that are used to create finished 
    products. The Part class manages inventory tracking, state transitions, and supply chain 
    relationships for manufacturing components.

    Parts are connected to various components in the manufacturing system:
    - Products they are used in
    - Storage locations where they are kept
    - Suppliers who provide them
    - Actions that process them
    - Resources that handle them
    - Jobs that require them

    Parts can be categorized into different types:
    - Raw Materials: Unprocessed materials used in manufacturing
    - Purchased Components: Pre-made components from external suppliers
    - Work-in-Progress: Partially completed components

    **Best Practices**:
    - Maintain accurate inventory levels
    - Track minimum stock thresholds
    - Monitor part states
    - Record supplier information
    - Track cost and value
    - Monitor quality metrics
    - Manage batch/lot numbers
    - Track expiration dates
    - Document specifications
    - Monitor usage patterns
    - Track reorder points

    **Attributes**:
    | Name              | Data Type         | Description                                                     |
    |-------------------|-------------------|-----------------------------------------------------------------|
    | `name`            | `str`             | Human-readable name of the Part                                 |
    | `quantity`        | `int`             | Current quantity in stock                                       |
    | `volume`          | `float`           | Physical volume of one unit                                     |
    | `state`           | `ProductionState` | Current state. See [ProductionState](/docs/classes/productionstate) |
    | `part_type`       | `PartType`        | Category of part. See [PartType](/docs/classes/parttype)          |
    | `cost`            | `float`           | Cost per unit                                                   |
    | `supplier`        | `Actor`           | Supplier providing this part                                    |
    | `min_stock_level` | `int`             | Minimum quantity to maintain                                    |
    | `id`              | `str`             | Unique identifier                                               |
    | `creation_date`   | `datetime`        | Timestamp when part was created                                 |
    | `last_modified`   | `datetime`        | Timestamp of last modification                                  |

    **States include**:
    - **Raw**: Unprocessed material
    - **New**: Newly received item
    - **Work in Progress**: In production
    - **Finished**: Complete and ready
    - **Defective**: Failed quality check
    - **On Hold**: Suspended from use

    **Example Configuration**:
    ```python
    part = Part(
        name="Steel Bracket",
        quantity=100,
        volume=0.5,  # cubic meters
        state=ProductionState.NEW,
        part_type=PartType.PURCHASED_COMPONENT,
        cost=25.50,
        min_stock_level=50
        )
    ```
    :::note
    `Parts` are components in the manufacturing process that get transformed into finished products and can be analogous to Materials. They typically require inventory management and state tracking throughout their lifecycle in the manufacturing system.
    :::


## Constructor

```python
def __init__(self, name: str, quantity: int, volume: float, state: omm.ProductionState = <ProductionState.NEW: 2>, part_type: omm.PartType = <PartType.RAW_MATERIAL: 'Raw Material'>, cost: float = 0.0, supplier: Optional[~ActorT] = None, min_stock_level: int = 0, id: Optional[str] = None) -> None:
```

Initialize a Part instance.


## Properties


### `last_modified`

Return the last modified timestamp.

```python
@property
def last_modified(self):
    # Returns <class 'datetime.datetime'>
```


## Methods


### `adjust_quantity`

Adjust the quantity of the part by the given amount.
        
        Args:
            amount: Amount to adjust (positive or negative)
            
        Raises:
            ValueError: If resulting quantity would be negative

```python
def adjust_quantity(self, amount: int) -> None:
```


### `calculate_value`

Calculate total value of part based on quantity and cost.

```python
def calculate_value(self) -> float:
```


### `is_below_min_stock`

Check if current quantity is below minimum stock level.

```python
def is_below_min_stock(self) -> bool:
```


### `to_dict`

Convert the part instance to a dictionary representation.

```python
def to_dict(self) -> Dict[str, Any]:
```


### `update_state`

Update the production state of the part.
        
        Args:
            new_state: New ProductionState to set
            
        Raises:
            ValueError: If state transition is invalid

```python
def update_state(self, new_state: omm.ProductionState) -> None:
```


## Example Usage

```python
# Example: Managing manufacturing parts inventory
aluminum_block = Part(
    name='Aluminum_Block_6061',
    quantity=50,
    volume=0.008,  # cubic meters
    state=ProductionState.NEW,
    part_type=PartType.RAW_MATERIAL,
    cost=15.0,  # cost per unit
    supplier=Actor('MetalsRUs'),
    min_stock_level=10
)

# Track inventory movements
aluminum_block.adjust_quantity(-5)  # Use 5 units

# Check inventory status
if aluminum_block.is_below_min_stock():
    print(f'Low stock alert for {aluminum_block.name}!')
    print(f'Current quantity: {aluminum_block.quantity}')
    print(f'Minimum level: {aluminum_block.min_stock_level}')

# Calculate inventory value
total_value = aluminum_block.calculate_value()
print(f'Total inventory value: ${total_value:.2f}')
```
