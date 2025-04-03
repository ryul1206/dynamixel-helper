<!---------------------------->
<!-- multilingual suffix: en, ko -->
<!---------------------------->

<!-- [en] -->
# Position Control
<!-- [ko] -->
# 위치 제어
<!-- [common] -->

🌏
<!-- [en] -->
English |
[**한국어**](../ko/position_control.md)
<!-- [ko] -->
[**English**](../en/position_control.md) |
한국어
<!-- [common] -->

<!-- [en] -->
- Next Tutorial: Not yet.
- [Back to the tutorial front page](TUTORIAL.md)
<!-- [ko] -->
- 다음 튜토리얼: 준비되지 않았습니다.
- [튜토리얼 전체 목차로 돌아가기](TUTORIAL.md)
<!-- [common] -->

---

<!-- [en] -->
The basic `Operating Mode` of Dynamixel is `Position Control Mode`. So we used the remainder of 4096. 4096 represent one round in Dynamixel unit. For details, see the control table of each motor.
<!-- [ko] -->
다이나믹셀의 기본 `Operating Mode`는 `위치제어 모드(Position Control Mode)`입니다. 그래서 한바퀴를 나타내는 4096의 나머지를 사용하였습니다. 4096의 단위는 다이나믹셀 단위(unit)입니다. 자세한 내용은 각 모터의 컨트롤 테이블을 보아주세요.
<!-- [common] -->

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

<!-- [en] -->
- Next Tutorial: Not yet.
- [Back to the tutorial front page](TUTORIAL.md)
<!-- [ko] -->
- 다음 튜토리얼: 준비되지 않았습니다.
- [튜토리얼 전체 목차로 돌아가기](TUTORIAL.md)
<!-- [common] -->
