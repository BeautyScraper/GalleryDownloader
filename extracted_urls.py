import pandas as pd
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='Extract URLs from a file')
parser.add_argument('-d', '--dir', help='dir which contains shortlisted files', required=True)
parser.add_argument('-c', '--csv', help='csv File to extract URLs from', required=True)
parser.add_argument('-t', '--text', help='csv File to extract URLs from', required=True)
args = parser.parse_args()


#list corresponding file values of dir from csv
def list_files_from_csv(csv_path,dir_path):
    if csv_path.is_file():
        csv_data = pd.read_csv(csv_path)
        dir_csv = pd.DataFrame(data=list(x.name for x in dir_path.glob('*')),columns=['filename'])
        joined_result = csv_data.merge(dir_csv,how='left',on='filename')
        return list(joined_result['associated_url'])
    else:
        raise Exception("%s is not a file" % csv_path)

def main(csv_path,dir_path,txt_path):
    url_list = list_files_from_csv(csv_path,dir_path)
    with open(txt_path,'a+') as f:
        for x in url_list:
            f.write(x+'\n')


if __name__ ==  '__main__':
    dir_path = Path(args.file)
    csv_path = Path(args.csv)
    txt_path = Path(args.text)
    main(csv_path,dir_path)