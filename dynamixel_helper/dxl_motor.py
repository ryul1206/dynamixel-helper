#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import dynamixel_sdk as dxlsdk
from itertools import product

from .constant import _baudrates, _verbose_level, assert_verbosity
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
        assert_verbosity(verbosity)
        self.verbosity = _verbose_level[verbosity]

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
        control_table_path = pkg_directory + "/tables/"
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

        if self.verbosity >= _verbose_level['detailed']:
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
            NotImplementedError: If there is a typo in the baud rate of the preset file.
        """
        if self.verbosity >= _verbose_level['detailed']:
            print("Helper: [START] a validation of port and baud-rate.")
            print("           ==> ID:{}".format(self.id))
        # These are intended error!
        # So, change the verbosity level to 'quiet' temporarily.
        original_verbosity = self.verbosity
        if self.verbosity <= _verbose_level['minimal']:
            self.verbosity = _verbose_level['quiet']

        # "auto" keywords
        if isinstance(baud_rates, list):
            baud_list = baud_rates
        elif baud_rates == "auto":
            baud_list = _baudrates
        else:
            print("Helper: [ERROR] There is a typo in the baud rate of the preset file.")
            raise NotImplementedError

        # flags
        success = False
        failed_at_least_once = False

        # Try all combinations of (port, packet, baud)
        for port, packet in product(port_handlers, packet_handlers):
            port_info = port_handlers[port]
            self.port_handler = port_info['handler']
            self.packet_handler = packet_handlers[packet]

            # If baud rate is already set, try only that rate
            valid_baud = port_info['baud rate']
            baud_rates_to_try = [valid_baud] if valid_baud is not None else baud_list

            for baud in baud_rates_to_try:
                if valid_baud is None:
                    self.port_handler.setBaudRate(baud)

                pose, success = self.get_present_position()
                if success:
                    self.port_name = port
                    self.protocol = packet
                    self.baud = baud
                    if valid_baud is None:
                        port_info['baud rate'] = baud
                    break
                failed_at_least_once = True

            if success:
                break

        self.verbosity = original_verbosity

        if self.verbosity >= _verbose_level['detailed']:
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
            if self.verbosity >= _verbose_level['minimal']:
                print(self.packet_handler.getTxRxResult(dxl_result))
            return False
        elif dxl_error != 0:
            if self.verbosity >= _verbose_level['minimal']:
                print(self.packet_handler.getRxPacketError(dxl_error))
            return False
        return True

    ############################################
    #                 EEPROM
    ############################################
    def set_drive_mode(self, mode):
        """Change drive mode.(EEPROM)

        Return:
            <bool> True is a success. False is a fail.
        """
        if self.get_torque() is False:
            print("Helper: [ERROR] You can edit the EEPROM section ONLY when the torque is disabled.")
        dxl_result, dxl_error = self.packet_handler.write1ByteTxRx(
            self.port_handler, self.id, self.EEPROM['drive mode'], mode)
        return self.__is_success(dxl_result, dxl_error)

    def get_drive_mode(self) -> int:
        if self.get_torque() is False:
            print("Helper: [ERROR] You can edit the EEPROM section ONLY when the torque is disabled.")
        mode, dxl_result, dxl_error = self.packet_handler.read1ByteTxRx(
            self.port_handler, self.id, self.EEPROM['drive mode'])
        return mode, self.__is_success(dxl_result, dxl_error)

    def set_operating_mode(self, mode):
        """Change operating mode.(EEPROM)

        Return:
            <bool> True is a success. False is a fail.
        Raises:
            ValueError: If input mode is not supported
        """
        val = (0, 1, 3, 4, 5, 16)
        if mode not in val:
            print("Helper: [ERROR] This is incorrect operating mode.")
            print("        Supported modes are: "+str(val))
            raise ValueError(mode)
        if self.get_torque() is False:
            print("Helper: [ERROR] You can edit the EEPROM section ONLY when the torque is disabled.")
        dxl_result, dxl_error = self.packet_handler.write1ByteTxRx(
            self.port_handler, self.id, self.EEPROM['operating mode'], mode)
        return self.__is_success(dxl_result, dxl_error)

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

    def get_torque(self):
        """Read the torque.

        Return:
            [0]: <bool> True is enabled. False is disabled.
            [1]: <bool> True is a success. False is a fail.
        """
        torque, dxl_result, dxl_error = self.packet_handler.read1ByteTxRx(
            self.port_handler, self.id, self.RAM['torque enable'])
        return torque, self.__is_success(dxl_result, dxl_error)

    def set_goal_velocity(self, dxl_unit):
        """Write the [goal velocity] on the CONTROL TABLE.

        Args:
            dxl_unit: -(limit) ~ (limit) (1unit == 0.229rpm)
        Return:
            <bool> True is a success. False is a fail.
        """
        dxl_result, dxl_error = self.packet_handler.write4ByteTxRx(
            self.port_handler, self.id, self.RAM['goal velocity'],
            dxl_unit)
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

    def get_present_velocity(self):
        """Read the [present velocity] from the CONTROL TABLE.

        Return:
            [0]: <int> This position value is the DxlUnit(1unit == 0.229rpm).
            [1]: <bool> True is a success. False is a fail.
        """
        velocity, dxl_result, dxl_error = self.packet_handler.read4ByteTxRx(
            self.port_handler, self.id, self.RAM['present velocity'])
        return velocity, self.__is_success(dxl_result, dxl_error)

    def get_present_position(self):
        """Read the [present position] from the CONTROL TABLE.

        Return:
            [0]: <int> This position value is the DxlUnit(0 ~ 4095).
            [1]: <bool> True is a success. False is a fail.
        """
        position, dxl_result, dxl_error = self.packet_handler.read4ByteTxRx(
            self.port_handler, self.id, self.RAM['present position'])
        return position, self.__is_success(dxl_result, dxl_error)

    def set_profile_velocity(self, dxl_unit):
        """ Write the profile velocity on CONTROL TABLE

        Args:
            dxl_unit : 0 ~ 32767
                - Velocity-based mode : 0.229 [rev/min]
                - Time-based mode : 0.001 [sec]
        """
        dxl_result, dxl_error = self.packet_handler.write4ByteTxRx(
            self.port_handler, self.id, self.RAM['profile velocity'],
            dxl_unit)
        return self.__is_success(dxl_result, dxl_error)
    
    def set_profile_acceleration(self, dxl_unit):
        """ Write the profile acceleration on CONTROL TABLE

        Args:
            dxl_unit : 0 ~ 32767
                - Velocity-based mode : 214.577 [rev/min^2]
                - Time-based mode : 0.001 [sec]
        """
        dxl_result, dxl_error = self.packet_handler.write4ByteTxRx(
            self.port_handler, self.id, self.RAM['profile acceleration'],
            dxl_unit)
        return self.__is_success(dxl_result, dxl_error)
    
    def set_homing_offset(self, dxl_unit):
        """ Add homing offset to current Position

        Args: 
            dxl_unit : 0.08789 [deg] (-255 ~ 255 rev)
        """
        dxl_result, dxl_error = self.packet_handler.write4ByteTxRx(
            self.port_handler, self.id, self.EEPROM['homing offset'],
            dxl_unit)
        return self.__is_success(dxl_result, dxl_error)
    
    def get_present_current(self):
        """Read the [present current] from the CONTROL TABLE.

        Return:
            [0]: <int> This current value is the DxlUnit(1unit == 2.69mA).
            [1]: <bool> True is a success. False is a fail.
        """
        current, dxl_result, dxl_error = self.packet_handler.read2ByteTxRx(
            self.port_handler, self.id, self.RAM['present current'])
        return current, self.__is_success(dxl_result, dxl_error)

    def set_current_limit(self, dxl_unit):
        """ Write the current limit on motor controller

        Args:
            dxl_unit : 2.69 [mA] (0 ~ 2047)
        """
        if self.get_torque() is False:
            print("Helper: [ERROR] You can edit the EEPROM section ONLY when the torque is disabled.")
        dxl_result, dxl_error = self.packet_handler.write2ByteTxRx(
            self.port_handler, self.id, self.EEPROM['current limit'],
            dxl_unit)
        return self.__is_success(dxl_result, dxl_error)

    def set_pwm_limit(self, dxl_unit):
        """ Write the pwm limit on motor controller

        Args:
            dxl_unit : 0.113 [%] (0 ~ 885)
        """
        if self.get_torque() is False:
            print("Helper: [ERROR] You can edit the EEPROM section ONLY when the torque is disabled.")
        dxl_result, dxl_error = self.packet_handler.write2ByteTxRx(
            self.port_handler, self.id, self.EEPROM['pwm limit'],
            dxl_unit)
        return self.__is_success(dxl_result, dxl_error)
    
    def set_goal_current(self, dxl_unit):
        """Write the [goal current] on the CONTROL TABLE.

        Args:
            dxl_unit: 2.69 [mA] (-(Current Limit) ~ (Current Limit))
        """
        dxl_result, dxl_error = self.packet_handler.write2ByteTxRx(
            self.port_handler, self.id, self.RAM['goal current'],
            dxl_unit)
        return self.__is_success(dxl_result, dxl_error)
    
    def set_goal_pwm(self, dxl_unit):
        """Write the [goal pwm] on the CONTROL TABLE.

        Args:
            dxl_unit: 0.113 [%] (-(PWM Limit) ~ (PWM Limit))
        """
        dxl_result, dxl_error = self.packet_handler.write2ByteTxRx(
            self.port_handler, self.id, self.RAM['goal pwm'],
            dxl_unit)
        return self.__is_success(dxl_result, dxl_error)

    def set_moving_threshold(self, dxl_unit):
        if self.get_torque() is False:
            print("Helper: [ERROR] You can edit the EEPROM section ONLY when the torque is disabled.")
        dxl_result, dxl_error = self.packet_handler.write4ByteTxRx(
            self.port_handler, self.id, self.EEPROM['moving threshold'],
            dxl_unit)
        return self.__is_success(dxl_result, dxl_error)
    
    def moving(self):
        """Check If motor is moving or not based on moving threshold

        Return:
            [0]: <bool> True indicates moving motor. False vice versa
            [1]: <bool> True is a success. False is a fail.
        """
        moving, dxl_result, dxl_error = self.packet_handler.read1ByteTxRx(
            self.port_handler, self.id, self.RAM['moving'])
        
        return moving, self.__is_success(dxl_result, dxl_error)
