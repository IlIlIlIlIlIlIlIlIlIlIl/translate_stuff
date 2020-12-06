import requests
import urllib3
import re
import threading
import string
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation
from urllib.parse import urlparse, urljoin
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ParserClass(threading.Thread):
    def __init__(self, url, _db_ref):
        super().__init__()
        self.data = {}
        self._id = url
        self.url = url
        self._db_ref = _db_ref
    
    def update(self, _status, _message):
        _dict = {"status": _status, "message": _message}
        self._db_ref.document(self._id).set(_dict)
    
    def run(self):
        self.update(0, "Parsing Url")
        self.url = self.parse_url(self.url)
        self.update(1, "Loading index html")
        self.html = self.get_html_page()
        self.update(3, "Parsing all Url links")
        self.get_links_from_page(self.html)
        self.update(3, "Loading all pages")
        self.get_all_pages()
        self.update(99, "Analysing Pages...")
        self.parse_all_pages()
        self.update(100, "Done!")
        # self.text = self.get_text_from_html()
        # self.proc_text = self.post_process()
        # self.stats = self.get_stats()
            
    
    def parse_url(self, _url):
        url_dict = {}
        parsed = urlparse(_url)
        # My lord, this is ugly.. there must be an easier way
        if parsed.netloc == "":
            if parsed.path and parsed.path.startswith('www.'):
                url_dict['netloc'] = urlparse(parsed.path.replace('www.',''))
                url_dict['www_netloc'] = urlparse(parsed.path)
            else:
                url_dict['netloc'] = urlparse(parsed.path)
                url_dict['www_netloc'] = urlparse("www." + parsed.path)
            url_dict['https'] = urlparse('https://' + url_dict['netloc'].path)
            url_dict['https_www'] = urlparse('https://' + url_dict['www_netloc'].path)
        else:
            if parsed.netloc and parsed.netloc.startswith('www.'):
                url_dict['netloc'] = urlparse(parsed.netloc.replace('www.',''))
                url_dict['www_netloc'] = urlparse(parsed.netloc)
            else:
                url_dict['netloc'] = urlparse(parsed.netloc)
                url_dict['www_netloc'] = urlparse("www." + parsed.netloc)
            url_dict['https'] = urlparse('https://' + url_dict['netloc'].path)
            url_dict['https_www'] = urlparse('https://' + url_dict['www_netloc'].path)
        return url_dict
    
    def get_links_from_page(self, _html):
        soup = BeautifulSoup(_html, features="html.parser")
        for link in soup.findAll('a'):
            link = link.get('href')
            if link is None or link == '':
                continue
            if link in self.data:
                continue
            if link.startswith('/'):
                link = self.url['https'].geturl() + link
            link = link.replace('www.','')
            link = urlparse(link)
            if link.scheme != 'https':
                continue
            if link.path == '/':
                link = urlparse(link.scheme +'://' + link.netloc)
            if link.params != '' or link.query != '' or link.fragment != '':
                new_link = link.scheme + '://' + link.netloc
                if link.path != '':
                    new_link = urljoin(new_link, link.path)
                link = urlparse(new_link)
            if link.path and link.path.endswith('/'):
                link = urlparse(link.geturl()[:-1])
            if link.path.lower().split('.')[-1] in ['exe', 'zip', 'png', 'jpg', 'pdf']:
                continue
            if link.geturl() not in self.data:
                if link.netloc == self.url['https'].netloc:
                    self.status_message = 'Found new link: ' + link.geturl()
                    self.data[link.geturl()] = None
    
    def get_all_pages(self):
        get_links_from = []
        length_for_status = len(self.data)
        i = 1
        for link in self.data:
            if self.data[link] is None:
                status = int((i / length_for_status) *60)
                status_message = 'Parsing: ' + link
                self.update(status, status_message)
                i += 1

                page = requests.get(link, verify=False)
                if page.status_code != 200:
                    continue
                page = page.content
                self.data[link] = page
                get_links_from.append(page)
        for page in get_links_from:
            self.get_links_from_page(page)
        length_for_status = len(self.data)
        for link in self.data:
            if self.data[link] is None:
                status = min(100, int((i / length_for_status)*40)+60)
                status_message = 'Parsing: ' + link
                self.update(status, status_message)
                i += 1
                page = requests.get(link, verify=False)
                if page.status_code != 200:
                    continue
                page = page.content
                self.data[link] = page

    def get_html_page(self):
        raw_page = requests.get(self.url['https'].geturl(), verify=False)
        return raw_page.content
    
    def parse_all_pages(self):
        for data in self.data:
            value = self.data[data]
            if value is not None:
                value = self.get_text_from_html(value)
                self.data[data] = value

    def get_text_from_html(self, _html):
        soup = BeautifulSoup(_html, features="html.parser")
        text = soup.get_text()
        regexes = ['\\s[\\W*|\\d*|,*]*\\s', '\t', '\xa0', '\r+', '\n+', ' +']
        for reg in regexes:
            text = re.sub(reg, ' ', text)
        processed_text = self.post_process(text)
        return processed_text

    def post_process(self, _text):
        processed_text = _text.lower()
        processed_text = processed_text.split(' ')
        chars_to_remove = ['', '-', '–', '•', '|', '&'] 
        for idx, word in enumerate(processed_text):
            if len(word) > 20:
                processed_text[idx] = ''
        for char in chars_to_remove:
            while char in processed_text:
                processed_text.remove(char)
        for i, s in enumerate(processed_text):
            processed_text[i] = s.translate(str.maketrans('', '', string.punctuation))
        return ' '.join(processed_text)

    def get_stats(self):
        result = {}
        result['Number of words found:'] = len(self.proc_text)
        result['Number of unique words found:'] = len(set(self.proc_text))
        result['Unique words:'] = ', '.join(list(set(self.proc_text)))
        # text_p = (''.join(s.findAll(text=True))for s in self.soup.findAll('header'))
        # c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))
        # text_p = (''.join(s.findAll(text=True))for s in self.soup.findAll('footer'))
        # c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))
        # text_p = (''.join(s.findAll(text=True))for s in self.soup.findAll('p'))
        # c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))

        # # We get the words within divs
        # text_div = (''.join(s.findAll(text=True))for s in self.soup.findAll('div'))
        # c_div = Counter((x.rstrip(punctuation).lower() for y in text_div for x in y.split()))
        return result