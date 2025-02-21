---
sidebar_position: 2
---

# OMM in 5 Minutes

Welcome to a quick tour of the Open Manufacturing Model (OMM)! Let's explore how OMM helps represent and organize your manufacturing system in a clear and intuitive way.

## The Big Picture

Think of OMM as a digital blueprint of your manufacturing facility. It helps you keep track of:
- Where everything is (Locations)
- What you have (Resources, Products, Parts)
- Who's involved (Actors and Workers)
- What's happening (Actions and Jobs)
- How things move around (Routes)
- Where things are stored (Storage)

## How Everything Connects

![A simple visualization would go here showing the relationships between classes]


At its heart, OMM models your manufacturing system through interconnected components that work together, just like your real facility. Here's how they relate:

- **Jobs** coordinate the production of **Products**
- **Products** are made from **Parts** using various **Resources**
- **Workers** operate the **Resources** to perform **Actions**
- Everything happens at specific **Locations**
- **Routes** connect different **Locations**
- **Storage** areas hold your **Products** and **Parts**

## Meet the Classes

Let's meet each major component of OMM.

### 🏭 Resources
Resources are your facility's workhorses - the physical equipment that gets things done. This includes:
- Machines (like CNC machines, 3D printers)
- Workstations (assembly areas, quality control stations)
- Vehicles (forklifts, automated guided vehicles)
- Conveyors (for moving materials)
- Robotic Arms
- Tools (handheld equipment)

:::tip
Think of Resources as anything that actively helps in manufacturing.
:::

### 📍 Locations
Locations are the "where" of your facility. They can be:
- Inside your facility (production areas, storage zones)
- Outside (supplier locations, customer sites)
- Connected by routes
- Associated with specific resources and activities

:::note
Depening on the required level of detail, OMM allows you to connect your resources to *indvidual* locations (e.g., a Location for each Machine), or *group* them to one location (e.g., all Machines belong to the same Location - your manufacturing plant). 
:::

### 👥 Actors & Workers
These represent the people directly or indirectly involved in your manufacturing system:
- **Actors** are any stakeholders (customers, suppliers, managers)
- **Workers** are specialized actors who actively work in production
  - They have specific roles and authorizations
  - They operate resources and perform actions
  - They can be assigned to specific locations

### ⚙️ Actions
Actions are the individual tasks that make up your manufacturing processes:
- Setting up machines
- Moving materials
- Assembly operations
- Quality checks
- Maintenance tasks  

:::tip
Think of Actions as the building blocks of your manufacturing processes.
:::

### 📦 Products & Parts
- **Products** are what you're making - your finished goods
- **Parts** are what you use to make products:
  - Raw materials
  - Purchased components
  - Work-in-progress items

### 📋 Jobs
Jobs are your master organizers. They:
- Track production of specific products
- Manage required resources and workers
- Schedule and coordinate actions
- Monitor progress and completion
- Handle priorities and due dates

:::tip
Think of Jobs as everything that needs to be done to fulfill an order.
:::

### 🗺️ Routes
Routes are the paths that connect different locations or resources:
- Used for moving materials and products
- Define paths for vehicles

:::note
You can create routes between *resources* (from Machine A to Workstation B) or between *internal* locations (if you chose to have *individual* locations per resource). You can also create routes between *external* locations (from your Manufacturing Facility to the Warehouse across the street). You can also mix-and-match *resources*, *interal locations*, and *external locations*. It's up to you!
:::

### 🏪 Storage
Storage areas are specialized locations for keeping your inventory:
- Warehouses for longer-term storage
- Buffer zones between operations
- Racks and shelving systems

## Real-World Example

Let's look at a simple example: Making a custom electric motor.

1. A **Job** is created when a **Customer** (Actor) orders the motor
2. The job specifies which **Parts** are needed (housing, rotor, stator)
3. **Workers** operate **Resources** (machines, tools) to perform **Actions**:
   - Machining the housing
   - Assembling components
   - Testing the motor
4. **Vehicles** or **Workers** move materials along **Routes** between **Locations** or **Resources**
5. Finished motors wait in **Storage** until shipping


## What's Next?

Now that you have a basic understanding of OMM, you can:
- Explore each component in more detail. See our [Reference](/docs/classes/index.md)
- Map your facility using OMM concepts
- Start implementing OMM in your systems or Digital Twins
- Use OMM to monitor and improve your operations

Remember, OMM is flexible and can be adapted to fit your specific manufacturing needs, whether you're running a small workshop or a large factory. You are encouraged to adapt, extend, and remix OMM to fit your specific use case. 