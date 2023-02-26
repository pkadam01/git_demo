"""The following test cases verify the feature
[Sending generic commands](../reqs/reqs.md#3-feature-sending-generic-commands) described in the requirements.

The test cases do not need any prior condition before being executed, unless explicitly stated otherwise.
"""
import lattehhpel as eload
import logging
import config
import time


def setup_module():
    """**Description**: Prepares test suite execution"""
    eload.set_pel_logging_level(logging.CRITICAL)


def teardown_module():
    """**Description**: Finishes test suite execution"""
    pass


def test__send_generic_command_qkit():
    """**Description**: Checks it is possible to send the generic commands to the programmable electronic load

    **Requirements tested**:

    - [17002](../reqs/reqs.md#req-id-17002) Sending generic commands to the programmable electronic load

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Set the constant voltage mode by sending command `MODE:VOLT` using the API `send_command()`

    **Evaluation criteria**:

   - Check the mode is set to constant voltage by sending command `MODE?` using the API `send_command()`
    """
    pel = eload.HHPEL(config.serial_port)
    time.sleep(1)
    pel.send_command('MODE:VOLT')
    resp = pel.send_command('MODE?')
    assert resp == "VOLT\n"
    pel.close_connection()
