# Requirement

A class to represent Requirements for manufacturing Actions.

Requirements define the specific resources, components, tools, or personnel needed
to execute an Action. Each Requirement specifies a type (e.g., Machine, Part, Worker)
and detailed specifications for that type.

The Requirement types are defined by the [RequirementType](/docs/classes/requirementtype):
- *Machine*: Manufacturing equipment requirements
- *Workstation:* Workstation requirements
- *Conveyor*: Conveyor system requirements
- *Robotic Arm*: Robotic Arm requirements
- *Vehicle*: Transport requirements
- *Part*: Part/Material requirements
- *Product*: Product requirements
- *Worker*: Personnel requirements
- *Tool*: Equipment requirements

**Best Practices**:
- Specify requirements at the appropriate level of detail
- Include quantity information for parts and products
- Clearly define skill requirements for workers
- Specify exact machine types when necessary
- Use generic types when flexibility is possible

**Attributes**:
| Name   | Data Type         | Description                                                                                     |
|--------|-------------------|-------------------------------------------------------------------------------------------------|
| `type` | `RequirementType` | Type of requirement. See [RequirementType](/docs/classes/requirementtype)                        |
| `specs`| `List[Any]`       | Specifications for the requirement, format depends on type                                      |

**Example Requirements**:

* Specific machine requirement  
```python
Requirement(type=RequirementType.MACHINE, specs=["CNC Mill"])
```
* Part requirement with quantity  
```python
Requirement(type=RequirementType.PART, specs=["Steel Plate", 5])
```
* Generic worker requirement  
```python
* Requirement(type=RequirementType.WORKER, specs=[])
```python
* Specific worker role requirement  
```python
Requirement(type=RequirementType.WORKER, specs=["Technician"])
```
:::note
The format of the specs list varies depending on the requirement type. Always validate the specs format against the requirement type's expectations.
:::


## Constructor

```python
def __init__(self, type: omm.RequirementType, specs: List[Any]) -> None:
```


## Methods


## Example Usage

```python
# Create a new Requirement instance
Requirement(
    type=<RequirementType>
    specs=<List>
)
```
