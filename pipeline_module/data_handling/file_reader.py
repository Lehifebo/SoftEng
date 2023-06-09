import os
import pandas as pd
import logging


class FileReader:
    def __init__(self, path):
        self.path = path

    def get_excels(self):
        # Get the current directory
        path = self.path
        if not os.path.exists(path):
            logging.warning(f"Path {path} does not exist.")
        dataframes = []
        for file_name in os.listdir(path):
            if os.path.isfile(path + file_name) and "xlsx" in file_name:
                # read the excel files to pandas df
                df = pd.read_excel(path + file_name)
                # assume that the file names are matching XXXX_
                dataframes.append((file_name.split('_')[0], df))
        return dataframes
