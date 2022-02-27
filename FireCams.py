import galleryCrawler as gC
import json
class SantaEvent(gC.rssImageExtractor):
    website = "firecams.com"

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
                cook = "PHPSESSWCDC=763e9b2bd437a00741b19921f2f8f698; _uuid=5eb9322a6bf5f1.66796351;"
                c = self.getScrapyCookie(cook)
                yield gC.scrapy.Request(url=url.rstrip(), callback=self.parseFnc,cookies=c)

    def parseFnc(self,response):
        print(self.website)
        y = json.loads(response.body)
        ph = y["data"]["photoList"]["photos"]
        imgUrls = [x["photo"] for x in ph]
        # imgUrls = [x.replace("thumbs/","") for x in imgUrls]
        fileNames = [x.split("/")[-1] for x in imgUrls]
        # prefix = url.split("/")[-1]
        
        # fileNames = [prefix +" "+ str(i)+".jpg" for i in response.css("img[src*=thumb]::attr(data-photo-id)").extract()]
        self.downloadGalleryGeneric(response, imgUrls, fileNames, galCode="@")



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
