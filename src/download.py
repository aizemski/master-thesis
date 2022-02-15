import sys
from argparse import ArgumentParser, RawTextHelpFormatter, ArgumentTypeError
from datetime import *
import pandas as pd
from constants import *
from utility import download_file, get_start_end_date_objects, convert_to_date_object, \
    get_path


def download_monthly_klines(trading_type, symbols,  intervals, years, months, start_date="", end_date="", folder=""):
    current = 0
    date_range = None

    if start_date and end_date:
        date_range = start_date + " " + end_date

    if not start_date:
        start_date = START_DATE
    else:
        start_date = convert_to_date_object(start_date)

    if not end_date:
        end_date = END_DATE
    else:
        end_date = convert_to_date_object(end_date)

    for symbol in symbols:
        for interval in intervals:
            for year in years:
                for month in months:
                    current_date = convert_to_date_object(
                        '{}-{}-01'.format(year, month))
                    if current_date >= start_date and current_date <= end_date:
                        path = get_path("monthly", symbol, interval)
                        file_name = "{}-{}-{}-{}.zip".format(
                            symbol.upper(), interval, year, '{:02d}'.format(month))
                        download_file(path, file_name, date_range, folder)

        current += 1
