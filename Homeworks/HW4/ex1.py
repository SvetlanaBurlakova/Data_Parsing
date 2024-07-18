import requests
from lxml import html
from pymongo import MongoClient
import csv
import time

# Функция для скрейпинга табличных данных с одной страницы
def scrape_page_data(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)
    table_rows = tree.xpath('//*[@id="rrp_table_wrapper"]/table/tbody/tr')
    data = []
    for row in table_rows:
        columns = row.xpath(".//td/text()")
        # Парсинг позиции в рейтинге, преобразование данных в целочисленное значение
        try:
            rank = int(columns[0].strip())
        except:
            rank = None
        # Парсинг названия университета, прописаны 2 варианты, учитавающие наличие/отсутствие лого
        try:
            name = row.xpath('.//th[2]/div/div/div[2]/a/b/text()')[0]
        except:
            name = row.xpath('.//th[2]/div/div/div/a/text()')[0].strip()
        # Парсинг позиции в рейтинге в 2022 году, преобразование данных в число с плавающей точкой
        try:
            rank_2022 = float(columns[1].strip())
        except:
            rank_2022 = None
        # Парсинг уровня качества, преобразование данных в целочисленное значение
        try:
            quality = int(columns[2].strip())
        except:
            quality = None
        # Парсинг уровня спроса, преобразование данных в целочисленное значение
        try:
            demand = int(columns[3].strip())
        except:
            demand = None
        # Парсинг уровня научных исследований в университете, преобразование данных в целочисленное значение
        try:
            science = int(columns[4].strip())
        except:
            science = None
        # Добавления данных по университету в словарь
        data.append({
            'rank': rank,
            'name': name,
            'rank_2022': rank_2022,
            'quality': quality,
            'demand': demand,
            'science': science})
    return data


# Main function
def main():
    #Ссылка на главную страницу
    url = "https://raex-rr.com/education/russian_universities/top-100_universities/2023/"
    data = scrape_page_data(url)
    # Создание файла csv и запись в файл полученного словаря с информацией об университетах
    with open('top_universities.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['rank', 'name', 'rank_2022', 'quality', 'demand', 'science'])
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    main()