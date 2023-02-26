"""The following test cases verify the feature
[Performing the pulse current](../reqs/reqs.md#8-feature-performing-the-pulse-current) described in the requirements.

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


def test__perform_pulse():
    """**Description**: Checks the API `perform_pulse()`

    **Requirements tested**:

    - [17011](../reqs/reqs.md#req-id-17011) Set the programmable electronic load to perform pulse current

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Set the programmable electronic load to perform a specific pulse current using `perform_pulse()`

    **Evaluation criteria**:

    - Ask the user the if the waveform generated is the expected one, and check it is YES
    """
    pel = eload.HHPEL(config.serial_port)
    pel.perform_pulse(3, 0.3)
    resp = input('\nIs the captured waveform a pulse of 3 amps during 0.3 seconds? (YES/NO): ').upper()
    assert resp == 'YES'
    pel.close_connection()


def test__perform_pulse_failure_qkit(caplog):
    """**Description**: Checks failures are detected when setting the electronic load in pulse current simulation

    **Requirements tested**:

    - [17011](../reqs/reqs.md#req-id-17011) Set the programmable electronic load to perform pulse current

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Simulate an error while setting the programmable electronic load to perform pulse current

    **Evaluation criteria**:

    - Check that an exception is raised when calling the API `perform_pulse()`
    - Check logger contains error text indicating the problem
    """
    caplog.set_level(logging.INFO, logger=eload.__package__)
    pel = fake_pel.FakePEL(config.serial_port)
    with pytest.raises(RuntimeError):
        pel.perform_pulse(5, 3.0)
    assert 'Not possible to set the programmable electronic load to perform pulse current' in caplog.text
