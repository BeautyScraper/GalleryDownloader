import galleryCrawler as gC

class SantaEvent(gC.rssImageExtractor):
    website = "allporncomic.com"

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
                yield gC.scrapy.Request(url=url.rstrip(), callback=self.parseFnc1)
                

    def parseFnc1(self,response):
        # if 'avita' in response.url:
            # import pdb; pdb.set_trace()
        t = response.css('.listing-chapters_wrap .wp-manga-chapter > a::attr(href)').extract()
        t = [response.url] if t == [] else t 
        for url in t:
            print(url)
            yield gC.scrapy.Request(url=url.rstrip(), callback=self.parseFnc,priority = 2,dont_filter = True)

    def parseFnc(self,response):
        print(self.website)
        if 'avita' in response.url and False:
            import pdb; pdb.set_trace()

        
        imageSrc = response.css('.wp-manga-chapter-img::attr(src)').extract()
        imageSrc = [x.strip() for x in imageSrc]
        len(imageSrc)
        fileNames = [x.split("/")[-1].split('?')[0] for x in imageSrc]
        folderName = self.properName(response.css("title::text").extract()[0].split('.')[-1])
        self.downloadGalleryGeneric(response, imageSrc,fileNames, folderName,True,"comics1\\%s" % folderName)



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
