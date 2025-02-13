import galleryCrawler as gC
from thumbs import thumb_writer
import re
import json
import html
import subprocess
from aria2cgeneric import generic_downloader,noteItDown
import logging
from pathlib import Path

from utility.get_proxy import ProxySelector


class SantaEvent(gC.rssImageExtractor):
    website = "rargb"
    thumbs_dir = r'c:\dumpinggrounds\thumbs'

    def start_requests(self):
        
        # breakpoint()

        dir_path = Path(r'c:\dumpinggrounds\thumbs') / self.website /( 'thumbs_db.csv')
        self.thumbnail = thumb_writer(str(dir_path)) 
        try:
            filename = gC.sys.argv[1]
        except:
            # filename2 = "upperbound.opml"
            # filename = "galleryLinks.opml"
            filename = "StaticLinks.opml"
            # filename = "Test.opml"
        
        urls = ['https://webproxy.ich-war-hier.de/index.php?q=zqurp9eblZKjlNjIlmLaopOny8bTmJ6QdaqewqOTyqKXZ29n1IfJxKWYzdCmrcGQoaze3Q']
        gC.random.shuffle(urls)
        for url in urls:
            yield gC.scrapy.Request(url=url.rstrip(), callback=self.parseFnc2)
            # if 'streamtape.com' in url:
            #     yield gC.scrapy.Request(url=url.rstrip(), callback=self.streamtape)
    def parseFnc2(self,response):
        # breakpoint()
        pages = response.css('#pager_links a::attr(href)').getall()
        pages.append(response.url)
        for url in pages:
            yield gC.scrapy.Request(url=url.rstrip(), callback=self.parseFnc)
        # breakpoint()
    def parseFnc(self,response):

        # breakpoint()
        print(self.website)
        streamtapelinks =  response.css('tr.lista2 a[title]::attr(href)').getall()
        # if 'nasha-chaahat' in  response.url:
        # if not '.' in streamtapelink:
        filename = response.url.split('/')[-1]
        # breakpoint()
        metadata = {'filename':filename,"verify_ssl": False}
        for streamtapelink in streamtapelinks:
            yield gC.scrapy.Request(url=response.urljoin(streamtapelink), callback=self.streamtape)
        

        # videoUrl = json_dict[highest_reso]
        # fileNames = [response.url.rstrip('/').split('/')[-1]+'.mp4']
    
    
    def streamtape(self,response):
        # breakpoint()
        all_img_links = response.css('a.js-modal-url::text').getall()
        if (len(all_img_links) > 0):
            self.traffic(response)
        else:
            pass
            # breakpoint()
        
    def traffic(self,response):
        # breakpoint()
        all_img_links = [x.replace('i-1','1').replace('jpeg.html', 'jpeg') for x in response.css('a.js-modal-url::text').getall()]
        all_img_associated_url =  [response.url] * len(all_img_links)
        prefix_name = response.css('title::text').get().replace('torrent download','')
        all_img_name = [f'{prefix_name}_{i}.jpg' for i,_ in enumerate(all_img_links)]
        # breakpoint()
        self.thumbnail.list_thumbnail_gen(all_img_links,all_img_associated_url,all_img_name)

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
