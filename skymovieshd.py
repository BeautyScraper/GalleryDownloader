import galleryCrawler as gC
import re
import json
import html
import subprocess
from aria2cgeneric import generic_downloader
import logging


#https://desijugar.info/2022/06/23/glow-with-the-flow-simran-kaur/


class SantaEvent(gC.rssImageExtractor):
    website = "skymovieshd"
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
        for url in urls:
            sqaureP = gC.re.search("@\[(.*)\]", url)
            if sqaureP != None:
                lb, ub = [int(x) for x in gC.re.split("[-,]",sqaureP[1])]
                NewUrls = [url.replace(sqaureP[0],str(ui)) for ui in range(lb,ub)]
                [urls.append(NewUrl) for NewUrl in NewUrls]
                continue
            if self.website in url:
                # breakpoint()
                yield gC.scrapy.Request(url=url.rstrip(), callback=self.parseFnc)

    def parseFnc(self,response):
        print(self.website)
        streamtapelink = response.css('a[href*=streamtape]::attr(href)').get()
        # if 'nasha-chaahat' in  response.url:
        # if not '.' in streamtapelink:
            # breakpoint()
        filename = response.url.split('/')[-1]
        # breakpoint()
        metadata = {'filename':filename}
        logging.debug('this url does not contain streamtape link:\n'+ response.url)
        if not streamtapelink is None: 
            streamtapelink = streamtapelink.strip()
            yield gC.scrapy.Request(url=streamtapelink, callback=self.streamtape, meta=metadata)
        else:
            # breakpoint()
            yield gC.scrapy.Request(url=response.url, callback=self.streamtape, dont_filter = True, meta=metadata)

        # videoUrl = json_dict[highest_reso]
        # fileNames = [response.url.rstrip('/').split('/')[-1]+'.mp4']
        # print(videoUrl)
        # # fileNames = [re.split('[=]',x)[-1] for x in videoUrl] if fileNames == [] else fileNames
        # self.downloadGalleryGeneric(response, videoUrl, fileNames, fileNames[0],True,"gifs" )

    def streamtape(self,response):
        videolink = response.css('#ideoooolink::text').get()
        if videolink is None:
            with open('streamtapenot.txt', 'a+') as fp:
                    fp.write(response.url+'\n') 
                    # return 
            # breakpoint()
            return 
        videolink = videolink.split('token=')[0] 
        token_string =  response.css('script').re('\&token=([^\'\"]*)\'\)\.substring')[-1] 
        videolink =  html.unescape('https:/'+videolink) + 'token=' +token_string + '&stream=1'
        filename = response.url.split('/')[-1]
        if not response.meta['filename'] is None:
            filename =  response.meta['filename'].replace('-',' ').replace('.html','.mp4')
        # breakpoint()
        generic_downloader(videolink,filename,filename,4,r'D:\paradise\stuff\new\hott') 

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
