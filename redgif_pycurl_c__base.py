from pathlib import Path
import galleryCrawler as gC
from aria2cgeneric import gdurls 
from headertodic import read_header_file
import pycurl_requests as requests
from scrapy.http import HtmlResponse
import json


class SantaEvent(gC.rssImageExtractor):
    website = "redgifs.com"

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
                print(url)
                resp = requests.get(url.rstrip("\n"),headers=request_dict)
                response = HtmlResponse(url=url.rstrip("\n"), body=resp.text, encoding='utf-8') 
                self.parseFnc(response) 
                # yield gC.scrapy.Request(url=url.rstrip(), callback=self.parseFnc, headers=request_dict)


    def parseFnc(self,response):
        # breakpoint()
        data = json.loads(response.text) 
        data = data['gifs']
        dir = r'D:\paradise\stuff\new\to_be_clipped'
        data_srcs = [url['urls']['hd'] for url in data]
        gdurls(data_srcs, dir,connections=4)
        # breakpoint()
        # breakpoint()
        
            

    def parseFnc1(self,response):
        data_srcs = response.css('.page-break img::attr(data-src)').getall()
        data_srcs = [x.strip() for x in data_srcs]
        comicsdirectory = r'D:\paradise\stuff\new\comics'
        # breakpoint()
        mix_dir = str(Path(comicsdirectory) / response.url.strip('/').split('/')[-2] / response.css('title::text').get())
        gdurls(data_srcs, mix_dir,connections=1)



if __name__ == "__main__":
    print(SantaEvent.website)
    request_dict =  read_header_file(SantaEvent.website + '.txt')
    # breakpoint()
    try:
        # process = gC.CrawlerProcess({
        #     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        # })
        process = gC.CrawlerProcess(request_dict)
        process.crawl(SantaEvent)
        process.start()
    except Exception as e:
        with open("log.txt", "a+") as inF:
            inF.write(str(e) + "\n")
