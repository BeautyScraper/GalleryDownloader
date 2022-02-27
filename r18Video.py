import galleryCrawler as gC

class SantaEvent(gC.rssImageExtractor):
    website = "r18.com"

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
        imgUrls = response.css(".js-view-sample::attr(data-video-high)").extract()
        fileNames = response.css("cite::text").extract()
        prefix = response.css("title::text").extract()[0].replace(" - Japanese Adult Movies - R18.com","")
        fileNames = [prefix +" "+ x+".mp4" for x in fileNames]
        self.downloadGalleryGeneric(response, imgUrls, fileNames,folderName= "GIFS")
        



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
