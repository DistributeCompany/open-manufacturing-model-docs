# Actor

A class to represent an Actor in the manufacturing system.

    Actors are entities that participate in the manufacturing environment without directly 
    performing manufacturing operations. They represent stakeholders such as customers, 
    suppliers, service providers, and other external or internal parties that interact 
    with the manufacturing system.

    Actors establish relationships with manufacturing processes through:
        - Business relationships (customer orders, supplier deliveries)
        - Service agreements (maintenance providers, logistics partners)
        - Resource ownership (equipment providers, facility owners)
        - Process oversight (quality inspectors, auditors)

    The Actor class serves as a base class for more specialized actor types:
        - `Worker`: Performs actual manufacturing operations
        - `Customer`: Places orders and receives finished products (not yet implemented)
        - `Supplier`: Provides raw materials and components (not yet implemented)
        - `Service Provider`: Offers maintenance and support services (not yet implemented)

    **Best Practices**:
    - Associate Actors with specific locations where they operate
    - Use meaningful names that describe the Actor's role

    **Attributes**:
    | Name            | Data Type       | Description                                               |
    |-----------------|-----------------|-----------------------------------------------------------|
    | `name`          | `str`           | Human-readable name of the Actor                          |
    | `id`            | `str`           | Unique identifier                                         |
    | `locations`     | `List[Location]`| List of locations associated with this actor              |
    | `creation_date` | `datetime`      | Timestamp when the actor was created                      |
    | `last_modified` | `datetime`      | Timestamp of last modification       

    **Example Configuration**
    ```python
    actor = Actor(
        name="Acme Corporation",
        locations=[main_warehouse, shipping_dock], # instances of Location class
        id="SUPPLIER_001"
        )
    ```

    :::note
    For actors who actively perform manufacturing operations (operators, technicians, maintenance staff), use the `Worker` subclass instead of the `Actor` base class.
    :::


## Constructor

```python
def __init__(self, name: str, id: Optional[str] = None, locations: List[~LocationT] = None) -> None:
```

Initialize an Actor instance.


## Properties


### `last_modified`

Return the last modified timestamp.

```python
@property
def last_modified(self):
    # Returns <class 'datetime.datetime'>
```


### `locations`

Return a copy of the actor's locations.

```python
@property
def locations(self):
    # Returns typing.List[~LocationT]
```


## Methods


### `add_location`

Add a location to the actor.

```python
def add_location(self, location: ~LocationT) -> None:
```


### `remove_location`

Remove a location from the actor.

```python
def remove_location(self, location: ~LocationT) -> None:
```


### `to_dict`

Convert the actor instance to a dictionary representation.

```python
def to_dict(self) -> Dict[str, Any]:
```


### `update_location`

Replace an existing location with a new location.

```python
def update_location(self, old_location: ~LocationT, new_location: ~LocationT) -> None:
```


## Example Usage

```python
# Example: Creating and managing an actor in the system
supplier = Actor(
    name='Precision Parts Ltd',
    locations=[
        Location('Warehouse A', [45.5, 23.7], LocationType.EXTERNAL),
        Location('Loading Dock B', [45.6, 23.8], LocationType.EXTERNAL)
    ]
)

# Add a new delivery location
new_location = Location('Distribution Center', [46.0, 24.0], LocationType.EXTERNAL)
supplier.add_location(new_location)

# Track supplier's delivery points
print(f'Delivery locations for {supplier.name}:')
for loc in supplier.locations:
    print(f'  - {loc.name} at {loc.georeference}')
```
