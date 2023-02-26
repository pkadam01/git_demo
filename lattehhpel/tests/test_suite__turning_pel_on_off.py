"""The following test cases verify the feature
[Turning the programmable electronic load input on/off and reading the status](../reqs/reqs.md#4-feature-turning-the-
programmable-electronic-load-input-onoff-and-reading-the-status) described in the requirements.

The test cases do not need any prior condition before being executed, unless explicitly stated otherwise.
"""
import lattehhpel as eload
import logging
import config
import pytest
import fake_pel


def setup_module():
    """**Description**: Prepares test suite execution"""
    eload.set_pel_logging_level(logging.CRITICAL)


def teardown_module():
    """**Description**: Finishes test suite execution"""
    pass


def test__turn_on_pel_qkit():
    """**Description**: Checks the APIs `set_input_on()` and `is_input_on_off()`

    **Requirements tested**:

    - [17003](../reqs/reqs.md#req-id-17003) Turning the programmable electronic load input ON/OFF
    - [17004](../reqs/reqs.md#req-id-17004) Reading the programmable electronic load input status

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Turn OFF the programmable electronic load input using the API `set_input_off()`
    - Turn ON the programmable electronic load input using the API `set_input_on()`
    - Read the input status of the programmable electronic load using the API `is_input_on_off()`

    **Evaluation criteria**:

    - Check the programmable electronic load input is ON
    """
    pel = eload.HHPEL(config.serial_port)
    pel.set_input_off()
    pel.set_input_on()
    resp = pel.is_input_on_off()
    assert resp == 'ON'
    pel.close_connection()


def test__turn_off_pel_qkit():
    """**Description**: Checks the APIs `set_input_off()` and `is_input_on_off()`

    **Requirements tested**:

    - [17003](../reqs/reqs.md#req-id-17003) Turning the programmable electronic load input ON/OFF
    - [17004](../reqs/reqs.md#req-id-17004) Reading the programmable electronic load input status

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Turn ON the programmable electronic load input using the API `set_input_on()`
    - Turn OFF the programmable electronic load input using the API `set_input_off()`
    - Read the input status of the programmable electronic load using the API `is_input_on_off()`

    **Evaluation criteria**:

    - Check the programmable electronic load input is OFF
    """
    pel = eload.HHPEL(config.serial_port)
    pel.set_input_on()
    pel.set_input_off()
    resp = pel.is_input_on_off()
    assert resp == 'OFF'
    pel.close_connection()


def test__turn_on_pel_failure_qkit(caplog):
    """**Description**: Checks failure is detected when calling the API `set_input_on()

    **Requirements tested**:

    - [17003](../reqs/reqs.md#req-id-17003) Turning the programmable electronic load input ON/OFF

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Simulate an error while setting the programmable electronic load input ON

    **Evaluation criteria**:

    - Check that an exception is raised when calling the API `set_input_on()`
    - Check logger contains error text indicating the problem
    """
    caplog.set_level(logging.INFO, logger=eload.__package__)
    pel = fake_pel.FakePEL(config.serial_port)
    with pytest.raises(RuntimeError):
        pel.set_input_on()
    assert 'Not possible to turn ON the programmable electronic load input' in caplog.text


def test__turn_off_pel_failure_qkit(caplog):
    """**Description**: Checks failure is detected when calling the API `set_input_off()

    **Requirements tested**:

    - [17003](../reqs/reqs.md#req-id-17003) Turning the programmable electronic load input ON/OFF

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Simulate an error while setting the programmable electronic load input OFF

    **Evaluation criteria**:

    - Check that an exception is raised when calling the API `set_input_off()`
    - Check logger contains error text indicating the problem
    """
    caplog.set_level(logging.INFO, logger=eload.__package__)
    pel = fake_pel.FakePEL(config.serial_port)
    with pytest.raises(RuntimeError):
        pel.set_input_off()
    assert 'Not possible to turn OFF the programmable electronic load input' in caplog.text


def test__is_input_on_off_failure_qkit(caplog):
    """**Description**: Checks failure is detected when calling the API `is_input_on_off()`

    **Requirements tested**:

    - [17004](../reqs/reqs.md#req-id-17004) Reading the programmable electronic load input status

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Simulate an error while reading the input status

    **Evaluation criteria**:

    - Check that an exception is raised when calling the API `is_input_on_off()`
    - Check logger contains error text indicating the problem
    """
    caplog.set_level(logging.INFO, logger=eload.__package__)
    pel = fake_pel.FakePEL(config.serial_port)
    with pytest.raises(RuntimeError):
        pel.is_input_on_off()
    assert 'Not possible to read the input status' in caplog.text
