# Route

A class to represent a Route.

    Routes define paths that connect different Locations within and outside the manufacturing
    environment. They are primarily used for planning and executing movement Actions of 
    mobile Resources like Vehicles, and typically include multiple waypoints.

    Routes are connected to various components in the manufacturing system:
    - Locations that the route connects
    - Vehicles that can traverse the route
    - Actions that use the route (i.e, 'move' actions)

    **Best Practices**:
    - Define accurate georeference coordinates for the entire path
    - Calculate and maintain correct route lengths

    **Attributes**:
    | Name              | Data Type         | Description                                               |
    |-------------------|-------------------|-----------------------------------------------------------|
    | `name`            | `str`             | Human-readable name of the Route                          |
    | `georeference`    | `List[List[float]]`| Coordinates describing the entire route path             |
    | `length`          | `float`           | Total length of the route in meters                       |
    | `id`              | `str`             | Unique identifier                                         |
    | `actors`          | `List[Actor]`     | Actors associated with the route                          |
    | `creation_date`   | `datetime`        | Timestamp when route was created                          |
    | `last_modified`   | `datetime`        | Timestamp of last modification       

    **Example Configuration**
    ```python
    route = Route(
        name="Assembly to Warehouse",
        georeference=[[0.0, 0.0], [5.0, 0.0], [5.0, 5.0]],
        length=10.0,  # meters
        nodes=[1, 2, 3]  # waypoint IDs
        )
    ```
    :::info
    The georeference attribute for `Routes` differs from other classes as it contains the coordinates for the entire path, not just a single point. The format depends on the implementation but typically includes a list of coordinate pairs or a more complex path description.
    :::


## Constructor

```python
def __init__(self, name: str, georeference: List[List[float]], length: float, id: Optional[str] = None, actors: List[omm.Actor] = None) -> None:
```

Initialize a Route instance.


## Properties


### `actors`

Return a copy of the route's associated actors.

```python
@property
def actors(self):
    # Returns typing.List[omm.Actor]
```


### `georeference`

Return the route's georeference.

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


## Methods


### `add_actor`

Add an actor to the route.

```python
def add_actor(self, actor: omm.Actor) -> None:
```


### `remove_actor`

Remove an actor from the route.

```python
def remove_actor(self, actor: omm.Actor) -> None:
```


### `to_dict`

Convert the route instance to a dictionary representation.

```python
def to_dict(self) -> dict:
```


### `update_actor`

Replace an existing actor with a new one.

```python
def update_actor(self, old_actor: omm.Actor, new_actor: omm.Actor) -> None:
```


### `update_georeference`

Update the route's entire georeference.

```python
def update_georeference(self, new_georeference: List[float]) -> None:
```


## Example Usage

```python
# Create a new Route instance
Route(
    name=<str>
    georeference=<List>
    length=<float>
)
```
