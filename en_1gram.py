from selenium import webdriver
import urllib
import json
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os


def read_json(filename):
    """Read json file"""
    with open(filename, mode='r', encoding='utf-8', newline='') as f:
        return json.load(f)


def write_json(filename, data):
    """Write data to json file"""
    with open(filename, mode='w', encoding='utf-8', newline='') as f:
        json.dump(data, f, ensure_ascii=False)


def write_file(text, filename):
    """Write text to file"""
    with open(filename, mode='w', encoding='utf-8') as f:
        f.write(text)


if __name__ == '__main__':
    driver = webdriver.Remote(command_executor=f'http://localhost:4444/wd/hub', options=webdriver.ChromeOptions())
    driver.maximize_window()

    words = read_json('en_1gram.json')

    # get not downloaded words
    downloaded_en_words = [x.split('.')[0] for x in os.listdir('en_words')]
    words = list(set(words) - set(downloaded_en_words))

    for en_word in words:
        url = 'https://www.online-translator.com/conjugation%20and%20declination/english/{}'.format(
            en_word)
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "bott_link")))
        write_file(driver.page_source, os.path.join('en_words', en_word + '.html'))
    driver.close()
    driver.quit()
