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
    website = "spankbang"
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
        all_img_links = []
        all_img_name = []
        all_img_associated_url = []
        articles = response.css('.video-item[id*=v_id_]')
        print(len(articles))
        for artrticle in articles: 
            # breakpoint()
            all_img_links.append(artrticle.css('img::attr(data-src)').get())
            str_list =  artrticle.css('a::attr(href)').get().split('/')
            all_img_name.append(str_list[1]+' '+ str_list[-1])
            all_img_associated_url.append(response.urljoin(artrticle.css('a::attr(href)').get()))
        # breakpoint()
        self.thumbnail.list_thumbnail_gen(all_img_links,all_img_associated_url,all_img_name)
        pass
 
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
