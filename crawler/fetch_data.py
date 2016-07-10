# -*- coding: utf-8 -*-

from urllib import urlopen
from bs4 import BeautifulSoup

from crawler.offer import OfferFlat
from url import UrlModel

SEPARATOR = ';'


def get_pagination_urls(district, price):
    url_model = UrlModel(district=district)
    url_model.set_filter_price(price=price)

    html_document = urlopen(url_model.get_url()).read()
    soup = BeautifulSoup(html_document, "html.parser")

    pages_number = int(soup.find('form', id='pagerForm').find("strong", {'class': 'current'}).text)

    return [url for url in url_model.generate_all_urls(range(1, pages_number + 1))]


def get_offers_for_page(soup):
    for offer in soup.find(u'div', {u'class': u'col-md-content'}) \
            .findAll(u'article', {u'class': u'offer-item'}):
        yield offer


def fetch_data(district, price):
    urls = get_pagination_urls(district=district, price=price)
    soup_list = []
    offers = []

    for url in urls:
        html_document = urlopen(url).read()
        soup_list.append(BeautifulSoup(html_document, u'html.parser'))

    if not len(soup_list):
        raise ValueError(u'Found no offers')

    for soup in soup_list:
        offers.append(get_offers_for_page(soup))

    for offer_gen in offers:
        for offer in offer_gen:
            offer_flat = OfferFlat(offer)
            offer_flat.populate_object()
            yield offer_flat


def print_offers_data(district, price):

    with open('file.scv', 'w') as outfile:
        for offer in fetch_data(district=district, price=price):
            outfile.write(str(offer.title) + SEPARATOR + str(offer.area) + SEPARATOR +
                          str(offer.price) + SEPARATOR + str(offer.price_mkw) + SEPARATOR +
                          offer.url + SEPARATOR + '\n')
            print offer.title
            print offer.area
            print offer.price
            print offer.price_mkw
            print '---------------------'
