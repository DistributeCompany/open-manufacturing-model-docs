# Product

A class to represent a Product.

    Products are the finished goods that result from manufacturing processes. They represent 
    completed items that are ready for delivery to customers. The Product class manages the 
    bill of materials, manufacturing processes, and product lifecycle states for finished goods.

    Products are connected to various components in the manufacturing system:
    - Parts they are made from
    - Actions required to produce them
    - Jobs that require them
    - Customers who order them
    - Storage locations where they are kept
    - Resources used in their production
    - Workers involved in their manufacture

    **Best Practices**:
    - Maintain accurate bill of materials
    - Track production states
    - Monitor quality metrics
    - Record customer requirements
    - Track manufacturing costs
    - Document production processes
    - Monitor completion dates
    - Track product variants
    - Maintain revision history
    - Document specifications
    - Track serialization

    **Attributes**:
    | Name                | Data Type                         | Description                                                                          |
    |---------------------|-----------------------------------|--------------------------------------------------------------------------------------|
    | `name`              | `str`                             | Human-readable name of the Product                                                   |
    | `volume`            | `float`                           | Physical volume of the product                                                       |
    | `production_state`  | `ProductionState`                 | Current state. See [ProductionState](/docs/classes/productionstate)                   |
    | `customer`          | `str`                             | Customer who ordered the product                                                     |
    | `due_date`          | `datetime`                        | Required completion date                                                             |
    | `id`                | `str`                             | Unique identifier                                                                    |
    | `actions`           | `List[Action]`                    | Manufacturing steps required                                                         |
    | `parts`             | `Dict[str, tuple[Part, int]]`      | Bill of materials with quantities                                                    |
    | `creation_date`     | `datetime`                        | Timestamp when product was created                                                   |
    | `last_modified`     | `datetime`                        | Timestamp of last modification                                                       |

    **States include**:
    - **New**: Product order received
    - **Work in Progress**: In production
    - **Finished**: Complete and ready
    - **Defective**: Failed quality check
    - **On Hold**: Production suspended

    ***Example Configuration**:
    ```python
    product = Product(
        name="Electric Motor Assembly",
        volume=2.5,  # cubic meters
        production_state=ProductionState.NEW,
        customer="Acme Industries",
        due_date=datetime(2025, 3, 15)
        )
    ```
    Add required parts:
    ```python
    product.add_part(motor_housing, 1)
    product.add_part(rotor_assembly, 1)
    product.add_part(stator_assembly, 1)
    product.add_part(mounting_brackets, 4)
    ```

    :::note
    `Products` represent the output of manufacturing processes and require careful management of their components, production steps, and quality requirements. Each product maintains its bill of materials through `Parts` and associated manufacturing actions to ensure proper production.
    :::


## Constructor

```python
def __init__(self, name: str, volume: float, production_state: omm.ProductionState = <ProductionState.WORK_IN_PROGRESS: 3>, customer: Optional[str] = None, due_date: Optional[datetime.datetime] = None, id: Optional[str] = None, actions: List[~ActionT] = None) -> None:
```

Initialize a Product instance.


## Properties


### `actions`

Return a copy of the Product's actions.

```python
@property
def actions(self):
    # Returns typing.List[~ActionT]
```


### `customer`

Return a copy of the Products customer.

```python
@property
def customer(self):
    # Returns ~ActorT
```


### `last_modified`

Return the last modified timestamp.

```python
@property
def last_modified(self):
    # Returns <class 'datetime.datetime'>
```


## Methods


### `add_action`

Add an action to the product's process.

```python
def add_action(self, action: omm.Action) -> None:
```


### `add_part`

Add a part to the product's bill of materials.
        
        Args:
            part: Part to add
            quantity: Quantity of the part needed
            
        Raises:
            ValueError: If quantity is invalid

```python
def add_part(self, part: omm.Part, quantity: int = 1) -> None:
```


### `calculate_total_cost`

Calculate total cost of product based on parts and quantities.

```python
def calculate_total_cost(self) -> float:
```


### `is_overdue`

Check if product is overdue based on due date.

```python
def is_overdue(self) -> bool:
```


### `remove_action`

Remove an action from the product's process.

```python
def remove_action(self, action: omm.Action) -> None:
```


### `remove_part`

Remove a part from the product's bill of materials.
        
        Args:
            part_id: ID of part to remove
            
        Raises:
            KeyError: If part is not found

```python
def remove_part(self, part_id: str) -> None:
```


### `to_dict`

Convert the product instance to a dictionary representation.

```python
def to_dict(self) -> Dict[str, Any]:
```


### `update_part_quantity`

Update the quantity of a part in the bill of materials.
        
        Args:
            part_id: ID of part to update
            new_quantity: New quantity to set
            
        Raises:
            KeyError: If part is not found
            ValueError: If new quantity is invalid

```python
def update_part_quantity(self, part_id: str, new_quantity: int) -> None:
```


### `update_state`

Update the production state of the product.

```python
def update_state(self, new_state: omm.ProductionState) -> None:
```


## Example Usage

```python
# Create a new Product instance
Product(
    name=<str>
    volume=<float>
)
```
