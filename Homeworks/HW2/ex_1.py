import requests # Используется для отправки HTTP-запросов
from bs4 import BeautifulSoup # Для парсинга HTML и XML документов
import urllib.parse # Для склейки URL
from datetime import datetime # Для работы с датами и временем
import time # Для работы со временем
import re # Для работы с регулярными выражениями
import json # Для работы с форматом данных JSON

# Функция для получения данных о кассовых сборах
def get_box_office_data():
    # URL страницы, с которой будут собираться данные
    url = 'https://books.toscrape.com/'
    # Заголовки запроса для имитации запроса от браузера
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    data = []
    # Отправка GET-запроса на URL
    response = requests.get(url, headers=headers)
    # Разбор HTML-кода страницы
    soup = BeautifulSoup(response.content, 'html.parser')

    # Список для хранения ссылок на страницы с детальной информацией о книгах
    release_links = []
    # Поиск всех элементов td с определенным классом, содержащих ссылки на фильмы
    for link in soup.find_all('article', class_='product_pod'):
        h3 = link.find('h3')
        if h3:
            a_tag = link.find('a') # Поиск тега <a> внутри элемента
            if a_tag:
                release_links.append(a_tag.get('href')) # Добавление ссылки на книгу в список
    # Преобразование относительных ссылок в абсолютные
    url_joined = [urllib.parse.urljoin('https://books.toscrape.com/', link) for link in release_links]
    # Список для хранения собранных данных
    data = []
    # Перебор всех ссылок для получения детальной информации о каждом фильме
    for url in url_joined:
        response = requests.get(url, headers=headers) # Отправка запроса
        soup = BeautifulSoup(response.content, 'html.parser') # Разбор HTML
        table = soup.find('div', class_='col-sm-6 product_main')

        if not table:
            continue
        prices = []
        instocks = []
        # Сбор данных из таблицы
        row_data = {}  # Словарь для хранения данных о книге
        title = table.find('h1').text
        if title:
            row_data['title'] = title

        price = table.find('p', class_='price_color').text.replace('£', '')
        if price:
            row_data['price'] = price

        instock = table.find('p', class_='instock availability').text.strip()
        instock = int(re.sub('[^0-9]', '', instock))
        if instock:
            row_data['instock_availability'] = instock

        common = soup.find('article', class_='product_page').find_all('p')
        for com in common:
             if len(com.contents) == 1 and com.contents[0][0] !='£':
                 row_data['description'] = com.text.strip()
        if row_data:
            data.append(row_data)  # Добавление данных о фильме в общий список
            time.sleep(1)  # Задержка для предотвращения блокировки (закомментировано)

    return data

# Функция для сохранения данных в формате JSON
def save_data_to_json(data, filename='books.json'):
    with open(filename, 'w') as f: # Открытие файла для записи
        json.dump(data, f, indent=4) # Сохранение данных в формате JSON с отступами

# Главная функция
def main():
    data = get_box_office_data() # Получение данных о кассовых сборах
    save_data_to_json(data) # Сохранение данных в файл

if __name__ == "__main__":
    main()