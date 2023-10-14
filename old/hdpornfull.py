import galleryCrawler as gC
import re
import json
import html
import subprocess
from aria2cgeneric import generic_downloader,noteItDown
import logging


#https://desijugar.info/2022/06/23/glow-with-the-flow-simran-kaur/


class SantaEvent(gC.rssImageExtractor):
    website = "hdpornfull.com"

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
                yield gC.scrapy.Request(url=url.rstrip(), callback=self.parseFnc)
            if 'streamtape.com' in url:
                yield gC.scrapy.Request(url=url.rstrip(), callback=self.streamtape)

    def parseFnc(self,response):
        print(self.website)
        # breakpoint()
        strelinks = response.css('a[href*=streamtape]::attr(href)').getall()
        # if '%' in streamtapelink:
        # if 'filename' in 
        if strelinks == []:
            # breakpoint().
            fppath = r'C:\Personal\Developed\sbddownloader\test.opml'
            # breakpoint()
            sdfe_url = response.css('a[href*=sdefx\.cloud]::attr(href)').get()
            if sdfe_url is None:
                sdfe_url = response.css('a[href*=strdef\.world]::attr(href)').get()
            if sdfe_url is None:
                # breakpoint()
                return
            noteItDown(fppath,sdfe_url,response.url,response.url.split('/')[2]+'txt')
            # with open('streamtapenot.txt', 'a+') as fp:
            #     fp.write(sdfe_url+'\n') 
            # return 
        for streamtapelink in strelinks: 
            streamtapelink = streamtapelink.strip()
            meta= {'filename':response.url.strip('/').split('/')[-1]+'.mp4'}
            yield gC.scrapy.Request(url=streamtapelink, callback=self.streamtape,meta=meta)
        # logging.debug('this url  does not contain streamtape link:\n'+ response.url)

        # videoUrl = json_dict[highest_reso]
        # fileNames = [response.url.rstrip('/').split('/')[-1]+'.mp4']
        # print(videoUrl)
        # # fileNames = [re.split('[=]',x)[-1] for x in videoUrl] if fileNames == [] else fileNames
        # self.downloadGalleryGeneric(response, videoUrl, fileNames, fileNames[0],True,"gifs" )

    def streamtape(self,response):
        videolink = response.css('#ideoooolink::text').get()
        if videolink is None:
            # breakpoint()
            with open('streamtapenot.txt', 'a+') as fp:
                fp.write(response.url+'\n') 
            return 
        videolink = videolink.split('token=')[0] 
        token_string =  response.css('script').re('\&token=([^\'\"]*)\'\)\.substring')[-1] 
        videolink =  html.unescape('https:/'+videolink) + 'token=' +token_string + '&stream=1'
        filename = response.url.split('/')[-1]
        # breakpoint()
        pgtitle = response.css('meta[name=\"og:title\"]::attr(content)').get()
        if 'mp4' in pgtitle:
            filename = pgtitle
        if 'filename' in response.meta:
            filename = response.meta['filename']
        # breakpoint()
        savepath = r'D:\paradise\stuff\new\hardcore'
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
