"""The following test cases verify the feature
[Setting and reading the resistance](../reqs/reqs.md#7-feature-setting-and-reading-the-resistance) described in
the requirements.

The test cases do not need any prior condition before being executed, unless explicitly stated otherwise.
"""
import lattehhpel as eload
import fake_pel
import logging
import config
import time
import pytest
import fake_pel_2

RESISTANCE_TOLERANCE = 0.1

RESISTANCE = [12.0, 12.5, 13.0, 9, 5]


def setup_module():
    """**Description**: Prepares test suite execution"""
    eload.set_pel_logging_level(logging.CRITICAL)


def teardown_module():
    """**Description**: Finishes test suite execution"""
    pass


def test__set_read_resistance_qkit():
    """**Description**: Checks the APIs `set_resistance()` and `read_resistance_set()`

    **Requirements tested**:

    - [17009](../reqs/reqs.md#req-id-17009) Set a specific resistance in the programmable electronic load
    - [17010](../reqs/reqs.md#req-id-17010) Read the resistance value that is set in the programmable electronic load

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Set known resistance using the API `set_resistance()`

    **Evaluation criteria**:

    - Check the resistance set are correct using the API `read_resistance_set()`
    """

    pel = eload.HHPEL(config.serial_port)
    for res in RESISTANCE:
        pel.set_resistance(res)
        time.sleep(1)
        actual_resistance = pel.read_resistance_set()
        assert res * (1.0 - RESISTANCE_TOLERANCE) <= actual_resistance <= res * (1.0 + RESISTANCE_TOLERANCE)
    pel.close_connection()


def test__set_resistance_failure_qkit(caplog):
    """**Description**: Checks failure is detected when setting the resistance in the programmable electronic load

    **Requirements tested**:

     - [17009](../reqs/reqs.md#req-id-17009) Set a specific resistance in the programmable electronic load

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Simulate an error while setting the resistance

    **Evaluation criteria**:

    - Check that an exception is raised when calling the API `set_resistance()`
    - Check logger contains error text indicating the problem
    """
    caplog.set_level(logging.INFO, logger=eload.__package__)
    pel = fake_pel.FakePEL(config.serial_port)
    with pytest.raises(RuntimeError):
        pel.set_resistance(12)
    assert 'Not possible to set resistance value' in caplog.text


def test__read_resistance_failure_qkit(caplog):
    """**Description**: Checks failure is detected when reading an incorrect resistance (not a float value)

    **Requirements tested**:

    - [17010](../reqs/reqs.md#req-id-17010) Read the resistance value that is set in the programmable electronic load

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Simulate an incorrect resistance reading from the programmable electronic load

    **Evaluation criteria**:

    - Check that an exception is raised when calling the API `read_resistance_set()`
    - Check logger contains error text indicating the problem
    """
    caplog.set_level(logging.INFO, logger=eload.__package__)
    pel = fake_pel_2.FakePEL(config.serial_port)
    with pytest.raises(RuntimeError):
        pel.read_resistance_set()
    assert 'Not possible to read resistance value' in caplog.text
    pel.close_connection()
