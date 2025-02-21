# Sensor

A class to represent a Sensor in the manufacturing system.

    Sensors are devices that monitor and collect data about Resources, Locations, or other 
    manufacturing system components. They provide real-time or periodic measurements of 
    various parameters like temperature, pressure, position, speed, etc.

    Sensors are connected to various components in the manufacturing system:
    - Resources they monitor (machines, tools, conveyors)
    - Locations they observe
    - Products they inspect
    - Parts they measure

    **Best Practices**:
    - Define clear measurement ranges and units
    - Set appropriate sampling frequencies
    - Maintain calibration schedules
    - Monitor sensor health
    - Handle measurement errors
    - Track data history
    - Set alert thresholds
    - Validate measurements

    **Attributes**:
    | Name                  | Data Type           | Description                                                        |
    |-----------------------|---------------------|--------------------------------------------------------------------|
    | `name`                | `str`               | Human-readable name of the Sensor                                  |
    | `sensor_type`         | `str`               | Type of sensor (temperature, pressure, etc.)                       |
    | `measurement_unit`    | `str`               | Unit of measurement (°C, bar, mm, etc.)                           |
    | `range_min`           | `float`             | Minimum measurable value                                          |
    | `range_max`           | `float`             | Maximum measurable value                                          |
    | `accuracy`            | `float`             | Measurement accuracy (± value)                                     |
    | `sampling_rate`       | `float`             | Measurements per second                                           |
    | `last_reading`        | `float`             | Most recent measurement                                           |
    | `last_reading_time`   | `datetime`          | Timestamp of last measurement                                     |
    | `alert_min`           | `float`             | Lower threshold for alerts                                        |
    | `alert_max`           | `float`             | Upper threshold for alerts                                        |
    | `status`              | `str`               | Current sensor status (active, fault, etc.)                       |
    | `calibration_date`    | `datetime`          | Last calibration timestamp                                        |
    | `calibration_due`     | `datetime`          | Next calibration due date                                         |
    | `id`                  | `str`               | Unique identifier                                                 |
    | `location`            | `Location` or `Resource`         | Physical location of the sensor                                   |
    | `creation_date`       | `datetime`          | Timestamp when sensor was created                                 |
    | `last_modified`       | `datetime`          | Timestamp of last modification                                    |

    **Example Configuration**:
    ```python
    # Temperature sensor for a CNC machine
    temp_sensor = Sensor(
        name="CNC-1 Spindle Temperature",
        sensor_type="temperature",
        measurement_unit="°C",
        range_min=0.0,
        range_max=150.0,
        accuracy=0.1,
        sampling_rate=1.0,  # Hz (readings per second)
        alert_min=10.0,     # alert if below 10°C
        alert_max=120.0,    # alert if above 120°C
        resource=cnc_machine_1
    )

    # Vibration sensor for predictive maintenance
    vib_sensor = Sensor(
        name="Robot-2 Vibration Monitor",
        sensor_type="vibration",
        measurement_unit="mm/s",
        range_min=0.0,
        range_max=50.0,
        accuracy=0.01,
        sampling_rate=100.0,  # 100 Hz sampling
        alert_max=30.0,       # alert if vibration too high
        resource=robot_arm_2
    )

    # Position sensor for an AGV
    pos_sensor = Sensor(
        name="AGV-1 Position Tracker",
        sensor_type="position",
        measurement_unit="m",
        range_min=0.0,
        range_max=100.0,
        accuracy=0.005,
        sampling_rate=10.0,  # 10 Hz position updates
        resource=agv_1
    )
    ```

    :::note
    Sensors are used for monitoring manufacturing processes.
    :::


## Constructor

```python
def __init__(self, /, *args, **kwargs):
```

Initialize self.  See help(type(self)) for accurate signature.


## Example Usage

```python
# Create a new Sensor instance
Sensor(
    args=<_empty>
    kwargs=<_empty>
)
```
