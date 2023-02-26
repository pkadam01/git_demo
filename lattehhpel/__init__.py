from .hhpel import *
from .about import __version__, __package__
import sys
import logging


def get_pel_lib_info():
    """String containing the name + version of this library.

    Returns:
        String containing the name + version of this library.

    Example:
    ```python
    import lattehhpel as eload

    print(eload.get_pel_lib_info())
    ```
    """
    return ' '.join([__package__, __version__])


def set_pel_logging_level(level):
    """Sets the logger to the desired level.

    Example:
    ```python
    import lattehhpel as eload
    import logging

    eload.set_pel_logging_level(logging.WARNING)
    ```
    """
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)


# Create a custom logger
logger = logging.getLogger(__package__)
# Create console handler and set level
console_handler = logging.StreamHandler(stream=sys.stdout)  # This will sync prints and logs
# Create formatter and add it to the console handler
message_format = logging.Formatter('%(levelname)s (%(module)s): %(message)s')
console_handler.setFormatter(message_format)
# Add console handler to the logger, and set level also to the main logger
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)
