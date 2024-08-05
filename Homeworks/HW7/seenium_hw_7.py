import csv
import os
import re

import requests
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import json

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
chrome_options = Options()
chrome_options.add_argument(f'user-agent={user_agent}')
browser = webdriver.Chrome(options=chrome_options)
try:
    browser.get("https://www.themoviedb.org/")
    WebDriverWait(browser, 10).until(ec.presence_of_all_elements_located((By.TAG_NAME, 'body')))
    search_box = browser.find_element(By.XPATH,  '//*[@id="inner_search_v4"]')
    search_box.send_keys("трансформеры")
    browser.find_element(By.XPATH, '//*[@id="inner_search_form"]/input').click()
    table = browser.find_element(By.XPATH, '//*//div[@class="white_column"]')
    for row in table.find_elements(By.XPATH, './/*//div[@class="details"]'):
        try:
            title = row.find_element(By.XPATH, './/*//a/h2')
            title_name = title.text
# Так как на данном сайте категории меняются в зависимости от того, что введено в поиске, я сделала скрэппинг только  первой страницы поиска,
# не переходя в другие категории
            if not title_name:
                break
        except:
            title_name = 'Название неизвестно'
        try:
            release_date = row.find_element(By.XPATH, './/span[@class="release_date"]')
            release_date_name = release_date.text
        except:
            release_date_name = 'Дата выхода неизвестна'
        try:
            info = row.find_element(By.XPATH, './/*//p')
            info_name = info.text
        except:
            info_name = 'Описания нет'

        data = {'title': title_name, 'release_date': release_date_name, 'info': info_name}
        print(data)
        with open('hw_sem_7.csv', 'a+', newline='', encoding='utf-8') as f:
            fieldnames = ['title', 'release_date', 'info']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if os.path.getsize('hw_sem_7.csv') == 0:
                writer.writeheader()
            writer.writerow(data)


except Exception as E:
    print(f'Произошла ошибка {E}')
finally:
    browser.quit()