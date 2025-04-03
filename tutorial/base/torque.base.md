<!---------------------------->
<!-- multilingual suffix: en, ko -->
<!---------------------------->

<!-- [en] -->
# Torque On/Off
<!-- [ko] -->
# 토크 켜기/끄기
<!-- [common] -->

🌏
<!-- [en] -->
English |
[**한국어**](../ko/torque.md)
<!-- [ko] -->
[**English**](../en/torque.md) |
한국어
<!-- [common] -->

<!-- [en] -->
- Next Tutorial: [Multiple USB ports](multiple_ports.md)
- [Back to the tutorial front page](TUTORIAL.md)
<!-- [ko] -->
- 다음 튜토리얼: [다중 USB 포트](multiple_ports.md)
- [튜토리얼 전체 목차로 돌아가기](TUTORIAL.md)
<!-- [common] -->

---

<!-- [en] -->
# Control with ID

In the previous tutorial, we created `my_preset.json` for one motor. Now we are going to change the torque of this motor. Create a new Python file named `torque.py`.

> Make sure the motor power is on before executing the code below.
<!-- [ko] -->
# ID로 제어하기

이전 튜토리얼에서 하나의 모터를 위한 `my_preset.json`을 만들었습니다. 이제 우리는 이 모터의 토크를 변경해보겠습니다. `torque.py`라는 이름으로 새 파이썬 파일을 만들어 주세요.

> 아래의 코드를 실행하기 전에 모터의 전원이 켜져 있는지 확인하세요.
<!-- [common] -->

```python
from dynamixel_helper import DxlHelper

helper = DxlHelper("my_preset.json")

motor_id = 0
motor = helper.get_motor(motor_id)
motor.set_torque(True)
```

<!-- [en] -->
Now let's do it. Opening a port on Linux requires `root` permission, so I am going to add a `sudo` command.
<!-- [ko] -->
이제 실행해 봅시다. 리눅스에서 포트를 여는 행위는 `root` 권한이 필요하기 때문에 `sudo` 명령을 붙이겠습니다.
<!-- [common] -->

```bash
sudo python torque.py
```

<!-- [en] -->
Since the program was terminated without turning off the torque, the torque of the motor will remain on. You can turn off the torque simply by replacing the last line above with:
<!-- [ko] -->
이 프로그램은 토크를 끄지 않고 종료되었기 때문에, 모터의 토크는 계속 켜져 있을 것입니다. 위의 마지막 줄을 다음과 같이 바꾸면 간단하게 토크를 끌 수 있습니다.
<!-- [common] -->

```python
motor.set_torque(False)
```

<!-- [en] -->
## Control with Alias

You ​​can define an alias in `my_preset.json` and use like an ID.
<!-- [ko] -->
## 별칭으로 제어하기

`my_preset.json`에서 별칭(Alias)를 정의하여 ID와 동일하게 사용할 수 있습니다.
<!-- [common] -->

```python
from dynamixel_helper import DxlHelper

helper = DxlHelper("my_preset.json")

motor = helper.get_motor('joint_0')
motor.set_torque(True)
```

---

<!-- [en] -->
- Next Tutorial: [Multiple USB ports](multiple_ports.md)
- [Back to the tutorial front page](TUTORIAL.md)
<!-- [ko] -->
- 다음 튜토리얼: [다중 USB 포트](multiple_ports.md)
- [튜토리얼 전체 목차로 돌아가기](TUTORIAL.md)
<!-- [common] -->
