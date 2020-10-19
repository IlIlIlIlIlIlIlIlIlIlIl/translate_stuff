import requests
import re
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation


class ParserClass:
    def __init__(self, url):
        self.url = url
        self.html = self.get_html_page()
        self.soup = BeautifulSoup(self.html, features="html.parser")
        self.text = self.get_text_from_html()
        self.proc_text = self.post_process()
        self.stats = self.get_stats()

    def get_html_page(self):
        raw_page = requests.get('http://' + self.url)
        return raw_page.content

    def get_text_from_html(self):
        text = self.soup.get_text()
        regexes = ['\\s[\\W*|\\d*|,*]*\\s', '\t', '\xa0', '\r+', '\n+', ' +']
        for reg in regexes:
            text = re.sub(reg, ' ', text)
        return text

    def post_process(self):
        processed_text = self.text.lower()
        processed_text = processed_text.split(' ')
        chars_to_remove = ['', '-', '–', '•', '|', '&'] 
        for char in chars_to_remove:
            while char in processed_text:
                processed_text.remove(char)
        return processed_text

    def get_stats(self):
        result = {}
        result['Number of words found:'] = len(self.proc_text)
        result['Number of unique words found:'] = len(set(self.proc_text))
        result['Unique words:'] = ', '.join(list(set(self.proc_text)))
        text_p = (''.join(s.findAll(text=True))for s in self.soup.findAll('header'))
        c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))
        print(c_p)
        text_p = (''.join(s.findAll(text=True))for s in self.soup.findAll('footer'))
        c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))
        print(c_p)
        text_p = (''.join(s.findAll(text=True))for s in self.soup.findAll('p'))
        c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))
        print(c_p)

        # We get the words within divs
        text_div = (''.join(s.findAll(text=True))for s in self.soup.findAll('div'))
        c_div = Counter((x.rstrip(punctuation).lower() for y in text_div for x in y.split()))
        print(c_div)
        return result