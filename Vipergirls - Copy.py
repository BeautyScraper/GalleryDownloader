import galleryCrawler as gC

class SantaEvent(gC.rssImageExtractor):
    website = "vipergirls.to"

    def start_requests(self):
        try:
            filename = gC.sys.argv[1]
        except:
            # filename2 = "upperbound.opml"
            # filename = "galleryLinks.opml"
            # filename = "StaticLinks.opml"
            filename = "Test.opml"
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

    def check(self,response,totalImgs):
        url = response.url
        if str(totalImgs) not in url:
            with open("checkFail.txt",'a+') as fp:
                # import pdb;pdb.set_trace()
                fp.write("%s :: %s\n" % (url,totalImgs))                
    
    def parseFnc(self,response):
        print(self.website)
        imageSrc = response.css("img[src*=imx]::attr(src)").extract()
        imageSrc = [x.replace("/t/","/i/") for x in imageSrc]
        len(imageSrc)
        # import pdb; pdb.set_trace()
        fileNames = [x.split("/")[-1] for x in imageSrc]
        folderName = self.properName(response.css("title::text").extract()[0])
        if fileNames != []:
            self.check(response,len(imageSrc))
            self.downloadGalleryGeneric(response, imageSrc,fileNames, folderName,True,"imageSet\\%s" % folderName)
        # elif len(response.css("a[href*=imagebam]::attr(href)").extract()) > 0:
            # urls = response.css("a[href*=imagebam]::attr(href)").extract()
            # metaData = {'folderName': response.css("title::text").extract()[0] }
            # for url in urls:
                # import pdb; pdb.set_trace()
                # yield gC.scrapy.Request(url=url.rstrip(), callback=self.imagebamSingleImageLink,meta=metaData, priority=1)
            # else:
                # if len(urls) > 0:
                    # self.removeLine(response.url + "\n", r"D:\Developed\Automation\GalleryDownloader\galleryLinks.opml")
        else:
            urls = response.css("a[href*=turboimage]::attr(href)").extract()
            metaData = {'folderName': response.css("title::text").extract()[0] }
            for url in urls:
                # import pdb; pdb.set_trace()
                yield gC.scrapy.Request(url=url.rstrip(), callback=self.turboimagehostSingleImageLink,meta=metaData, priority=1)
            else:
                if len(urls) > 0:
                    self.removeLine(response.url + "\n", r"D:\Developed\Automation\GalleryDownloader\galleryLinks.opml")
        self.pixhost(response)
        self.imgbox(response)

    def pixhost(self,response):
        # import pdb; pdb.set_trace()
        imageSrc = response.css("img[src*=pixhost]::attr(src)").extract()
        if imageSrc == []:
            return
        imageSrc = [x.replace("https://t","https://img").replace("/thumbs/","/images/") for x in imageSrc]
        fileNames = [x.split("/")[-1] for x in imageSrc]
        folderName = self.properName(response.css("title::text").extract()[0])
        self.check(response,len(imageSrc))
        self.downloadGalleryGeneric(response, imageSrc,fileNames, folderName,True,"imageSet\\%s" % folderName)

    def imgbox(self,response):
        # import pdb; pdb.set_trace()
        imageSrc = response.css("img[src*=imgbox]::attr(src)").extract()
        if imageSrc == []:
            return
        imageSrc = [x.replace("thumbs2.","images2.").replace("_t.jpg","_o.jpg") for x in imageSrc]
        fileNames = [x.split("/")[-1] for x in imageSrc]
        folderName = self.properName(response.css("title::text").extract()[0])
        self.check(response,len(imageSrc))
        self.downloadGalleryGeneric(response, imageSrc,fileNames, folderName,True,"imageSet\\%s" % folderName)

    def turboimagehostSingleImageLink(self,response):
        # import pdb; pdb.set_trace()
        imageSrc = response.css("#imageid::attr(src)").extract()
        fileNames = [x.split("/")[-1] for x in imageSrc]
        folderName = response.meta['folderName']
        self.check(response,len(imageSrc))
        self.downloadGalleryGeneric(response, imageSrc,fileNames, "",True,"imageSet\\%s" % folderName) 
        
     


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
