import galleryCrawler as gC
import re
import json
import html
import subprocess
from aria2cgeneric import generic_downloader,noteItDown
import logging
from qtorrent import add_magnet_links
from utility.get_proxy import ProxySelector 
from scrapy.core.downloader.handlers.http import HTTPDownloadHandler
import aiohttp

#https://desijugar.info/2022/06/23/glow-with-the-flow-simran-kaur/



class SantaEvent(gC.rssImageExtractor):
    website = "rargb"

    def start_requests(self):
        # selector = ProxySelector("utility/proxy.opml", 'https://rargb.to/' )
        # working_proxy = selector.get_working_proxy()
        # if working_proxy:
        #     print(f"Working proxy found: {working_proxy}")
        # else:
        #     breakpoint()
        #     print("No working proxy found.")
        logging.basicConfig(filename=r'c:\\'+self.website+'.log',level=logging.DEBUG)
        try:
            filename = gC.sys.argv[1]
        except:
            # filename2 = "upperbound.opml"
            filename = "rargb_proxy_links.opml"
            # filename = "StaticLinks.opml"n
            # filename = "Test.opml"
        t = open(filename, "r+")
        urls = t.readlines()
        t.close()
        gC.random.shuffle(urls)
        for url in urls:
            yield gC.scrapy.Request(url=url.rstrip(), callback=self.streamtape,meta={'dont_filter':True})


    
    def streamtape(self,response):

        # breakpoint()
        magnets_links = response.css('a[href*=magnet]::attr(href)').get()
        try:
            add_magnet_links(magnet_link=magnets_links,key_id=response.url,save_path=r'D:\paradise\stuff\new\torrents')
        except Exception as e:
            print(e)
            breakpoint()
            logging.debug(str(e))


    def singleToManyImg(self,response,iurl,l=0,u=20):
        print(iurl)
        imgUrls = [iurl.replace("@",str(i)) for i in range(l,u)]
        galcode = iurl.split("/")[-2]
        fileNames = [galcode+" %s .jpg" % str(i) for i in range(l,u)]
        self.downloadGalleryGeneric(response, imgUrls, fileNames, galCode=galcode)

if __name__ == "__main__":
    print(SantaEvent.website)
    try:
        process = gC.CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        })
        process.crawl(SantaEvent)
        process.start()
    except Exception as e:
        with open("log.txt", "a+") as inF:
            inF.write(str(e) + "\n")
