
# `preset.json`으로 모터 정의하기

🌏
[**English**](../en/make_preset.md) |
한국어

- 다음 튜토리얼: [토크 켜기/끄기](torque.md)
- [튜토리얼 전체 목차로 돌아가기](TUTORIAL.md)

---

## 프리셋 파일의 용도

프리셋 파일은 모터와 포트에 대한 정보를 적어두는 곳입니다. 그러면 헬퍼가 알아서 프리셋 파일을 분석하고 모터를 사용할 수 있도록 준비를 마칩니다.

## 프리셋이 필요한 이유

모터를 컴퓨터와 연결하려면 포트(port) 이름, 보드레이트(baud rate), 프로토콜(protocol), 모터의 모델명, 어떤 모터가 어느 포트에 꼽혀 있는지 등등... 많은 귀찮은 것들을 알아야 합니다. 그리고 물론 이러한 것들을 프로그램 코드에 적어야 합니다.

하지만 이러한 환경설정들을 코드에 적으면 코드가 지저분해지는 문제가 있습니다. 그런데 환경설정은 로봇을 바꾸지 않으면 수정할 일이 거의 없습니다. 실수로 수정하는 일이 일어나서는 안됩니다. 그래서 각종 설정들을 별도의 파일로 따로 빼두는 것이 깨끗할 뿐만 아니라 안전합니다. 코드를 수정하다가 실수로 바꿀 일도 없으니까요.

## 프리셋의 형태(미리보기)

프리셋 파일의 기본 형태를 아래와 같습니다.

```json
{
    "ports":[  ],
    "baud rates":[  ],
    "protocol versions":[  ],
    "motors":[  ]
}
```

위와 같은 형태의 파일을 [json 파일](https://ko.wikipedia.org/wiki/JSON)이라고 합니다. json을 처음 접하더라도 걱정하지 마세요. json은 사람이 쉽게 데이터를 이해할 수 있도록 만들어진 것이니까요.

## 직접 해보기

프리셋의 각 구성 요소별로 하나씩 적어보겠습니다. 그전에 먼저 작업할 폴더에 `my_preset.json` 파일을 만들어 주세요. 내용을 쓰는 방법은 아래 내용을 따라하면서 배울 수 있습니다.

### "ports"

모터가 어떤 USB포트에 연결되어 있는지 적습니다. 포트의 이름은 운영체제(OS)마다 다릅니다. 그리고 USB의 연결상태에 따라 뒤에 붙는 숫자도 다를 수 있습니다. (포트 이름을 확인하는 방법까지 설명하면 너무 많기 때문에 [구글](https://www.google.com)에서 검색해주세요.)

- 윈도우(windows)라면 `COM1`
- 리눅스(linux)라면 `/dev/ttyUSB0`
- 맥OS(mac)라면 `/dev/tty.usbserial-*`

예를 들어, 지금 사용하는 운영체제가 리눅스이고, `/dev/ttyUSB0`에 연결되어 있다면 다음과 같이 쓸 수 있습니다.

```json
{
    "ports":[ "/dev/ttyUSB0" ],
}
```

여러 개의 USB를 꼽아서 사용하는 경우는 [다른 튜토리얼](multiple_ports.md)에서 다루겠습니다. 일단 이번에는 하나의 모터 연결에만 집중하겠습니다.

### "baud rates"

조금 전에 포트(port)를 적었으니 이제는 보드레이트(baud rate)를 적어보겠습니다. 다이나믹셀의 보드레이트의 기본값은 보통 `57600`입니다.

```json
{
    "ports":[ "/dev/ttyUSB0" ],
    "baud rates":[ 57600 ],
}
```

만약에 보드레이트가 기억나지 안 나더라도 걱정하지마세요. 오토 키워드를 적어두면 헬퍼가 알아서 맞는 값을 찾아줍니다! `"auto"`를 적을 때에는 `[ ]`가 없음에 주의하세요.

```json
{
    "ports":[ "/dev/ttyUSB0" ],
    "baud rates": "auto",
}
```

### "protocol versions"

프로토콜 작성도 동일합니다. 다이나믹셀의 프로토콜 버전은 `1.0`과 `2.0`이 있고, 모터마다 사용하는 버전이 다릅니다. 최신 다이나믹셀은 모두 `2.0`입니다.

```json
{
    "ports":[ "/dev/ttyUSB0" ],
    "baud rates": "auto",
    "protocol versions":[ 2.0 ],
}
```

사실 프로토콜에도 `"auto"` 키워드를 쓸 수 있습니다.

```json
{
    "ports":[ "/dev/ttyUSB0" ],
    "baud rates": "auto",
    "protocol versions": "auto",
}
```

### "motors"

모터 정보에는 ID와 모델명이 있습니다. 뿐만 아니라 코딩을 좀더 알아보기 쉽게 하기 위해서 모터의 별명(alias)을 지어줄 수도 있습니다. 모터 ID가 `0`이고 모델이 `XM430-W210`이면서 `joint_0`이라고 부르고 싶다면 완성된 `my_preset.json`은 다음과 같습니다.

```json
{
    "ports":[ "/dev/ttyUSB0" ],
    "baud rates": "auto",
    "protocol versions": "auto",
    "motors":[
        {
            "id": 0,
            "alias": "joint_0",
            "model": "XM430-W210"
        }
    ]
}
```

### 완성된 프리셋

만약 `"auto"`를 쓰지 않았다면 최종적으로 완성된 `my_preset.json`은 다음과 같습니다.

```json
{
    "ports":[ "/dev/ttyUSB0" ],
    "baud rates": [ 57600 ],
    "protocol versions":[ 2.0 ],
    "motors":[
        {
            "id": 0,
            "alias": "joint_0",
            "model": "XM430-W210"
        }
    ]
}
```

---

- 다음 튜토리얼: [토크 켜기/끄기](torque.md)
- [튜토리얼 전체 목차로 돌아가기](TUTORIAL.md)