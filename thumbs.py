import re
from aria2cgeneric import generic_downloader
from pathlib import Path
import pandas as pd


class thumb_writer:
    def __init__(self,csv_path='') -> None:
        if csv_path == '':
            self.csv_path = r'c:\temp\thumbs.csv'
        self.connections = 1
        if csv_path != '':
            self.csv_path = csv_path
        Path(self.csv_path).parent.mkdir(parents=True,exist_ok=True)
        if Path(self.csv_path).is_file():
            self.csv_data = pd.read_csv(self.csv_path)
        else:
            self.csv_data = pd.DataFrame(columns=['filename','associated_url'])

    def list_thumbnail_gen(self,img_urls,associated_urls,filenames):
        zipped_thumb = zip(img_urls,associated_urls,filenames)
        if len(img_urls) != len(associated_urls) or len(img_urls) != len(filenames):
            print("Error: img_urls, associated_urls, and filenames must be the same length")
            breakpoint()
        for x in zipped_thumb:
            self.single_thumbnail_gen(x[0],x[1],x[2])
        self.thumbs_write()
        return

    def single_thumbnail_gen(self,img_url,associated_url,filename):
        if Path(filename).suffix != '.jpg':
            filename += '.jpg'
        filename = re.sub('[^0-9a-zA-Z\.]+', '_', filename)
        generic_downloader(img_url,filename,img_url,self.connections,str(Path(self.csv_path).parent))
        self.csv_data = self.csv_data.append({'filename':filename,'associated_url':associated_url},ignore_index=True)
        return
    
    def thumbs_write(self):
        self.csv_data.to_csv(self.csv_path,index=False)
        return