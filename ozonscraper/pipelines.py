# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
import logging


class OzonscraperPipeline:
    def process_item(self, item, spider):
        return item


class ExcelWriterPipeline:
    def __init__(self):
        self.data = []

    def process_item(self, item, spider):
        self.data.append(item)
        return item
    
    def close_spider(self, spider):
        df = pd.DataFrame(self.data)
        excel_filename = 'scraped_data.xlsx'
        df.to_excel(excel_filename, index=False)
        logging.info(f"Data saved to {excel_filename}")