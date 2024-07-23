import re

import scrapy


class TopSchoolSpider(scrapy.Spider):
    name = "top_school"
    allowed_domains = ["raex-rr.com"]
    start_urls = ["https://raex-rr.com/education/best_schools/top-100_russian_schools/2023/"]

    def parse(self, response):
        rows = response.xpath('//table[contains(@class, "rrp_table")]//tbody/tr')
        for row in rows:
            number = row.xpath(".//th[1]/text()").get()
            university_name = row.xpath('.//th[2]//a/text()').get()
            city = row.xpath('.//td[2]/text()').get()
            rank = row.xpath('.//td[3]/text()').get()
            budget_places_share = row.xpath('.//td[4]/text()').get()
            paid_places_share = row.xpath('.//td[5]/text()').get()
            olimpics_winner = row.xpath('.//td[6]/text()').get()
            link = row.xpath('.//a//@href').get()
            yield response.follow(url=link, callback=self.parse_country,
                                  meta={'number': number,
                                        'university_name': university_name,
                                        'city': city,
                                        'rank': rank,
                                        'budget_places_share': budget_places_share,
                                        'paid_places_share': paid_places_share,
                                        'olimpics_winner' : olimpics_winner
                                        })

    def parse_country(self, response):
        rows = response.xpath("//div[contains(@class, 'rr_entryContent flo_mb_7')]")
        for row in rows:
            mark = response.xpath('//div/div[2]/div[1]/div/ul[2]/li[1]/text()').get()
            average_mark = float(re.findall('\d+\.\d+', mark)[0])
            number = int(response.request.meta['number'].strip())
            university_name = response.request.meta['university_name']
            city = response.request.meta['city']
            rank = float(response.request.meta['rank'].strip())
            budget_places_share = response.request.meta['budget_places_share']
            paid_places_share = response.request.meta['paid_places_share']
            olimpics_winner = response.request.meta['olimpics_winner']
            yield {
                'average_mark': average_mark if average_mark else 0,
                'number': number if number else 0,
                'university_name': university_name.strip() if university_name else "",
                'city': city.strip() if city else "",
                'rank': rank if rank else 0,
                'budget_places_share': budget_places_share.strip() if budget_places_share else "",
                'paid_places_share': paid_places_share.strip() if rank else "",
                'olimpics_winner': olimpics_winner.strip() if olimpics_winner else ""
            }
