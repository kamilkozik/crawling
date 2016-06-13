from urllib import urlopen
from bs4 import BeautifulSoup

from url import UrlModel


def fetch_data(district, price):
    url_model = UrlModel(district=district)
    url_model.set_filter_price(price=price)

    site_content = urlopen(url_model.get_url()).read()
    soup = BeautifulSoup(site_content, "html.parser")

    pages_number = int(soup.find('form', id='pagerForm').find("strong", {'class': 'current'}).text)

    for url in url_model.generate_all_urls(range(1, pages_number + 1)):
        print url
