"""The following test cases verify the feature
[Establishing connection](../reqs/reqs.md#1-feature-establishing-connection) and
[Closing the connection](../reqs/reqs.md#11-feature-closing-the-connection) described in the requirements.

The test cases do not need any prior condition before being executed, unless explicitly stated otherwise.
"""
import lattehhpel as eload
import logging
import config
import time
import pytest


def setup_module():
    """**Description**: Prepares test suite execution"""
    eload.set_pel_logging_level(logging.CRITICAL)


def teardown_module():
    """**Description**: Finishes test suite execution"""
    pass


def test__pel_connection_qkit(caplog):
    """**Description**: Checks the programmable electronic load connection

    **Requirements tested**:

    - [17000](../reqs/reqs.md#req-id-17000) Establishing connection with the programmable electronic load

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load

    **Evaluation criteria**:

    - Check instance variable `is_connected` equals to `True`
    """
    pel = eload.HHPEL(config.serial_port)
    time.sleep(1)
    assert pel.is_connected is True


def test__pel_connection_close_qkit(caplog):
    """**Description**: Checks the programmable electronic load connection is closed

    **Requirements tested**:

    - [17015](../reqs/reqs.md#req-id-17015) Closing connection with the programmable electronic load

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load, and then close the connection using `close_connection()`

    **Evaluation criteria**:

    - Check logger contains INFO text indicating the connection is closed
    """
    caplog.set_level(logging.INFO, logger=eload.__package__)

    pel = eload.HHPEL(config.serial_port)
    time.sleep(1)
    pel.close_connection()
    assert 'Closed connection with programmable electronic load on serial port' in caplog.text


def test__pel_connection_failure_qkit(caplog):
    """**Description**: Checks failure is detected when connecting to the programmable electronic load using incorrect
    port

    **Requirements tested**:

    - [17000](../reqs/reqs.md#req-id-17000) Establishing connection with the programmable electronic load

    **Initial conditions**:

    - None

    **Actions to be performed**:

    - Connect to the programmable electronic load using an incorrect serial port

    **Evaluation criteria**:

    - Check that an exception is raised
    - Check logger contains error text indicating the problem
    """
    caplog.set_level(logging.DEBUG, logger=eload.__package__)

    with pytest.raises(RuntimeError):
        eload.HHPEL('COMX')
    assert 'Not possible to open serial port' in caplog.text


def test__pel_connection_close_failure_qkit(caplog):
    """**Description**: Checks failure is detected when trying to close connection with the programmable electronic load
    when it is already closed

    **Requirements tested**:

    - [17015](../reqs/reqs.md#req-id-17015) Closing connection with the programmable electronic load

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load, and close the connection using `close_connection()`
    - Close the connection again using `close_connection()`

    **Evaluation criteria**:

    - Check logger contains warning text indicating the problem
    """
    caplog.set_level(logging.WARNING, logger=eload.__package__)
    pel = eload.HHPEL(config.serial_port)
    time.sleep(1)
    pel.close_connection()
    pel.close_connection()
    assert 'Connection with programmable electronic load is already closed on serial port' in caplog.text


def test__port_closed_api_failure_qkit(caplog):
    """**Description**: Checks failure is detected when calling any API after the port has been closed

    **Requirements tested**:

    - [17015](../reqs/reqs.md#req-id-17015) Closing connection with the programmable electronic load.

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Close the connection using `close_connection()`
    - Try to execute the API `measure_voltage()`

    **Evaluation criteria**:

    - Check that an exception is raised
    - Check logger contains error text indicating the problem
    """

    caplog.set_level(logging.DEBUG, logger=eload.__package__)
    pel = eload.HHPEL(config.serial_port)
    pel.close_connection()
    with pytest.raises(RuntimeError):
        pel.measure_voltage()
    assert 'Can not execute the command requested, connection with the programmable electronic load is closed' in \
           caplog.text
    pel.close_connection()
