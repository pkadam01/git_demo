"""The following test cases verify the feature
[Resetting the programmable electronic load](../reqs/reqs.md#10-feature-resetting-the-programmable-electronic-load)
described in the requirements.

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


def test__reset_pel_qkit():
    """**Description**: Checks the API `reset()`

    **Requirements tested**:

    - [17014](../reqs/reqs.md#req-id-17014) Reset the programmable electronic load in default state of operation

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Turn ON the programmable electronic load using the API `set_input_on()`
    - Reset programmable electronic load using API `reset()`
    - Read the programmable electronic load input status using the API `is_input_on_off()`

    **Evaluation criteria**:

    - Check the input is turned OFF
    """
    pel = eload.HHPEL(config.serial_port)
    pel.set_input_on()
    pel.reset()
    resp = pel.is_input_on_off()
    assert resp == 'OFF'
    pel.close_connection()


def test__reset_pel_failure_qkit(caplog):
    """**Description**: Checks failure is detected when resetting the programmable electronic load

    **Requirements tested**:

    - [17014](../reqs/reqs.md#req-id-17014) Reset the programmable electronic load in default state of operation

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Simulate an error while resetting the programmable electronic load

    **Evaluation criteria**:

    - Check that an exception is raised when calling the API `reset()`
    - Check logger contains error text indicating the problem
    """
    caplog.set_level(logging.DEBUG, logger=eload.__package__)
    pel = fake_pel.FakePEL(config.serial_port)
    with pytest.raises(RuntimeError):
        pel.reset()
    assert 'Not possible to reset the programmable electronic load' in caplog.text
