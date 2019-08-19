import urllib.request
import csv
import brotli

from bs4 import BeautifulSoup

headers = {"Host": "glavcom.ua",
           "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
           "Accept": "text/css,*/*;q=0.1",
           "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
           "Accept-Encoding": "gzip, deflate, br",
           "DNT": "1",
           "Connection": "keep-alive",
           "Cookie": "__cfduid=d96a511dc113177453717c58ea2a775381566151570; xs=cec6ad7a6605ef7a5cb3dcb813cdb835; sa_userid=0; cbtYmTName=WSJ7MD17Y3toazg4Om84YThsO2s7bWw8eyQ4; 5183af98523bb467d9fc4781603dd09d=9abcd682a463cfd524eb5926652b4e83", }

burl = "https://glavcom.ua/tags/ministerstvo-osviti-i-nauki.html#"


def get_html(url):
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    content = brotli.decompress(response.read())

    return content.decode('utf-8')


def get_page_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    paggination = soup.find('ul', class_='pagination')
    return int(paggination.find_all('a')[-2].text)


def parse(html):
    projects = []
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('ul', class_='list')

    for nev in div.find_all('li'):
        for a in nev.find_all('a'):
            photo ='https://glavcom.ua' + nev.find('img').get('src')
            headerr = nev.a.text.replace('\n', '')
            opis = nev.find('div', class_="header").text
            link = 'https://glavcom.ua' + nev.find('a').get('href')

        projects.append({
            'image': photo,
            'head': headerr,
            'opis': opis,
            'link': link
        })

    for project in projects:
        print(project)

    return projects


def save(projects, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')

        writer.writerow(('Image_Link', 'Title', 'Discription', 'News_Link'))

        writer.writerows(
            (project['image'], project['head'], project['opis'], project['link']) for project in projects
        )


def get_pages(html):
    soup = BeautifulSoup(html, 'html.parser')

    pages = soup.find_all('ul', class_='pagination').find_all('a')[-1].get('href')

    print('pages')


def main():
    projects = []

    total_pages = get_page_count(get_html(burl))

    print('%d all_pages...' % total_pages)

    for page in range(1, total_pages):
        print('\nPars %d%% (%d/%d)' % (page / total_pages * 100, page, total_pages))
        projects.extend(parse(get_html(burl + 'page=%d' % page)))

    save(projects, 'glavcom.csv')


if __name__ == '__main__':
    main()
