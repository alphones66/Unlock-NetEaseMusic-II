# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0040A8DAD94A5493279A06C51B534B5E7AD8F8FA116494090081E177A5FF22A6889331AE4F45C58941E1E27A2DF1E19F31BD3732A1512929601F791000632283692D1DD2F8C2A5A238262B185C4E43BFC55999FE4D62705D65849835DE76F0F135DA718F53B55AA76B2F67B3201448ED4140575887C49CEFA6568A734E421C02CFB178AEE81F59705DF5312A8CA205BB6F8ABFC47A2F57323D6904F5AE7927054E725065EEA89BF841FA2825A6A2A109111FCDA32B844C684119637E9E4D2202817751593E64A7B4551F34E417683311A973CC58522172297EEB79DCF0CF7723EBA5EBE2B27D2F76AE6728CAE31EDEC604A931B3CFA4A850832E3022172ED9DE99685E91362D3E84DB8F972D1AE25BF6097F35637E849C7590AF35F2E1E9F91FC5C7C09E125C3564E71C96928C75AD69FC40D6539CE4C6E57C7EFFF7E24BC8984C846AC939EE84A7684F7AD5F454699A643D0594B68F1FE586EDFB514A83C4708B9ED29999D6D1A7CE860BF057EA5F7D128AAF572C6437309070404F4A84DB53AD2A5062B2645A6FD0EA133EB2B97B033E8541004EA4FAD2A85000858812306B52"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
