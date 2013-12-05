from urllib2 import urlopen

from bs4 import BeautifulSoup


class BaseScraper(object):
    def __init__(self, url, img_hostname):
        self.url = url
        self.img_hostname = img_hostname
        self.url_buffer = urlopen(url)
        self.scraper = BeautifulSoup(self.url_buffer.read())
        self.url_buffer.close()

    def get_sightings(self):
        return []
