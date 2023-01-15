
import os
import datetime
import pandas as pd
def remove_empty_lines_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    with open(file_path, 'w') as file:
        file.writelines([line for line in lines if line.strip() != ''])


def timestamp_file(file_path:str, timestamp_path:str):
    """
    Creates a new timestamp file if it doesn't exist
    Writes the current timestamp for each line in the original file
    """
    remove_empty_lines_from_file(file_path)
    if not os.path.exists(timestamp_path):
        timestamp_df = pd.DataFrame(columns=['Line', 'Timestamp'])
    else:
        timestamp_df = pd.read_csv(timestamp_path)
    with open(file_path, "r") as file:
        lines = file.readlines()
    with open(file_path, "w") as file:
        for line in lines:
            if line not in timestamp_df['Line'].values:
                timestamp_df = timestamp_df.append({'Line': line, 'Timestamp': str(datetime.datetime.now().date())}, ignore_index=True)
            file.write(line)
        timestamp_df.to_csv(timestamp_path, index=False)


def remove_old_lines(file_path:str, timestamp_path:str, days:int):
    """
    Removes lines from the original file that are older than a specified number of days
    """
    timestamp_df = pd.read_csv(timestamp_path)
    kr = pd.to_datetime(timestamp_df['Timestamp'])
    # breakpoint()
    breaking_date = (pd.to_datetime(datetime.datetime.now()) - pd.Timedelta(days=days))
    timestamp_df = timestamp_df[kr >= breaking_date]
    timestamp_df.to_csv(timestamp_path, index=False)
    with open(file_path, 'w') as f:
        for line in timestamp_df['Line']:
            f.write(line)



if __name__ == '__main__':
    file_path = "D:\Developed\Automation\GalleryDownloader\galleryLinks.opml"
    timestamp_path = "galleryLinks_timestamps.csv"
    days = 15

    timestamp_file(file_path, timestamp_path)
    remove_old_lines(file_path, timestamp_path, days)