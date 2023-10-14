import galleryCrawler as gC

class SantaEvent(gC.rssImageExtractor):
    website = "camster.com"

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
        imgUrls = response.css("img[src*=thumb]::attr(src)").extract()
        imgUrls = [x.replace("thumbs/","") for x in imgUrls]
        fileNames = []
        prefix = url.split("/")[-1]
        fileNames = [prefix +" "+ str(i)+".jpg" for i in response.css("img[src*=thumb]::attr(data-photo-id)").extract()]
        self.downloadGalleryGeneric(response, imgUrls, fileNames, galCode="@")
        temp = response.css("a[href*=\?pg\=]::text").extract()
        text = temp[0] if len(temp) > 0 else ""

        print(imgUrls)
        if "Next" in text:
            print("traversingNext")
            url = response.css("a[href*=\?pg\=]::attr(href)").extract()[0]
            url = gC.urllib.request.urljoin(response.url, url)
            yield gC.scrapy.Request(url=url.rstrip(), callback=self.parseFnc)



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
