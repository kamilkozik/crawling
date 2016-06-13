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
        if not isinstance(soup, BeautifulSoup):
            raise TypeError('Expected %s type' % type(BeautifulSoup))

        if soup.find('article', {'class': 'offer-item'}):
            self.soup = soup
        else:
            raise ValueError('Cannot find article html tag.')

    def get_offer_title(self):
        return self.soup.find('header').find('p', {'class': 'text-nowrap'})

    def set_offer_title(self):
        self.title = self.get_offer_title()

    def get_offer_url(self):
        return self.soup.find('article').get('data-url')

    def set_offer_url(self):
        self.title = self.get_offer_url()

    def get_offer_price(self):
        price_text = self.soup.find('li', {'class': 'offer-item-price'}).text
        price = int(price_text.replace(u'zł', u'').replace(u' ', u''))
        return price

    def set_offer_price(self):
        self.title = self.get_offer_url()

    def get_offer_area(self):
        area_text = self.soup.find('li', {'class': 'offer-item-area'}).text
        area = int(area_text.replace(u'm', u'').replace(u'&#178;', u'').replace(u' ', u''))
        return area

    def set_offer_price(self):
        self.title = self.get_offer_url()

    def generate_row(self):
        pass
