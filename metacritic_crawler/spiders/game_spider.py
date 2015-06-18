
import scrapy
from metacritic_crawler.items import GameItem


class GameSpider(scrapy.Spider):
    name = "game_spider"
    allowed_domains = ["metacritic.com"]
    start_urls = ["http://www.metacritic.com/browse/games/release-date/available/pc/metascore"]

    def parse(self, response):
        for sel in response.xpath('//div[@class="product_wrap"]'):
            title = sel.xpath('div[@class="basic_stat product_title"]/a/text()').extract()[0].strip()
            expert_score = sel.xpath('div/div[contains(@class, "metascore_w")]/text()').extract()[0].strip()
            user_score = sel.xpath('div/ul/li/span[contains(@class, "textscore")]/text()').extract()[0].strip()
            item = GameItem()
            item['title'] = title
            item['expert_score'] = expert_score
            item['user_score'] = user_score
            print title, expert_score, user_score
            yield item
