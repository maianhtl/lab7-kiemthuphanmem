"""Core backend rules for the YummyApp ordering sample."""

from gps_service import gps_service

MENU = {
    "pho": 50000,
    "com": 45000,
    "phobosaurieng": 999000,
}

PROMO_CODES = {
    "PROMO10": 0.10,
    "NEW-USER": 0.15,
}

RESTAURANTS_BY_LOCATION = {
    (10.0, 105.0): ["Quan Pho Ha Noi", "Com Tam Sai Gon"],
}


class ConnectionError(Exception):
    """Raised when an online-only operation is attempted offline."""


class YummyApp:
    """Application service for ordering and nearby restaurant lookup."""

    def __init__(self, online=True, os_version=30):
        self.online = online
        self.os_version = os_version

    def calculate_order_total(self, cart):
        """Calculate a cart total, ignoring unknown menu items."""
        return sum(
            MENU[item] * quantity
            for item, quantity in cart.items()
            if item in MENU and quantity > 0
        )

    def apply_promo_code(self, total, code):
        """Apply a valid promotion after checking network and OS constraints."""
        if not self.online:
            raise ConnectionError("Khong co ket noi mang de xac thuc ma")
        if code not in PROMO_CODES:
            raise ValueError("Ma khuyen mai khong hop le")
        if code == "NEW-USER" and self.os_version < 26:
            raise ValueError("NEW-USER yeu cau Android API 26 tro len")
        return total * (1 - PROMO_CODES[code])

    def get_nearby_restaurants(self):
        """Look up restaurants for the current GPS position."""
        try:
            latitude, longitude = gps_service.get_current_location()
        except gps_service.GPSSignalLostError:
            return "Khong the xac dinh vi tri"
        return RESTAURANTS_BY_LOCATION.get((latitude, longitude), [])
