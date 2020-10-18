import requests
import re
from bs4 import BeautifulSoup


class ParserClass:
    def __init__(self, url):
        self.url = url
        self.html = self.get_html_page()
        self.text = self.get_text_from_html()
        self.proc_text = self.post_process()
        self.stats = self.get_stats()

    def get_html_page(self):
        raw_page = requests.get('http://' + self.url)
        return raw_page.text

    def get_text_from_html(self):
        soup = BeautifulSoup(self.html, features="html.parser")
        text = soup.get_text()
        text = re.sub('\s[\\W*|\\d*|,*]*\s', ' ', text)
        text = re.sub('\t', ' ', text)
        text = re.sub('\xa0', ' ', text)
        text = re.sub('\r+', ' ', text)
        text = re.sub('\n+', ' ', text)
        text = re.sub(' +', ' ', text)
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
        result = []
        result.append('Number of words found: {}'.format(len(self.proc_text)))
        result.append('Number of unique words found: {}'.format(len(set(self.proc_text))))
        result.append(set(self.proc_text))
        return result