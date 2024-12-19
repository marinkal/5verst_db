from bs4 import BeautifulSoup as bsoup
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from helpers import generate_dates


import csv
import re
import requests


def process_page_rows(page_rows: list, href: str, location) -> list[dict]:
    pattern_time = r'\d{2}:\d{2}:\d{2}'
    pattern_cat = r'[МЖ]\d{2}(-\d{2})?'
    pattern_id = r'https?://5verst.ru/userstats/(\d+)'
    page_runners = []
    for p_row in page_rows:
        new_row = {
            'href': href,
            'location': location,
            'sat': saturday,
            'place': None,
            'runner_id': None,
            'fio': None,
            'category': None,
            'time': None,
            'show_time': None
        }
        first = True
        for child in p_row:
            if first:
                if not child.get_text().isdigit():
                    return page_runners
                new_row['place'] = child.get_text()
                first = False
                continue

            a = child.select_one('td a')
            if a and hasattr(a, 'attrs'):
                m = re.match(pattern_id, a.attrs['href'])
                if m:
                    new_row['runner_id'] = m[1]
                    new_row['fio'] = a.get_text()
                    
            if re.match(pattern_time, child.get_text()):
                new_row['show_time'] = datetime.strptime(child.get_text(), '%H:%M:%S')
                parts = child.get_text().split(':')
                new_row['time'] = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            if m := re.match(pattern_cat, child.get_text()):
                new_row['category'] = m[0]  # в строке содержится инфа о категории

        page_runners.append(new_row)

    return page_runners


def get_location_from_link(link: str) -> str:
    if m := re.match(r'https?://5verst.ru/(\w+)/results/\d{2}\.\d{2}\.\d{4}', 
                     link):
        return m[1]


def process_page(row, saturday):
    href = row.attrs['href'].replace('all', f'{saturday}/')
    location = get_location_from_link(href)
    response = requests.get(href)
    page_content = response.content
    soup = bsoup(page_content, 'html.parser')
    page_rows = soup.select('tbody tr')
    if not page_rows:
        return []

    return process_page_rows(page_rows, href, location)


def process_saturday(saturday: str, url: str):
    response = requests.get(url)
    content = response.content
    soup = bsoup(content, 'html.parser')
    rows = soup.select('tbody tr>td div a')

    with ThreadPoolExecutor(max_workers=8) as executor:
        runners_exec = [
            executor.submit(process_page, row, saturday)
            for row in rows
        ]

    all_runners = []
    for part in runners_exec:
        all_runners.extend(part.result())

    return all_runners


saturdays = generate_dates('02.12.2023', '%d.%m.%Y')


all_rows = []
url = 'https://5verst.ru/results/all/'
for saturday in saturdays:
    all_rows.extend(process_saturday(saturday, 'https://5verst.ru/results/all/'))
with open('data1.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Страница', 'Локация', 'Дата', 'Место в рейтинге', 'id бегуна', 'категория', 'секунды', 'время'])
    for row in all_rows:
        csvwriter.writerow(row.values())
