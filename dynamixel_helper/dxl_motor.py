#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import dynamixel_sdk as dxlsdk
from itertools import product

import constant
from .byteify import byteify


class DxlMotor(object):
    """One DxlMotor represents one motor.

    The DxlMotor directly modifies its control table.

    Attributes:
        verbosity: <int>
        id: <int>
        alias: <str>
        model: <str>
        port_handler: <dynamixel_sdk...PortHandler object>
        packet_handler: <dynamixel_sdk...PacketHandler object>
        EEPROM: <dict> Address of EEPROM section
        RAM: <dict> Address of RAM section
    """

    def __init__(self, id_, alias, model, port_handlers, baud_rates,
                 packet_handlers, verbosity):
        """Inits

        Args:
            id_: .
            alias: .
            model: .
            port_handlers: .
            baud_rates: .
            packet_handlers: .
            verbosity: 'quiet' or 'minimal' or 'detailed'
        Raises:
            RuntimeError: If the verbosity string is not in verbose_level
        """
        # Verbose
        constant.assert_verbosity(verbosity)
        self.verbosity = constant.verbose_level[verbosity]

        # Properties
        self.id = id_
        self.alias = alias
        self.model = model
        self.port_name = ""
        self.protocol = None
        self.baud = None

        # Load control tables
        # TODO customizable path
        pkg_directory = os.path.dirname(os.path.abspath(__file__))
        control_table_path = pkg_directory + "/config/"
        control_table_file = control_table_path + model + ".json"

        with open(control_table_file, 'r') as f:
            control_table = json.load(f, object_hook=byteify)
        self.EEPROM = control_table['eeprom']
        self.RAM = control_table['ram']

        # port_handlers: {'/dev/ttyUSB0': {'handler:xx, 'baud rate':None}}
        # packet_handlers: {2.0: xx}
        self.port_handler = None
        self.packet_handler = None
        self.__find_correct_handle(port_handlers, baud_rates, packet_handlers)

        if self.verbosity >= constant.verbose_level['detailed']:
            print("Helper: One motor instance was created. id: "+str(self.id))

    def __eq__(self, other):
        """Compare with ID"""
        return self.id == other.id

    def __find_correct_handle(self, port_handlers, baud_rates, packet_handlers):
        """Try all possibilities and save success case.

        1. Get all combinations of (port, packet) tuples
        2. Find correct baud rate
           "setBaudRate()" returns True if the baud value is "possible".
           Without a motor, we don't know which value is actually matched.

        Raises:
            RuntimeError: If there is no matched options
        """
        if self.verbosity >= constant.verbose_level['detailed']:
            print("Helper: [START] a validation of port and baud-rate.")
            print("           ==> ID:{}".format(self.id))
        # These are intended error!
        # So, change the verbosity level to 'quiet' temporarily.
        original_verbosity = self.verbosity
        if self.verbosity <= constant.verbose_level['minimal']:
            self.verbosity = constant.verbose_level['quiet']

        success = False
        failed_at_least_once = False
        
        # Get all cases of (port, packet) tuples
        for port, packet in product(port_handlers, packet_handlers):
            self.port_handler = port_handlers[port]['handler']
            self.packet_handler = packet_handlers[packet]

            original_baud = port_handlers[port]['baud rate']

            for baud in baud_rates:
                if original_baud is None:
                    self.port_handler.setBaudRate(baud)
                else:
                    continue
                pose, success = self.get_present_position()
                if success:
                    self.port_name = port
                    self.protocol = packet
                    self.baud = baud
                    port_handlers[port]['baud rate'] = baud
                    break
                else:
                    failed_at_least_once = True
            if success:
                break

        self.verbosity = original_verbosity

        if self.verbosity >= constant.verbose_level['detailed']:
            if failed_at_least_once:
                print("Helper: ⤷ Do not worry, if the message you are seeing is")
                print("            \"[TxRxResult] There is no status packet!\".")
                print("          This is the intended error. This is an error generated")
                print("          by the process of matching the port and baud rate automatically.")
                print("          Only displayed when verbosity is \"detailed\".")
            print("Helper: [FINISH] the validation of port and baud-rate.")
            print("           ==> ID:{}".format(self.id))

        if not success:
            print("Helper: [ERROR] ID:{}, Alias:{}, Model:{}".format(
                self.id, self.alias, self.model))
            print("        Motor connection failed.")
            print("        Please check the connection or \"<preset>.json\".")
            print("        Common causes of this phenomenon like below:")
            print("          1. The motor is turned OFF.")
            print("          2. Using a different baud rate in the same port.")
            print("          3. Some other descriptions are incorrect in \"<preset>.json\".")
            raise RuntimeError

    def __is_success(self, dxl_result, dxl_error):
        """Handles all responses received from the motor.

        Args:
            dxl_result, dxl_error:
                These values are handled by the SDK. Check the protocol
                documentation and SDK source code for more information.
        Return:
            <bool> True is a success. False is a fail.
        """
        if dxl_result != dxlsdk.COMM_SUCCESS:
            # [TxRxResult] There is no status packet!
            # motor power not connected
            if self.verbosity >= constant.verbose_level['minimal']:
                print(self.packet_handler.getTxRxResult(dxl_result))
            return False
        elif dxl_error != 0:
            if self.verbosity >= constant.verbose_level['minimal']:
                print(self.packet_handler.getRxPacketError(dxl_error))
            return False
        return True

    ############################################
    #                 EEPROM
    ############################################

    ############################################
    #                 RAM
    ############################################
    def set_torque(self, enable):
        """Enable or Disable the torque.

        Args:
            enable: True(turn on), False(turn off)
        Return:
            <bool> True is a success. False is a fail.
        """
        dxl_result, dxl_error = self.packet_handler.write1ByteTxRx(
            self.port_handler, self.id, self.RAM['torque enable'],
            1 if enable else 0)
        return self.__is_success(dxl_result, dxl_error)

    def set_goal_position(self, dxl_unit):
        """Write the [goal position] on the CONTROL TABLE.

        Args:
            dxl_unit: 0 ~ 4095
        Return:
            <bool> True is a success. False is a fail.
        """
        dxl_result, dxl_error = self.packet_handler.write4ByteTxRx(
            self.port_handler, self.id, self.RAM['goal position'],
            dxl_unit)
        return self.__is_success(dxl_result, dxl_error)

    def get_present_position(self):
        """Read the [present position] from the CONTROL TABLE.

        Args:
            dxl_unit: 0 ~ 4095
        Return:
            <int> This position value is the DxlUnit(0 ~ 4095).
            <bool> True is a success. False is a fail.
        """
        position, dxl_result, dxl_error = self.packet_handler.read4ByteTxRx(
            self.port_handler, self.id, self.RAM['present position'])
        return position, self.__is_success(dxl_result, dxl_error)
