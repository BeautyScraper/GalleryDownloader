import scrapy
import urllib.request
import re
from scrapy.crawler import CrawlerProcess
import galleryCrawler
import os
import pickle
import sys


class rssImageExtractor(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            if (len(sys.argv) > 1):
                t = open(sys.argv[1], "r+")
            else:
                t = open(dir_path + "\\babesource.opml", "r+")
            urls = t.readlines()
            t.close()
            # print("hello")
            # print(self.getFileMeta("pamela-jay-tight-and-busty.jpg"))
            # http: // www.foxhq.com / showgals.php?page = 2
            # self.urlDownload("http://t.umblr.com/redirect?z=https%3A%2F%2Fs1.webmshare.com%2FxO4Gb.webm&t=ZTY2ZDA1MjVjZTViMzgzOWNkYmY3MWU4OWM3MWFhMzhjMDAzMzQ2NCxnYVJmc2tUSg%3D%3D&b=t%3Ar19b_e4ZaWchfT4jGaBDFA&p=https%3A%2F%2Fbruh-sfm.tumblr.com%2Fpost%2F163066829714%2Flara-croft-rise-of-the-tomb-raider-webmwebm&m=1","newTest.mp4")
            for url in urls:
                if "babesource.com" in url:
                    yield scrapy.Request(url=url[:-1], callback=self.downloadThumbnails)
                if "ddfnetwork.com" in url:
                    yield scrapy.Request(url=url[:-1], callback=self.downloadDDF2)
                if "scoreland2.com" in url:
                    yield scrapy.Request(url=url[:-1], callback=self.scoreland2)
                if "porngals4.com" in url:
                    yield scrapy.Request(url=url[:-1], callback=self.Porngals4)
                if "blissbucks.com" in url:
                    yield scrapy.Request(url=url[:-1], callback=self.alluringVixen)
                if "dirtynakedpics.com" in url:
                    yield scrapy.Request(url=url[:-1], callback=self.dirtyNakedpics)
                if "youtube.com" in url:
                    print(url)
                    googleApiUrl = self.youtube_fetch_username(url)
                    yield scrapy.Request(callback=self.youtubeThumbs1, priority=1, url=googleApiUrl)
                if "foxhq.com" in url:
                    yield scrapy.Request(url=url[:-1], callback=self.foxHQ)
                if "evilangel.com" in url:
                    yield scrapy.Request(url=url[:-1], callback=self.EvilAngel)
                if "aziani.com" in url:
                    yield scrapy.Request(url=url[:-1], callback=self.aziani)
                if "eurotica.org" in url:
                    yield scrapy.Request(url=url[:-1], callback=self.eurotica)
                if "babeshowpromo.co.uk" in url:
                    yield scrapy.Request(url=url[:-1], callback=self.babeShow)
                if "jenniferjade" in url:
                    yield scrapy.Request(url=url[:-1], callback=self.babeShow)
                if "lyndaleigh.com" in url:
                    yield scrapy.Request(url=url[:-1], callback=self.babeShow)
                if "bound-cash.com" in url:
                    yield scrapy.Request(url=url[:-1], callback=self.downloadThumbnailsBoundCash)
                if "scoreland.com" in url:
                    yield scrapy.Request(url=url[:-1], callback=self.downloadThumbnailsScoreland)
                if "spizoo.com" in url:
                    metaData = {
                        'Samplelink': "http://galleries.spizoo.com/pictures/@gallery@/pics.php?nats=MzQuMi4xMi4yOC4wLjE2MTUyLjAuMC4w",
                        'galCodeFromImgExtractorRe': "content/DL02/(.*?)/"}
                    yield scrapy.Request(url=url[:-1], callback=self.findingGalCodeFromImage, meta=metaData)
                if "devilsfilm.com" in url:
                    metaData = {
                        'Samplelink': "http://html.sxx.com/2/105/pics/@gallery@/nude/82_c1848_01.html?pr=8&su=1&ad=12950&pg=2",
                        'galCodeFromImgExtractorRe': "photo_set/(.*?)/previews/"}
                    yield scrapy.Request(url=url[:-1], callback=self.devilsFilm, meta=metaData)
        except Exception as e:
            with open("logThumbnail.txt", "a+") as inF:
                inF.write(str(e) + "\n")

    def alreadyNotDownloaded(self, fileName, Id):
        return galleryCrawler.rssImageExtractor().alreadyNotDownloaded("Gallery\\" + fileName, Id)

    def downloadCompleteRegister(self, fileName, Id):
        return galleryCrawler.rssImageExtractor().downloadCompleteRegister("Gallery\\" + fileName, Id)

    def properName(self, name):
        return galleryCrawler.rssImageExtractor().properName(name)

    def findingGalCodeFromImage(self, response):
        replacement = response.css("img::attr(src)").re(response.meta['galCodeFromImgExtractorRe'])
        link = response.meta['Samplelink']
        print(response.meta['galCodeFromImgExtractorRe'])
        self.modifyToGalleryLink(response, link, replacement)

    def devilsFilm(self, response):
        replacement = response.css("body").re("photo_set/(.*?)/previews/")
        link = response.meta['Samplelink']
        print(response.meta['galCodeFromImgExtractorRe'])
        self.modifyToGalleryLink(response, link, replacement)

    def foxHQ(self, response):
        websiteName = self.properName(response.url.split("/")[2]) + "IndexGallery"
        if True:
            galleryLinks = response.css("td[align*=cen] a[target*=blank]::attr(href)").extract()
            imgLinks = response.css("td[align*=cen] a[target*=blank]").css("img::attr(src)").extract()
            fileNames = []
            for imgL in galleryLinks:
                fileNames.append(imgL.split("/")[-2] + ".jpg")
            self.downloadTHumbsGeneric(response, galleryLinks, imgLinks, fileNames)
            self.downloadCompleteRegister(websiteName, response.url)

    def youtube_fetch_username(self, url):
        print("youtube")
        userName = re.search("user/(.*?)[/]?$", url)[1]
        googleApiUrl = "https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forUsername=%s&key=%s" % (
            userName, "AIzaSyCkuJYk8_AMFBtD6zZtPF9nXRi7uJRgZyo")
        return googleApiUrl

        # response.css("body").re("\"id\" *: *\"(.*?)\"")

    def youtubeThumbs1(self, response):
        id = response.css("body").re("\"uploads\" *: *\"(.*?)\"")[0]
        print(id)
        googleApiUrl = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=%s&maxResults=50&key=%s" % (
            id, "AIzaSyCkuJYk8_AMFBtD6zZtPF9nXRi7uJRgZyo")
        print("CheckYoutube" + googleApiUrl)
        yield scrapy.Request(callback=self.startYoutubeThumbnails, priority=2, url=googleApiUrl)

    def startYoutubeThumbnails(self, response):
        nextPageToken = "@@"
        if response.css("body").re("\"nextPageToken\" *: *\"(.*?)\""):
            nextPageToken = response.css("body").re("\"nextPageToken\" *: *\"(.*?)\"")[0]
        channelId = re.search("\&playlistId=(.*?)\&", response.url)[1] + "Youtube"
        if self.alreadyNotDownloaded(channelId, nextPageToken) or nextPageToken == "":
            thumbLinks = response.css("body").re("\"([^\"]*?hqdefault\.jpg)\"")
            galleryLinks = []
            fileNames = []
            fileName = [self.properName((x).replace("\\", "")) for x in
                        response.css("body").re("\"title\" *: *\"(.*?)\"")]
            i = 0
            for t in thumbLinks:
                fileNames.append(fileName[i] + " " + t.split("/")[4] + ".jpg")
                i += 1
                galleryLinks.append("https://www.youtube.com/watch?v=%s" % (t.split("/")[4]))
            self.downloadTHumbsGeneric(response, galleryLinks, thumbLinks, fileNames)
            self.downloadCompleteRegister(channelId, nextPageToken)
        urlPart = "&pageToken=" + nextPageToken
        if "&pageToken=" not in response.url:
            googleApiUrl = response.url + urlPart
        else:
            googleApiUrl = re.sub("\&pageToken=.*$", urlPart, response.url)
            print("Keep it uptube" + googleApiUrl)

        yield scrapy.Request(callback=self.startYoutubeThumbnails, priority=2, url=googleApiUrl)

    def downloadTHumbsGeneric(self, response, galleryLinks, imgLinks, fileNames):
        websiteName = self.properName(response.url.split("/")[2]) + "Gallery"
        for i in range(len(galleryLinks)):
            links = galleryLinks[i]
            imgLink = imgLinks[i]
            fileName = fileNames[i]
            if self.alreadyNotDownloaded(websiteName, links):
                # urllib.request.urlretrieve(imgUrl, "NewBabes\\%s" % imgFileName)
                formedUrl = links
                if not re.search("http", formedUrl):
                    temp = "/".join(response.url.split("/")[:-1])
                    temp = temp.strip("/") + "/"
                    formedUrl = temp + formedUrl
                print(formedUrl)
                os.system("md NewBabes\\%s" % websiteName)
                urllib.request.urlretrieve(imgLink, "NewBabes\\%s\\%s" % (websiteName, fileName))
                self.setFileMeta(fileName, formedUrl, websiteName)
                # self.downloadThisGallery(formedUrl)
                self.downloadCompleteRegister(websiteName, links)
            print(links)

    def modifyToGalleryLink(self, response, link, replacement):
        galleryLinks = []
        for replacer in replacement:
            galleryLinks.append(link.replace("@gallery@", replacer))
            print(galleryLinks[-1])
            self.writeNewLinks(response, galleryLinks)

    def writeNewLinks(self, response, galleryLinks):
        # t = open("galleryLinks.opml", "a")
        websiteName = self.properName(response.url.split("/")[2]) + "Gallery"
        for links in galleryLinks:
            if self.alreadyNotDownloaded(websiteName, links):
                # urllib.request.urlretrieve(imgUrl, "NewBabes\\%s" % imgFileName)
                formedUrl = links
                if not re.search("http", formedUrl):
                    temp = "/".join(response.url.split("/")[:-1])
                    temp = temp.strip("/") + "/"
                    formedUrl = temp + formedUrl
                print(formedUrl)
                self.downloadThisGallery(formedUrl)
                self.downloadCompleteRegister(websiteName, links)
            print(links)

    def findNewMasalaGallery(self, response):
        print(response.url)
        # galleryCodes = response.css("a")
        fileName = "indianMasala.txt"
        galleryCodes = response.css("a").re("hqgallery=(.*?)\">")
        print(galleryCodes)
        for galleryCode in galleryCodes:
            if self.alreadyNotDownloaded(fileName, galleryCode):
                yield scrapy.Request(url="http://www.indianmasala.com/index.php?hqgallery=" + galleryCode,
                                     callback=self.downloadFromGalleryPage)
        print(galleryCode)

    def downloadFromGalleryPage(self, response):
        print("bheeghiSaree")
        reativeURL = True
        imgUrls = response.css("img").re("src=\"([^\"]*)\"")
        for url in [x for x in imgUrls if "thumbnails" in x]:
            # url = url.replace("%20"," ")
            url = url.replace("/thumbnails", "")
            match = re.search("/([^/]*?)$", url)
            imgFileName = re.sub('[^A-Za-z0-9\.]+', '_', "".join(url.split("/")[-2:]))
            # urllib.request.urlretrieve(imgUrl)
            # print(relativeFormedUrl+url)
            if reativeURL:
                relativeFormedUrl = response.url.split("/")[0] + "//" + response.url.split("/")[2] + "/" + url

                # if url[:2]=="..":
                # relativeFormedUrl="".join(urls + "/" for urls in response.url.split("/")[:-2])
                print(relativeFormedUrl)
                urllib.request.urlretrieve(relativeFormedUrl, "downloaded\\%s" % imgFileName)
            else:
                print(url)
                urllib.request.urlretrieve(url, "downloaded\\%s" % imgFileName)
            # response.url.split("/")[2]
            self.downloadCompleteRegister("indianMasala.txt", re.search('hqgallery=(.*)', response.url)[1])

    def downloadThumbnails(self, response):
        imgUrls = response.css("img").re("src=\"([^\"]*.jpg)\"")
        print("Downloading Pictures from URL:%s" % response.url)
        # galleryLinks = response.css("a[href*=galleries]::attr(href)").extract()
        galleryLinks = response.css("a").re("href=\"https?://babesource.com/galleries/([^\"]*).html\"")
        i = 0
        for imgUrl in imgUrls:
            imgFileName = galleryLinks[i] + ".jpg"
            i += 1
            print(imgUrl)
            if self.alreadyNotDownloaded("babesourceGallery", galleryLinks[i - 1]):
                if self.ExoticEnough("heartQueens.txt", galleryLinks[i - 1]):
                    print("Apsara Aali")
                    absLink = "https://babesource.com/galleries/%s.html" % (galleryLinks[i - 1])
                    self.downloadThisGallery(absLink)
                else:
                    urllib.request.urlretrieve(imgUrl, "NewBabes\\%s" % imgFileName)
                self.downloadCompleteRegister("babesourceGallery", galleryLinks[i - 1])

    def downloadThisGallery(self, link):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + "\\galleryLinks.opml", "a") as file:
            file.write(link + "\n")

    def eurotica(self, response):
        print("writing euroticaGallery named:%s" % response.url)
        galleryLinks = response.css(".item a[href*=galleries]::attr(href)").extract()
        i = 0
        # t = open("galleryLinks.opml", "a")
        for links in galleryLinks:
            if self.alreadyNotDownloaded("euroticaGallery", links):
                # urllib.request.urlretrieve(imgUrl, "NewBabes\\%s" % imgFileName)
                # t.write(links + "\n")
                self.downloadThisGallery(links)
                self.downloadCompleteRegister("euroticaGallery", links)
                print("http://www.scoreland.com" + links)
        # t.close()

    def scoreland2(self, response):
        print("writing euroticaGallery named:%s" % response.url)
        websiteName = self.properName(response.url.split("/")[2])
        galleryLinks = response.css("a[href*=big-boob-scenes]::attr(href)").extract()
        i = 0
        # t = open("galleryLinks.opml", "a")
        for links in galleryLinks:
            if self.alreadyNotDownloaded(websiteName + "gallery", links):
                # urllib.request.urlretrieve(imgUrl, "NewBabes\\%s" % imgFileName)
                self.downloadThisGallery("http://www.scoreland2.com" + links)
                self.downloadCompleteRegister(websiteName + "gallery", links)
                print("http://www.scoreland2.com" + links)
        #

    def babeShow(self, response):
        print("writing babeshow named:%s" % response.url)
        galleryLinks = response.css("a[href*=\/gallery].uk-button::attr(href)").extract()
        code = response.url.split("/")[-1].split(".")[0]
        i = 0
        # t = open("galleryLinks.opml", "a")
        for links in galleryLinks:
            if self.alreadyNotDownloaded("BabeShowGallery", "@" + links.split("/")[-1].split(".")[0] + "@"):
                # urllib.request.urlretrieve(imgUrl, "NewBabes\\%s" % imgFileName)
                self.downloadThisGallery(links)
                self.downloadCompleteRegister("BabeShowGallery", "@" + links.split("/")[-1].split(".")[0] + "@")
            # print("http://www.scoreland.com" + links)

    def downloadThumbnailsScoreland(self, response):
        print("writing ScoredGallery named:%s" % response.url)
        galleryLinks = response.css("a").re("href=\"(.*?/\d\d\d\d\d/.*)?\"")
        i = 0
        # t = open("galleryLinks.opml", "a")
        for links in galleryLinks:
            if self.alreadyNotDownloaded("scorelandGallery", links):
                # urllib.request.urlretrieve(imgUrl, "NewBabes\\%s" % imgFileName)
                self.downloadThisGallery("http://www.scoreland.com" + links)
                self.downloadCompleteRegister("scorelandGallery", links)
                print("http://www.scoreland.com" + links)

    def downloadThumbnailsBoundCash(self, response):
        print("writing ScoredGallery named:%s" % response.url)
        galleryLinks = response.css("rss").re("\'(.*?)\'")
        i = 0
        # t = open("galleryLinks.opml", "a")
        for links in galleryLinks:
            if self.alreadyNotDownloaded("BoundCashGallery", links):
                # urllib.request.urlretrieve(imgUrl, "NewBabes\\%s" % imgFileName)
                self.downloadThisGallery(links)
                self.downloadCompleteRegister("BoundCashGallery", links)
        print(links)

    def downloadDDF(self, response):
        print("writing ScoredGallery named:%s" % response.url)
        galleryLinks = response.css(".cover-wrap").re("href=\"(.*?)\"")
        i = 0

        for links in galleryLinks:
            if self.alreadyNotDownloaded("DDFGallery", links):
                # urllib.request.urlretrieve(imgUrl, "NewBabes\\%s" % imgFileName)
                self.downloadThisGallery("https://ddfnetwork.com" + links)
                self.downloadCompleteRegister("DDFGallery", links)
                print(links)

    def downloadDDF2(self, response):
        # print("Aziani named:%s" % response.url)
        modelLink = [urllib.request.urljoin(response.url, x) for x in response.css(".card h5 a::attr(href)").extract()]
        modelPhoto = [x for x in response.css(".card a img::attr(src)").extract() if x != "#"]
        modelFilename = [self.properName(x.split("/")[-2].split("?")[0]) for x in modelLink]
        modelName = response.css(".card h6 a:first-of-type::attr(href)").extract()
        filename = []
        for fm in range(len(modelFilename)):
            filename.append(self.properName(modelFilename[fm] + "_" + modelName[fm].split("/")[2] + ".jpg"))
        self.downloadTHumbsGeneric(response, modelLink, modelPhoto, filename)

    def aziani(self, response):
        # print("Aziani named:%s" % response.url)
        galleryLinks = response.css("a").re("href=\"(.*?updates.*?)\"")
        i = 0
        # t = open("galleryLinks.opml", "a")
        for links in galleryLinks:
            print("Aziani url under consideration: " + links)
            if self.alreadyNotDownloaded("AzianiGallery", links):
                # urllib.request.urlretrieve(imgUrl, "NewBabes\\%s" % imgFileName)

                self.downloadThisGallery(links)
                self.downloadCompleteRegister("AzianiGallery", links)
                print(links)

    def aziani2(self, response):
        # print("Aziani named:%s" % response.url)
        modelLink = response.css('.no-before::attr(href)').extract()
        modelPhoto = response.css('.no-before img::attr(src)').extract()

        # t = open("galleryLinks.opml", "a")
        for i in range(0, len(modelLink)):
            modelName = modelLink[i].split("/")[-1].split(".")[0]
            links = modelName
            print("Aziani url under consideration: " + modelPhoto[i])
            if self.alreadyNotDownloaded("AzianiGallery1", links):
                urllib.request.urlretrieve("http://www.aziani.com" + modelPhoto[i], "models\\%s.jpg" % modelName)

                # t.write("http://www.aziani.com" + links + "\n")
                self.downloadCompleteRegister("AzianiGallery1", links)
                print(links)

    def EvilAngel(self, response):
        print("writing EvilAngel named:%s" % response.url)
        items = response.css(".tlcItem ")
        i = 0
        # t = open("galleryLinks.opml", "a")
        for item in items:
            links = "https://www.evilangel.com" + item.css("a").re("href=\"(.*?)\"")[0]
            all = "".join(item.css("a").re("href=\"(.*?)\""))
            if self.ExoticEnough("heartQueens.txt", all) and self.alreadyNotDownloaded("EvilAngelGallery", links):
                # urllib.request.urlretrieve(imgUrl, "NewBabes\\%s" % imgFileName)
                self.downloadThisGallery(links)
                self.downloadCompleteRegister("EvilAngelGallery", links)
                print(links)

    def dirtyNakedpics(self, response):
        print("writing dirtyNakedpics named:%s" % response.url)
        items = response.css("a").re("href=\"(.*?galleries.*?)\"")
        i = 0
        # t = open("galleryLinks.opml", "a")
        for item in items:
            links = "http://www.dirtynakedpics.com/" + item
            all = links
            if self.ExoticEnough("dirtyEnough.txt", all) and self.alreadyNotDownloaded("dirtynakedpicsGallery", links):
                # urllib.request.urlretrieve(imgUrl, "NewBabes\\%s" % imgFileName)
                self.downloadThisGallery(links)
                self.downloadCompleteRegister("dirtynakedpicsGallery", links)
                print(links)

    def Porngals4(self, response):
        print("writing dirtyNakedpics named:%s" % response.url)
        items = response.css(".img").css("a").re("href=\"(.*?)\"")
        i = 0
        # t = open("galleryLinks.opml", "a")
        for item in items:
            links = "https://www.porngals4.com" + item
            all = links
            if self.ExoticEnough("porngal4me.txt", all) and self.alreadyNotDownloaded("Porngals4Gallery", links):
                # urllib.request.urlretrieve(imgUrl, "NewBabes\\%s" % imgFileName)
                self.downloadThisGallery(links)
                self.downloadCompleteRegister("Porngals4Gallery", links)
                print(links)

    def alluringVixen(self, response):
        print("writing dirtyNakedpics named:%s" % response.url)
        items = response.css("rss").re("href=\"(.*?)\"")
        i = 0
        # t = open("galleryLinks.opml", "a")
        for item in items:
            links = item
            all = links
            if self.alreadyNotDownloaded("alluringVixenGallery", links):
                # urllib.request.urlretrieve(imgUrl, "NewBabes\\%s" % imgFileName)
                self.downloadThisGallery(links)
                self.downloadCompleteRegister("alluringVixenGallery", links)
                print(links)

    def ExoticEnough(self, filename, hay):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + "\\" + filename, "r") as f:
            content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
            content = [x.strip() for x in content]
            for apsara in content:
                # print("Exotic " + apsara)
                if re.search(apsara, hay, re.IGNORECASE) and apsara != "" and len(apsara) > 3:
                    print("%s was found in %s" % (apsara, hay))
                    return True
                # print(hay + "was not exotic enough")
            return False

    def setFileMeta(self, fileName, Meta, websiteName):
        fileMeta = {}
        try:
            with open("NewBabes\\%s\\FileUrl.pkl" % websiteName, "rb+") as inFile:
                fileMeta = pickle.load(inFile)
        except Exception as e:
            with open("NewBabes\\%s\\FileUrl.pkl" % websiteName, "wb") as inFile:
                pass
            print(e.__str__())
        fileMeta[fileName] = Meta
        pickle.dump(fileMeta, open("NewBabes\\%s\\FileUrl.pkl" % websiteName, "wb"))

    def getFileMeta(self, fileName):
        with open("NewBabes\\www.foxhq.comGallery\\FileUrl.pkl", "rb") as inFile:
            fileMeta = pickle.load(inFile)
        return fileMeta[fileName]


if __name__ == "__main__":
    try:
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
        process.crawl(rssImageExtractor)
        process.start()
    except Exception as e:
        with open("logThumbnail.txt", "a+") as inF:
            inF.write(str(e) + "\n")
