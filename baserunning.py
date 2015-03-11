import csv
import re
import pickle


with open("C:/Users/Logan/Documents/Baseball/2014eve/master.csv", "rb") as f:
    reader = csv.reader(f, delimiter=',')
    data = []
    for row in reader:
        data.append(row[6])

single = re.compile("\AS[^B]")
double = re.compile("\AD")
triple = re.compile("\AT")
homer = re.compile("\AHR")
strikeout = re.compile("\AK")
out = re.compile("\A[0-9]+")
walk = re.compile("\AW")
steal2 = re.compile("SB2")
steal3 = re.compile("SB3")
advance_info = re.compile("\.")

event_times = {"S": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
               "D": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
               "T": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
               "HR": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
               "K": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
               "O": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
               "W": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
               "S2": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
               "S3": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}}}

for i in data:
    if single.search(i) is not None:
        if advance_info.search(i) is not None:
            tmp = advance_info.split(i)[1]
            if re.search(";", tmp) is not None:
                tmp2 = re.split(";", tmp)
                if len(tmp2) > 2:
                    print i