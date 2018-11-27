from pprint import pprint

from bs4 import BeautifulSoup
from requests_xml import XMLSession


class NewsGrubber:
    def create_news_list(self, site_url):
        news_list = []
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                                 '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        session = XMLSession()
        result = session.get(site_url, headers=headers)
        if result.status_code != 200:
            return print({'error': "HTTP error status {}".format(result.status_code)})
        text = result.xml.xml
        soup = BeautifulSoup(text, 'xml')
        if site_url == 'http://www.kommersant.ru/RSS/news.xml':
            soup = BeautifulSoup(text, 'lxml')
        objects = soup.find_all('item')
        for item in objects:
            if item.find('guid'):
                news_item = {'link': item.find('guid').text}
            elif item.find('link'):
                news_item = {'link': item.find('link').text}
            news_item['title'] = item.find('title').text
            news_item['description'] = item.find('description').text
            if item.find('enclosure'):
                news_item['image'] = item.find('enclosure').attrs['url']
            news_list.append(news_item)
        return news_list


class Lenta(NewsGrubber):

    def __init__(self):
        self.lenta_news_list = self.create_news_list('https://lenta.ru/rss')

    def news(self, limit=None):
        if limit and limit <= 199:
            return pprint(self.lenta_news_list[0:limit])
        return pprint(self.lenta_news_list)

    def grub(self, url=None):
        for object in self.lenta_news_list:
            if object['link'] == url:
                object.pop('link')
                return pprint(object)
        else:
            print({"error": "Data of such url not found, please enter another"})


class M24News(NewsGrubber):

    def __init__(self):
        self.news_list = self.create_news_list('https://www.m24.ru/rss.xml')

    def news(self, limit=None):
        if limit and limit <= 29:
            return pprint(self.news_list[0:limit])
        return pprint(self.news_list)

    def grub(self, url=None):
        for object in self.news_list:
            if object['link'] == url:
                object.pop('link')
                return pprint(object)
        else:
            print({"error": "Data of such url not found, please enter another"})


class Kommersant(NewsGrubber):

    def __init__(self):
        self.news_list = self.create_news_list('http://www.kommersant.ru/RSS/news.xml')

    def news(self, limit=None):
        if limit and limit <= 270:
            return pprint(self.news_list[0:limit])
        return pprint(self.news_list)

    def grub(self, url=None):
        for object in self.news_list:
            if object['link'] == url:
                object.pop('link')
                return pprint(object)
        else:
            print({"error": "Data of such url not found, please enter another"})


class Interfax(NewsGrubber):

    def __init__(self):
        self.news_list = self.create_news_list('https://www.interfax.ru/rss.asp')

    def news(self, limit=None):
        if limit and limit <= 24:
            return pprint(self.news_list[0:limit])
        return pprint(self.news_list)

    def grub(self, url=None):
        for object in self.news_list:
            if object['link'] == url:
                object.pop('link')
                return pprint(object)
        else:
            print({"error": "Data of such url not found, please enter another"})


if __name__ == '__main__':
    lenta = Lenta()
    news = lenta.news(1)
    data = lenta.grub('https://lenta.ru/news/2018/11/27/safe/')

    m24 = M24News()
    news = m24.news(1)
    data = m24.grub('https://www.m24.ru/news/vlast/27112018/55783')

    kommersant = Kommersant()
    news = kommersant.news(1)
    data = kommersant.grub('https://www.kommersant.ru/doc/3812950')

    interfax = Interfax()
    news = interfax.news(1)
    data = interfax.grub('https://www.interfax.ru/business/639685')
