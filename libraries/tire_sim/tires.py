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
    Stats.NORMAL_FORCE: 200,
    Stats.PRESSURE: 25,
}


class TireParser:
    def __init__(self, path_to_summary_table, path_to_data_spreadsheet):
        summary_data = pd.read_excel(path_to_summary_table)
        raw_data = loadmat(path_to_data_spreadsheet)

        self.normal_force_data = raw_data["FZ"]
        self.pressure_data = raw_data["P"]
        self.camber_data = raw_data["IA"]

        self.camber_indices = self.find_indices(self.camber_data, Stats.CAMBER_ANGLE)
        self.normal_force_indices = self.find_indices(
            self.normal_force_data, Stats.NORMAL_FORCE
        )
        self.pressure_indices = self.find_indices(self.pressure_data, Stats.PRESSURE)

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

        unique = []
        curr_val = data_column[0]
        for i, val in enumerate(data_column):
            if abs(val - curr_val) > TOLERANCE[key]:
                unique.append(i)
                # print(val, curr_val)
                curr_val = val

        return unique

    def show_data(self, data, indices, title=None):
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
        for index in indices:
            plt.axvline(x=index, color="red")

        plt.title(title)
        plt.show()


if __name__ == "__main__":
    tire_parser = TireParser(
        path_to_summary_table="assets/tire_data/ttc_data.xls",
        path_to_data_spreadsheet="assets/tire_data/B1464run19.mat",
    )

    pattern = tire_parser.normal_force_indices
    tire_parser.show_data(tire_parser.camber_data, pattern, "camber on camber")
    tire_parser.show_data(
        tire_parser.normal_force_data,
        pattern,
        "camber on normal force",
    )
    tire_parser.show_data(tire_parser.pressure_data, pattern, "camber on pressure")
