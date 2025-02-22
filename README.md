# Open Manufacturing Model (OMM)

OMM creates seamless communication between machines, software, and people by providing a standardized vocabulary for manufacturing systems. Visit a human-readable version of this documentation here. 

## 🚀 Features

- **Common Language**: Standardized vocabulary for manufacturing systems
- **Digital Blueprint**: Create perfect digital twins of manufacturing facilities
- **Smart Manufacturing**: Connect and coordinate all manufacturing operations
- **Production Insights**: Track and optimize processes in real-time

## 📋 Requirements

- Python 3.8+
- Make sure you have `pandas` installed

## ⚡️ Quick Start

```bash
# Create a simple manufacturing model
from omm import WorkStation, Worker, Action

# Create a workstation
workstation = WorkStation(
    name="Assembly Station 1",
    capabilities=["manual_assembly"],
    max_capacity=1
)

# Create a worker
worker = Worker(
    name="Berry Gerrits",
    roles={"Assembler": ["manual_assembly"]}
)

# Create an action
action = Action(
    name="Assemble Widget",
    location=workstation,
    worker=worker,
    duration=0.5  # 30 minutes
)
```

## 📚 Documentation

Visit our [comprehensive documentation](https://omm.readthedocs.io) for:
- Detailed guides
- Examples
- Best practices
- Tutorials
- Our blog

## 🤝 Contributing

We welcome contributions! Hit me an [email](mailto:b.gerrits@distribute.company) or create a pull request. 

## ⭐️ Project Support

The Open Manufacturing Model is being developed by [dr. ir. Berry Gerrits](https://nl.linkedin.com/in/berry-gerrits) as part of the [NXTGEN Hightech](https://nxtgenhightech.nl/) Growth Fund, financed by the Dutch Government. More specifically, the Open Manufacturing Model is the result of activities carried out in the **Smart Industry 02 Autonomous Factory - Industrieel Cluster Oost** (**Factory2030**).

## 📝 License

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />
All Open Manufacturing Model documentation is licensed under
a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0
International License</a>.

## ✨ Acknowledgments

Special thanks to:
- [NXTGEN Hightech](https://nxtgenhightech.nl/) for project support
- All contributors and community members
- Factory2030 consortium members

## 📫 Contact

- Project Lead: [Berry Gerrits](https://nl.linkedin.com/in/berry-gerrits)
- Issue Tracker: [GitHub Issues](https://github.com/Factory2030/omm/issues)

## 🔗 Related Projects

- [Open Trip Model](https://www.opentripmodel.org/)
- [Digital Twin documentation](https://factory2030.github.io/digital-twin/)

---

<p align="center"> Made with ❤️ by the Factory2030 team</p>