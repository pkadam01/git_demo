"""The following test cases verify the feature
[Reading the voltage](../reqs/reqs.md#6-feature-reading-the-voltage) described in the requirements.

The test cases do not need any prior condition before being executed, unless explicitly stated otherwise.
"""
import lattehhpel as eload
import logging
import config
import time
import pytest
import fake_pel_2

VOLTAGE_TOLERANCE = 0.1


def setup_module():
    """**Description**: Prepares test suite execution"""
    eload.set_pel_logging_level(logging.CRITICAL)


def teardown_module():
    """**Description**: Finishes test suite execution"""
    pass


def test__measure_voltage():
    """**Description**: Checks the API `measure_voltage()`

    **Requirements tested**:

    - [17008](../reqs/reqs.md#req-id-17008) Read the actual voltage from the programmable electronic load

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Ask the user to introduce the actual voltage from the display

    **Evaluation criteria**:

    - Read the actual voltage from the programmable electronic load using the API `measure_voltage()`
    and check it equals to the user value
    """

    pel = eload.HHPEL(config.serial_port)
    expected_voltage = round(float(input('\nEnter the actual voltage from the programmable electronic load'
                                         ' display: ')), 1)
    time.sleep(1)
    actual_voltage = round(pel.measure_voltage(), 1)
    assert expected_voltage * (1.0 - VOLTAGE_TOLERANCE) <= actual_voltage <= expected_voltage * (
            1.0 + VOLTAGE_TOLERANCE)
    pel.close_connection()


def test__measure_voltage_failure_qkit(caplog):
    """**Description**: Checks failure is detected when reading an incorrect voltage (not a float value)

    **Requirements tested**:

    - [17008](../reqs/reqs.md#req-id-17008) Read the actual voltage from the programmable electronic load

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Simulate an incorrect voltage reading from the programmable electronic load

    **Evaluation criteria**:

    - Check that an exception is raised when calling the API `measure_voltage()`
    - Check logger contains error text indicating the problem
    """
    caplog.set_level(logging.DEBUG, logger=eload.__package__)
    pel = fake_pel_2.FakePEL(config.serial_port)
    with pytest.raises(RuntimeError):
        pel.measure_voltage()
    assert 'Not possible to read voltage value' in caplog.text
    pel.close_connection()
