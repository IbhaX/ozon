import copy
from typing import Iterable
import scrapy
from ozonscraper.input_files.utils import load_urls
from datetime import datetime, timezone


# Format the date in "11 ноября 2023" style
def format_date(date):
    months_russian = {
        1: "января", 2: "февраля", 3: "марта", 4: "апреля",
        5: "мая", 6: "июня", 7: "июля", 8: "августа",
        9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
    }

    # Get the month in Russian
    month_russian = months_russian[date.month]

    # Format the date in "11 ноября 2023"
    formatted_date_custom = f"{date.day} {month_russian} {date.year}"
    return formatted_date_custom


class OzonSpider(scrapy.Spider):
    name = "ozon"
    
    def default_response(self, response, status="Not Found"):
        self.logger.info(f"Item out of stock: {response.url}")
        item = copy.deepcopy(response.meta['item'])  # Create a deep copy of the item
        item['url_status'] = status
        item['data_published'] = ""
        item['data_author'] = ""
        item['data_score'] = ""
        item['data_published_parsed'] = ""
        item['data_content'] = ""
        yield item
    
    def start_requests(self):
        items  = load_urls()
        # items = [("https://www.ozon.ru/product/novyy-golosovoy-pult-distantsionnogo-upravleniya-dlya-philips-serii-7900-43pus7906-12-smart-tv-971777249/", {"product_link": "https://www.ozon.ru/product/novyy-golosovoy-pult-distantsionnogo-upravleniya-dlya-philips-serii-7900-43pus7906-12-smart-tv-971777249/"})]
        for url, item in items:
            yield scrapy.Request(url=url, callback=self.check_product_availability, meta={'item': copy.deepcopy(item)})
    
    def check_product_availability(self, response):
        out_of_stock = response.xpath('//div[@data-widget="webOutOfStock"]')
        page_error = response.xpath('//div[@data-widget="error"]')
        
        # Этот товар закончился - Out of stock
        if "Этот товар закончился" in response.text:
            self.logger.error("Out of stock")
            yield from self.default_response(response, status="No reviews")

        # Такой страницы не существует - Page does not exist
        elif "Такой страницы не существует" in response.text:
            self.logger.error("page does not exist")
            yield from self.default_response(response, status="Not found")
            
        elif out_of_stock and page_error:
            yield self.default_response(response, status="Not Found")
            
        else:
            url = f"{response.url}reviews" if response.url.endswith("/") else f"{response.url}/reviews"
            yield scrapy.Request(url=url, callback=self.parse, meta={'item': response.meta['item']})
            
    def parse(self, response):
        item = copy.deepcopy(response.meta['item'])  # Create a deep copy of the item for each request
        reviews_list = response.xpath('//div[@data-review-uuid]')
        
        if response.status == 404:
            self.logger.error(f"Status code 404: {response.url}")
            yield from self.default_response(response, status="Not found")
        
        if not reviews_list:
            yield self.default_response(response, status="No reviews")
    
        else:
            for review in reviews_list:
                comments_div = review.css("div.v4q_29.wq2_29")
                comments = "".join(comments_div.xpath(".//text()").getall()).strip() or ""
                
                data_author = review.css('span.qs6_29::text').get()
                
                if not comments or len(comments) < 2:
                    comments = ""
                
                published_at = int(review.css('::attr(publishedat)').get())
                item["data_published"] = format_date(datetime.fromtimestamp(published_at, timezone.utc))
                item["data_score"] = len(review.css("div.a5d14-a.a5d14-a0 svg[style='color:rgba(255, 168, 0, 1);']"))
                item["url_status"] = "Data Extracted"
                item["data_published_parsed"] = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
                item["data_content"] = comments.strip()
                item["data_author"] = data_author.strip() or "No Author"
                self.logger.info(f"Item scraped: {response.url}")
                yield item
            
            next_page = response.xpath('//div[@data-widget="webListReviews"]/*[last()]/*[last()]/a/@href').get()

            if next_page:
                next_url = response.urljoin(next_page)
                yield scrapy.Request(next_url, callback=self.parse, meta={'item': response.meta['item']})
