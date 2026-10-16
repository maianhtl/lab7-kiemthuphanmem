"""Minimal GPS gateway used by YummyApp."""


class GPSSignalLostError(Exception):
    """Raised when the device cannot provide a GPS position."""


def get_current_location():
    """Return the current device location.

    The real mobile integration is intentionally outside this sample. Tests
    replace this function with a mock to model the device boundary.
    """
    return 10.762622, 106.660172
