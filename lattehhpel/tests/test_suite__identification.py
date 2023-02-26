"""The following test cases verify the feature
[Reading the identification](../reqs/reqs.md#2-feature-reading-the-identification) described in the requirements.

The test cases do not need any prior condition before being executed, unless explicitly stated otherwise.
"""
import lattehhpel as eload
import config
import time

PEL_UNIT = "HOECHERL&HACKL,ZS506"


def test__pel_identifier_qkit():
    """**Description**: Checks the programmable electronic load identification

    **Requirements tested**:

    - [17001](../reqs/reqs.md#req-id-17001) Reading programmable electronic load identification

    **Initial conditions**:

    - Programmable electronic load is connected

    **Actions to be performed**:

    - Connect to the programmable electronic load
    - Read the identification using API `read_identification()`

    **Evaluation criteria**:

    - Check return value contains meaningful text "HOECHERL&HACKL,ZS506"
    """
    pel = eload.HHPEL(config.serial_port)
    time.sleep(1)
    pel_name = pel.read_identification()
    assert PEL_UNIT in pel_name
    pel.close_connection()
