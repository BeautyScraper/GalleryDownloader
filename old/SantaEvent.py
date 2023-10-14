import galleryCrawler as gC

class SantaEvent(gC.rssImageExtractor):
    website = "santabanta.com"

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
            if self.website in url and "gallery" in url:
                yield gC.scrapy.Request(url=url.rstrip(), callback=self.galDownloader)
    
    def galDownloader(self,response):
        print(self.website + " penetration started")
        # imgtwistLinks = response.css("a[href*=postimage\.org]::attr(href)").extract()
        url = response.url
        imgtwistLinks = response.css("a[href*=\/gallery\/]::attr(href)").extract()
        for link in imgtwistLinks:
            print("pat fond in link")
            link = gC.urllib.request.urljoin(response.url, link)
            yield gC.scrapy.Request(url=link, callback=self.parseFnc)

    def parseFnc(self,response):
        imgUrls = response.css("img.imagedropshadow").css("::attr(src)").extract()
        imgUrls = [x.replace("_th.jpg", ".jpg") for x in imgUrls]
        fileNames = response.css("img.imagedropshadow").css("::attr(title)").extract()
        prefix = response.css("title::text").extract()[0]
        fileNames = [prefix +" me chudi "+ x+".jpg" for x in fileNames]
        self.downloadGalleryGeneric(response, imgUrls, fileNames,folderName= "Expande")
        nextPages = [x for x in response.css("a[href*=\/gallery\/]::attr(href)").extract() if "page=" in x]
        for link in nextPages:
            link = gC.urllib.request.urljoin(response.url, link)
            gC.scrapy.Request(url=link, callback=self.parseFnc)



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
