#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The Official Dynamixel SDK Manual is here.
# http://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/api_reference/python/python_porthandler/#python

import json
import dynamixel_sdk as dxlsdk

from .constant import _baudrates, _verbose_level, assert_verbosity
from .dxl_motor import DxlMotor
from .byteify import byteify


class DxlHelper(object):
    """The main class of this package.

    Attributes:
        verbosity: <int>
        port_handlers: {
            '/dev/ttyUSB':{'handler':PortHandler, 'baud rate':None}}
        packet_handlers: {2.0:PacketHandler}
        __motors: <dict> The ID is a key and motorInstance is a value.
    TODO:
        check alias when empty in json. Is None value correctly inside?
    """

    def __init__(self, preset_file, verbosity='minimal'):
        """Inits

        Args:
            preset_file: The path of the \'<preset>.json\' file
            verbosity: 'quiet' or 'minimal' or 'detailed'
        Raises:
            RuntimeError: If some motor has no ID
        """
        # Verbose
        assert_verbosity(verbosity)
        self.verbosity = _verbose_level[verbosity]

        # Load preset
        with open(preset_file, 'r') as f:
            preset = json.load(f, object_hook=byteify)

        ############################################
        #              Port Handlers
        ############################################
        # The 'PortHandler' requires 'device name' for initialization.
        # And the device name is different for each OS.
        #     windows: "COM1"
        #     linux: "/dev/ttyUSB0"
        #     mac: "/dev/tty.usbserial-*"

        self.port_handlers = {}
        # e.g.
        # {
        #     "/dev/ttyUSB0": {
        #         "handler": PortHandler,
        #         "baud rate": None
        # }

        # Open port
        for name in preset['ports']:
            self.__check_type_n_dupe('port', str, name, self.port_handlers)
            port_handler = dxlsdk.PortHandler(name)
            try:
                port_handler.openPort()
            except Exception as inst:
                print("Helper: [ERROR] " + inst.__str__())
                raise inst
            else:
                self.port_handlers[name] = {'handler': port_handler,
                                            'baud rate': None}
                if self.verbosity >= _verbose_level['detailed']:
                    print("Helper: Succeeded to open the port: \""+name+"\"")

        ############################################
        #             Packet Handlers
        ############################################
        # The 'PacketHandler' requires 'protocol version' for initialization.
        # KEY: 'protocol version', VALUE: 'packet_handler'

        # "auto" keywords
        if isinstance(preset["protocol versions"], list):
            # Duplicate cleaning
            protocol_set = set(preset["protocol versions"])
        elif preset["protocol versions"] == "auto":
            protocol_set = [1.0, 2.0]
        else:
            print("Helper: [ERROR] There is a typo in the protocol of the preset file.")
            raise NotImplementedError
        self.packet_handlers = {
            version: dxlsdk.PacketHandler(version) for version in protocol_set}

        ############################################
        #                 Motor
        ############################################

        # Motor List
        id_set = set()
        alias_set = set()
        motor_list = []
        for motor in preset['motors']:
            # ID Validation
            try:
                self.__check_type_n_dupe('motor.id', int, motor['id'], id_set)
            except KeyError:
                print("Helper: [ERROR] One motor has no ID.")
                print("        Please check again: "+preset_file)
                raise RuntimeError
            else:
                id_set.add(motor['id'])
            # Alias Validation
            try:
                if motor['alias']:
                    self.__check_type_n_dupe('motor.alias', str, motor['alias'], alias_set)
                    alias_set.add(motor['alias'])
                else:
                    motor['alias'] = None
            except KeyError:
                motor.update({'alias': None})
            # Clean list
            motor_list.append(motor)
            # {
            #     "id": 1,
            #     "alias": "joint_L1",
            #     "model": "XM430-W210"
            # }

        # KEY: 'robotID' or 'alias', VALUE: 'DxlMotor'
        self.__motors = {}
        logging = {'O': [], 'X': []}
        for motor in motor_list:
            motor_log = [motor['id'], motor['alias'], motor['model']]
            try:
                motorInstance = DxlMotor(
                    motor['id'], motor['alias'], motor['model'],
                    self.port_handlers, preset['baud rates'],
                    self.packet_handlers, verbosity=verbosity)
            except Exception as inst:  # to catch all errors
                logging['X'].append(motor_log)
                if self.verbosity >= _verbose_level['detailed']:
                    print("Helper: One motor setup was skipped.")
                    print("        The reason is: \""+inst.__str__()+"\"")
                    raise inst
            else:
                logging['O'].append(motor_log)
                self.__motors[motor['id']] = motorInstance
                if motor['alias']:
                    self.__motors[motor['alias']] = motorInstance
                if self.verbosity >= _verbose_level['detailed']:
                    print("Helper: One motor setup was completed.")

        ############################################
        #                 Log
        ############################################

        if self.verbosity >= _verbose_level['minimal']:
            print("Helper: All motor setups have been completed.")
            print("        Success: {} motor(s) / Fail: {} motor(s)"
                  .format(len(logging['O']), len(logging['X'])))
            for ox, logs in logging.items():
                logs.sort()
                for log in logs:
                    print("          ({}) id:{}, alias:{}, model:{}"
                          .format(ox, log[0], log[1], log[2]))

    def __del__(self):
        """Close the all ports."""
        for port in self.port_handlers.values():
            port['handler'].closePort()

    @staticmethod
    def __check_type_n_dupe(name, expected_type, value, list_like):
        """Check the type is correct and values ​​are not duplicated.

        Args:
            name: Required for the error message
            expected_type: The value should be this type.
            value: This is the value to be checked.
            list_like: The list you want to check for the duplicate.
        Raises:
            TypeError: If the \'value\' is not the \'expected_type\'
            ValueError: If \'list_like\' already has the same elem as \'value\'
        """
        if not isinstance(value, expected_type):
            print("Helper: [ERROR] \"{}\" must be \'{}\', not \'{}\'."
                  .format(name, expected_type.__name__, type(value).__name__))
            print("        Value: {}".format(value))
            raise TypeError
        elif value in list_like:
            print("Helper: [ERROR] Duplicate {} detected. Value: {}"
                  .format(name, value))
            raise ValueError

    def get_motor(self, id_) -> DxlMotor:
        """Get an instance of the DxlMotor.

        Args:
            id_: Motor ID
        """
        return self.__motors[id_]
