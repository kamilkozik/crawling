# -*- coding: utf8 -*-

from bs4 import BeautifulSoup


class OfferFlat(object):
    url = None
    title = None
    price = None
    price_mkw = None
    area = None

    soup = None

    def __init__(self, soup):
        if len(soup):
            self.soup = soup

    def populate_object(self):
        self.set_offer_title()
        self.set_offer_area()
        self.set_offer_price()
        self.set_offer_price_mkw()
        self.set_offer_url()

    def get_offer_title(self):
        return self.soup.find('header').find('p', {'class': 'text-nowrap'}).text.encode('utf8', 'ignore')

    def set_offer_title(self):
        self.title = self.get_offer_title()

    def get_offer_url(self):
        return self.soup.get('data-url').encode('utf8', 'ignore')

    def set_offer_url(self):
        self.url = self.get_offer_url()

    def get_offer_price(self):
        price_text = self.soup.find('li', {'class': 'offer-item-price'}).text.encode('utf8', 'ignore')
        price = float(price_text.replace('zł', '').replace(' ', '')
                      .replace(',', '.'))
        return price

    def set_offer_price(self):
        self.price = self.get_offer_price()

    def get_offer_price_mkw(self):
        price_text = self.soup.find('li', {'class': 'offer-item-price-per-m'}).text.encode('utf8', 'ignore')
        price_mkw = price_text.replace('zł/m²', '').replace(' ', '')\
            .replace(',', '.')
        return price_mkw

    def set_offer_price_mkw(self):
        self.price_mkw = self.get_offer_price_mkw()

    def get_offer_area(self):
        area_text = self.soup.find('li', {'class': 'offer-item-area'}).text.encode('utf8', 'ignore')
        area = area_text.replace('m²', '').replace(' ', '') \
            .replace(',', '.')

        if area.find('do'):
            area_range = area.split('do')
            return area_range[0]
        return area

    def set_offer_area(self):
        self.area = self.get_offer_area()
