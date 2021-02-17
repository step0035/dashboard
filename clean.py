#put all csv file in a directory (srcPath)
#create new empty directory for cleaned csv (desPath)

from datetime import datetime
import os
import numpy as np
import pandas as pd

#change "date_time" and "first_next_bus_estimated_arrival" columns to datetime objects
def change_to_date(row):
    row["date_time"] = datetime.strptime(str(row["date_time"][0:-7]), "%Y,%m,%d,%H,%M,%S")
    row["first_next_bus_estimated_arrival"] = datetime.strptime(str(row["first_next_bus_estimated_arrival"][0:-7]), "%Y,%m,%d,%H,%M,%S")
    return row

#add new "late" column
#True if bus is late, False if not late
def check_late():
    df["late"] = np.where(df["date_time"] > df["first_next_bus_estimated_arrival"], True, False)
    df["late_by"] = np.where(df["late"]==True, (df["date_time"] - df["first_next_bus_estimated_arrival"]).dt.total_seconds(), np.NaN)


srcPath = "./data/dirty_csv_data/" #replace with your own
desPath = "./data/clean_csv_data/" # replace with your own

for fileName in os.listdir(srcPath):
    filePath = srcPath + fileName

    df = pd.read_csv(filePath)
    df = df.apply(change_to_date, axis="columns")
    check_late()

    print(f"Exporting {fileName}")
    df.to_csv(desPath + fileName, index=False)