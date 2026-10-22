"""Capture a browser-only animated GIF of the Urban Routes booking flow."""

from io import BytesIO
from pathlib import Path
import sys
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import data  # noqa: E402
import helpers  # noqa: E402
from pages import UrbanRoutesPage  # noqa: E402


def main():
    gif_path = ROOT / "docs" / "assets" / "urban-routes-booking.gif"
    browser = webdriver.Chrome(options=Options())
    browser.set_window_size(1280, 820)
    browser.implicitly_wait(0)
    frames = []

    def capture(step):
        time.sleep(1)
        frame = Image.open(BytesIO(browser.get_screenshot_as_png())).convert("RGB")
        frames.append(frame)
        print(f"Demo step: {step}")

    try:
        browser.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(browser)
        capture("Plan a ride")
        page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        capture("Enter the route")
        page.click_personal()
        page.click_request_taxi()
        page.select_comfort()
        capture("Choose Comfort")
        page.enter_phone(data.PHONE_NUMBER)
        code = None
        for attempt in range(5):
            try:
                code = helpers.retrieve_phone_code(browser)
                break
            except Exception:
                if attempt == 4:
                    raise
                time.sleep(1)
        page.enter_sms_code(code)
        capture("Confirm the phone")
        page.add_card(data.CARD_NUMBER, data.CARD_CODE)
        capture("Add payment")
        page.enter_comment(data.MESSAGE_FOR_DRIVER)
        page.open_requirements()
        page.request_blanket()
        page.request_ice_creams(2)
        capture("Set ride options")
        page.order_taxi()
        capture("Review the booking")

        gif_path.parent.mkdir(parents=True, exist_ok=True)
        frames[0].save(
            gif_path,
            save_all=True,
            append_images=frames[1:],
            duration=[1200] * (len(frames) - 1) + [2500],
            loop=0,
            optimize=True,
        )
        print(f"Saved browser-only demo GIF: {gif_path}")
    finally:
        browser.quit()


if __name__ == "__main__":
    main()
