import galleryCrawler as gC
from thumbs import thumb_writer
import re
import json
import html
import subprocess
from aria2cgeneric import generic_downloader,noteItDown
import logging
from pathlib import Path


def extract_resolution(filename):
    # Extract resolution from the filename using a regular expression
    pattern = r'-(\d+p)-'
    match = re.search(pattern, filename)
    if match:
        return int(match.group(1)[:-1])
    return None

def higher_resolution_version_exists(filename, filename_list):
    # movie_name = filename.split('-(')[0]  # Extract the movie name before the first '-('
    n_resolution = extract_resolution(filename)
    # breakpoint()
    
    regn = filename.replace(str(n_resolution), 'HD##XX').split('-[')[0] 
    for file in filename_list:
        h_resolution = extract_resolution(file)
        regh = file.replace(str(h_resolution), 'HD##XX').split('-[')[0]
        if regh == regn:
            if h_resolution > n_resolution:
                # breakpoint()
                return True
    return False


class SantaEvent(gC.rssImageExtractor):
    website = "skymovieshd"
    thumbs_dir = r'c:\dumpinggrounds\thumbs'

    def start_requests(self):
        dir_path = Path(r'c:\dumpinggrounds\thumbs') / self.website /( 'thumbs_db.csv')
        self.thumbnail = thumb_writer(str(dir_path)) 
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
            if '##' in url:
                continue
            sqaureP = gC.re.search("@\[(.*)\]", url)
            if sqaureP != None:
                lb, ub = [int(x) for x in gC.re.split("[-,]",sqaureP[1])]
                NewUrls = [url.replace(sqaureP[0],str(ui)) for ui in range(lb,ub)]
                [urls.append(NewUrl) for NewUrl in NewUrls]
                continue
            if self.website in url:
                yield gC.scrapy.Request(url=url.rstrip(), callback=self.streamtape)
            # if 'streamtape.com' in url:
            #     yield gC.scrapy.Request(url=url.rstrip(), callback=self.streamtape)

    
    def streamtape(self,response):
        links = response.css('.L *>a::attr(href)')
        all_filenames = [x.split('/')[-1] for x in links.getall()]
        for link in links:
            if higher_resolution_version_exists(link.get().split('/')[-1],all_filenames):
                continue
            yield response.follow(link, self.parse_page) 
        # breakpoint()
        # sec = response.css('div.main-content__card')
        # galleryLinks =  sec.css('a::attr(href)').getall()
        # imgLinks = sec.css('img::attr(data-src)').getall()
        # stars_name = sec.css('h5::text').getall()
        # stars_name = [x.replace(' ', '-') for x in stars_name]
        # fileNames = [(x+'-'+y.split('/')[-1]).replace(',','') for (x,y) in zip(stars_name,imgLinks)]
        # # import pdb;pdb.set_trace()
  
        # self.thumbnail.list_thumbnail_gen(imgLinks,galleryLinks,fileNames)
    def parse_page(self,response):
        imgLinks = response.css('.L *>img::attr(src)').getall()
        galleryLinks = [response.url] * len(imgLinks)
        # breakpoint()
        
        fileNames = [Path(response.url.split('/')[-1]).stem + str(i) + '_.jpg' for i,_ in enumerate(imgLinks)] 
        self.thumbnail.list_thumbnail_gen(imgLinks,galleryLinks,fileNames)
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
