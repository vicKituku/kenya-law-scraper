import scrapy
from time import sleep

class KenyalawSpider(scrapy.Spider):
    name = "kenyalaw"
    allowed_domains = ["kenyalaw.org"]
    start_urls = ["https://kenyalaw.org/caselaw/cases/advanced_search/page/40000/"]

    def parse(self, response):

        case_links = response.css('a.show-more')

        for case_link in case_links:
            url = case_link.attrib['href']
            yield scrapy.Request(response.urljoin(url), callback=self.parse_product)
        
        # Follow pagination links
        next_page = response.css('li.next > a::attr(href)').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_product(self, response):
        # Extract link to PDF file
        pdf_link = response.css('a.Pdf::attr(href)').get()

        # Download PDF file
        if pdf_link:
            yield {
                'pdf_url': response.urljoin(pdf_link),
                'date': response.xpath('//*[@id="case_meta"]/table/tbody/tr[4]').get()
            }
