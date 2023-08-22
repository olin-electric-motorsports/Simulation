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

TOLERANCE = {
    "camber": 0.5,
    "normal_force": 200,
    "pressure":25,
}

def find_indices(data_column, key):
    unique = []
    curr_val = data_column[0]
    for i, val in enumerate(data_column):
        if abs(val-curr_val)>TOLERANCE[key]:
            unique.append(i)
            print(val, curr_val)
            curr_val = val
            
    return unique

def show_data(data, indices):
    plt.plot(data)
    for index in indices:
        plt.axvline(x = index, color = "red")
    
    plt.show()



if __name__ == "__main__":
    summary_data = pd.read_excel("assets/tire_data/ttc_data.xls")
    raw_data = loadmat("assets/tire_data/B1464run19.mat")

    print(raw_data.keys())

    normal_force = raw_data["FZ"]
    pressure = raw_data["P"]
    camber = raw_data["IA"]
    # show_data()

    normal_force_unique = find_indices(normal_force, "normal_force")
    show_data(normal_force, normal_force_unique)
    
    pressure_unique = find_indices(pressure, "pressure")
    show_data(pressure, pressure_unique)
    
    camber_unique = find_indices(camber, "camber")
    show_data(camber, camber_unique)
