
# Position Control

🌏
English |
[**한국어**](../ko/position_control.md)

- Next Tutorial: Not yet.
- [Back to the tutorial front page](TUTORIAL.md)

---

The basic `Operating Mode` of Dynamixel is `Position Control Mode`. So we used the remainder of 4096. 4096 represent one round in Dynamixel unit. For details, see the control table of each motor.

```python
from dynamixel_helper import DxlHelper

helper = DxlHelper("my_preset.json")

motor_id = 0
motor = helper.get_motor(motor_id)
motor.set_torque(True)

dxl_unit, res = motor.get_present_position()
motor.set_goal_position((dxl_unit + 2000) % 4096)
```

---

- Next Tutorial: Not yet.
- [Back to the tutorial front page](TUTORIAL.md)