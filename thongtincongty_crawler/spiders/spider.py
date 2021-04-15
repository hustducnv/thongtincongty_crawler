from scrapy import Spider, Request
from my_configs import Config
from pandas import read_csv


class CompanySpider(Spider):
    name = 'company_spider'
    allowed_domains = ['https://www.thongtincongty.com/']

    def start_requests(self):
        if Config.TYPE == 'LINK':
            base_url = 'https://www.thongtincongty.com/?page='
            for i in range(Config.START_PAGE, Config.END_PAGE):
                url = base_url + str(i)
                yield Request(url=url, callback=self.parse_company_links)
        elif Config.TYPE == 'INFO':
            df = read_csv(Config.PATH_TO_LINKS_CSV, header=0)
            links = df[df.columns[0]][Config.START_IDX, Config.END_IDX].tolist()

            # links = ['https://www.thongtincongty.com/company/3fab67f2-cong-ty-tnhh-fancy-group/',
            #          'https://www.thongtincongty.com/company/c24bca28-cong-ty-co-phan-thuong-mai-va-dich-vu-omy/']

            for link in links:
                yield Request(url=link, callback=self.parse_company)
        else:
            raise Exception('TYPE ERROR! Please see Config.TYPE from my_configs.py')

    def parse_company_links(self, response, **kwargs):
        company_links = response.xpath('/html/body/div[1]/div[1]/div[3]/div/a/@href').extract()
        for link in company_links:
            yield {'link': link}

    def parse_company(self, response, **kwargs):
        item = dict()

        item['url'] = response.url

        tmp = response.xpath('/html/body/div[1]/div[1]/div[3]/h4/a/span/text()').extract()
        if len(tmp) > 0:
            item['vi_name'] = tmp[0]

        raw_lines = response.xpath('/html/body/div[1]/div[1]/div[3]/text()').extract()
        info_lines = []
        for line in raw_lines:
            line = line.strip()
            if line != '':
                info_lines.append(line)
        item['info_lines'] = info_lines

        tmp = response.xpath('/html/body/div[1]/div[1]/div[3]/a/img/@src').extract()
        if len(tmp) > 0:
            item['tax_id_img'] = tmp[0]

        tmp = response.xpath('/html/body/div[1]/div[1]/div[3]/img/@src').extract()
        if len(tmp) > 0:
            item['phone_img'] = tmp[0]

        yield item

