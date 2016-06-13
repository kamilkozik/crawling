# -*- coding: utf8 -*-

PROTOCOL = u'http://'
DOMAIN = u'otodom.pl/'
FILTER_PRICE_URL = u'search%%5Bfilter_float_price%%3Ato%%5D=%d'
FILTER_DISTRICT_URL = u'search%%5Bdistrict_id%%5D=%d'
URL_SUFFIX = u'sprzedaz/mieszkanie/warszawa/'

# We need mapping for districts
# Districts names

BIELANY = u'bielany'
ZOLIBORZ = u'zoliborz'

DISTRICTS_IDS = {
    BIELANY: 38,
    ZOLIBORZ: 53,
}


class UrlModel(object):
    protocol = str()
    domain = str()
    url_suffix = str()
    url = str()

    filter_price = None
    filter_district_id = None

    def __init__(self, district):
        if not isinstance(district, str):
            raise AttributeError('Invalid district type: %s' % type(district))

        if not district:
            raise AttributeError('District attr has not been provided, got: %s' % district)

        if self.get_district_id(self.district_name_prepare(district)):
            self.filter_district_id = self.get_district_id(self.district_name_prepare(district))
        else:
            raise ValueError('District id for %s has not been found.' % district)

        self.protocol = PROTOCOL
        self.domain = DOMAIN
        self.url_suffix = URL_SUFFIX

    @staticmethod
    def get_district_id(district):
        return DISTRICTS_IDS.get(district)

    @staticmethod
    def district_name_prepare(string):
        return string.strip().lower()

    def set_filter_price(self, price):
        if isinstance(price, int):
            self.filter_price = price
        else:
            raise ValueError("Invalid price type: %s" % type(price))

    def get_base_url(self):
        if self.protocol and self.domain and self.url_suffix:
            return ''.join([self.protocol, self.domain, self.url_suffix])

    def set_url(self):
        base_url = self.get_base_url()
        filter_urls = []

        if self.filter_district_id:
            filter_urls.append(FILTER_DISTRICT_URL % self.filter_district_id)

        if self.filter_price:
            filter_urls.append(FILTER_PRICE_URL % self.filter_price)

        # Display 72 offers per site
        filter_urls.append(u'nrAdsPerPage=72')
        if filter_urls:
            self.url = base_url + u'?' + u'&'.join(filter_urls)
        else:
            self.url = base_url
        print "[UrlModel](Applying url: %s)" % self.url
        return self.url

    def get_url(self):
        return self.set_url()

    def generate_all_urls(self, range_offset):
        if not self.url:
            self.set_url()
        urls = [self.url + u'&page=%d' % page for page in range_offset]
        print 'Generated urls: %d' % len(urls)
        return urls

# List of needed tools and features:
#   1. Class that handle files jobs
#   2. Class that will handle fetching html documents
#   3. http://otodom.pl/sprzedaz/mieszkanie/warszawa/?search%5Bfilter_float_price%3Ato%5D=400000&&search%5Bdistrict_id%5D=53