
# `preset.json`으로 모터 정의하기

🌏
[**English**](../en/multiple_ports.md) |
한국어

> 이번 튜토리얼은 여러 개의 USB 포트가 필요한 사람을 위한 것입니다. USB 선을 하나만 쓴다면 건너뛰어도 좋습니다.

- 다음 튜토리얼: [위치 제어](position_control.md)
- [튜토리얼 전체 목차로 돌아가기](TUTORIAL.md)

---

## 다중 USB 포트

[첫번째 튜토리얼](make_preset.md)에서 프리셋을 만드는 법을 배웠습니다. 아래와 같이 포트를 정의했던 게 기억나시나요?

```json
"ports":[ "/dev/ttyUSB0" ],
```

만약에 USB를 여러 개 꼽아서 사용하더라도 쉽게 쓸 수 있습니다. 그저 쉼표 `,`를 적고 추가하면 됩니다. 이때 중요한 것은 **어떤 포트에 어떤 모터가 연결되었는지 몰라도 된다**는 것입니다. 아래의 경우는 `/dev/ttyUSB0`과 `/dev/ttyUSB1`을 모두 사용하는 경우를 나타냅니다.

```json
"ports":[ "/dev/ttyUSB0", "/dev/ttyUSB1" ],
```

## 추가적인 모터

포트를 여러 개 쓴다는 것은 모터도 여러 개라는 뜻입니다. 다음은 모터가 추가된 `my_preset.json`입니다. 물론 프리셋 파일의 이름은 아무 이름이나 상관없습니다.

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

이제 USB 꼽는 순서로부터 자유로워지세요.😄

---

- 다음 튜토리얼: [위치 제어](position_control.md)
- [튜토리얼 전체 목차로 돌아가기](TUTORIAL.md)