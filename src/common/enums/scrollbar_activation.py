"""Defines the enum of activation of scrollbars for textboxes."""
from enum import Enum


class ScrollbarActivation(Enum):
    """Defines the values for whether scrollbars are activated or not."""

    ACTIVE = True
    HIDDEN = False
