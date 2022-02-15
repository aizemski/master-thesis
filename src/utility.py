import os, sys, re, shutil
import json
from pathlib import Path
from datetime import *
import urllib.request
from zipfile import ZipFile as zip
from constants import *

def get_destination_dir(file_url, folder=None):
    store_directory = STORE_DIRECTORY
    if folder:
        store_directory = folder
    if not store_directory:
        store_directory = os.path.dirname(os.path.realpath(__file__))
    print(os.path.join(store_directory, file_url))
    return os.path.join(store_directory, file_url)

def get_download_url(file_url):
    return "{}{}".format(BASE_URL, file_url)


def download_file(base_path, file_name, date_range=None, folder=None):
    download_path = "{}{}".format(base_path, file_name)
    
    if folder:
        base_path = os.path.join(folder, base_path)
    if date_range:
        date_range = date_range.replace(" ","_")
        base_path = os.path.join(base_path, date_range)
    save_path = get_destination_dir(os.path.join(base_path, file_name), folder)

    if os.path.exists(save_path):
        print("\nfile already exists! {}".format(save_path))
        return
    # make the directory
    if not os.path.exists(base_path):
        Path(get_destination_dir(base_path)).mkdir(parents=True, exist_ok=True)

    try:
        print(download_path)

        download_url = get_download_url(download_path)
        dl_file = urllib.request.urlopen(download_url)
        length = dl_file.getheader('content-length')
        if length:
            length = int(length)
            blocksize = max(4096,length//100)
        print('save_path-2',save_path)
        with open(save_path, 'wb+') as out_file:
            dl_progress = 0
            print("\nFile Download: {}".format(save_path))
            while True:
                    buf = dl_file.read(blocksize)   
                    if not buf:
                        break
                    dl_progress += len(buf)
                    out_file.write(buf)
                    done = int(50 * dl_progress / length)
                    sys.stdout.write("\r[%s%s]" % ('#' * done, '.' * (50-done)) )    
                    sys.stdout.flush()
        with zip(save_path, 'r') as zip_file:
            zip_file.extractall(path=os.path.join(STORE_DIRECTORY,base_path.replace('spot/monthly/klines/','')))
        
        os.remove(save_path)    
    except urllib.error.HTTPError:
        print("\nFile not found: {}".format(download_url))
        pass

def convert_to_date_object(d):
    year, month, day = [int(x) for x in d.split('-')]
    date_obj = date(year, month, day)
    return date_obj

def get_start_end_date_objects(date_range):
    start, end = date_range.split()
    start_date = convert_to_date_object(start)
    end_date = convert_to_date_object(end)
    return start_date, end_date



def check_directory(arg_value):
    if os.path.exists(arg_value):
        while True:
            option = input('Folder already exists! Do you want to overwrite it? y/n  ')
            if option != 'y' and option != 'n':
                print('Invalid Option!')
                continue
            elif option == 'y':
                shutil.rmtree(arg_value)
                break
            else:
                break
    return arg_value

def get_path( time_period, symbol, interval): 
    return f'data/spot/{time_period}/klines/{symbol.upper()}/{interval}/'
    
