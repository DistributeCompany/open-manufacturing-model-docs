---
sidebar_position: 3
---

# OTM versus OMM

The [Open Trip Model (OTM)](https://www.opentripmodel.org/) and Open Manufacturing Model (OMM) are complementary data models that serve different yet related purposes. While OTM focuses on logistics and transportation, OMM specializes in manufacturing operations. Let's explore their similarities and differences.

## Comparison

| Class/Concept | Open Trip Model (OTM 5.6) | Open Manufacturing Model (OMM 1.0) |
|--------------|:---------------------:|:-----------------------------:|
| Actions | ✅ | ✅ |
| Actors | ✅ | ✅ |
| Constraints | ✅ | ✅ |
| Locations | ✅ | ✅ |
| Routes | ✅ | ✅ |
| Sensors | ✅ | ✅ |
| Vehicles | ✅ | ✅ |
| Consignments | ✅ | ❌ |
| Documents | ✅ | ❌ |
| Events | ✅ | ❌ |
| Goods | ✅ | ❌ |
| TransportOrders | ✅ | ❌ |
| Trips | ✅ | ❌ |
| Conveyors | ❌ | ✅ |
| Jobs | ❌ | ✅ |
| Parts | ❌ | ✅ |
| Products | ❌ | ✅ |
| Machines | ❌ | ✅ |
| Resources | ❌ | ✅ |
| Robotic Arms | ❌ | ✅ |
| Storage | ❌ | ✅ |
| Tools | ❌ | ✅ |
| Workers | ❌ | ✅ |
| Workstations | ❌ | ✅ |

## Key Differences

1. **Resource Focus**
   - OTM primarily focuses on transportation and logistics resources (trips, routes, consignments, etc.)
   - OMM includes a wide range of manufacturing resources (machines, workstations, conveyors, etc.)

2. **Process Detail**
   - OTM models transport processes
   - OMM models manufacturing processes including assembly, quality control, and material handling

3. **Equipment Modeling**
   - OTM has limited equipment modeling
   - OMM provides detailed equipment modeling with capabilities, constraints, and monitoring

4. **Material Handling**
   - OTM focuses on finished goods transport
   - OMM includes internal material handling and work-in-progress tracking

## Common Ground

Both models share several fundamental concepts:
- Location tracking
- Route definition
- Actor management
- Coupling of entities via Actions
- Vehicle movements
- Constrained operations

## When to Use Which

**Use OTM when:**
- Focusing on transportation and logistics
- Managing delivery routes
- Tracking vehicle movements
- Handling external shipments
- Data-exchange between logistics parties

**Use OMM when:**
- Managing manufacturing operations
- Controlling production processes
- Monitoring equipment
- Tracking internal material flow
- Managing production resources
- Data-exchange between manufacturing equipment

## Combined Usage

OTM and OMM can be used together to create end-to-end supply chain solutions. OMM handles internal manufacturing operations while OTM manages external logistics and transportation.

:::tip
When integrating both models, use their shared concepts (Locations, Routes, Actions, etc.) as integration points between manufacturing and logistics operations.
:::