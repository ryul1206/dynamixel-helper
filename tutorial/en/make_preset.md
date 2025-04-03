
# Define Motors in `preset.json`

🌏
English |
[**한국어**](../ko/make_preset.md)

- Next Tutorial: [Torque On/Off](torque.md)
- [Back to the tutorial front page](TUTORIAL.md)

---

## Purpose

A preset file is a place to write down information about motors and ports. Then the helper analyzes the preset file and prepares the motors to use.

## Why Presets Needed

Connecting a motor to a computer, We need to know the port name, baud rate, protocol, the model name of the motor, which motor is in which port, and so on. Of course, you have to write these things in your program code.

However, writing these preferences in your code can get messy. By the way, the configuration is rarely modified unless the robot is changed. Besides, you should not change it by mistake. So it's not only clean but also safe to separate these settings into separate files. It helps prevent unnecessary mistakes, especially for beginners.

## Preview

The basic format of the preset file is shown below.

```json
{
    "ports":[  ],
    "baud rates":[  ],
    "protocol versions":[  ],
    "motors":[  ]
}
```

This type of file is called a [JSON](https://en.wikipedia.org/wiki/JSON). Don't worry if you're new to JSON. JSON is designed to make it easier for humans to understand data.

## Do It Yourself

The first of all, create a file `my_preset.json` in the folder you are working on. You can learn how to make your preset by following below.

### "ports"

Write down which USB port the motor is connected to. The names of the ports vary by the operating system. And also, the suffix numbers can be different. (If you want to know how to check the port name, search on [Google](https://www.google.com). This is beyond the scope of this article.)

- Windows: `COM1`
- Linux: `/dev/ttyUSB0`
- Mac: `/dev/tty.usbserial-*`

For example, if your operating system is Linux and connected on `/dev/ttyUSB0`, you can write:

```json
{
    "ports":[ "/dev/ttyUSB0" ],
}
```

If you are using multiple USB devices, I will explain that in [another tutorial](multiple_ports.md). For now, let's focus on just one motor.

### "baud rates"

Now let's write the baud rate. The default baud rate for Dynamixel is usually `57600`.

```json
{
    "ports":[ "/dev/ttyUSB0" ],
    "baud rates":[ 57600 ],
}
```

If you don't remember the baud rate, don't worry. Use the Auto-keyword and then the helper will find the right value for you! But caution that there is no `[ ]` when you write `"auto"`.

```json
{
    "ports":[ "/dev/ttyUSB0" ],
    "baud rates": "auto",
}
```

### "protocol versions"

Writing a protocol is the same. There are `1.0` and `2.0` protocol versions of Dynamixel, and different versions are used for each motor. All the latest Dynamixels are `2.0`.

```json
{
    "ports":[ "/dev/ttyUSB0" ],
    "baud rates": "auto",
    "protocol versions":[ 2.0 ],
}
```

Actually, you can also use the keyword `"auto"` in protocols.

```json
{
    "ports":[ "/dev/ttyUSB0" ],
    "baud rates": "auto",
    "protocol versions": "auto",
}
```

### "motors"

All motor has an ID and model name. You can also alias motors to make coding easier to read. If the motor ID is `0` and the model is `XM430-W210` and you want to call it `joint_0`, then the completed `my_preset.json` looks like this:

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

### Completed Preset

If you didn't use `"auto"`, the final `my_preset.json` would look like this:

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

- Next Tutorial: [Torque On/Off](torque.md)
- [Back to the tutorial front page](TUTORIAL.md)