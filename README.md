
# Dynamixel Helper

[![PyPI](https://img.shields.io/pypi/v/dynamixel-helper.svg)](https://pypi.org/project/dynamixel-helper/)
[![Total Downloads](https://pepy.tech/badge/dynamixel-helper)](https://pepy.tech/project/dynamixel-helper)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/dynamixel-helper)](https://pypi.org/project/dynamixel-helper/)
[![GitHub](https://img.shields.io/github/license/ryul1206/dynamixel-helper.svg)](https://github.com/ryul1206/dynamixel-helper/blob/main/LICENSE)

🌏
English |
[**한국어**](https://github.com/ryul1206/dynamixel-helper/blob/main/README.ko.md)

This helper is a wrapper for the Dynamixel-SDK. With this, configure and drive your motor more quickly. You do not need to know how the SDK works. In other words, this helper makes it easy to modify the control table.

```bash
pip install dynamixel_helper --user
```

**Table of Contents**

1. [Features](#-features)
1. [Simple Example](#-simple-example)
1. [Getting Started](#-getting-started)
    1. [Prerequisites](#prerequisites)
    1. [Installation](#installation)
1. [Tutorials](#-tutorials)
1. [Release Notes](#-release-notes)
1. [Current Coverage](#-current-coverage)
    1. [Model List](#model-list)
    1. [Control Table](#control-table)
1. [Contributing](#-contributing)
    1. [Style Guide](#style-guide)
1. [Maintainers](#-maintainers)
1. [Licenses](#-licenses)

## 💎 Features

- Baud rate auto-matching
- Protocol auto-matching
- Port auto-matching (*Easy connections in multi-USB*)
- Motor configurations in JSON format
- Support for Python 3 and 2
- Make your code simple and clean
- **Easy to use even for beginners.**

## 🐣 Simple Example

The following code is an example of turning on the motor torque.

```python
from dynamixel_helper import DxlHelper

helper = DxlHelper("preset/{my_robot}.json")
motor = helper.get_motor(0)  # id: 0
motor.set_torque(True)
```

## 🚀 Getting Started

### Prerequisites

1. **pip (package manager)**

    ```bash
    # Python 2
    sudo apt install python-pip
    python -m pip install -U pip
    # Python 3
    sudo apt install python3-pip
    python3 -m pip install -U pip
    ```

2. **Dynamixel SDK**

    **CAUTION💥**: Please install the `pip` **before** installing the `Dynamixel SDK`. Otherwise, when you install this `Dynamixel Helper`, you will get an dependency error of `Dynamixel SDK`.

    You need to install the official [Dynamixel SDK](https://github.com/ROBOTIS-GIT/DynamixelSDK) before using this helper.

    <details><summary>Click here: Dynamixel SDK Installation</summary>
    <p>

    1. Clone the official SDK repository into your custom folder, for example, I created `~/lib`.

        ```bash
        git clone https://github.com/ROBOTIS-GIT/DynamixelSDK.git
        ```

    2. Go into the folder `/DynamixelSDK/python` of your cloned SDK.

        ```bash
        cd ${your_download_path}/DynamixelSDK/python
        ```

    3. Run `setup.py` with `--user` option to install the library. Administrator privileges, a.k.a. `sudo`, are not recommended. More information [here](https://pages.charlesreid1.com/dont-sudo-pip/).

        ```bash
        python setup.py install --user
        ```

    </p>
    </details>

### Installation

Simply type `pip` command below to install this helper.

```bash
pip install dynamixel_helper --user
```

## 🌱 Tutorials

[Go to tutorials](https://github.com/ryul1206/dynamixel-helper/blob/main/tutorial/en/TUTORIAL.md)

## 🚩 Release Notes


[Go to release notes](https://github.com/ryul1206/dynamixel-helper/blob/main/CHANGELOG.md#Release-Notes)

## 🔭 Current Coverage

### Model List

- Tested models
  - [XM430-W210](http://emanual.robotis.com/docs/en/dxl/x/xm430-w210/#control-table-of-eeprom-area)
  - [XL430-W250](http://emanual.robotis.com/docs/en/dxl/x/xl430-w250/#control-table-of-eeprom-area)
- Non-tested models (Only the control tables are included.)
  - [AX-12W](https://emanual.robotis.com/docs/en/dxl/ax/ax-12w/#control-table-of-eeprom-area)
  - [XL-320](https://emanual.robotis.com/docs/en/dxl/x/xl320/#control-table-of-eeprom-area)

### Control Table

Different models have slightly different control tables. Please check the documentation for each model. Just click the model name above to go to the document.

- EEPROM section
    - drive mode (w)
    - operating mode (w)
- RAM section
    - torque (r/w)
    - goal velocity (w)
    - goal position (w)
    - present velocity (r)
    - present position (r)

## 💌 Contributing

- We will welcome whatever your contribution is!
- If you are planning to send a new `Pull request`, please send them into the `develop` Branch.😍

### Style Guide

> This style guide is only a recommendation, never more important than your interest and contributions.

- Our default Python style is [PEP 8](https://www.python.org/dev/peps/pep-0008/).
- If you use [VSCode](https://code.visualstudio.com/) as your code editor, please refer to the following settings. This setting is a part of our `setting.json`.

    ```json
    {
        "editor.tabSize": 4,
        "[json]": {
            "editor.tabSize": 2
        },
        "python.linting.pylintEnabled": false,
        "python.linting.pep8Enabled": true,
        "python.linting.enabled": true
    }
    ```

## 🔧 Maintainers

- **Hong-ryul Jung** _Initial work_ [ryul1206](https://github.com/ryul1206)
- **Il-ho Oh** _Initial work_ [ohilho](https://github.com/ohilho)

## 📜 Licenses

The contents of this repository are subject to the [MIT License](https://github.com/ryul1206/dynamixel-helper/blob/main/LICENSE) by default, except as noted below.

- Dynamixel SDK is under the [Apache-2.0](https://github.com/ROBOTIS-GIT/DynamixelSDK/blob/main/LICENSE)
