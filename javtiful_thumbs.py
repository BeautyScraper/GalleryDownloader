import galleryCrawler as gC
from thumbs import thumb_writer
import re
import json
import html
import subprocess
from aria2cgeneric import generic_downloader,noteItDown
import logging
from pathlib import Path


class SantaEvent(gC.rssImageExtractor):
    website = "javtiful.com"
    thumbs_dir = r'c:\dumpinggrounds\thumbs'

    def start_requests(self):
        dir_path = Path(r'c:\dumpinggrounds\thumbs') / self.website /( 'thumbs_db.csv')
        self.thumbnail = thumb_writer(str(dir_path)) 
        try:
            filename = gC.sys.argv[1]
        except:
            # filename2 = "upperbound.opml"
            # filename = "galleryLinks.opml"
            filename = "StaticLinks.opml"
            # filename = "Test.opml"
        t = open(filename, "r+")
        urls = t.readlines()
        t.close()
        gC.random.shuffle(urls)
        for url in urls:
            if '##' in url:
                continue
            sqaureP = gC.re.search("@\[(.*)\]", url)
            if sqaureP != None:
                lb, ub = [int(x) for x in gC.re.split("[-,]",sqaureP[1])]
                NewUrls = [url.replace(sqaureP[0],str(ui)) for ui in range(lb,ub)]
                [urls.append(NewUrl) for NewUrl in NewUrls]
                continue
            if self.website in url:
                yield gC.scrapy.Request(url=url.rstrip(), callback=self.streamtape)
            # if 'streamtape.com' in url:
            #     yield gC.scrapy.Request(url=url.rstrip(), callback=self.streamtape)

    
    def streamtape(self,response):
        # breakpoint()
        all_img_links = response.xpath('//div[@class="col pb-3"]//a//img/@data-src').getall()[1:] 
        all_img_name = [x[:100] + '.jpg' for x in response.xpath('//div[@class="col pb-3"]//a//img/@alt').getall()]
        all_img_associated_url = response.xpath('//div[@class="col pb-3"]//a[@title]//@href').getall()[1:]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
            'Accept': 'image/avif,image/webp,*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://javtiful.com/',
            'Sec-Fetch-Dest': 'image',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'cross-site'
        }
        self.thumbnail.list_thumbnail_gen(all_img_links,all_img_associated_url,all_img_name,headers)
 
if __name__ == "__main__":
    print(SantaEvent.website)
    try:
        process = gC.CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
        process.crawl(SantaEvent)
        process.start()
    except Exception as e:
        with open("log.txt", "a+") as inF:
            inF.write(str(e) + "\n")
