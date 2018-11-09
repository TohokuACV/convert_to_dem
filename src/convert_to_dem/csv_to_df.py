from .to_df_converter import ToDfConverter

import pandas as pd


class CsvToDf(ToDfConverter):
    def __init__(self):
        pass

    @staticmethod
    def read(x_csv, y_csv, z_csv):
        """
        Reads in a CSV file representing the 2D grid and return a DataFrame
        :param x_csv: the CSV file containing X values
        :return: pandas DataFrame where indices are X and Y grid number
        :rtype: pd.DataFrame
        """
        x_df = pd.read_csv(x_csv, header=None)
        y_df = pd.read_csv(y_csv, header=None)
        z_df = pd.read_csv(z_csv, header=None)
        xyz = pd.concat([x_df.stack(), y_df.stack(), z_df.stack()], axis=1)
        xyz.columns = list('xyz')
        return xyz
