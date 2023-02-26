"""The following test cases verify the feature
[Generating an inrush current](../reqs/reqs.md#9-feature-generating-an-inrush-current)
described in the requirements.

The test cases do not need any prior condition before being executed, unless explicitly stated otherwise.
"""
import lattehhpel as eload
import logging
import config
import pytest
import fake_pel
import fake_pel_2
import time

CURRENT_TOLERANCE = 0.1
VOLTAGE_TOLERANCE = 0.1

VOLTAGES = [0, 2.5, 3, 3.6, 5]


def setup_module():
    """**Description**: Prepares test suite execution"""
    eload.set_pel_logging_level(logging.CRITICAL)


def teardown_module():
    """**Description**: Finishes test suite execution"""
    pass


def test__preconfigure_inrush_current_non_exponential():
    """**Description**: Checks the API `set_inrush_current()` when the current is non-exponential and inrush time is
    not 0

    **Requirements tested**:

    - [17013](../reqs/reqs.md#req-id-17013) Preconfigure the inrush current parameters on programmable electronic load
    for simulating inrush behavior.

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Turn OFF the power supply
    - Preconfigure the inrush current parameters using the API `set_inrush_current()`
    - Turn ON the power supply

    **Evaluation criteria**:

    - Ask the user the status of the waveform generated for given inrush current parameters, and check it is YES
    """
    pel = eload.HHPEL(config.serial_port)
    input('\nTurn OFF the power supply and press ENTER to continue...')
    pel.set_inrush_current(nominal_value=1, inrush_value=3, inrush_time=0.3, is_exponential=False)
    input('\nTurn ON the power supply and press ENTER to continue...')
    resp = input('\nIs the captured waveform a square pulse of 3 amps during 0.3 seconds '
                 'and then 1 amp? (YES/NO): ').upper()
    assert resp == 'YES'
    pel.close_connection()


def test__preconfigure_inrush_current_exponential():
    """**Description**: Checks API `set_inrush_current()` when the current is exponential and inrush time is not 0

    **Requirements tested**:

    - [17013](../reqs/reqs.md#req-id-17013) Preconfigure the inrush current parameters on programmable electronic load
    for simulating inrush behavior.

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Turn OFF the power supply
    - Preconfigure the inrush current parameters using the API `set_inrush_current()`
    - Turn ON the power supply

    **Evaluation criteria**:

    - Ask the user the status of the waveform generated for given inrush current parameter, and check it is YES
    """
    pel = eload.HHPEL(config.serial_port)
    input('\nTurn OFF the power supply and press ENTER to continue...')
    pel.set_inrush_current(nominal_value=1, inrush_value=3, inrush_time=0.3, is_exponential=True)
    input('\nTurn ON the power supply and press ENTER to continue...')
    resp = input('\nIs the captured waveform an exponential pulse of 3 amps during 0.3 seconds '
                 'and then 1 amp? (YES/NO): ').upper()
    assert resp == 'YES'
    pel.close_connection()


def test__preconfigure_inrush_current_zero_time_exponential_qkit():
    """**Description**: Checks API `set_inrush_current()` when inrush time is set to 0

    **Requirements tested**:

    - [17013](../reqs/reqs.md#req-id-17013) Preconfigure the inrush current parameters on programmable electronic load
    for simulating inrush behavior.

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Preconfigure the inrush current parameters using the API `set_inrush_current()`

    **Evaluation criteria**:

    - Read the nominal current value that is set when inrush time is zero using API `read_current()`
    """
    pel = eload.HHPEL(config.serial_port)
    pel.set_inrush_current(nominal_value=2, inrush_value=3, inrush_time=0)
    actual_current = pel.read_current_set()
    assert 2 * (1.0 - CURRENT_TOLERANCE) <= actual_current <= 2 * (1.0 + CURRENT_TOLERANCE)
    pel.close_connection()


def test__preconfig_inrush_current_failure_qkit(caplog):
    """**Description**: Checks failure is detected when setting the current value in programmable electronic load

    **Requirements tested**:

    - [17013](../reqs/reqs.md#req-id-17013) Preconfigure the inrush current parameters on programmable electronic load
    for simulating inrush behavior.

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Simulate an error when preconfiguring the inrush current parameters in the programmable electronic load

    **Evaluation criteria**:

    - Check that an exception is raised when calling the API `set_inrush_current()`
    - Check logger contains error text indicating the problem
    """
    caplog.set_level(logging.INFO, logger=eload.__package__)
    pel = fake_pel.FakePEL(config.serial_port)
    with pytest.raises(RuntimeError):
        pel.set_inrush_current(nominal_value=1, inrush_value=3, inrush_time=0.3)
    assert 'Not possible to set the current value' in caplog.text


def test__set__read_trigger_voltage_qkit():
    """**Description**: Checks APIs `set_trigger_voltage()` and `read_trigger_voltage_set()`

    **Requirements tested**:

    - [17012](../reqs/reqs.md#req-id-17012) Set and read the trigger voltage on programmable electronic load for
    simulating inrush behavior

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Set known voltages using the API `set_trigger_voltage()`

    **Evaluation criteria**:

    - Check the voltages set are correct using the API `read_trigger_voltage_set()`
    """

    pel = eload.HHPEL(config.serial_port)
    for voltage in VOLTAGES:
        pel.set_trigger_voltage(voltage)
        time.sleep(1)
        actual_voltage = pel.read_trigger_voltage_set()
        assert voltage * (1.0 - VOLTAGE_TOLERANCE) <= actual_voltage <= voltage * (1.0 + VOLTAGE_TOLERANCE)
    pel.close_connection()


def test__set_trigger_voltage_failure_qkit(caplog):
    """**Description**: Checks failure is detected when setting the trigger voltage value in programmable electronic
     load

    **Requirements tested**:

     - [17012](../reqs/reqs.md#req-id-17012) Set and read the trigger voltage on programmable electronic load for
     simulating inrush behavior

    **Initial conditions**:

    - programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Simulate an error when setting the voltage in the programmable electronic load

    **Evaluation criteria**:

    - Check that an exception is raised when calling the API `set_trigger_voltage()`
    - Check logger contains error text indicating the problem
    """
    caplog.set_level(logging.INFO, logger=eload.__package__)
    pel = fake_pel.FakePEL(config.serial_port)
    with pytest.raises(RuntimeError):
        pel.set_trigger_voltage(12)
    assert 'Not possible to set the trigger voltage value' in caplog.text


def test__read_trigger_voltage_failure_qkit(caplog):
    """**Description**: Checks failure is detected when reading an incorrect voltage (not a float value)

    **Requirements tested**:

    - [17012](../reqs/reqs.md#req-id-17012) Set and read the trigger voltage on programmable electronic load for
     simulating inrush behavior

    **Initial conditions**:

    - programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Simulate an incorrect voltage reading from the programmable electronic load

    **Evaluation criteria**:

    - Check that an exception is raised when calling the API `read_trigger_voltage_set()`
    - Check logger contains error text indicating the problem
    """
    caplog.set_level(logging.DEBUG, logger=eload.__package__)
    pel = fake_pel_2.FakePEL(config.serial_port)
    with pytest.raises(RuntimeError):
        pel.read_trigger_voltage_set()
    assert 'Not possible to read trigger voltage value' in caplog.text
    pel.close_connection()
