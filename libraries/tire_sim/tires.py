"""
Script to filter out TTC data and grab indices for camber, pressure + normal force.

ET = elasped time
V = speed
N?
SA = slip angle
IA = Camber angle
RL
RE
P = pressure
FX = long force
FY = lat force
FZ = normal force
MX = roll moment?
MZ = overturning moment?
AMBTMP = ambient temp
SR = slip ratio

"""

import pandas as pd
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum, auto
from pprint import pprint


class Stats(Enum):
    ELAPSED_TIME = auto()
    SPEED = auto()
    N = auto()
    SLIP_ANGLE = auto()
    CAMBER_ANGLE = auto()
    RL = auto()
    RE = auto()
    PRESSURE = auto()
    LONGITUDINAL_FORCE = auto()
    LATITUDINAL_FORCE = auto()
    NORMAL_FORCE = auto()
    MX = auto()
    MZ = auto()
    AMBIENT_TEMP = auto()
    SLIP_RATIO = auto()


TOLERANCE = {
    Stats.CAMBER_ANGLE: 0.5,
    Stats.NORMAL_FORCE: 500,
    Stats.PRESSURE: 25,
}


class TireParser:
    def __init__(self, path_to_summary_table, path_to_data_spreadsheet):
        """
        Initialize all of the index dictionaries given a data spreadsheet.

        :param path_to_summary_table: _description_
        :type path_to_summary_table: _type_
        :param path_to_data_spreadsheet: _description_
        :type path_to_data_spreadsheet: _type_
        """
        summary_data = pd.read_excel(path_to_summary_table)
        raw_data = loadmat(path_to_data_spreadsheet)

        self.tireid = raw_data["tireid"]
        print(f"Tire ID being queried: {self.tireid}")

        self.normal_force_data = raw_data["FZ"]
        self.pressure_data = raw_data["P"]
        self.camber_data = raw_data["IA"]

        self.camber = self.find_indices(self.camber_data, Stats.CAMBER_ANGLE)
        self.normal_force = self.find_indices(
            self.normal_force_data, Stats.NORMAL_FORCE
        )
        # pprint(self.normal_force)
        self.pressure = self.find_indices(self.pressure_data, Stats.PRESSURE)

        self.complete_dict = {
            Stats.CAMBER_ANGLE.name: self.camber,
            Stats.NORMAL_FORCE.name: self.normal_force,
            Stats.PRESSURE.name: self.pressure,
        }
        pprint(self.complete_dict)

    def find_indices(self, data_column, key):
        """
        Given a data column and key, find the indices were a different "test" has occurred.

        Determine differences by TOLERANCE dictionary.

        :param data_column: _description_
        :type data_column: _type_
        :param key: _description_
        :type key: _type_
        :return: _description_
        :rtype: _type_
        """

        unique = {}
        curr_val = data_column[0]
        for i, val in enumerate(data_column):
            if abs(val - curr_val) > TOLERANCE[key]:
                # FIGURE OUT HOW TO MAKE THIS AN ESTIMATED INSTEAD OF A SPECIFIC VAL
                unique[float(curr_val)] = i
                # print(val, curr_val)
                curr_val = val

        return unique

    def find_compliant_values(self, config_dict):
        """
        based on a specified set of values, find the indices that satisfy all of those conditions

        :param config_dict: _description_
        :type config_dict: _type_
        :param complete_dict: _description_
        :type complete_dict: _type_
        """

        # self.complete_dict

    def query(self, **kwargs):
        """
        Given a set of keyword arguments, find the data that satisfies all of those conditions

        :param kwargs: _description_
        :type kwargs: _type_
        """
        config = {}
        for arg in kwargs:
            # NAME OF SETTING
            setting = list(kwargs[arg].keys())[0]
            value = list(kwargs[arg].values())[0]
            config[setting] = value

        self.find_compliant_values(config)
        pass

    def show_data(self, data, index_dict, title=None):
        """
        Show a set of data with certain indices highlighted

        :param data: _description_
        :type data: _type_
        :param indices: _description_
        :type indices: _type_
        :param title: _description_, defaults to None
        :type title: _type_, optional
        """
        plt.plot(data)
        # this iterates through the keys, which are indexes
        for index in index_dict:
            plt.axvline(x=index_dict[index], color="red")

        plt.title(title)
        plt.show()


if __name__ == "__main__":
    parser = TireParser(
        path_to_summary_table="assets/tire_data/ttc_data.xls",
        path_to_data_spreadsheet="assets/tire_data/B1464run19.mat",
    )

    parser.query(val1={Stats.CAMBER_ANGLE: 2.004})

    pattern = parser.camber
    # parser.show_data(parser.camber_data, pattern, "camber on camber")
    # parser.show_data(
    #     parser.normal_force_data,
    #     pattern,
    #     "camber on normal force",
    # )
    # parser.show_data(parser.pressure_data, pattern, "camber on pressure")
