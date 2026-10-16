import unittest
from unittest.mock import patch

from gps_service.gps_service import GPSSignalLostError
from yummy_app import ConnectionError, YummyApp


class TestEasyLevel(unittest.TestCase):
    """Core calculation tests supplied for Level 1."""

    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        cart = {"pho": 2}
        self.assertEqual(self.app.calculate_order_total(cart), 100000)

    def test_calculate_total_for_multiple_items(self):
        cart = {"pho": 1, "com": 1}
        self.assertEqual(self.app.calculate_order_total(cart), 95000)

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0)

    def test_calculate_total_with_zero_quantity(self):
        self.assertEqual(self.app.calculate_order_total({"pho": 0}), 0)

    def test_phobosaurieng(self):
        cart = {"phobosaurieng": 1}
        self.assertEqual(self.app.calculate_order_total(cart), 999000)


class TestMediumLevel(unittest.TestCase):
    """Mocking tests for the online promotion service."""

    def test_apply_promo_code_online(self):
        app = YummyApp(online=True)
        self.assertEqual(app.apply_promo_code(100000, "PROMO10"), 90000)

    def test_apply_promo_code_offline_raises_connection_error(self):
        app = YummyApp(online=False)
        with self.assertRaises(ConnectionError):
            app.apply_promo_code(100000, "PROMO10")

    def test_apply_promo_code_unknown_code_raises_value_error(self):
        app = YummyApp()
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "INVALID")

    def test_new_user_promo_requires_supported_os(self):
        app = YummyApp(os_version=25)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "NEW-USER")


class TestHardLevel(unittest.TestCase):
    """GPS boundary tests using mocks instead of a mobile device."""

    @patch("yummy_app.gps_service.get_current_location", return_value=(10.0, 105.0))
    def test_get_nearby_restaurants_for_mocked_location(self, mocked_location):
        app = YummyApp()
        self.assertEqual(
            app.get_nearby_restaurants(),
            ["Quan Pho Ha Noi", "Com Tam Sai Gon"],
        )
        mocked_location.assert_called_once_with()

    @patch(
        "yummy_app.gps_service.get_current_location",
        side_effect=GPSSignalLostError,
    )
    def test_get_nearby_restaurants_when_gps_signal_is_lost(self, mocked_location):
        app = YummyApp()
        self.assertEqual(app.get_nearby_restaurants(), "Khong the xac dinh vi tri")
        mocked_location.assert_called_once_with()
