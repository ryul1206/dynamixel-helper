<!---------------------------->
<!-- multilingual suffix: en, ko -->
<!---------------------------->

<!-- [en] -->
# Define Motors in `preset.json`
<!-- [ko] -->
# `preset.json`으로 모터 정의하기
<!-- [common] -->

🌏
<!-- [en] -->
English |
[**한국어**](../ko/multiple_ports.md)
<!-- [ko] -->
[**English**](../en/multiple_ports.md) |
한국어
<!-- [common] -->

<!-- [en] -->
> This tutorial is for anyone who needs multiple USB ports. If you use only one USB cable, you can skip this.

- Next Tutorial: [Position Control](position_control.md)
- [Back to the tutorial front page](TUTORIAL.md)
<!-- [ko] -->
> 이번 튜토리얼은 여러 개의 USB 포트가 필요한 사람을 위한 것입니다. USB 선을 하나만 쓴다면 건너뛰어도 좋습니다.

- 다음 튜토리얼: [위치 제어](position_control.md)
- [튜토리얼 전체 목차로 돌아가기](TUTORIAL.md)
<!-- [common] -->

---

<!-- [en] -->
## Multiple USB Ports

You learned how to create a preset in [the first tutorial](make_preset.md). Do you remember defining the port as shown below?
<!-- [ko] -->
## 다중 USB 포트

[첫번째 튜토리얼](make_preset.md)에서 프리셋을 만드는 법을 배웠습니다. 아래와 같이 포트를 정의했던 게 기억나시나요?
<!-- [common] -->

```json
"ports":[ "/dev/ttyUSB0" ],
```

<!-- [en] -->
Even if you use multiple USB devices, you can use them easily. Just add a comma `,` and append the new port.
The important thing is that **you don't need to know which motor is connected to which port**. The following is an example of using both `/dev/ttyUSB0` and `/dev/ttyUSB1`.
<!-- [ko] -->
만약에 USB를 여러 개 꼽아서 사용하더라도 쉽게 쓸 수 있습니다. 그저 쉼표 `,`를 적고 추가하면 됩니다. 이때 중요한 것은 **어떤 포트에 어떤 모터가 연결되었는지 몰라도 된다**는 것입니다. 아래의 경우는 `/dev/ttyUSB0`과 `/dev/ttyUSB1`을 모두 사용하는 경우를 나타냅니다.
<!-- [common] -->

```json
"ports":[ "/dev/ttyUSB0", "/dev/ttyUSB1" ],
```

<!-- [en] -->
## Additional Motor
<!-- [ko] -->
## 추가적인 모터
<!-- [common] -->

<!-- [en] -->
Using multiple ports means multiple motors. The below is `my_preset.json` with the motor added. Of course, you can rename the preset file.
<!-- [ko] -->
포트를 여러 개 쓴다는 것은 모터도 여러 개라는 뜻입니다. 다음은 모터가 추가된 `my_preset.json`입니다. 물론 프리셋 파일의 이름은 아무 이름이나 상관없습니다.
<!-- [common] -->

```json
{
    "ports":[ "/dev/ttyUSB0", "/dev/ttyUSB1" ],
    "baud rates": "auto",
    "protocol versions": "auto",
    "motors":[
        {
            "id": 0,
            "alias": "joint_0",
            "model": "XM430-W210"
        },
        {
            "id": 1,
            "alias": "joint_1",
            "model": "XM430-W210"
        }
    ]
}
```

<!-- [en] -->
Now be free from the order of USB plug-in.😄
<!-- [ko] -->
이제 USB 꼽는 순서로부터 자유로워지세요.😄
<!-- [common] -->

---

<!-- [en] -->
- Next Tutorial: [Position Control](position_control.md)
- [Back to the tutorial front page](TUTORIAL.md)
<!-- [ko] -->
- 다음 튜토리얼: [위치 제어](position_control.md)
- [튜토리얼 전체 목차로 돌아가기](TUTORIAL.md)
<!-- [common] -->
