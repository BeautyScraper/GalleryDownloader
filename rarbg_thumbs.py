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
    website = "rargb"
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
        proxy = "https://147.93.116.2:3128"
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
                yield gC.scrapy.Request(url=url.rstrip(), callback=self.parseFnc, meta={"verify_ssl": False, "proxy": proxy})
            # if 'streamtape.com' in url:
            #     yield gC.scrapy.Request(url=url.rstrip(), callback=self.streamtape)
    def parseFnc(self,response):

        # breakpoint()
        print(self.website)
        streamtapelinks =  response.css('a[href*=torrent]::attr(href)').getall()
        # if 'nasha-chaahat' in  response.url:
        # if not '.' in streamtapelink:
        filename = response.url.split('/')[-1]
        # breakpoint()
        metadata = {'filename':filename,"verify_ssl": False}
        for streamtapelink in streamtapelinks:
            streamtapelink = streamtapelink.strip()
            yield gC.scrapy.Request(url=response.urljoin(streamtapelink), callback=self.streamtape,meta=metadata)
        

        # videoUrl = json_dict[highest_reso]
        # fileNames = [response.url.rstrip('/').split('/')[-1]+'.mp4']
    
    
    def streamtape(self,response):
        # breakpoint()
        all_img_links = response.css('a[href*=imgtraffic]::attr(href)').getall()
        if (len(all_img_links) > 0):
            self.traffic(response)
        
    def traffic(self,response):
        # breakpoint()
        all_img_links = [x.replace('i-1','1').replace('jpeg.html', 'jpeg') for x in response.css('a[href*=imgtraffic]::attr(href)').getall()]
        all_img_associated_url =  [response.url] * len(all_img_links)
        all_img_name = [x.split('/')[-1].replace('jpeg.html', 'jpg') for x in response.css('a[href*=imgtraffic]::attr(href)').getall()]
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
