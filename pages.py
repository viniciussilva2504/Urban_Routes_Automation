from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from locators import UrbanRoutesLocators as L


class UrbanRoutesPage:
    FROM = L.ADDRESS_FROM
    TO = L.ADDRESS_TO
    PERSONAL = L.PERSONAL_MODE
    COMFORT = L.COMFORT_TARIFF
    PHONE_OPTION = L.PHONE_OPTION
    PHONE = L.PHONE_INPUT
    PHONE_SUBMIT = L.PHONE_MODAL_SUBMIT
    SMS_CODE = L.SMS_CODE_INPUT
    SMS_SUBMIT = L.PHONE_MODAL_SUBMIT
    PHONE_MODAL = L.PHONE_MODAL
    PAYMENT_OPTION = L.PAYMENT_PICKER_BUTTON
    ADD_CARD = L.ADD_CARD_OPTION
    CARD_NUMBER = L.CARD_NUMBER_INPUT
    CARD_CODE = L.CARD_CODE_INPUT
    CARD_SUBMIT = L.CARD_SUBMIT
    PAYMENT_CLOSE = L.PAYMENT_CLOSE
    COMMENT = L.COMMENT_FOR_DRIVER
    REQUIREMENTS_ARROW = L.REQUIREMENTS_TOGGLE
    BLANKET_SWITCH = L.BLANKET_CHECKBOX
    BLANKET_SLIDER = L.BLANKET_SLIDER
    ICE_CREAM_PLUS = L.ICE_CREAM_PLUS
    ICE_CREAM_VALUE = L.ICE_CREAM_VALUE
    ORDER_BUTTON = L.ORDER_BUTTON
    ORDER_MODAL = L.ORDER_MODAL

    def __init__(self, driver):
        self.driver = driver

    def _find(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def _find_present(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def _click(self, locator, timeout=10):
        self._click_element(WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator)))

    def _click_element(self, element):
        element.click()

    def _type(self, element, value):
        element.send_keys(str(value))

    def enter_locations(self, from_text, to_text):
        if from_text:
            self._type(self._find(self.FROM), from_text)
        if to_text:
            self._type(self._find(self.TO), to_text)

    def click_personal(self):
        element = self._find(self.PERSONAL)
        if "active" not in (element.get_attribute("class") or ""):
            self._click(self.PERSONAL)

    def click_request_taxi(self):
        self._click(L.REQUEST_TAXI)

    def ride_options_are_available(self):
        return any(
            element.is_displayed()
            for locator in (self.PERSONAL, self.COMFORT)
            for element in self.driver.find_elements(*locator)
        )

    def select_comfort(self):
        card = self._find(self.COMFORT)
        if "active" not in (card.get_attribute("class") or ""):
            self._click(self.COMFORT)

    def enter_phone(self, phone):
        self._click(self.PHONE_OPTION)
        self._type(self._find(self.PHONE), phone)
        self._click(self.PHONE_SUBMIT)

    def enter_sms_code(self, code):
        field = self._find(self.SMS_CODE)
        self._type(field, code)
        for button in WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(self.SMS_SUBMIT)):
            if button.is_displayed() and button.is_enabled():
                self._click_element(button)
                break

    def phone_modal_is_visible(self):
        return self._find(self.PHONE_MODAL).is_displayed()

    def open_card_form(self):
        for option in WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.PAYMENT_OPTION)
        ):
            if option.is_displayed():
                self._click_element(option)
                break
        self._click(self.ADD_CARD)

    def submit_empty_card_form(self):
        buttons = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.CARD_SUBMIT)
        )
        for button in buttons:
            if button.is_displayed():
                if button.is_enabled():
                    self._click_element(button)
                return

    def get_card_number_value(self):
        return self._find(self.CARD_NUMBER).get_attribute("value")

    def get_card_code_value(self):
        return self._find(self.CARD_CODE).get_attribute("value")

    def card_form_is_visible(self):
        return self._find(self.CARD_NUMBER).is_displayed()

    def add_card(self, number, code):
        for option in WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(self.PAYMENT_OPTION)):
            if option.is_displayed():
                self._click_element(option)
                break
        self._click(self.ADD_CARD)
        self._type(self._find(self.CARD_NUMBER), number)
        cvv = self._find(self.CARD_CODE)
        self._type(cvv, code)
        cvv.send_keys(Keys.TAB)
        for button in WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(self.CARD_SUBMIT)):
            if button.is_displayed() and button.is_enabled():
                self._click_element(button)
                break
        for close in WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(self.PAYMENT_CLOSE)):
            if close.is_displayed():
                self._click_element(close)
                break

    def enter_comment(self, comment):
        field = self._find(self.COMMENT)
        field.clear()
        self._type(field, comment)

    def open_requirements(self):
        arrow = self._find(self.REQUIREMENTS_ARROW)
        if "open" not in (arrow.get_attribute("class") or ""):
            self._click(self.REQUIREMENTS_ARROW)

    def request_blanket(self):
        checkbox = self._find_present(self.BLANKET_SWITCH)
        if not checkbox.is_selected():
            self._click(self.BLANKET_SLIDER)
            WebDriverWait(self.driver, 10).until(lambda _driver: checkbox.is_selected())

    def blanket_requested(self):
        return self._find_present(self.BLANKET_SWITCH).is_selected()

    def request_ice_creams(self, quantity=2):
        self.open_requirements()
        for _ in range(quantity):
            current_quantity = self.ice_cream_quantity()
            self._click(self.ICE_CREAM_PLUS)
            WebDriverWait(self.driver, 10).until(
                lambda _driver: self.ice_cream_quantity() == current_quantity + 1
            )

    def ice_cream_quantity(self):
        return int(self._find(self.ICE_CREAM_VALUE).text)

    def order_taxi(self):
        self._click(self.ORDER_BUTTON)

    def order_modal_is_visible(self):
        return self._find(self.ORDER_MODAL).is_displayed()

    def get_from_value(self):
        return self._find(self.FROM).get_attribute("value")

    def get_to_value(self):
        return self._find(self.TO).get_attribute("value")

    def get_comfort_text(self):
        return self._find(self.COMFORT).text

    def get_comment_text(self):
        return self._find(self.COMMENT).get_attribute("value")
