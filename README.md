# Easy Dynamixel Helper

![GitHub](https://img.shields.io/github/license/ryul1206/easy-dynamixel-helper.svg)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/ryul1206/easy-dynamixel-helper.svg)
[![CodeFactor](https://www.codefactor.io/repository/github/ryul1206/easy-dynamixel-helper/badge/master)](https://www.codefactor.io/repository/github/ryul1206/easy-dynamixel-helper/overview/master)

TODO: a badge of pypi release version (/pypi/v/:packageName.svg)

This helper is a wrapper for the Dynamixel-SDK. With this, configure and drive your motor more quickly. You do not need to know how the SDK works.

Supported language: Python

**[Warning]** Currently, I have not tested this helper. (The test will be on **July**)

TODO: korean readme

TODO: update figure (direct writing on the control table)

<!-- Your code ===> DXL Helper ===> Your motor(control table) -->

1. [특징](#특징)
2. [Getting Started](#Getting-Started)
    1. [Prerequisites](#Prerequisites)
    2. [Installation](#Installation)
3. [Simple Example](#Simple-Example)
4. [Tutorial](#Tutorial)
5. [Maintainers](#Maintainers)
6. [Contributions](#Contributions)
7. [Release Notes](#Release-Notes)
8. [Licenses](#Licenses)

<!-- https://gist.github.com/PurpleBooth/109311bb0361f32d87a2 -->

## 특징

- json 으로 연결 설정
- python 2, 3 지원
- 동일한 ID구성을 갖는 여러 대의 로봇 연결 지원
- 여러 개의 포트를 사용하는 로봇 지원

## Getting Started

### Prerequisites

You need to install the official [Dynamixel SDK](https://github.com/ROBOTIS-GIT/DynamixelSDK) before using this helper.

<details><summary>CLICK ME (Dynamixel SDK Installation)</summary>
<p>

1. Clone the official SDK repository into your custom folder, for example, I created `~/lib`.

    ```bash
    git clone https://github.com/ROBOTIS-GIT/DynamixelSDK.git
    ```

2. Go into the folder `/DynamixelSDK/python` of your cloned SDK.

    ```bash
    cd ${your_download_path}/DynamixelSDK/python
    ```

3. Run `setup.py` as administrator to install the library.

    ```bash
    sudo python setup.py install
    ```

</p>
</details>

### Installation

TODO: pip install will be update

## Simple Example

TODO: one motor

## Tutorial

TODO: detail tutorial / use new markdown.

## Maintainers

- **Hong-ryul Jung** _Initial work_ [ryul1206](https://github.com/ryul1206)
- **Il-ho Oh** _Initial work_ [ohilho](https://github.com/ohilho)

## Contributions

vscode `setting.json`

```json
"editor.tabSize": 4,
"[json]": {
    "editor.tabSize": 2
},
"python.linting.pylintEnabled": false,
"python.linting.pep8Enabled": true,
"python.linting.enabled": true
```

## Release Notes

[here](/CHANGELOG)

## Licenses

The contents of this repository are subject to the [MIT license](/LICENSE) by default, except as noted below.

- Dynamixel SDK is under the [Apache-2.0](https://github.com/ROBOTIS-GIT/DynamixelSDK/blob/master/LICENSE)
