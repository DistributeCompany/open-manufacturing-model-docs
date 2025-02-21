# Storage

A class to represent a Storage location.

    Storage locations are specialized Location instances that manage the storage of Parts and 
    Products within the manufacturing facility. They represent dedicated areas like warehouses, 
    buffer zones, racks, or queues where materials and finished goods are stored. The Storage 
    class extends the Location class to include inventory management capabilities and capacity 
    tracking.

    Storage locations are connected to various components in the manufacturing system:
    - Parts stored within them
    - Products stored within them
    - Workers who manage them
    - Vehicles that access them
    - Actions performed in them
    - Resources used to manage them
    - Jobs that require items from them

    Storage locations can be categorized into different types:
    - **General**: Multi-purpose storage area without specific designation
    - **Warehouse**: Large-scale storage facility
    - **Rack**: Structured storage system with multiple levels
    - **Buffer**: Temporary storage area between operations
    - **Queue**: FIFO storage area for sequential processing

    **Best Practices**:
    - Monitor capacity utilization
    - Track item locations
    - Maintain inventory accuracy
    - Implement proper storage conditions
    - Manage access control
    - Monitor environmental conditions
    - Implement FIFO/LIFO as needed
    - Track storage duration
    - Maintain safety clearances
    - Monitor storage conditions
    - Implement zone organization
    - Track item movements

    **Attributes**:
    | Name               | Data Type                         | Description                                                                           |
    |--------------------|-----------------------------------|---------------------------------------------------------------------------------------|
    | `name`             | `str`                             | Human-readable name of the Storage                                                    |
    | `georeference`     | `List[float]`                     | Physical location coordinates [x, y] or [x, y, z]                                      |
    | `storage_type`     | `StorageType`                     | Type of storage. See [StorageType](/docs/classes/storagetype)                         |
    | `max_capacity`     | `float`                           | Maximum storage capacity in volume units                                              |
    | `id`               | `str`                             | Unique identifier                                                                      |
    | `actors`           | `List[Actor]`                     | Workers who manage this storage                                                        |
    | `actions`          | `List[Action]`                    | Actions performed in this storage                                                      |
    | `constraints`       | `List[constraints]`                      | Operating constraints                                                                  |
    | `storage`          | `Dict[str, Union[Product, Part]]` | Dictionary of stored items by ID                                                       |
    | `current_capacity` | `float`                           | Current used capacity                                                                  |
    | `creation_date`    | `datetime`                        | Timestamp when storage was created                                                     |
    | `last_modified`    | `datetime`                        | Timestamp of last modification                                                         |

    **Storage Operations**:
    - Add items to storage
    - Remove items from storage
    - Query stored items
    - Track capacity utilization
    - Monitor storage conditions
    - Manage item locations
    - Track inventory levels
    - Handle item retrievals

    **Example Configuration**:
    ```python
        storage = Storage(
            name="Main Warehouse",
            georeference=[52.2376489846171, 6.847945014035459],
            storage_type=StorageType.WAREHOUSE,
            max_capacity=1000.0,  # cubic meters
            actors=[warehouse_manager, inventory_clerk], # instances of Actor class
            constraints=[temperature_constraint] # instance of Constraint class
            )
    ```

    Add items to storage
    ```python
    storage.add_item(raw_material_batch)
    storage.add_item(finished_product)
    ```

    Check utilization
    ```python
    print(f"Storage utilization: {storage.utilization}%")
    ```
    
    :::note
    The `Storage` class inherits base attributes from the `Location` class while adding specialized capabilities for inventory management. Use this class for any areas dedicated to storing `Parts` or `Products`, whether temporary or long-term. The class supports different storage types and maintains accurate capacity tracking to prevent overflow conditions.
    :::


## Inheritance

Inherits from: `Location`


## Constructor

```python
def __init__(self, name: str, georeference: List[float], storage_type: omm.StorageType, max_capacity: float, id: Optional[str] = None, actors: List[~ActorT] = None, actions: List[~ActionT] = None, constraints: Optional[List[~ConstraintT]] = None) -> None:
```

