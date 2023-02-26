"""Module providing a high level API for working with the programmable electronic load devices of HOECHERL&HACKL ZS506.

This module uses the serial port for communicating with the programmable electronic load.
"""

import serial
import time
import inspect
import logging
from math import pow
from .about import __package__

# Access the logger created in __init__.py
logger = logging.getLogger(__package__)


class HHPEL:
    """
    Class for controlling a HOECHERL&HACKL ZS506 programmable electronic load.

    Attributes:
        port_name (str): String with the serial port, e.g. 'COM4'.
        is_connected (bool): Indicates if the programmable electronic load is connected or not.
        pel_com (Serial): Handler to the serial port.
    """

    def __init__(self, port_name):
        """
        Initializes the different components to establish the connection with the programmable electronic load.

        Args:
            port_name (str): String with the serial port, e.g. 'COM4'.

        Raises:
            RuntimeError: If the connection couldn't be established.
        """
        self.port_name = port_name
        self.is_connected = False
        self.pel_com = None
        self.configured_current = 0
        self.last_current_range = 1
        try:
            pel_com = serial.Serial(
                port=port_name,
                baudrate=9600,
                parity=serial.PARITY_EVEN,
                stopbits=serial.STOPBITS_TWO,
                bytesize=serial.EIGHTBITS
            )
            self.pel_com = pel_com
            self.is_connected = True
            logger.info(f'Connection with programmable electronic load successful on serial port {self.port_name}')
        except serial.SerialException:
            error_text = f'Not possible to open serial port {port_name} {self._line()}'
            logger.error(error_text)
            self.pel_com = None
            self.is_connected = False
            raise RuntimeError(error_text) from None

    @staticmethod
    def _line():

        # Returns the line of the main script from where a function of this file was called
        # The number x in inspect.stack()[x] indicates the level of the caller:
        #  1 means that we access the first caller
        #  2 means that we access the second caller (the caller of the caller)
        init_level = 2
        caller = inspect.stack()[init_level]
        while caller.filename.split('\\')[-1] == 'hhpel.py':
            init_level += 1
            caller = inspect.stack()[init_level]
        return f'(line {caller.lineno})'

    def _check_pel_connected(self):
        if not self.is_connected:
            error_text = f'Can not execute the command requested, connection with the programmable electronic load ' \
                         f'is closed {self._line()}'
            logger.error(error_text)
            raise RuntimeError(error_text)

    def _convert_to_float(self, value, error_message):
        try:
            value = float(value)
        except TypeError:
            error_text = f'{error_message} {value} {self._line()}'
            logger.error(error_text)
            raise RuntimeError(error_text)
        return value

    def _mode_resistance(self):
        self.send_command('MODE:RES')
        logger.debug(f'Programmable electronic load is set to constant resistance mode')

    def _mode_current(self):
        self.send_command('MODE:CURR')
        logger.debug(f'Programmable electronic load is set to constant current mode')

    def read_identification(self):
        """Reads programmable electronic load identification.

        Returns:
            (str): String with the serial number.

        Example:
        ```py
        import lattehhpel as eload

        pel = eload.HHPEL('COM4')
        serial = pel.read_identification()
        # Reads the identification
        ```
        """
        identification = self.send_command("*IDN?")
        logger.debug(f'Programmable electronic load identification: {identification}')
        return identification

    def send_command(self, command_string):
        """Sends a command to the programmable electronic load and reads the response (if any).

        Args:
            command_string(str): String with the command to send.

        Returns:
            (str): If the programmable electronic load gives a response, a string with the output contained in the
            buffer.
            (None): If the programmable electronic load does not give any response.

        Example:
        ```py
        import lattehhpel as eload

        pel = eload.HHPEL('COM4')
        serial = pel.send_command('*IDN?')
        # Sends a command
        ```
        """
        self._check_pel_connected()
        self.pel_com.flushOutput()
        self.pel_com.write((command_string + '\n').encode())
        time.sleep(0.2)
        if command_string.find('?') != -1:
            data = (self.pel_com.read(self.pel_com.inWaiting())).decode()
            return data
        return None

    def set_input_on(self):
        """Turn ON the programmable electronic load input.

        Raises:
            RuntimeError: If not possible to turn ON the programmable electronic load input.

        Example:
        ```py
        import lattehhpel as eload

        pel = eload.HHPEL('COM4')
        pel.set_input_on()
        # Turn ON the input
        ```
        """
        try:
            self.send_command(f'CURR:RANG {self.last_current_range}')
            self.send_command('INP ON')
        except serial.SerialException:
            error_text = f'Not possible to turn ON the programmable electronic load input {self._line()}'
            logger.error(error_text)
            raise RuntimeError(error_text)

    def set_input_off(self):
        """Turn OFF the programmable electronic load input.

        Raises:
            RuntimeError: If not possible to turn OFF the programmable electronic load input.

        Example:
        ```py
        import lattehhpel as eload

        pel = eload.HHPEL('COM4')
        pel.set_input_off()
        # Turn OFF the input
        ```
        """
        try:
            self.send_command('CURR:RANG 0.01')
            self.send_command('INP OFF')
        except serial.SerialException:
            error_text = f'Not possible to turn OFF the programmable electronic load input {self._line()}'
            logger.error(error_text)
            raise RuntimeError(error_text)

    def is_input_on_off(self):
        """Checks the input status of the programmable electronic load.

        Returns:
           (str): String with the input status `ON` or `OFF`.

        Raises:
            RuntimeError: If not possible to read the input status.

        Example:
        ```py
        import lattehhpel as eload

        pel = eload.HHPEL('COM4')
        status = pel.is_input_on_off()
        # Checks the input status
        ```
        """
        try:
            resp = int(self.send_command('INP?'))
            if resp == 1:
                resp = 'ON'
            else:
                resp = 'OFF'
            return resp
        except serial.SerialException:
            error_text = f'Not possible to read the input status {self._line()}'
            logger.error(error_text)
            raise RuntimeError(error_text)

    def measure_current(self):
        """Reads the actual current from the programmable electronic load.

        Returns:
            (float): Float with the actual current on the programmable electronic load, in Amperes.

        Raises:
            RuntimeError: If not possible to read the current value.

        Example:
        ```py
        import lattehhpel as eload

        pel = eload.HHPEL('COM4')
        current = pel.measure_current()
        # Reads the actual current
        ```
        """
        resp = self.send_command('MEAS:CURR?')
        if resp is not None:
            base = resp.split('E')[0].replace('+', '')
            exp = resp.split('E')[1].replace('+', '')
        else:
            base = None
            exp = None
        base = self._convert_to_float(base, 'Not possible to read current value')
        exp = self._convert_to_float(exp, 'Not possible to read current value')
        return base * pow(10, exp)

    def measure_voltage(self):
        """Reads the actual voltage from the programmable electronic load.

        Returns:
            (float): Float with the measured voltage on the programmable electronic load, in Volts.

        Raises:
            RuntimeError: If not possible to read the voltage value.

        Example:
        ```py
        import lattehhpel as eload

        pel = eload.HHPEL('COM4')
        voltage = pel.measure_voltage()
        # Reads the actual voltage
        ```
        """
        resp = self.send_command('MEAS:VOLT?')
        if resp is not None:
            base = resp.split('E')[0].replace('+', '')
            exp = resp.split('E')[1].replace('+', '')
        else:
            base = None
            exp = None
        base = self._convert_to_float(base, 'Not possible to read voltage value')
        exp = self._convert_to_float(exp, 'Not possible to read voltage value')
        return base * pow(10, exp)

    def set_resistance(self, value):
        """Set a specific resistance in the programmable electronic load.

        Args:
            value (float): Float with the value of resistance, in ohm's

        Raises:
            RuntimeError: If not possible to set the resistance value.

        Example:
        ```py
        import lattehhpel as eload

        pel = eload.HHPEL('COM4')
        pel.set_resistance(13)
        # Set a specific resistance
        ```
        """
        try:
            self.send_command('SFUN:EXP:ENAB OFF')
            self.send_command('RES ' + format(value))
            self._mode_resistance()
        except serial.SerialException:
            error_text = f'Not possible to set resistance value {self._line()}'
            logger.error(error_text)
            raise RuntimeError(error_text)

    def read_resistance_set(self):
        """Reads the resistance value from the programmable electronic load.

        Returns:
            (float): Float with the value of resistance, in ohm's.

        Raises:
            RuntimeError: If not possible to read the resistance value.

        Example:
        ```py
        import lattehhpel as eload

        pel = eload.HHPEL('COM4')
        res = pel.read_resistance_set()
        # Reads the set resistance value
        ```
        """
        resp = self.send_command('RES?')
        if resp is not None:
            base = resp.split('E')[0].replace('+', '')
            exp = resp.split('E')[1].replace('+', '')
        else:
            base = None
            exp = None
        base = self._convert_to_float(base, 'Not possible to read resistance value')
        exp = self._convert_to_float(exp, 'Not possible to read resistance value')
        return base * pow(10, exp)

    def set_constant_current(self, nominal_value):
        """Sets a specific constant current in the programmable electronic load.

        Args:
            nominal_value (float): Float with the value of constant current, in Amperes.

        Raises:
            RuntimeError: If not possible to set the current value.

        Example:
        ```py
        import lattehhpel as eload

        pel = pel.HHPEL('COM4')
        pel.set_constant_current(2.0)
        # sets the required current
        ```
        """
        self.configured_current = nominal_value
        try:
            self.send_command('VOLT:PROT 0')
            self.send_command('SFUN:EXP:ENAB OFF')
            self.send_command(f'CURR:RANG {nominal_value}')
            self.last_current_range = nominal_value
            self.send_command(f'CURR {nominal_value}')
            self._mode_current()
        except serial.SerialException:
            error_text = f'Not possible to set the current value {self._line()}'
            logger.error(error_text)
            raise RuntimeError(error_text)

    def set_inrush_current(self, nominal_value, inrush_value=0.0, inrush_time=0.0, is_exponential=False,
                           off_to_on_thr=6):
        """Configures the load as an inrush type load.

        Args:
            nominal_value (float): Float with the nominal current value in Amperes after inrush time.
            inrush_value (float, optional): Float with the peak inrush current value in Amperes.
            inrush_time (float, optional): Float with the inrush time in seconds during which the peak inrush current
            will be applied.
            is_exponential (bool, optional): True (the inrush current will use an exponential function type) or False
            (the inrush current will use a pulse function type).
            off_to_on_thr (int, optional): Integer with the threshold/trigger voltage value in Volts to start the inrush
            current behavior.

        Raises:
            RuntimeError: If not possible to set the inrush current value.

        Example:
        ```py
        import lattehhpel as eload

        pel = pel.HHPEL('COM4')
        pel.set_inrush_current(1,3,0.3,True,6)
        # Preconfigures the required inrush current parameters
        ```
        """
        self.configured_current = nominal_value
        try:
            if inrush_time == 0:
                self.set_constant_current(nominal_value)
            else:
                self.send_command(f'CURR:RANG {inrush_value};:CURR 0;MODE:CURR')
                self.last_current_range = inrush_value
                time.sleep(1)
                self.set_trigger_voltage(off_to_on_thr)
                if is_exponential:
                    self.send_command(f'SFUN:EXP {inrush_value},{nominal_value},{inrush_time / 3.0},0.0,0.0')
                else:
                    self.send_command(f'SFUN:EXP {inrush_value},{nominal_value},0.000001,{inrush_time},0.02')
                self.send_command('SFUN:EXP:ENAB ON')
                self.send_command('INP ON')
        except serial.SerialException:
            error_text = f'Not possible to set the current value {self._line()}'
            logger.error(error_text)
            raise RuntimeError(error_text)

    def perform_pulse(self, current, duration):
        """Sets the programmable electronic load to perform a pulse current.

        Args:
            current (float): Float with the peak current value in Amperes for a given duration.
            duration (float): Float with the time in seconds during which the peak current will be applied.

        Raises:
            RuntimeError: If not possible to set the programmable electronic load to perform pulse current.

        Example:
        ```py
        import lattehhpel as eload

        pel = eload.HHPEL('COM4')
        pel.perform_pulse(3,0.3)
        # Performs a pulse current
        ```
        """
        try:
            duration = '{0:.3f}'.format(duration)
            current_after_pulse = '{0:.3f}'.format(self.configured_current)
            max_current = max(float(current), float(current_after_pulse))
            self.last_current_range = max_current
            self.send_command('SFUN:EXP:ENAB OFF')
            self.send_command(f'CURR:RANG {max_current}')
            self.send_command(f'LIST:CURR {current},{current_after_pulse}')
            self.send_command('LIST:CURR:RTIM 0, 0')
            self.send_command(f'LIST:CURR:DWEL {duration},0.001')
            self.send_command('LIST:COUN 1')
            self.send_command('INP ON')
            self.send_command('LIST:STAT ON')
        except serial.SerialException:
            error_text = f'Not possible to set the programmable electronic load to perform pulse current {self._line()}'
            logger.error(error_text)
            raise RuntimeError(error_text)

    def reset(self):
        """Resets the programmable electronic load to its default operating state.

         Raises:
             RuntimeError: If resetting the programmable electronic load fails.

        Example:
        ```py
        import lattehhpel as eload

        pel = eload.HHPEL('COM4')
        pel.reset()
        # Resets the programmable electronic load
        ```
        """
        try:
            self.send_command('*RST')
        except serial.SerialException:
            error_text = f'Not possible to reset the programmable electronic load {self._line()}'
            logger.error(error_text)
            raise RuntimeError(error_text)

    def read_current_set(self):
        """Reads the current value that is set in the programmable electronic load.

        Returns:
            (float): Float with the constant current value on the programmable electronic load, in Amperes.

        Raises:
            RuntimeError: If not possible to read the current value.

        Example:
        ```py
        import lattehhpel as eload

        pel = eload.HHPEL('COM3')
        current = pel.read_current_set()
        # Reads the set current value
        ```
        """
        resp = self.send_command('CURR?')
        if resp is not None:
            base = resp.split('E')[0].replace('+', '')
            exp = resp.split('E')[1].replace('+', '')
        else:
            base = None
            exp = None
        base = self._convert_to_float(base, 'Not possible to read current value')
        exp = self._convert_to_float(exp, 'Not possible to read current value')
        return base * pow(10, exp)

    def set_trigger_voltage(self, value):
        """Sets the trigger voltage on the programmable electronic load.

        Args:
            value (float): Float with the value of trigger voltage in Volts.

        Raises:
            RuntimeError: If not possible to set the trigger voltage value.

        Example:
        ```py
        import lattehhpel as eload

        pel = eload.HHPEL('COM4')
        pel.set_trigger_voltage(13)
        # Sets the trigger voltage
        ```
        """
        try:
            self.send_command('VOLT:PROT ' + format(value))
        except serial.SerialException:
            error_text = f'Not possible to set the trigger voltage value {self._line()}'
            logger.error(error_text)
            raise RuntimeError(error_text)

    def read_trigger_voltage_set(self):
        """Reads the trigger voltage value from the programmable electronic load.

        Returns:
            (float): Float with the trigger voltage value from the programmable electronic load, in Volts.

        Raises:
            RuntimeError: If not possible to read the trigger voltage value.

        Example:
        ```py
        import lattehhpel as eload

        pel = eload.HHPEL('COM4')
        trigger_voltage = pel.read_trigger_voltage_set()
        # Reads the set trigger voltage value
        ```
        """
        resp = self.send_command('VOLT:PROT?')
        if resp is not None:
            base = resp.split('E')[0].replace('+', '')
            exp = resp.split('E')[1].replace('+', '')
        else:
            base = None
            exp = None
        base = self._convert_to_float(base, 'Not possible to read trigger voltage value')
        exp = self._convert_to_float(exp, 'Not possible to read trigger voltage value')
        return base * pow(10, exp)

    def close_connection(self):
        """Ends connection with the programmable electronic load and sets it in the manual operation mode.

        Example:
        ```py
        import lattehhpel as eload

        pel = eload.HHPEL('COM4')
        pel.close_connection()
        # Closes the communication
        ```

        !!! attention "Important"
            This API should always be called before ending the test script.
        """
        if self.is_connected:
            self.send_command('GTL')  # Set manual operation before closing the connection
            self.pel_com.close()
            self.is_connected = False
            logger.info(f'Closed connection with programmable electronic load on serial port {self.port_name}')
        else:
            logger.warning(
                f'Connection with programmable electronic load is already closed on serial port {self.port_name}')
