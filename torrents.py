import galleryCrawler as gC
import re
import json
import html
import subprocess
from aria2cgeneric import generic_downloader,noteItDown
import logging
from qtorrent import add_magnet_links 


#https://desijugar.info/2022/06/23/glow-with-the-flow-simran-kaur/


class SantaEvent(gC.rssImageExtractor):
    website = "rargb"

    def start_requests(self):
        logging.basicConfig(filename=r'c:\\'+self.website+'.log',level=logging.DEBUG)
        try:
            filename = gC.sys.argv[1]
        except:
            # filename2 = "upperbound.opml"
            filename = "galleryLinks.opml"
            # filename = "StaticLinks.opml"n
            # filename = "Test.opml"
        t = open(filename, "r+")
        urls = t.readlines()
        t.close()
        gC.random.shuffle(urls)
        for url in urls:
            sqaureP = gC.re.search("@\[(.*)\]", url)
            if sqaureP != None:
                lb, ub = [int(x) for x in gC.re.split("[-,]",sqaureP[1])]
                NewUrls = [url.replace(sqaureP[0],str(ui)) for ui in range(lb,ub)]
                [urls.append(NewUrl) for NewUrl in NewUrls]
                continue
            if self.website in url and '1080p' in url:
                yield gC.scrapy.Request(url=url.rstrip(), callback=self.streamtape,  meta={"verify_ssl": False,'proxy': '//3.124.133.93:3128'})


    
    def streamtape(self,response):

        magnets_links = response.css('a[href*=magnet]::attr(href)').get()

        try:
            add_magnet_links(magnet_link=magnets_links,key_id=response.url,save_path=r'D:\paradise\stuff\new\hott')
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
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
        process.crawl(SantaEvent)
        process.start()
    except Exception as e:
        with open("log.txt", "a+") as inF:
            inF.write(str(e) + "\n")
