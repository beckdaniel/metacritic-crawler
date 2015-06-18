
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from metacritic_crawler.items import GameItem, ReviewItem
import sys


class GameSpider(scrapy.Spider):
    name = "game_spider"
    allowed_domains = ["www.metacritic.com"]
    start_urls = ["http://www.metacritic.com/browse/games/release-date/available/pc/metascore"]

    def parse(self, response):
        """
        Parse the reviews list.
        """
        for sel in response.xpath('//div[@class="product_wrap"]'):
            title = sel.xpath('div[@class="basic_stat product_title"]/a/text()').extract()[0].strip()
            item_page = sel.xpath('div[@class="basic_stat product_title"]/a/@href').extract()[0].strip()
            item_page = 'http://www.metacritic.com' + item_page
            critic_score = sel.xpath('div/div[contains(@class, "metascore_w")]/text()').extract()[0].strip()
            user_score = sel.xpath('div/ul/li/span[contains(@class, "textscore")]/text()').extract()[0].strip()
            item = GameItem()
            item['title'] = title
            item['avg_critic_score'] = critic_score
            item['avg_user_score'] = user_score
            #print title, critic_score, user_score
            #print item_page
            #yield item
            yield scrapy.Request(item_page, callback=self.parse_item_page, meta={'item': item})
            break
        #sys.exit(0)

        # This handles the next page in the review list
        try:
            #raise IndexError
            next_page = response.xpath('//a[@rel="next"]/@href').extract()[0]
            next_page = "http://www.metacritic.com" + next_page
            yield scrapy.Request(next_page, callback=self.parse)
        except IndexError:
            pass #finished the crawling

    def parse_item_page(self, response):
        """
        This parse the item page. For now we do not get anything here,
        we just create the URLs for the reviews page.
        """
        critics_page = response.url + '/critic-reviews'
        #print critics_page
        #print response.meta['item']
        yield scrapy.Request(critics_page, callback=self.parse_critics_page, meta=response.meta)
        #print response.meta['item']
        users_page = response.url + '/user-reviews'
        yield scrapy.Request(users_page, callback=self.parse_users_page, meta=response.meta)
        #print response.meta['item']
        yield response.meta['item']

    def parse_critics_page(self, response):
        """
        Parse the critic reviews page.
        """
        item = response.meta['item']
        item['critic_reviews'] = []
        for sel in response.xpath('//li[contains(@class, " critic_review")]'):
            review = ReviewItem()
            source = sel.xpath('.//div[@class="source"]/a/text()')[0].extract()
            score = sel.xpath('.//div[contains(@class, "metascore_w")]/text()')[0].extract()
            text = sel.xpath('.//div[contains(@class, "review_body")]/text()')[0].extract().strip()
            review['source'] = source
            review['score'] = score
            review['text'] = text
            item['critic_reviews'].append(review)
            #print review
        #print 'CRITIC'
        #print item
        return item

    def parse_users_page(self, response):
        """
        Parse the user reviews page. Notice that this can span multiple pages.
        """
        item = response.meta['item']
        item['user_reviews'] = []
        for sel in response.xpath('//li[contains(@class, " user_review")]'):
            review = ReviewItem()
            try:
                source = sel.xpath('.//div[@class="name"]/a/text()').extract()[0]
            except IndexError: #user without a link
                source = sel.xpath('.//div[@class="name"]/span/text()').extract()[0]
            score = sel.xpath('.//div[contains(@class, "metascore_w")]/text()')[0].extract()
            text =  ' '.join(sel.xpath('.//span[contains(@class, "blurb_expanded")]/text()').extract())
            review['source'] = source
            review['score'] = score
            review['text'] = text
            item['user_reviews'].append(review)
        return item
