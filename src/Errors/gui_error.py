"""Defines the GUIError class used for throwing errors connected to the GUI."""
from src.Common.Enums.err_no_enum import ErrNoEnum


class GUIError(Exception):
    """The GUIError class defines a container for all GUI errors."""

    def __init__(self, error_code: ErrNoEnum, error_message: str) -> None:
        """Initialise GUI Error.

        Initialises an instance of a GUIError to be caught in the code
        :param error_code: Error code, taken from ErrNoEnum
        :param error_message: Error message
        """
        self.error_code = error_code
        self.error_message = error_message
