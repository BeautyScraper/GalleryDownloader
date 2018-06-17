import scrapy
import urllib.request
import re
import requests
import shutil
import time
import random
import sys
import os

from scrapy.crawler import CrawlerProcess


class rssImageExtractor(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        try:
            filename = sys.argv[1]
        except:
            # filename2 = "upperbound.opml"
            # filename = "galleryLinks.opml"
            # filename = "StaticLinks.opml"
            filename = "Test.opml"
        # filename = "foxHQ.opml"
        # filename = "puba.opml"
        t = open(filename, "r+")
        urls = t.readlines()
        t.close()
        random.shuffle(urls)
        # self.urlDownload("http://t.umblr.com/redirect?z=https%3A%2F%2Fs1.webmshare.com%2FxO4Gb.webm&t=ZTY2ZDA1MjVjZTViMzgzOWNkYmY3MWU4OWM3MWFhMzhjMDAzMzQ2NCxnYVJmc2tUSg%3D%3D&b=t%3Ar19b_e4ZaWchfT4jGaBDFA&p=https%3A%2F%2Fbruh-sfm.tumblr.com%2Fpost%2F163066829714%2Flara-croft-rise-of-the-tomb-raider-webmwebm&m=1","newTest.mp4")
        for url in urls:
            if "evilangel.com" in url:

                yield scrapy.Request(url=url[:-1].replace("picture", "photogallery") + "/2", callback=self.EvilAngel)
            elif "puba.com" in url:
                print("pubaOriginal " + url)
                yield scrapy.Request(url=url[:-1].replace("picture", "photogallery") + "/2", callback=self.puba)
            elif "pubacash.com" in url:
                yield scrapy.Request(url=url[:-1].replace("picture", "photogallery") + "/2", callback=self.puba)
            elif "ddfnetwork.com" in url:
                yield scrapy.Request(url=url[:-1], callback=self.ddf)
            elif "ddfnetwork.com" in url:
                yield scrapy.Request(url=url[:-1], callback=self.ddf)
            elif "indianmasala" in url:
                yield scrapy.Request(url=url[:-1], callback=self.indianMasala)
            elif "phdcash.com" in url:
                yield scrapy.Request(url=url[:-1], callback=self.photodromm)
            elif "dirtyhardcash.com" in url:
                yield scrapy.Request(url=url[:-1], callback=self.dirtyHardcash)
            elif "comicvine.gamespot.com" in url:
                yield scrapy.Request(url=url[:-1], callback=self.comicVine)
            elif "devilsfilm.com" in url:
                yield scrapy.Request(url=url[:-1], callback=self.DevilsFilm)
            elif "galleries.spizoo.com" in url:
                yield scrapy.Request(url=url[:-1], callback=self.thumbToLarge,
                                     meta={"search": "thumbs\/thumbnail-0?", "replace": "hires/SP", "index": -2,
                                           "galleryCodeFromURL": ""})
            elif "misslk.com" in url:
                code = re.search("dir=e0([0-9]+)", url)[1]
                yield scrapy.Request(url=url[:-1], callback=self.thumbToLarge,
                                     meta={"search": "\/tn\/", "replace": "/full/", "index": -2,
                                           "galleryCodeFromURL": code})
            elif "scoreland2.com" in url:
                code = " ".join(url.split("/")[-3:-1])
                yield scrapy.Request(url=url[:-1], callback=self.thumbToLarge,
                                     meta={"search": "_tn", "replace": "", "index": -2, "galleryCodeFromURL": code})
            elif "alluringvixens.com" in url:
                yield scrapy.Request(url=url[:-1], callback=self.alluringvixens)
            elif "foxhq.com" in url:
                spiderMeta = {'index': -2}
                # spiderMeta = {'index':-2}
                yield scrapy.Request(url=url[:-1], callback=self.imgLinks, meta=spiderMeta)
            elif "eurotica.org" in url:
                yield scrapy.Request(url=url[:-1], callback=self.eurotica)
            elif "8muses.com" in url:
                yield scrapy.Request(url=url[:-1], callback=self.download8Muses)
            elif "porngals4" in url:
                yield scrapy.Request(url=url[:-1], callback=self.porngals4)
            elif "porncomix.info" in url:
                yield scrapy.Request(url=url[:-1], callback=self.downloadPorncomix)
            elif "lucyzara.com" in url:
                yield scrapy.Request(url=url[:-1], callback=self.BoundCash)
            elif "santabanta.com" in url:
                yield scrapy.Request(url=url[:-1], callback=self.santabanta)
            elif "aziani.com" in url:
                yield scrapy.Request(url=url[:-1], callback=self.aziani)
            elif "scoreland.com" in url:
                yield scrapy.Request(url=url[:-1], callback=self.ScoreLand)
            elif "r34anim.com" in url:
                yield scrapy.Request(url=url[:-1], callback=self.r34anime)
            elif "babesource.com" in url:
                yield scrapy.Request(url=url[:-1], callback=self.downloadThisBabesGallery)
            elif "penthouse.com" in url:
                yield scrapy.Request(url=url[:-1], callback=self.pentHouse)
            elif "lyndaleigh.com" in url:
                yield scrapy.Request(url=url[:-1], callback=self.babeShow)
            elif "jenniferjade.xxx" in url:
                yield scrapy.Request(url=url[:-1], callback=self.babeShow)
            elif "deviantart.com" in url:
                yield scrapy.Request(url=url[:-1], callback=self.deviantArt)
            elif "lyndaleigh.com" in url:
                yield scrapy.Request(url=url[:-1], callback=self.babeShow)
            elif "instagram.com" in url:
                yield scrapy.Request(url=url[:-1], callback=self.instagramVideo)
            elif "japanesebeauties.net" in url:
                yield scrapy.Request(url=url[:-1], callback=self.japanesebeauties)
            elif "dogfartnetwork.com" in url:
                spiderMeta = {}
                spiderMeta["filterByHtml"] = "pics"
                spiderMeta["website"] = "dogfartnetwork.com"
                yield scrapy.Request(url=url[:-1], callback=self.expander, meta=spiderMeta)
            else:
                print("else " + url)
                yield scrapy.Request(url=url[:-1], callback=self.imgLinks)

    def r34anime(self, response):
        videoUrl = response.css("source::attr(src)").extract()[0]
        filename = videoUrl.split("/")[-1].split("?")[0]
        self.downloadThisVideo(response, r"C:\Heaven\Haven\pornTubes", filename, videoUrl)

    def alreadyNotDownloaded(self, fileName, Id):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        try:
            fp = open(dir_path + "\\list\\%s.txt" % fileName, "r")
            print("openening file name %s for checking id %s" % (fileName, Id))
        except(FileNotFoundError):
            return True
        data = fp.read()
        fp.close()
        if Id in data:
            print("%s already cntains %s" % (fileName, Id))
            return False
        else:
            return True

    def expander(self, response):
        print("Entering Expand And Download PHase")
        if "filterByHtml" in response.meta:
            filterByHtml = response.meta["filterByHtml"]
            links = response.css("a[href*=%s]::attr(href)" % (filterByHtml)).extract()
            print(filterByHtml)
        for link1 in links:
            link = response.urljoin(link1)
            print(link)
            if "dogfartnetwork.com" in link or True:
                spiderMeta = {}
                spiderMeta["filterBySrc"] = "hirez"
                spiderMeta["getNameBy"] = "Title"
                yield scrapy.Request(url=link, callback=self.SingleImage, meta=spiderMeta, priority=1)

    def SingleImage(self, response):
        print("Entering a page to download a single image")
        imgUrl = response.css("img[src*=%s]::attr(src)" % (response.meta["filterBySrc"])).extract()
        for Iurl in imgUrl:
            if response.meta["getNameBy"] == "fileName":
                imgFileCode = Iurl.split("/")[-1]
                imgFileName = imgFileCode.split("?")[0]
            if response.meta["getNameBy"] == "Title":
                imgFileName = response.css("title::text").extract()[0]
            self.downloadImg(Iurl, "Expande\\%s" % imgFileName)

    def downloadCompleteRegister(self, fileName, Id):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        print("Writing file name %s for id %s" % (fileName, Id))
        try:
            self.line_prepender(dir_path + "\\list\\%s.txt" % fileName, Id)
        except FileNotFoundError as e:
            with open(dir_path + "\\list\\%s.txt" % fileName, 'w') as f:
                pass
                self.line_prepender("list\\%s.txt" % fileName, Id)

        # fp = open("list\\%s.txt" % fileName, "a")
        # fp.write(Id+",")
        # fp.close()

    def instagramVideo(self, response):
        print("Downloadin from instagram videos")
        name = response.css("meta[property*=title]::attr(content)").extract()[0]
        print("name = " + name)
        response.meta['extractedName'] = re.search("^(.*?) on", name)[1]
        response.meta['imgId'] = response.url.split("/")[4]
        videoURL = response.css("head").re("<meta property=\"og:video\" content=\"(.*?)\"")[0]
        videoPath = r"D:\paradise\stuff\SinToWatch"
        filename = response.meta['extractedName'] + " " + response.meta['imgId'] + ".mp4"
        self.downloadThisVideo(response, videoPath, filename, videoURL)
        print(videoURL)

    def downloadThisVideo(self, response, videoPath, filename, videoUrl):
        filename = self.properName(filename)
        if self.alreadyNotDownloaded("videos", filename):
            cmd = r"C:\Program Files (x86)\Internet Download Manager\IDMan.exe"
            wholeCommand = 'start "" "%s" /d %s /p "%s" /f \"%s\" /n /a' % (cmd, videoUrl, videoPath, filename)
            print(wholeCommand)
            os.system(wholeCommand)
            self.downloadCompleteRegister("videos", filename)

    def extractFromBodyRe(self, response, codeRe):
        response.css("body").re(codeRe)

    def thumbToLarge(self, response):
        strInSrc = response.meta['search']
        replaceWith = response.meta['replace']
        if "index" in response.meta:
            index = response.meta['index']
        else:
            index = -1
        print("thumbToLarge")
        websiteName = self.properName(response.url.split("/")[2])
        if response.meta['galleryCodeFromURL'] == "":
            galleryCode = response.url.split("/")[int(index)]
        else:
            galleryCode = "@" + response.meta['galleryCodeFromURL'] + "@"
        i = 0
        imgUrls = response.css("a img::attr(src)").re(".*%s.*" % strInSrc)
        # imgUrls = response.css("a img[src*=%s]::attr(src)" % (strInSrc,)).extract()
        if self.alreadyNotDownloaded(websiteName, galleryCode):
            for imgUrl in imgUrls:
                i = i + 1
                formedUrl = re.sub(strInSrc, replaceWith, imgUrl)
                imgFileName = galleryCode + " " + str(i) + ".jpg"
                print(formedUrl)
                if not re.search("http", formedUrl):
                    temp = "/".join(response.url.split("/")[:-1])
                    temp = temp.strip("/") + "/"
                    formedUrl = temp + formedUrl
                print(formedUrl)
                self.downloadImg(formedUrl, "BabesImgs\\%s" % imgFileName)
            self.downloadCompleteRegister(websiteName, galleryCode)

    def thumbToLarge2(self, response):
        strInSrc = response.meta['search']
        replaceWith = response.meta['replace']
        if "index" in response.meta:
            index = response.meta['index']
        else:
            index = -1
        print("thumbToLarge")
        websiteName = self.properName(response.url.split("/")[2])
        if response.meta['galleryCodeFromURL'] == "":
            galleryCode = response.url.split("/")[int(index)]
        else:
            galleryCode = "@" + response.meta['galleryCodeFromURL'] + "@"
        i = 0
        imgUrls = response.css("a img::attr(src)").re(".*%s.*" % strInSrc)
        # imgUrls = response.css("a img[src*=%s]::attr(src)" % (strInSrc,)).extract()
        if self.alreadyNotDownloaded(websiteName, galleryCode):
            for imgUrl in imgUrls:
                i = i + 1
                formedUrl = re.sub(strInSrc, replaceWith, imgUrl)
                # imgFileName = galleryCode + " " + str(i) + ".jpg"
                imgFileName = galleryCode + " " + formedUrl.split("/")[-1]
                print(formedUrl)
                if not re.search("http", formedUrl):
                    temp = "/".join(response.url.split("/")[:-1])
                    temp = temp.strip("/") + "/"
                    formedUrl = temp + formedUrl
                print(formedUrl)
                self.downloadImg(formedUrl, "Expande\\%s" % imgFileName)
            self.downloadCompleteRegister(websiteName, galleryCode)

    def roadBlock(self, index, filename):
        print("entering roadblock")
        if index < 2:
            print("index is low")
            return True
        else:
            unblockingFile = self.properName("pending\\" + filename)
            if os.path.isfile(unblockingFile):
                print("file found in pending directory: " + filename)
                return True
            else:
                print(unblockingFile + " not found in pending directory")
                return False

    def imgLinks(self, response):
        if 'index' in response.meta:
            index = response.meta['index']
        else:
            index = 0
        # print("imgLinks " + index)
        websiteName = self.properName(response.url.split("/")[2])
        if 'galleryCodeFromURL' not in response.meta:
            if 'index' in response.meta:
                galleryCode = response.url.split("/")[index]
            else:
                galleryCode = response.url
        else:
            galleryCode = "@" + response.meta['galleryCodeFromURL'] + "@"
            print("galleryCode is " + galleryCode)
        i = 0
        imgUrls = response.css("a[href*=\.jpg]::attr(href)").extract()
        # imgUrls = response.css("a img[src*=%s]::attr(src)" % (strInSrc,)).extract()
        if self.alreadyNotDownloaded(websiteName, galleryCode):
            pendingFilename = ""
            print("setting pendingfile name to skip")
            for imgUrl in imgUrls:
                downloadDir = "BabesImgs"
                i = i + 1
                formedUrl = imgUrl
                imgFileName = galleryCode + " " + str(i) + ".jpg"
                print("Currently Formed URL is " + formedUrl)
                if not re.search("http", formedUrl):
                    temp = "/".join(response.url.split("/")[:-1])
                    temp = temp.strip("/") + "/"
                    formedUrl = temp + formedUrl
                print(formedUrl)
                if 'pending' in response.meta:
                    if not self.roadBlock(i, pendingFilename):
                        return
                    else:
                        if pendingFilename == "":
                            pendingFilename = imgFileName
                            downloadDir = "blocked"
                # imgFileName = "pending " + imgFileName
                self.downloadImg(formedUrl, "%s\\%s" % (downloadDir, imgFileName))
            if 'pending' in response.meta:
                print("Whats Happening" + pendingFilename)
                if pendingFilename == "":
                    pendingFilename = galleryCode + " " + str(1) + ".jpg"
                os.rename("C:\\Users\\Alind\\PycharmProjects\\ImgDownloader\\pending\\" + pendingFilename,
                          "C:\\Users\\Alind\\PycharmProjects\\ImgDownloader\\BabesImgs\\X" + pendingFilename)
            self.downloadCompleteRegister(websiteName, galleryCode)

    def line_prepender(self, filename, line):
        with open(filename, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(line.rstrip('\r\n') + '\n' + content)

    def DeleteThisLine(self, filename, line):
        with open(filename, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            content.replace(line, "")
            f.write(content)

    def indianMasala(self, response):
        print(response.url)

        MasalaDir = re.search("dir=(.*)", response.url)[1]
        galLinks = response.css("a[href*=%s]::attr(href)" % MasalaDir).extract()
        websiteName = self.properName(response.url.split("/")[2])
        for links in galLinks:
            forgedUrl = urllib.request.urljoin(response.url, links)
            galCode = forgedUrl.split("=")[-1]
            BheeghiMeta = {}
            if self.alreadyNotDownloaded(websiteName, "@" + galCode + "@"):
                BheeghiMeta["search"] = "thumbnails/"
                BheeghiMeta["replace"] = ""
                BheeghiMeta["galleryCodeFromURL"] = galCode

                yield scrapy.Request(url=forgedUrl, callback=self.thumbToLarge2, priority=1, meta=BheeghiMeta)

    def findNewMasalaGallery(self, response):
        print(response.url)
        # galleryCodes = response.css("a")
        fileName = "indianMasala.txt"
        print(fileName)
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

    def downloadThisBabesGallery(self, response):
        print("Downloading Pictures from URL:%s" % response.url)
        imgUrls = response.css("a").re("href=\"([^\"]*jpg)\"")
        i = 0
        if self.alreadyNotDownloaded("babeGallery", response.css("title").re("<title>(.*?)<")[0]):
            for imgUrl in imgUrls:
                i += 1
                imgFileName = response.css("title").re("<title>(.*?)<")[0] + str(i) + ".jpg"
                print(imgUrl)
                self.downloadImg(imgUrl, "BabesImgs\\%s" % imgFileName)
            self.downloadCompleteRegister("babeGallery", response.css("title").re("<title>(.*?)<")[0])

    def pentHouse(self, response):
        print("Downloading Pictures from URL:%s" % response.url)
        imgUrls = response.css("a").re("href=\"([^\"]*jpg)\"")
        i = 0
        imgCode = "@" + re.search("g/(.*?)/", response.url)[1] + "@"
        if self.alreadyNotDownloaded("babeGallery", imgCode):
            for imgUrl in imgUrls:
                i += 1
                imgFileName = response.css("title").re("<title>(.*?)<")[0] + str(i) + ".jpg"
                print(imgUrl)
                self.downloadImg(imgUrl, "BabesImgs\\%s" % imgFileName)
            self.downloadCompleteRegister("babeGallery", imgCode)

    def eurotica(self, response):
        print("Downloading Pictures from URL:%s" % response.url)
        imgUrls = response.css("a").re("href=\"([^\"]*jpg)\"")
        imgCode = response.css("title").re("<title>(.*?)<")[0] + " " + response.css("a[title*=model]::text").extract()[
            0]
        i = 0
        if self.alreadyNotDownloaded("eurotica", imgCode):
            for imgUrl in imgUrls:
                i += 1
                imgFileName = imgCode + str(i) + ".jpg"
                print(imgUrl)
                self.downloadImg(imgUrl, "BabesImgs\\%s" % imgFileName)
            self.downloadCompleteRegister("eurotica", imgCode)

    def babeShow(self, response):
        print("Downloading Pictures from URL:%s" % response.url)
        imgUrls = response.css("a").re("href=\"([^\"]*jpg)\"")
        imgCode = response.url.split("/")[-1].split(".")[0] + "@"
        i = 0
        if self.alreadyNotDownloaded("babeShow", imgCode):
            for imgUrl in imgUrls:
                i += 1
                imgFileName = imgCode + str(i) + " " + ".jpg"
                print(imgUrl)
                self.downloadImg(imgUrl, "BabesImgs\\%s" % imgFileName)
            self.downloadCompleteRegister("babeShow", imgCode)

    def dirtyHardcash(self, response):
        print("Downloading Pictures from URL:%s" % response.url)
        imgUrls = response.css("a").re("href=\"([^\"]*jpg)\"")
        imgCode = "@" + re.search("gallery_id=([0-9]+)", response.url)[1] + "@"
        i = 0
        if self.alreadyNotDownloaded("dirtyHardcash", imgCode):
            for imgUrl in imgUrls:
                i += 1
                imgFileName = imgCode + " dirtyHardCash " + str(i) + " " + ".jpg"
                print(imgUrl)
                self.downloadImg("http://dirtyhardcash.com/members/" + imgUrl.replace("&amp;", "&"),
                                 "BabesImgs\\%s" % imgFileName)
            self.downloadCompleteRegister("dirtyHardcash", imgCode)

    def santabanta(self, response):
        print("santabanta")
        imgLinks = response.css("img[src*=media]::attr(src)").extract()
        for links in imgLinks:
            filename = links.split("/")[-1]
            largeLink = links.replace("media.", "media1.").replace("/medium1/", "/full6/")
            self.downloadImg(largeLink, "Expande\\%s" % filename)

    def relativeToAbsoulute(self, response, relativeURL):
        f = response.url.split("/")
        f = "/".join(f[:-1]).rstrip("/") + "/"
        absURL = f + relativeURL.lstrip("/")
        return absURL

    def puba(self, response):
        print("Downloading Pictures from URL puba:%s" % response.request.url)
        print(response.url)
        imgUrls = response.css("a").re("href=\"([^\"]*jpg)\"")
        imgCode = response.url.split("/")[-2]
        t = response.url
        i = 0
        if self.alreadyNotDownloaded("puba", imgCode):
            for imgUrl in imgUrls:
                i += 1
                imgFileName = response.url.split("/")[-3] + " " + imgCode + str(i) + ".jpg"
                imgUrl = self.relativeToAbsoulute(response, imgUrl)
                print(imgUrl)
                self.downloadImg(imgUrl, "BabesImgs\\%s" % imgFileName)
            self.downloadCompleteRegister("puba", imgCode)
            self.downloadCompleteRegister("puba2", "@" + re.search("wmfear\.14\.9\.9\.0\.(.*?)\.0\.0\.0", t)[1] + "@")

    def aziani(self, response):
        print("Downloading Pictures from URL:%s" % response.url)
        StaticImgUrl = response.css("a").re("href=\"([^\"]*\.jpg)\"")[0]
        i = 0
        if self.alreadyNotDownloaded("aziani", response.css("title").re("<title>(.*?)<")[0].split("-")[0]):
            for picNumber in range(20):
                i += 1
                imgUrl = "http://thumbs.aziani.com:81" + re.sub("[0-9]+\-full", str(i) + "-full", StaticImgUrl)
                imgFileName = response.css("title").re("<title>(.*?)<")[0].split("-")[0] + str(i) + ".jpg"
                print(imgUrl)
                self.downloadImg(imgUrl, "BabesImgs\\%s" % imgFileName)
            self.downloadCompleteRegister("aziani", response.css("title").re("<title>(.*?)<")[0].split("-")[0])

    def deviantArt(self, response):
        parseTheseLink = [response.url] + response.css("div.gr a::attr(href)").extract()
        for links in parseTheseLink:
            yield scrapy.Request(links, callback=self.deviantArtConvertToRSS, priority=1)

    def deviantArtConvertToRSS(self, response):
        parseTheseLink = response.css("link[type*=application]::attr(href)").extract()
        for links in parseTheseLink:
            yield scrapy.Request(links, callback=self.downloadDeviantImages, priority=2)

    def downloadDeviantImages(self, response):
        imageUrls = response.css("media\:content::attr(url)").extract()
        for imgUrls in imageUrls:
            imgFileName = imgUrls.split("/")[-1]
            self.ensure_dir("Art\\")
            if not self.downloadImg(imgUrls, "Art\\%s" % imgFileName):
                break

    def ScoreLand(self, response):
        print("Downloading Pictures from URL:%s" % response.url)
        imgUrls = response.css("img").re("src=\"([^\"]*_tn.jpg)\"")
        i = 0
        if self.alreadyNotDownloaded("ScoreLand", response.css("title").re("<title>(.*?)<")[0]):
            for imgUrl in imgUrls:
                i += 1
                imgFileName = response.css("title").re("<title>(.*?)<")[0] + str(i) + ".jpg"
                formedUrl = imgUrl.replace("_tn.jpg", ".jpg")
                print(imgUrl)

                self.downloadImg(formedUrl, "BabesImgs\\%s" % imgFileName)
            self.downloadCompleteRegister("ScoreLand", response.css("title").re("<title>(.*?)<")[0])

    def porngals4(self, response):
        print("Downloading Pictures from URL:%s" % response.url)
        imgUrls = response.css("a").re("href=\"([^\"]*?jpg)\"")
        i = 0
        if self.alreadyNotDownloaded("porngals4", response.css("title").re("<title>(.*?)<")[0]):
            for imgUrl in imgUrls:
                i += 1
                imgFileName = response.css("title").re("<title>(.*?)<")[0] + str(i) + ".jpg"
                # print("currently Downloding This url from porngals88:" + imgUrls[i-1])
                self.downloadImg(imgUrl, "BabesImgs\\%s" % imgFileName)
            self.downloadCompleteRegister("porngals4", response.css("title").re("<title>(.*?)<")[0])

    def ddf(self, response):
        print("Downloading Pictures from URL:%s" % response.url)
        imgUrls = response.css("a").re("href=\"([^\"]*?\.jpg)\"")
        i = 0
        if self.alreadyNotDownloaded("ddf", response.css("title").re("<title>(.*?)<")[0]):
            for imgUrl in imgUrls:
                i += 1
                imgFileName = self.properName(response.css("title").re("<title>(.*?)<")[0] + str(i) + ".jpg")
                print(imgUrl)
                self.downloadImg("https:" + imgUrl, "BabesImgs\\%s" % imgFileName)
            self.downloadCompleteRegister("ddf", response.css("title").re("<title>(.*?)<")[0])

    def photodromm(self, response):
        print("Downloading Pictures from URL:%s" % response.url)
        imgUrls = response.css("img").re("src=\"(thumb.*?)\"")
        i = 0
        if self.alreadyNotDownloaded("photodromm", re.findall("[0-9]+", response.url)[0]):
            for imgUrl in imgUrls:
                i += 1
                imgFileName = "PhotoDromm " + re.findall("[0-9]+", response.url)[0] + str(i) + ".jpg"
                print(imgUrl)
                staticUrl = "http://www.phdcash.com/hosted/photodromm_614/higher/01.jpg"
                staticUrl = staticUrl.replace("614", re.findall("[0-9]+", response.url)[0])
                staticUrl = staticUrl.replace("01.jpg", str(i).zfill(2) + ".jpg")
                self.downloadImg(staticUrl, "BabesImgs\\%s" % imgFileName)
            self.downloadCompleteRegister("photodromm", re.findall("[0-9]+", response.url)[0])

    def alluringvixens(self, response):
        print("Downloading Pictures from URL:%s" % response.url)
        imgUrls = response.css("a").re("href=\"([^\"]*?\.jpg)\"")
        i = 0
        if self.alreadyNotDownloaded("alluringvixens", response.css("title").re("<title>(.*?)<")[0]):
            for imgUrl in imgUrls:
                i += 1
                imgFileName = response.css("title").re("<title>(.*?)<")[0] + str(i) + ".jpg"
                imgFileName = re.sub('[^A-Za-z0-9\. ]+', '', imgFileName)
                modelName = response.url.split("/")[-3] + "/"
                ForgedLink = "http://galleries.alluringvixens.com/" + modelName
                imgUrl = imgUrl.replace("../", ForgedLink)
                print(imgUrl)
                self.downloadImg(imgUrl, "BabesImgs\\%s" % imgFileName)
            self.downloadCompleteRegister("alluringvixens", response.css("title").re("<title>(.*?)<")[0])

    def dirtynakedpics(self, response):
        print("Downloading Pictures from URL:%s" % response.url)
        imgUrls = response.css("img").re("src=\"(.*?-tn\.jpg)\"")
        i = 0
        if self.alreadyNotDownloaded("dirtynakedpics", response.url.split("/")[-2]):
            for imgUrl in imgUrls:
                i += 1
                imgUrl = "http://www.dirtynakedpics.com/" + imgUrl
                imgUrl = imgUrl.replace("-tn.jpg", ".jpg")
                imgFileName = response.url.split("/")[-2] + str(i) + ".jpg"
                # imgFileName = imgUrl.split("/")[-1]
                print(imgUrl)
                self.downloadImg(imgUrl, "BabesImgs\\%s" % imgFileName)
            self.downloadCompleteRegister("dirtynakedpics", response.url.split("/")[-2])

    def japanesebeauties(self, response):
        print("Downloading Pictures from URL:%s" % response.url)
        imgUrls = response.css("a").re("href=\"([^\"]*jpg)\"")
        i = 0
        if self.alreadyNotDownloaded("japanesebeauties.net", response.url):
            for imgUrl in imgUrls:
                i += 1
                imgFileName = response.url.split("/")[-2] + imgUrl.split("/")[-1]
                print(imgUrl)
                self.downloadImg("https://www.japanesebeauties.net" + imgUrl, "BabesImgs\\%s" % imgFileName)
            self.downloadCompleteRegister("japanesebeauties.net", response.url)

    def BoundCash(self, response):
        print("boundCash")
        imgUrls = response.css("a").re("href=\"([^\"]*jpg)\"")
        i = 0
        if self.alreadyNotDownloaded("lucyZara", response.url):
            for imgUrl in imgUrls:
                i += 1
                formedUrl = imgUrl.replace("../", "http://www.lucyzara.com/directory_pages/")
                imgFileName = response.url.split("/")[-1].split(".")[0] + str(i) + ".jpg"
                print(formedUrl)
                self.downloadImg(formedUrl, "BabesImgs\\%s" % imgFileName)
            self.downloadCompleteRegister("lucyZara", response.url)

    def EvilAngel(self, response):
        print("evilAngel")
        imgUrls = response.css("a[href*=jpg]::attr(href)").extract()
        i = 0
        starName = " and ".join(response.css(".pgTitleActorsText").re("title=\"(.*?)\"")) + " "
        galCode = imgUrls[0].split("/")[-1].split(".")[0].split("_")[0]
        if self.alreadyNotDownloaded("evilAngel", response.url):
            for imgUrl in imgUrls:
                # formedUrl = imgUrl.replace("001.jpg", str(i).zfill(3) + ".jpg")
                imgFileName = starName + imgUrl.split("/")[-1].split(".")[0] + ".jpg"
                # print(formedUrl)

                self.downloadImg(imgUrl, "BabesImgs\\%s" % imgFileName)
            self.downloadCompleteRegister("evilAngel", response.url)
        thirdPartyUrlTemplate = "http://html.sxx.com/2/128/pics/@@/nude/153_c1848_01.html?pr=8&su=1&ad=12950"
        thirdPartyUrl = thirdPartyUrlTemplate.replace("@@", galCode)
        spiderMeta = {}
        spiderMeta["galCode"] = galCode
        spiderMeta["galleryName"] = starName
        yield scrapy.Request(url=thirdPartyUrl, callback=self.thirdParty, meta=spiderMeta)

    def thirdParty(self, response):
        galleryCode = response.meta["galCode"]
        galName = response.meta["galleryName"]
        websiteName = self.properName(response.url.split("/")[2])
        i = 0
        imgUrls = response.css("a[href*=\.jpg]::attr(href)").extract()
        # imgUrls = response.css("a img[src*=%s]::attr(src)" % (strInSrc,)).extract()
        if self.alreadyNotDownloaded(websiteName, galleryCode):
            pendingFilename = ""
            print("setting pendingfile name to skip")
            for imgUrl in imgUrls:
                downloadDir = "BabesImgs"
                i = i + 1
                formedUrl = imgUrl
                imgFileName = galName + " " + galleryCode + " " + str(i) + ".jpg"
                print("Currently Formed URL is " + formedUrl)
                if not re.search("http", formedUrl):
                    temp = "/".join(response.url.split("/")[:-1])
                    temp = temp.strip("/") + "/"
                    formedUrl = temp + formedUrl
                print(formedUrl)
                # imgFileName = "pending " + imgFileName
                self.downloadImg(formedUrl, "%s\\%s" % (downloadDir, imgFileName))
            self.downloadCompleteRegister(websiteName, galleryCode)

    def DevilsFilm(self, response):
        print("DevilsFilm")
        imgUrl = response.css("a").re("href=\"(.*?nva.*?)\"")[0]
        i = 0
        # starName = response.css("a[href*=pornstar]::attr(title)").extract()
        starName = " And ".join(response.css("a[href*=pornstar]::attr(title)").extract())
        if self.alreadyNotDownloaded("devilsfilm", response.url):
            for i in range(0, 84, 4):
                formedUrl = imgUrl.replace("001.jpg", str(i).zfill(3) + ".jpg")
                imgFileName = starName + " in " + " ".join(response.url.split("/")[-2:]) + " " + str(i) + ".jpg"
                print(formedUrl)
                self.downloadImg(formedUrl, "BabesImgs\\%s" % imgFileName)
            self.downloadCompleteRegister("devilsfilm", response.url)

    def downloadPorncomix(self, response):
        print("Downloading Pictures from URL:%s" % response.url)
        imgUrls = response.css("img.attachment-thumbnail.size-thumbnail").re("lazy-src=\"([^\"]*jpg)\"")
        i = 0
        comicsCode = re.sub('[^A-Za-z0-9\.\-]+', '', response.css("title").re("<title>(.*?)<")[0] + str(len(imgUrls)))
        if self.alreadyNotDownloaded("porncomix", response.css("title").re("<title>(.*?)<")[0]) or True:
            for imgUrl in imgUrls:
                i += 1
                print(imgUrl + "rock")
                replaceThis = "-" + imgUrl.split("-")[-1].split(".")[0] + "."
                formedUrl = imgUrl.replace(replaceThis, ".")
                # formedUrl = formedUrl.replace("-165x240.", ".")
                imgFileName = comicsCode
                self.ensure_dir(self.properName("comics\\%s\\%s" % (imgFileName, str(i) + ".jpg")))
                self.downloadImg(formedUrl, "comics\\%s\\%s" % (imgFileName, str(i) + ".jpg"))
            self.downloadCompleteRegister("porncomix", response.css("title").re("<title>(.*?)<")[0] + str(len(imgUrls)))

    def download8Muses(self, response):
        print("Downloading Pictures from URL:%s" % response.url)
        imgUrls = response.css(".lazyload").re("data-src=\"([^\"]*jpg)\"")
        i = 0
        comicsCode = re.sub('[^A-Za-z0-9\.\-]+', '', response.css("title").re("\\t\\t(.*)")[1])
        if self.alreadyNotDownloaded("8muses", comicsCode):
            for imgUrl in imgUrls:
                i += 1
                formedUrl = " https:" + imgUrl.replace("/th/", "/fm/")
                print(formedUrl)
                imgFileName = comicsCode
                self.ensure_dir("Comics\\%s\\%s" % (imgFileName, str(i) + ".jpg"))
                self.downloadImg(formedUrl, "Comics\\%s\\%s" % (imgFileName, str(i) + ".jpg"))
            self.downloadCompleteRegister("8muses", comicsCode)

    def comicVine(self,response):
        imgUrls = response.css(".fluid-width").css("img[src*=scale]::attr(src)").extract()
        print("Downloading Pictures from URL:%s" % response.url)
        i = 0
        galCode = response.css("title::text").extract()[0]
        if self.alreadyNotDownloaded("comicVine", galCode):
            for imgUrl in imgUrls:
                i += 1
                imgFileName = galCode + str(i) +".jpg"
                print(imgUrl)
                self.downloadImg(imgUrl, "Art\\%s" % imgFileName)
            self.downloadCompleteRegister("comicVine", galCode)


    def ensure_dir(self, file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def properName(self, name):
        name = name.replace("amp", "")
        return re.sub('[^A-Za-z0-9_\-\.\\\ ]+', "", name)

    def downloadImg(self, Url, path):
        regFile = "filewise\\" + re.sub('[^A-Za-z0-9\-]+', "", Url.split("/")[2])
        path = self.properName(path)
        try:
            if self.alreadyNotDownloaded(regFile, path):
                time.sleep(5)
                r = requests.get(Url, stream=True, timeout=5)
                if r.status_code == 200:
                    i = 0
                    self.ensure_dir("incomplete\\" + path)
                    with open("incomplete\\" + path, 'wb') as pdf:
                        for chunk in r.iter_content(chunk_size=1024):
                            # print(i)
                            # i = i + 1
                            # writing one chunk at a time to pdf file
                            # r.raise_for_status()
                            if chunk:
                                # print(chunk)
                                pdf.write(chunk)
                try:
                    os.rename("incomplete\\" + path, path)
                except Exception as e:
                    with open("logRenaming.txt", "a+") as inF:
                        inF.write(str(e) + "\n")
                        os.remove("incomplete\\" + path)
                self.downloadCompleteRegister(regFile, path)
                return True
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            raise scrapy.exceptions.DropItem("just drop it and continue")
            return False
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
        return False


if __name__ == "__main__":
    try:
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
        process.crawl(rssImageExtractor)
        process.start()
    except Exception as e:
        with open("log.txt", "a+") as inF:
            inF.write(str(e) + "\n")
