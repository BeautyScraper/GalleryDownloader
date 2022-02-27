import galleryCrawler as gC

class DesiBaba(gC.rssImageExtractor):
    website = "sexbaba.co"

    def start_requests(self):
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
            sqaureP = gC.re.search("@\[(.*)\]", url)
            if sqaureP != None:
                lb, ub = [int(x) for x in gC.re.split("[-,]",sqaureP[1])]
                NewUrls = [url.replace(sqaureP[0],str(ui)) for ui in range(lb,ub)]
                [urls.append(NewUrl) for NewUrl in NewUrls]
                continue
            if self.website in url:
                yield gC.scrapy.Request(url=url.rstrip(), callback=self.galDownloader)
    
    def galDownloader(self,response):
        print(self.website + " penetration started")
        # imgtwistLinks = response.css("a[href*=postimage\.org]::attr(href)").extract()
        url = response.url
        galCode = url.split("/")[-1].split(".")[0].replace("?page="," ").replace("Thread-", "")
        fDict = {"pixxxels":self.pixxxels,"imgfy":self.imgfy,"postimage\.org":self.pixxxels}
        print("28")
        for pat,parseFnc in fDict.items():
            imgtwistLinks = response.css("a[href*=%s]::attr(href)" % pat).extract()
            for link in imgtwistLinks:
                print("pat fond in link")
                yield gC.scrapy.Request(url=link, callback=parseFnc , meta = {"galCode":galCode})

    def pixxxels(self,response):
        fileNameExtension = response.meta["galCode"]
        imgUrls = response.css("#download::attr(href)").extract()
        fileNames = [fileNameExtension+" " + x.split("/")[-1].replace("?dl=1","").replace("out-php-i","") for x in imgUrls]
        self.downloadGalleryGeneric(response, imgUrls, fileNames,folderName= "Fakes")

    def imgfy(self,response):
        fileNameExtension = response.meta["galCode"]
        imgUrls = response.css(".btn-download::attr(href)").extract()
        fileNames = [fileNameExtension+" " + x.split("/")[-1].replace("?dl=1","").replace("out-php-i","") for x in imgUrls]
        self.downloadGalleryGeneric(response, imgUrls, fileNames,folderName= "Fakes")
    



if __name__ == "__main__":
    print(DesiBaba.website)
    try:
        process = gC.CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
        process.crawl(DesiBaba)
        process.start()
    except Exception as e:
        with open("log.txt", "a+") as inF:
            inF.write(str(e) + "\n")
