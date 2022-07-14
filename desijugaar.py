import galleryCrawler as gC
import re
import json
import html
import subprocess
from aria2cgeneric import generic_downloader
import logging
from pathlib import Path

#https://desijugar.info/2022/06/23/glow-with-the-flow-simran-kaur/
#https://desijugar.info/
#https://desijugar.info/page/2/

class SantaEvent(gC.rssImageExtractor):
    website = "desijugar.info"

    def start_requests(self):
        logging.basicConfig(filename=r'c:\\'+self.website+'.log',level=logging.DEBUG)
        try:
            filename = gC.sys.argv[1]
        except:
            # filename2 = "upperbound.opml"
            filename = "galleryLinks.opml"
            # filename = "StaticLinks.opml"
            # filename = "Test.opml"
        t = open(filename, "r+")
        urls = t.readlines()
        t.close()
        gC.random.shuffle(urls)
        static_urls = [
            'https://desijugar.info/',
            'https://desijugar.info/page/2/',
            'https://desijugar.info/page/3/',
            'https://desijugar.info/page/4/',
            'https://desijugar.info/page/5/',
            'https://desijugar.info/page/6/',
        ]
        for url in urls:
            sqaureP = gC.re.search("@\[(.*)\]", url)
            if sqaureP != None:
                lb, ub = [int(x) for x in gC.re.split("[-,]",sqaureP[1])]
                NewUrls = [url.replace(sqaureP[0],str(ui)) for ui in range(lb,ub)]
                [urls.append(NewUrl) for NewUrl in NewUrls]
                continue
            if self.website in url:
                yield gC.scrapy.Request(url=url.rstrip(), callback=self.parseFnc)
        for url in static_urls:
            yield gC.scrapy.Request(url=url.rstrip(), callback=self.parse_start_url)
    def parse_start_url(self, response):
        urls = response.css('a[href*=desijuga][title]::attr(href)').getall()
        for url in urls:
            yield gC.scrapy.Request(url=url.rstrip(), callback=self.parseFnc)


    def parseFnc(self,response):
        print(self.website)
        # breakpoint()
        strelinks = response.css('a[href*=streamtape]::attr(href)').getall()
        # if '%' in streamtapelink:
        # if 'filename' in 
        # logging.debug('this url does not contain streamtape link:\n'+ response.url)
        if strelinks == []:
            # breakpoint()
            with open('streamtapenot.txt', 'a+') as fp:
                fp.write(response.url+'\n') 
            return 
        for streamtapelink in strelinks: 
            streamtapelink = streamtapelink.strip()
            meta= {'filename':response.url.strip('/').split('/')[-1]+'.mp4'}
            yield gC.scrapy.Request(url=streamtapelink, callback=self.streamtape,meta=meta)

        # videoUrl = json_dict[highest_reso]
        # fileNames = [response.url.rstrip('/').split('/')[-1]+'.mp4']
        # print(videoUrl)
        # # fileNames = [re.split('[=]',x)[-1] for x in videoUrl] if fileNames == [] else fileNames
        # self.downloadGalleryGeneric(response, videoUrl, fileNames, fileNames[0],True,"gifs" )

    def streamtape(self,response):
        videolink = response.css('#ideoooolink::text').get()
        if videolink is None:
            # (Path.cwd() / 'streamtape.html').write_text(response.text)
            # breakpoint()
            with open('streamtapenot.txt', 'a+') as fp:
                fp.write(response.url+'\n') 
            return 
        # if not 'token=' in videolink:
        #     breakpoint()
        videolink = videolink.split('token=')[0] 
        token_string =  response.css('script').re('\&token=([^\'\"]*)\'\)\.substring')[-1] 
        videolink =  html.unescape('https:/'+videolink) + 'token=' +token_string + '&stream=1'
        filename = response.url.split('/')[-1]
        if 'filename' in response.meta:
            filename = response.meta['filename']
        # breakpoint()
        savepath = r'D:\paradise\stuff\new\pvd2'
        generic_downloader(videolink,filename,filename,4,savepath) 

    def singleToManyImg(self,response,iurl,l=0,u=20):
        # import pdb; pdb.set_trace()
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
