# Release Notes

<!-- Tags
NEW : added new feature
FIXED : bug fixed
IMPROVED : feature improved
REMOVED : feature removed
OTHER
TESTED
-->

## 1.0.2 (2025.04.04)

* **FIXED**: Fix motor check bug when baudrate is already set (#4)

## 1.0.1 (2020.08.10)

* **NEW**: Add the control tables of `XL-320` and `AX-12W`

## 1.0.0 (2019.08.07)

(eng) Now you no longer need to know which motor is connected to which port. Auto-matching will solve this problem.

(kor) 이제는 더이상 어떤 모터가 어떤 포트에 연결되어 있는지 확인하지 않아도 됩니다. 자동매칭 기능이 이 문제를 해결해 줄 것입니다.

* **NEW**: **Auto matching process for the port, baud-rate, and protocol**
* **NEW**: **Auto keyword for the baud-rate, protocol**
* **NEW**: The basic [tutorials](./tutorial/en/TUTORIAL.md)
* **NEW**: Add the control table of `XM430-W250`
* **NEW**: set_drive_mode, set_operating_mode, get_torque, set_goal_velocity, get_present_velocity
* **REMOVED**: Old style json. Now, we are in the new version.
* **OTHER**: ([PEP 257](https://www.python.org/dev/peps/pep-0257/)) Comment for all functions
* **TESTED**: New style json.(XM430-W210, 2 ports, 2 motors, Ubuntu 18.04)
    - alias
    - verbosity levels
    - set_operating_mode
    - set_goal_velocity
    - get_torque
    - set_torque
    - set_goal_position
    - get_present_position

## 0.0.0 (2019.07.22)

1st Release! Yeah!

* **NEW**: Basic features (torque on/off and position command)
* **NEW**: Apply [CodeFactor](https://www.codefactor.io/) to manage code quality
* **NEW**: multilingual README and tutorials (We are using [Multilingual Markdown Generator](https://github.com/ryul1206/multilingual-markdown)!!)
* **TESTED**: Test basic features with actual motor(XM430-W210) in Python 2.x and 3.x
    - set_torque
    - set_goal_position
    - get_present_position

---

<!-- EXAMPLE

* **New** Prefer unused links for reference link label completions ([#414](https://github.com/yzhang-gh/vscode-markdown/issues/414)). Thanks, [Chris (@alshain)](https://github.com/alshain).
* **Fix**: TOC and fenced code blocks ([#425](https://github.com/yzhang-gh/vscode-markdown/issues/425)).
* **Other**: Sort KaTeX functions (lowercase first) ([#413](https://github.com/yzhang-gh/vscode-markdown/issues/413)).
* **Other**: Update KaTeX supported functions ([#416](https://github.com/yzhang-gh/vscode-markdown/issues/416)). Thanks again, [Li Yiming (@upupming)](https://github.com/upupming).

-->