Initialize an Storage location.


## Properties


### `actions`

Return a copy of the location's actions.

```python
@property
def actions(self):
    # Returns typing.List[~ActionT]
```


### `actors`

Return a copy of the location's actors.

```python
@property
def actors(self):
    # Returns typing.List[~ActorT]
```


### `available_capacity`

Return the remaining available capacity.

```python
@property
def available_capacity(self):
    # Returns <class 'float'>
```


### `constraints`

Return the location's constraints.

```python
@property
def constraints(self):
    # Returns typing.Optional[typing.List[~ConstraintT]]
```


### `georeference`

Return the resource's georeference.

```python
@property
def georeference(self):
    # Returns typing.List[float]
```


### `last_modified`

Return the last modified timestamp.

```python
@property
def last_modified(self):
    # Returns <class 'datetime.datetime'>
```


### `utilization`

Return the current utilization as a percentage.

```python
@property
def utilization(self):
    # Returns <class 'float'>
```


## Methods


### `add_action`

Add a single action to the location's actions.

```python
def add_action(self, action: ~ActionT) -> None:
```


### `add_actor`

Add an actor to the location.

```python
def add_actor(self, actor: ~ActorT) -> None:
```


### `add_constraint`

Add a single constraint to the resource's constraints.

```python
def add_constraint(self, constraint: ~ConstraintT) -> None:
```


### `add_item`

Add a Product or Part to the storage.
        
        Args:
            item: The Product or Part to add
            
        Raises:
            TypeError: If item is not a Product or Part
            ValueError: If adding the item would exceed capacity

```python
def add_item(self, item: Union[omm.Product, omm.Part]) -> None:
```


### `get_current_action`

Get the current in-progress action.

```python
def get_current_action(self) -> Optional[~ActionT]:
```


### `get_item`

Get an item from storage by its ID without removing it.
        
        Args:
            item_id: The ID of the item to get
            
        Returns:
            The Product or Part
            
        Raises:
            KeyError: If item_id is not found in storage

```python
def get_item(self, item_id: str) -> Union[omm.Product, omm.Part]:
```


### `get_items_by_type`

Get all items of a specific type (Product or Part).
        
        Args:
            item_type: The type to filter by (Product or Part)
            
        Returns:
            List of items matching the specified type

```python
def get_items_by_type(self, item_type: type) -> List[Union[omm.Product, omm.Part]]:
```


### `list_items`

Return a list of all items in the storage.

```python
def list_items(self) -> List[Union[omm.Product, omm.Part]]:
```


### `remove_action`

Remove a specific action from the location's actions.

```python
def remove_action(self, action: ~ActionT) -> None:
```


### `remove_actor`

Remove an actor from the location.

```python
def remove_actor(self, actor: ~ActorT) -> None:
```


### `remove_constraint`

Remove a specific constraint from the resource's constraints.

```python
def remove_constraint(self, constraint: ~ConstraintT) -> None:
```


### `remove_item`

Remove and return an item from storage by its ID.
        
        Args:
            item_id: The ID of the item to remove
            
        Returns:
            The removed Product or Part
            
        Raises:
            KeyError: If item_id is not found in storage

```python
def remove_item(self, item_id: str) -> Union[omm.Product, omm.Part]:
```


### `to_dict`

Convert the storage instance to a dictionary representation.

```python
def to_dict(self) -> Dict[str, Any]:
```


### `update_action`

Replace an existing action with a new action.

```python
def update_action(self, old_action: ~ActionT, new_action: ~ActionT) -> None:
```


### `update_actor`

Replace an existing actor with a new actor.

```python
def update_actor(self, old_actor: ~ActorT, new_actor: ~ActorT) -> None:
```


## Example Usage

```python
# Create a new Storage instance
Storage(
    name=<str>
    georeference=<List>
    storage_type=<StorageType>
    max_capacity=<float>
)
```
