"""Locadores da interface Urban Routes para testes com Selenium.

Os valores seguem o formato ``(By, seletor)`` aceito por ``find_element`` e
``WebDriverWait.until``. Alguns IDs (``number`` e ``code``) são reutilizados
pela aplicação; por isso, os seletores correspondentes são delimitados pelo
modal que os contém.
"""

from selenium.webdriver.common.by import By


class UrbanRoutesLocators:
    """UI selectors grouped by application flow."""

    # Rota
    ADDRESS_FROM = (By.CSS_SELECTOR, "#from")
    ADDRESS_TO = (By.CSS_SELECTOR, "#to")
    PERSONAL_MODE = (By.XPATH, "//div[contains(@class,'mode') and normalize-space()='Personal']")
    COMFORT_TARIFF = (By.XPATH, "//div[contains(@class,'tcard') and .//div[contains(@class,'tcard-title') and normalize-space()='Comfort']]")
    REQUEST_TAXI = (By.XPATH, "//button[contains(@class,'button round')]")
    COMMENT_FOR_DRIVER = (By.CSS_SELECTOR, "#comment")
    ICE_CREAM_PLUS = (By.XPATH, "//div[contains(@class,'r-counter-container')][.//div[normalize-space()='Sorvete']]//div[contains(@class,'counter-plus')]")
    ICE_CREAM_VALUE = (By.XPATH, "//div[contains(@class,'r-counter-container')][.//div[normalize-space()='Sorvete']]//div[contains(@class,'counter-value')]")
    BLANKET_CHECKBOX = (By.XPATH, "//div[contains(@class,'r-sw-container')][.//div[normalize-space()='Cobertor e lençóis']]//input")
    BLANKET_SLIDER = (By.XPATH, "//div[contains(@class,'r-sw-container')][.//div[normalize-space()='Cobertor e lençóis']]//span[contains(@class,'slider')]")
    ADDRESS_ERROR = (By.CSS_SELECTOR, ".dst-picker .error")

    # Escolha de tipo, modo e tarifa
    TYPE_PICKER = (By.CSS_SELECTOR, ".type-picker")
    TRANSPORT_TYPES = (By.CSS_SELECTOR, ".type-picker .type")
    MODES = (By.CSS_SELECTOR, ".modes-container .mode")
    TARIFF_CARDS = (By.CSS_SELECTOR, ".tariff-cards .tcard")

    # Pedido e comentário
    ORDER_BUTTON = (By.CSS_SELECTOR, ".smart-button")
    ORDER_BUTTON_MAIN_TEXT = (By.CSS_SELECTOR, ".smart-button-main")
    ORDER_BUTTON_SECONDARY_TEXT = (By.CSS_SELECTOR, ".smart-button-secondary")

    # Modal de telefone/SMS
    PHONE_MODAL = (By.CSS_SELECTOR, ".number-picker")
    PHONE_OPTION = (By.XPATH, "//div[@class='np-text' and normalize-space()='Número de telefone']")
    PHONE_INPUT = (By.CSS_SELECTOR, ".number-picker #phone")
    SMS_CODE_INPUT = (By.CSS_SELECTOR, ".number-picker #code")
    PHONE_MODAL_SUBMIT = (By.CSS_SELECTOR, ".number-picker button[type='submit']")
    PHONE_MODAL_CLOSE = (By.CSS_SELECTOR, ".number-picker .section-close")

    # Forma de pagamento e cartão
    PAYMENT_PICKER = (By.CSS_SELECTOR, ".payment-picker")
    PAYMENT_PICKER_BUTTON = (By.CSS_SELECTOR, ".pp-button")
    CASH_OPTION = (By.CSS_SELECTOR, "#cash")
    ADD_CARD_OPTION = (By.XPATH, "//div[contains(@class,'pp-row')][.//div[normalize-space()='Adicionar cartão']]")
    CARD_NUMBER_INPUT = (By.CSS_SELECTOR, ".payment-picker #number")
    CARD_CODE_INPUT = (By.CSS_SELECTOR, ".payment-picker #code")
    CARD_SUBMIT = (By.CSS_SELECTOR, ".payment-picker button[type='submit']")
    PAYMENT_CLOSE = (By.CSS_SELECTOR, ".payment-picker .section-close")
    CARD_NUMBER_ERROR = (By.CSS_SELECTOR, ".payment-picker .card-number-error")
    CARD_CODE_ERROR = (By.CSS_SELECTOR, ".payment-picker .card-code-error")

    # CNH. O número também usa #number, portanto permanece limitado ao modal.
    RIGHTS_PICKER = (By.CSS_SELECTOR, ".rights-picker")
    DRIVER_FIRST_NAME = (By.CSS_SELECTOR, ".rights-picker #firstName")
    DRIVER_LAST_NAME = (By.CSS_SELECTOR, ".rights-picker #lastName")
    DRIVER_BIRTH_DATE = (By.CSS_SELECTOR, ".rights-picker #birthDate")
    DRIVER_LICENSE_NUMBER = (By.CSS_SELECTOR, ".rights-picker #number")
    DRIVER_LICENSE_SUBMIT = (By.CSS_SELECTOR, ".rights-picker button[type='submit']")

    # Requisitos adicionais e estado do pedido
    REQUIREMENTS = (By.CSS_SELECTOR, ".reqs")
    REQUIREMENTS_TOGGLE = (By.CSS_SELECTOR, ".reqs-arrow")
    REQUIREMENT_CHECKBOXES = (By.CSS_SELECTOR, ".reqs input[type='checkbox']")
    COUNTER_INCREMENT = (By.CSS_SELECTOR, ".counter-plus")
    COUNTER_DECREMENT = (By.CSS_SELECTOR, ".counter-minus")
    ORDER_MODAL = (By.CSS_SELECTOR, ".order")
    ORDER_DETAILS = (By.CSS_SELECTOR, ".order-details")
    ORDER_CANCEL = (By.CSS_SELECTOR, ".order button")


# Exemplo de uso:
# wait.until(EC.element_to_be_clickable(UrbanRoutesLocators.ADD_CARD_OPTION)).click()
# driver.find_element(*UrbanRoutesLocators.CARD_NUMBER_INPUT).send_keys("1234 5678 9100")
