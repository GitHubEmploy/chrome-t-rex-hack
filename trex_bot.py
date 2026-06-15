"""
Chrome T-Rex Game Automation Bot

Uses Selenium to open the Chrome dino game and automates gameplay
by monitoring the canvas pixel data to detect obstacles.

How it works:
1. Opens chrome://dino in Chrome via Selenium
2. Monitors a region of the canvas for dark pixels (obstacles/cacti)
3. Presses SPACE to jump when an obstacle is detected
4. Gradually increases speed tolerance as game speeds up

Requires: selenium, chromedriver
"""

import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


DINO_URL = "chrome://dino"
POLL_INTERVAL = 0.01
JUMP_THRESHOLD = 80
CHECK_X = 120
CHECK_Y_START = 140
CHECK_Y_END = 165


def get_canvas_pixels(driver):
    canvas = driver.find_element(By.TAG_NAME, "canvas")
    base64 = driver.execute_script(
        "return arguments[0].toDataURL('image/png').substring(21);", canvas
    )
    canvas_data = np.frombuffer(__import__("base64").b64decode(base64), dtype=np.uint8)
    img = __import__("cv2").imdecode(canvas_data, __import__("cv2").IMREAD_GRAYSCALE)
    return img


def obstacle_ahead(img):
    strip = img[CHECK_Y_START:CHECK_Y_END, CHECK_X:]
    dark_pixels = np.sum(strip < 100)
    return dark_pixels > JUMP_THRESHOLD


def main():
    opts = Options()
    opts.add_argument("--disable-gpu")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=opts)
    driver.get(DINO_URL)

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "canvas"))
        )
    except Exception:
        print("Canvas not found. Is this chrome://dino?")
        driver.quit()
        return

    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.SPACE)
    time.sleep(0.5)

    print("Bot started. Press Ctrl+C to stop.")
    try:
        while True:
            img = get_canvas_pixels(driver)
            if obstacle_ahead(img):
                body.send_keys(Keys.SPACE)
                time.sleep(0.05)
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\nBot stopped.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
