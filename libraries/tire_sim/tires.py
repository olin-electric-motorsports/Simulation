import pandas as pd
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum, auto
from pprint import pprint
from collections import defaultdict


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
        self.load_data(path_to_data_spreadsheet)
        print(f"Tire ID being queried: {self.tireid}")
        self.time_range = self.compute_time_range()
        self.complete_data = self._e()

    def load_data(self, path_to_data_spreadsheet):
        """Load data into attributes to our tire parser from the spreadsheet.
        We care primarily about normal force, pressure, and camber data.

        :param path_to_data_spreadsheet: _description_
        :type path_to_data_spreadsheet: _type_
        """
        raw_data = loadmat(path_to_data_spreadsheet)
        self.tireid = raw_data["tireid"]

        self.normforce_data = raw_data["FZ"]
        self.pressure_data = raw_data["P"]
        self.camber_data = raw_data["IA"]
        self.parameter_data = [
            self.normforce_data,
            self.pressure_data,
            self.camber_data,
        ]

        self.latforce_data = raw_data["FY"]
        self.slip_data = raw_data["SR"]

    def compute_time_range(self):
        """TODO: validation, not just checking normforce data

        :return: _description_
        :rtype: _type_
        """
        return len(self.normforce_data)

    def append_all_data(self, dict_to_append_to: defaultdict, idx):
        dict_to_append_to[idx].append(
            (Stats.NORMAL_FORCE.name, float(self.normforce_data[idx][0]))
        )
        dict_to_append_to[idx].append(
            (Stats.PRESSURE.name, float(self.pressure_data[idx][0]))
        )
        dict_to_append_to[idx].append(
            (Stats.CAMBER_ANGLE.name, float(self.camber_data[idx][0]))
        )
        return dict_to_append_to

    def _e(self):
        """This function is responsible for creating a dictionary.

        {
            TIME_STEP : [(NORMAL FORCE, ____), (PRESSURE, ______), (CAMBER, _____)]
        }
        """
        data_dict = defaultdict(list)
        old_normforce = self.normforce_data[0]
        old_pressure = self.pressure_data[0]
        old_camber = self.camber_data[0]
        self.append_all_data(data_dict, 0)
        for i in range(self.time_range - 1):
            if not old_normforce or (
                abs(old_normforce - self.normforce_data[i])
                > TOLERANCE[Stats.NORMAL_FORCE]
            ):
                data_dict = self.append_all_data(data_dict, i)
                old_normforce = self.normforce_data[i]
            if (
                not old_pressure
                or abs(old_pressure - self.pressure_data[i]) > TOLERANCE[Stats.PRESSURE]
            ):
                data_dict = self.append_all_data(data_dict, i)
                old_pressure = self.pressure_data[i]
            if (
                not old_camber
                or abs(old_camber - self.camber_data[i]) > TOLERANCE[Stats.CAMBER_ANGLE]
            ):
                data_dict = self.append_all_data(data_dict, i)
                old_camber = self.camber_data[i]

        return data_dict

    def display_data(self):
        """For every different value of pressure, camber, and normal force, compute the SR + Lateral force graph"""
        times = list(self.complete_data.keys())

        for i in range(len(times)):
            if i == 0:
                continue

            plt.plot(
                self.slip_data[times[i - 1] : times[i]],
                self.latforce_data[times[i - 1] : times[i]],
            )
            plt.xlabel("Slip")
            plt.ylabel("Lateral Force")
            plt.title(
                f"Normal Force = {self.complete_data[times[i]][0][1]} || Camber = {self.complete_data[times[i]][1][1]} || Pressure = {self.complete_data[times[i]][2][1]}\n"
            )
            plt.show()


if __name__ == "__main__":
    parser = TireParser(
        path_to_summary_table="assets/tire_data/ttc_data.xls",
        path_to_data_spreadsheet="assets/tire_data/B1464run19.mat",
    )

    parser.display_data()
    # pprint(parser.normforce_data)
    # print(len(parser.camber_data))
    # pprint(parser.complete_data)
    # print(parser.complete_data.keys())
