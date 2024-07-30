import csv
import os.path

import requests
import scrapy


class UnsplashPhotoSpider(scrapy.Spider):
    name = "unsplash_photo"
    # allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/"]

    def parse(self, response):
        for image in response.xpath('//*[@itemprop="contentUrl"]'):
            image_url = image.xpath('.//@href').get()
            yield scrapy.Request(response.urljoin(image_url), self.save_image)


    def save_image(self, response):
        filename_inter = response.url.split('/')[-1]
        filename = ' '.join([word for word in filename_inter.split('-')[:-1]]) + '.jpg'
        # //*[@class ='zb0Hu atI7H']/a
        # category_link = response.xpath('//*[@class ="ZhNv6"]//a/text()').get()
        category_link = response.xpath('//*[@class ="ZhNv6"]//a')
        categories = []
        for link in category_link:
            cat = link.xpath('.//text()').get()
            categories.append(cat)
        image = response.xpath('//*[@data-test="photos-route"]//div[@class ="Tbd2Y"]//img')[-1]
        image_ = image.xpath('@src').extract_first()
        data = {'filename':filename,
                'category':categories,
                'image_link': image_}

        with open('data.csv', 'a+', newline = '') as f:
            fieldnames = ['filename', 'category', 'image_link']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if os.path.getsize('data.csv') == 0:
                writer.writeheader()
            writer.writerow(data)

        response = requests.get(image_)
        with open(f'images/{filename}', 'wb') as f:
             f.write(response.content)

