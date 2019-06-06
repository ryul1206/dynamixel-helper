#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dynamixel_sdk as dxlsdk
import json
from getch import getch_exit, getch_ask
import random
import string
import copy


def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def byteify(input):
    # Thanks to Mark Amery from StackOverflow.
    # https://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-from-json
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


class DxlHelper:
    def __init__(self, preset_file):
        # Load preset
        preset = json.load(open(preset_file, 'r'), object_hook=byteify)

        # The number of connections (ports)
        # If you use 2 ports, ttyUSB0 and ttyUSB1, num_port == 2.
        num_port = len(preset)

        ############################################
        #              Port Handlers
        ############################################
        # The 'PortHandler' requires 'device name' for initialization.
        # And the device name is different for each OS.
        #     windows: "COM1"
        #     linux: "/dev/ttyUSB0"
        #     mac: "/dev/tty.usbserial-*"
        # TODO try except (AttributeError)
        self.port_handlers = [dxlsdk.PortHandler(
            preset[i]['device']) for i in range(num_port)]

        for i in range(num_port):
            name = preset[i]['device']
            # Open port
            if self.port_handlers[i].openPort():
                print("Succeeded to open the port: " + name)
            else:
                getch_exit("Failed to open the port: " + name)
            # Set baudrate
            if self.port_handlers[i].setBaudRate(preset[i]['baudrate']):
                print("Succeeded to change the baudrate: " + name)
            else:
                getch_exit("Failed to change the baudrate: " + name)

        ############################################
        #             Packet Handlers
        ############################################
        # The 'PacketHandler' requires 'protocol version' for initialization.
        # We can find 'packet_handler' with 'port_idx'
        self.packet_handlers = []
        packet_hd = {}
        for i in range(num_port):
            version = preset[i]['protocol_version']
            # TODO try except (AttributeError)
            if version not in packet_hd:
                packet_hd[version] = dxlsdk.PacketHandler(version)
            self.packet_handlers.append(packet_hd[version])

        ############################################
        #                 Motor
        ############################################
        self.motors_alias = {}
        self.motors_id = {}
        for port_idx in range(num_port):
            for m in preset[port_idx]['motors']:
                # Port number: int
                motor = copy.deepcopy(m)
                motor.update({'port': port_idx})
                # Empty alias
                if len(motor['alias']) == 0:
                    motor['alias'] = random_string()
                # Alias
                if motor['alias'] in self.motors_alias:
                    getch_exit("[Error] Duplicate Motor Alias Exists")
                else:
                    self.motors_alias[motor['alias']] = motor
                # ID
                if motor['id'] in self.motors_id:
                    getch_exit("[Error] Duplicate Motor ID Exists")
                else:
                    self.motors_id[motor['id']] = motor

        # Load control tables
        ctable_path = "../config/control_table/"
        self.ctables = {}
        for key in self.motors_id:
            model = self.motors_id[key]['model']
            # Check that already loaded
            if model in self.ctables:
                continue
            # Check that the file exists
            ctable_file = ctable_path + model + ".json"
            ctable = json.load(open(ctable_file, 'r'), object_hook=byteify)
            self.ctables[model] = ctable
            # TODO Verify the key of control table is correct

        print("Succeeded to read the motor config! \
            You have {} motor(s).".format(len(self.motors_id)))

    def __del__(self):
        # Close ports
        for port in self.port_handlers:
            port.closePort()

    def _is_success(self, packet_handler, dxl_result, dxl_error):
        if dxl_result != dxlsdk.COMM_SUCCESS:
            print(packet_handler.getTxRxResult(dxl_result))
            return False
        elif dxl_error != 0:
            print(packet_handler.getRxPacketError(dxl_error))
            return False
        else:
            return True

    def _find_motor(self, alias_or_id):
        if isinstance(alias_or_id, str):  # Alias
            return self.motors_alias[alias_or_id]
        else:  # ID
            return self.motor_id[alias_or_id]

    def _find_four(self, alias_or_id):
        motor = self._find_motor(alias_or_id)
        addr = self.catbles[mtr['model']]
        porthd = self.port_handlers[mtr['port']]
        packethd = self.packet_handlers[mtr['port']]
        return motor['id'], addr, porthd, packethd

    def set_torque(self, alias_or_id, enable):
        mid, addr, porthd, packethd = self._find_four(alias_or_id)
        dxl_result, dxl_error = packethd.write1ByteTxRx(
            porthd, mid, addr['ram']['torque enable'], 1 if enable else 0)
        return self._is_success(packethd, dxl_result, dxl_error)

    def set_goal_position(self, alias_or_id, dxl_unit):
        mid, addr, porthd, packethd = self._find_four(alias_or_id)
        dxl_result, dxl_error = packethd.write4ByteTxRx(
            porthd, mid, addr['ram']['goal position'], dxl_unit)
        return self._is_success(packethd, dxl_result, dxl_error)

    def get_present_position(self, alias_or_id):
        mid, addr, porthd, packethd = self._find_four(alias_or_id)
        position, dxl_result, dxl_error = packethd.read4ByteTxRx(
            porthd, mid, addr['ram']['present position'])
        return position, self._is_success(packethd, dxl_result, dxl_error)


if __name__ == "__main__":
    # Example code
    helper = DxlHelper("../config/preset/example_2port_4motor.json")

    # Enable Dynamixel torque
    motor_id = 1
    goals = [10, 4000]
    index = 0

    if helper.set_torque(motor_id, True):
        print("Successfully connected: Dynamixel ID {}".format(motor_id))

    count = 0
    while count < 10:
        print("Loop {}".format(count))
        getch_ask()

        helper.set_goal_position(index)

        while True:
            # Read present position
            position, result = helper.get_present_position()
            print("[ID:%03d] GoalPos:%03d  PresPos:%03d" %
                  (motor_id, goals[index], position))
            # Threshold
            if not abs(goals[index] - position) > 20:
                break

        # Change goal position
        index = (index + 1) % 2

    # Disable Dynamixel Torque
    helper.set_torque(motor_id, False)
    getch_exit("Example code was finished.")
