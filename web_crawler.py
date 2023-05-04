import re
from pprint import pprint
# from textfiles.file_factory import TextFile
from bs4 import BeautifulSoup
import requests


def manage_screp(host: str, link_n: str | int, restaurants: dict, count: int):
    link_to_next = restaurant_screp(host, link_n, restaurants, count)
    if link_to_next:
        manage_screp(host, link_to_next, restaurants, count)
        # return
    else:
        return


def restaurant_screp(host: str, link_n: str | int, restaurants: dict, count: int):

    if count == 0:
        return link_n
    elif link_n == 0:
        return None
    response = requests.get(f'{host}{link_n}')
    # print(response.text)

    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup.get_text(strip=True))
    all_li = soup.find_all('li', {'class': 'row restaraunt-one'})  # row restaraunt-one non-bg
    if not all_li:
        all_li = soup.find_all('li', {'class': 'row restaraunt-one non-bg'})
    for rest in all_li:
        # print(rest)
        name = rest.find('a', {'class': 'restaurant-logo'})
        res_id = name.attrs['id']
        if res_id not in restaurants:
            # print(rest.ul.li.span.a.get('onclick'))
            # print(name.attrs['href'])
            # print(name.img.attrs['src'])
            waze = rest.find('span', {'class': 'adress'})
            # print(waze.a.attrs['href'])
            new_restaurant = {
                'name': rest.h3.a.text,
                'link': name.attrs['href'],
                'id': res_id,
                'waze': waze.a.attrs['href'],
                'address': waze.a.text,
                'logo': name.img.attrs['src'],
                'description': rest.p.a.text,
            }
            restaurants[res_id] = new_restaurant

    # pprint(restaurants)
    next_page = soup.find('div', {'id': 'ctl00_ContentPlaceHolder1_Searchresaultstable1_pnlNext'})
    print(next_page.a.get('href'))
    return restaurant_screp(host, next_page.a.get('href') if next_page.a.get('href') else 0, restaurants, count-1)

    # print(name.a.text)
    # body = soup.find("button")

    # print(all_li)
    # body.find_all('p')










if __name__ == '__main__':

    host_name = 'https://www.2eat.co.il'
    link = '/searchrestaurants.aspx?RLoc=9&RSub=1'
    all_restaurant = {}

    manage_screp(host_name, link, all_restaurant, 20)
    pprint(all_restaurant)

    # url = "https://easy.co.il/list/Restaurants"
    # html_doc = requests.get(url).content
    # print(html_doc)
    # soup = BeautifulSoup(html_doc, 'html.parser')
    # print(soup.prettify())
    #
    # a_tags = soup.find_all("a")
    # print(a_tags)

    # header = soup.find("div", {'class': 'header'})
    # print(type(header))
    # print(header)
    # print(header.name)
    # print(header.attrs)

    # re.findall(r"/exercise/.*", "/exercise/2014/01/29/01-character-input.html")
    # all_a = soup.find_all("div", attrs=dict(href=re.compile("/exercise/.*")))
    # print(all_a[0].attrs['href'])

