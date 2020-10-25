# from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CrawlingSpider(CrawlSpider):
  name = 'CrawlingSpider'
  items = []
  allowed_domains = []
  start_urls = []
  rules = (Rule (LinkExtractor(), callback="parse_obj", follow=True),
  )

  def parse_obj(self,response):
    data = {'url': response.url, 'body': response.body, 'status': response.status}
    # self.log('Checking ---> %s' % response.url)
    self.items.append(data)

# process = CrawlerProcess()
