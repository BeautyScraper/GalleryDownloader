import galleryCrawler as gC
import re
import json

class SantaEvent(gC.rssImageExtractor):
    website = "moviespornsex.com"

    def start_requests(self):
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

    def parseFnc(self,response):
        print(self.website)
        url = response.url.strip("/#")
        reso_list = ['1080p', '720p', '480p', '320p', '240p']
        # import pdb;pdb.set_trace()
        videoUrl = response.css('source::attr(src)').extract()
        fileNames = [response.url.rstrip('/').split('/')[-1]+'.mp4']
        print(videoUrl)
        # fileNames = [re.split('[=]',x)[-1] for x in videoUrl] if fileNames == [] else fileNames
        self.downloadGalleryGeneric(response, videoUrl, fileNames, fileNames[0],True,"gifs" )
        
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
