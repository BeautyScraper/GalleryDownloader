from aria2cgeneric import generic_downloader
from pathlib import Path
import pandas as pd


class thumb_writer:
    def __init__(self,csv_path='') -> None:
        self.csv_path = r'c:\temp\thumbs.csv'
        self.connections = 1
        if csv_path != '':
            self.csv_path = csv_path
        if Path(self.csv_path).is_file():
            self.csv_data = pd.read_csv(self.csv_path)
        else:
            self.csv_data = pd.DataFrame(columns=['filename','associated_url'])

    def list_thumbnail_gen(self,img_urls,associated_urls,filenames):
        for x in zip(img_urls,associated_urls,filenames):
            self.single_thumbnail_gen(x[0],x[1],x[2])
        self.thumbs_write()
        return

    def single_thumbnail_gen(self,img_url,associated_url,filename):
        generic_downloader(img_url,filename,img_url,self.connections)
        self.csv_data = self.csv_data.append({'filename':filename,'associated_url':associated_url},ignore_index=True)
        return
    
    def thumbs_write(self):
        self.csv_data.to_csv(self.csv_path,index=False)
        return