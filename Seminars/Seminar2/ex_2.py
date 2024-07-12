from bs4 import BeautifulSoup
import requests
import urllib.parse
import pandas as pd

url = 'https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
# print(soup.prettify())
release_link = []
for link in soup.find_all('td', {'class': 'a-text-left mojo-field-type-release mojo-cell-wide'}):
    a_tag = link.find('a')
    if a_tag:
        release_link.append(a_tag.get('href'))

url_joined = [urllib.parse.urljoin('https://www.boxofficemojo.com', link) for link in release_link]
table = soup.find('table', {'class': 'a-bordered'})
headers = [header.text.strip() for header in table.find_all('th') if header.text]

data = []
for row in table.find_all('tr'):
    row_data = {}
    cells = row.find_all('td')
    if cells:
        row_data[headers[0]] = cells[0].find('a').text if cells[0].find('a') else ''
        row_data[headers[1]] = cells[1].find('a').text if cells[1].find('a') else ''
        row_data[headers[2]] = cells[2].text
        row_data[headers[3]] = cells[3].find('a').text if cells[3].find('a') else ''
        row_data[headers[4]] = cells[4].find('a').text.strip() if cells[4].find('a') else ''
        row_data[headers[5]] = cells[5].text.replace('$','').replace(',','')
        data.append(row_data)

df = pd.DataFrame(data)
print(df)

