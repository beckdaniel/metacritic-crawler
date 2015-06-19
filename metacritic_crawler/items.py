# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GameItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    pub_date = scrapy.Field()
    developer = scrapy.Field()
    genre = scrapy.Field()
    players = scrapy.Field()
    rating = scrapy.Field()
    avg_critic_score = scrapy.Field()
    avg_user_score = scrapy.Field()
    critic_reviews = scrapy.Field()
    user_reviews = scrapy.Field()


class ReviewItem(scrapy.Item):
    source = scrapy.Field()
    text = scrapy.Field()
    score = scrapy.Field()
