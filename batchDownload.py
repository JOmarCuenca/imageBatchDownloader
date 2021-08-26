"""
Created by Jesus Omar Cuenca Espino (jesomar.cuenca@gmail.com)
JOmarCuenca

26/08/2021
"""

import pandas as pd
from pandas.core.frame import DataFrame
import requests
import argparse
from os import makedirs, name
from shutil import copyfileobj
from progressbar import progressbar, streams

# Setup Progressbar wrapper function
streams.wrap_stderr()

TARGET_COL_URLS = "urls"
TARGET_COL_NAME = "names"
TARGET_LOCAL_DIR = "imgs/"

def batchDownload(names : list, urls : list, targetDir : str):
    assert len(names) == len(urls)
    for img in progressbar(range(len(names))):
        response = requests.get(urls[img], stream=True)
        with open(targetDir + names[img], 'wb') as out_file:
            copyfileobj(response.raw, out_file)
        del response

def getColumnValues(data : DataFrame, cols : str) -> list:
    return data[cols].values

class ProgramArgs:
    def __init__(self, filename : str, verbose : bool, targetDir : str, xlsx : bool) -> None:
        self.filename = filename
        self.verbose = verbose
        self.targetDir = targetDir
        self.xlsx = xlsx

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download as a batch a bunch of images with a progress bar.')
    parser.add_argument('fileName', type=str, help='path to the file to be used as a list to download stuff')
    parser.add_argument("--xlsx", dest='xlsx', nargs="?",
                        const=True, default=False,
                        help='If you want it can read a xlsx file.')
    parser.add_argument('-v', "--verbose", dest='verbose', nargs="?",
                        const=True, default=False,
                        help='Should display the head of the file recieved.')
    parser.add_argument("-t", "--target-dir", dest='dir', nargs="?",
                        type=str, default=TARGET_LOCAL_DIR,
                        help="Target Directory to store the downloaded files (defaults to 'imgs/'")

    args = parser.parse_args()
    args = ProgramArgs(args.fileName,args.verbose, args.dir, args.xlsx)
    makedirs(args.targetDir,exist_ok=True)
    data : DataFrame = None
    if(args.xlsx):
        data = pd.read_excel(args.filename)
    else:
        data = pd.read_csv(args.filename)
    if(args.verbose):
        print(data.head())
    names = getColumnValues(data, TARGET_COL_NAME)
    urls = getColumnValues(data, TARGET_COL_URLS)
    batchDownload(names, urls, args.targetDir)
