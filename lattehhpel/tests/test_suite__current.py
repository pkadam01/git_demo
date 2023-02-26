"""The following test cases verify the feature
[Setting and reading the current](../reqs/reqs.md#5-feature-setting-and-reading-the-current) described in the
requirements.

The test cases do not need any prior condition before being executed, unless explicitly stated otherwise.
"""
import lattehhpel as eload
import logging
import config
import pytest
import fake_pel
import time
import fake_pel_2

CURRENT_TOLERANCE = 0.1
CURRENT = [0.5, 0.7, 1, 1.5, 1.7, 0]


def setup_module():
    """**Description**: Prepares test suite execution"""
    eload.set_pel_logging_level(logging.CRITICAL)


def teardown_module():
    """**Description**: Finishes test suite execution"""
    pass


def test__set_and_read_current_qkit():
    """**Description**: Checks APIs `set_constant_current()` and `read_current_set()`

    **Requirements tested**:

    - [17005](../reqs/reqs.md#req-id-17005) Set a specific constant current
    - [17006](../reqs/reqs.md#req-id-17006) Read the current value that is set in the programmable electronic load

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Set a known current using API `set_constant_current()`

    **Evaluation criteria**:

    - Read current using API `read_current_set()` and check it is equal to the current value previously set
    """
    pel = eload.HHPEL(config.serial_port)
    for current in CURRENT:
        pel.set_constant_current(current)
        time.sleep(1)
        actual_current = pel.read_current_set()
        assert current * (1.0 - CURRENT_TOLERANCE) <= actual_current <= current * (1.0 + CURRENT_TOLERANCE)
    pel.close_connection()


def test__measure_current():
    """**Description**: Checks API `measure_current()`

    **Requirements tested**:

    - [17007](../reqs/reqs.md#req-id-17007) Read the actual current from the programmable electronic load

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Turn ON the programmable electronic load input using API `set_input_on()`
    - Ask the user to introduce the actual current from the display

    **Evaluation criteria**:

    - Read the actual current from the programmable electronic load using API `measure_current()`
    and check it equals to the user value
    """

    pel = eload.HHPEL(config.serial_port)
    pel.set_input_on()
    expected_current = round(float(input('\nEnter the actual current from the programmable electronic load '
                                         'display: ')), 1)
    time.sleep(0.5)
    actual_current = round(pel.measure_current(), 1)
    assert expected_current * (1.0 - CURRENT_TOLERANCE) <= actual_current <= expected_current * (
            1.0 + CURRENT_TOLERANCE)
    pel.close_connection()


def test__set_current_failure_qkit(caplog):
    """**Description**: Checks failure is detected when setting the current value in the programmable electronic load

    **Requirements tested**:

    - [17005](../reqs/reqs.md#req-id-17005) Set a specific constant current

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Simulate an error when setting current in the programmable electronic load

    **Evaluation criteria**:

    - Check that an exception is raised when calling API `set_constant_current()`
    - Check logger contains error text indicating the problem
    """
    caplog.set_level(logging.INFO, logger=eload.__package__)
    pel = fake_pel.FakePEL(config.serial_port)
    with pytest.raises(RuntimeError):
        pel.set_constant_current(5)
    assert 'Not possible to set the current value' in caplog.text


def test__read_current_failure_qkit(caplog):
    """**Description**: Checks failure is detected when reading an incorrect current (not a float value)

    **Requirements tested**:

    - [17006](../reqs/reqs.md#req-id-17006) Read the current value that is set in the programmable electronic load

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Simulate an incorrect current reading from the programmable electronic load

    **Evaluation criteria**:

    - Check that an exception is raised when calling API `read_current_set()`
    - Check logger contains error text indicating the problem
    """
    caplog.set_level(logging.INFO, logger=eload.__package__)
    pel = fake_pel_2.FakePEL(config.serial_port)
    with pytest.raises(RuntimeError):
        pel.read_current_set()
    assert 'Not possible to read current value' in caplog.text
    pel.close_connection()


def test__measure_current_failure_qkit(caplog):
    """**Description**: Checks failure is detected when reading an incorrect current (not a float value)

    **Requirements tested**:

    - [17007](../reqs/reqs.md#req-id-17007) Read the actual current from the programmable electronic load

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Simulate an incorrect current reading from the programmable electronic load

    **Evaluation criteria**:

    - Check that an exception is raised when calling API `measure_current()`
    - Check logger contains error text indicating the problem
    """
    caplog.set_level(logging.INFO, logger=eload.__package__)
    pel = fake_pel_2.FakePEL(config.serial_port)
    with pytest.raises(RuntimeError):
        pel.measure_current()
    assert 'Not possible to read current value' in caplog.text
    pel.close_connection()
