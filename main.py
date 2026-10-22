import time
import data
import helpers
from pages import UrbanRoutesPage
import pytest


class TestUrbanRoutes:
    @pytest.fixture(autouse=True)
    def use_browser(self, driver):
        self.driver = driver

    def prepare_request(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.click_personal()
        page.click_request_taxi()
        page.select_comfort()
        return page

    def retrieve_code(self):
        last_error = None
        for _ in range(5):
            try:
                return helpers.retrieve_phone_code(self.driver)
            except Exception as error:
                last_error = error
                time.sleep(1)
        raise last_error

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert page.get_from_value() == data.ADDRESS_FROM
        assert page.get_to_value() == data.ADDRESS_TO

    @pytest.mark.parametrize(
        "origin, destination",
        [("", data.ADDRESS_TO), (data.ADDRESS_FROM, "")],
        ids=["missing-origin", "missing-destination"],
    )
    def test_incomplete_route_is_rejected(self, origin, destination):
        """Keep ride options unavailable when either route address is missing."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_locations(origin, destination)

        assert page.get_from_value() == origin
        assert page.get_to_value() == destination
        assert not page.ride_options_are_available()

    def test_select_plan(self):
        page = self.prepare_request()
        assert "Comfort" in page.get_comfort_text()

    def test_fill_phone_number(self):
        page = self.prepare_request()
        page.enter_phone(data.PHONE_NUMBER)
        code = self.retrieve_code()
        page.enter_sms_code(code)

    def test_rejects_invalid_sms_code(self):
        """Keep phone confirmation open when the valid code is altered."""
        page = self.prepare_request()
        page.enter_phone(data.PHONE_NUMBER)
        valid_code = self.retrieve_code()
        assert valid_code, "Expected a test SMS code from the app network log"
        invalid_code = str((int(valid_code[0]) + 1) % 10) + valid_code[1:]

        page.enter_sms_code(invalid_code)

        assert page.phone_modal_is_visible()

    def test_fill_card(self):
        page = self.prepare_request()
        page.enter_phone(data.PHONE_NUMBER)
        page.enter_sms_code(self.retrieve_code())
        page.add_card(data.CARD_NUMBER, data.CARD_CODE)

    def test_rejects_empty_card_details(self):
        """Do not accept or advance from the card form when it is left empty."""
        page = self.prepare_request()
        page.enter_phone(data.PHONE_NUMBER)
        page.enter_sms_code(self.retrieve_code())
        page.open_card_form()
        page.submit_empty_card_form()

        assert page.card_form_is_visible()
        assert page.get_card_number_value() == ""
        assert page.get_card_code_value() == ""

    def test_comment_for_driver(self):
        page = self.prepare_request()
        page.enter_comment(data.MESSAGE_FOR_DRIVER)
        assert page.get_comment_text() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        page = self.prepare_request()
        page.open_requirements()
        page.request_blanket()
        assert page.blanket_requested()

    def test_order_2_ice_creams(self):
        page = self.prepare_request()
        page.request_ice_creams(2)
        assert page.ice_cream_quantity() == 2

    def test_car_search_model_appears(self):
        page = self.prepare_request()
        page.enter_phone(data.PHONE_NUMBER)
        page.enter_sms_code(self.retrieve_code())
        page.add_card(data.CARD_NUMBER, data.CARD_CODE)
        page.enter_comment(data.MESSAGE_FOR_DRIVER)
        page.open_requirements()
        page.request_blanket()
        page.request_ice_creams(2)
        page.order_taxi()
        assert page.order_modal_is_visible()
