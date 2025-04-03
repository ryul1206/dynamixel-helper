
# Torque On/Off

🌏
English |
[**한국어**](../ko/torque.md)

- Next Tutorial: [Multiple USB ports](multiple_ports.md)
- [Back to the tutorial front page](TUTORIAL.md)

---

# Control with ID

In the previous tutorial, we created `my_preset.json` for one motor. Now we are going to change the torque of this motor. Create a new Python file named `torque.py`.

> Make sure the motor power is on before executing the code below.

```python
from dynamixel_helper import DxlHelper

helper = DxlHelper("my_preset.json")

motor_id = 0
motor = helper.get_motor(motor_id)
motor.set_torque(True)
```

Now let's do it. Opening a port on Linux requires `root` permission, so I am going to add a `sudo` command.

```bash
sudo python torque.py
```

Since the program was terminated without turning off the torque, the torque of the motor will remain on. You can turn off the torque simply by replacing the last line above with:

```python
motor.set_torque(False)
```

## Control with Alias

You ​​can define an alias in `my_preset.json` and use like an ID.

```python
from dynamixel_helper import DxlHelper

helper = DxlHelper("my_preset.json")

motor = helper.get_motor('joint_0')
motor.set_torque(True)
```

---

- Next Tutorial: [Multiple USB ports](multiple_ports.md)
- [Back to the tutorial front page](TUTORIAL.md)