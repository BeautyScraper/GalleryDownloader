import subprocess
import os
from urllib.parse import urlparse
from pathlib import Path

def alreadyNotDownloaded(fileName, Id):
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

def downloadCompleteRegister(fileName, Id,removeLine = False):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("Writing file name %s for id %s" % (fileName, Id))
    try:
        line_prepender(dir_path + "\\list\\%s.txt" % fileName, Id)
    except FileNotFoundError as e:
        with open(dir_path + "\\list\\%s.txt" % fileName, 'w') as f:
            pass
            line_prepender("list\\%s.txt" % fileName, Id)

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def generic_downloader(singleurl,file2dname,id='',connections=4,dirpath=''):
    filename = urlparse(singleurl).netloc + '.txt'
    savepath = r'D:\paradise\stuff\new\hott'
    if dirpath != '':
        savepath = dirpath
    # fpath = Path(fpath)
    if id == '':
        id = singleurl.split('/')[-1]
    if alreadyNotDownloaded(filename, id):
        ariaDownload(singleurl, savepath, file2dname, connections)
        downloadCompleteRegister(filename, id)

def ariaDownload(url,downPath,filename,connections=4):
    # import pdb;pdb.set_trace()
    subprocess.call(['aria2c', '--dir', downPath, '-o', filename,'-x', str(connections) , url])
