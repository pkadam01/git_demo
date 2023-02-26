"""The following test cases verify the feature [Libray services](../reqs/reqs.md#12-feature-library-services) described
in the requirements.

The test cases do not need any prior condition before being executed, unless explicitly stated otherwise.
"""
import lattehhpel as eload


def test__pel_lib_info_qkit():
    """**Description**: Checks the library version

    **Requirements tested**:

    - [17016](../reqs/reqs.md#req-id-17016) Reading the programmable electronic load library version

    **Actions to be performed**:

    - Read library version

    **Evaluation criteria**:

    - Check it matches with the current library version
    """
    info = eload.get_pel_lib_info()

    assert info == ' '.join([eload.__package__, eload.__version__])
    