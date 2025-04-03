
# Define Motors in `preset.json`

🌏
English |
[**한국어**](../ko/multiple_ports.md)

> This tutorial is for anyone who needs multiple USB ports. If you use only one USB cable, you can skip this.

- Next Tutorial: [Position Control](position_control.md)
- [Back to the tutorial front page](TUTORIAL.md)

---

## Multiple USB Ports

You learned how to create a preset in [the first tutorial](make_preset.md). Do you remember defining the port as shown below?

```json
"ports":[ "/dev/ttyUSB0" ],
```

Even if you use multiple USB devices, you can use them easily. Just add a comma `,` and append the new port.
The important thing is that **you don't need to know which motor is connected to which port**. The following is an example of using both `/dev/ttyUSB0` and `/dev/ttyUSB1`.

```json
"ports":[ "/dev/ttyUSB0", "/dev/ttyUSB1" ],
```

## Additional Motor

Using multiple ports means multiple motors. The below is `my_preset.json` with the motor added. Of course, you can rename the preset file.

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

Now be free from the order of USB plug-in.😄

---

- Next Tutorial: [Position Control](position_control.md)
- [Back to the tutorial front page](TUTORIAL.md)