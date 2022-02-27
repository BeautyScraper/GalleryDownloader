import galleryCrawler as gC
from urllib.parse import urlparse,parse_qsl



class SantaEvent(gC.rssImageExtractor):
    website = "pics.vc"

    def qParse(self,url):
        return dict(parse_qsl(urlparse(url).query))

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

    def parseFnc(self,response):
        print(self.website)
        imageSrc = response.css("img.photo_el_img::attr(src)").extract()
        imageSrc = [x.replace("/s/","/o/") for x in imageSrc]
        # galCode =  response.url.split("?")[-1].split("=")[-1]
        g = self.qParse(response.url)['g']
        folderName = response.css("title::text").extract()[0].replace(" - PICS.VC","").replace("\n"," ") +g[:5]
        t = [x.split("=")[-1] for x in response.url.split("&") if "off" in x]
        off = 0 if t == [] else int(t[0])
        fileNames = [g[:20] + str(off + i)+".jpg" for i,_ in enumerate(imageSrc)]
        self.downloadGalleryGeneric(response, imageSrc,fileNames, "",True,"imageSet\\%s" % folderName)
        nextPage =  response.css("div#center_control>a::attr(href)").extract()[0] if response.css("div#center_control>a::attr(href)").extract()!=[] else "" 
        # import pdb;pdb.set_trace()
        if nextPage == "":
            return
        nextPage = gC.urllib.request.urljoin(response.url, nextPage)
        print(nextPage)
        yield gC.scrapy.Request(url=nextPage, callback=self.parseFnc)


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
