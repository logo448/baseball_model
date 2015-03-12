import csv
import re=


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
multiple_data = re.compile(";")

event_times = {"S": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
               "D": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
               "T": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
               "HR": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
               "K": {"total": 0, "1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
               "O": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
               "W": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
               "S2": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
               "S3": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}}}

for i in data:
    if single.search(i) is not None:
        if advance_info.search(i) is not None:
            tmp = advance_info.split(i)[1]
            if multiple_data.search(tmp) is not None:
                tmp2 = multiple_data.split(tmp)
                for i2 in tmp2:
                    if i2[0] != 'B':
                        event_times["S"][i2[0]]["times"] += 1
                        if i2[1] != 'X':
                            event_times["S"][i2[0]]["data"].append(i2[2])
                        else:
                            event_times["S"][i2[0]]["data"].append('x'+i2[2])
            else:
                if tmp[0] != 'B':
                    event_times["S"][tmp[0]]["times"] += 1
                    if tmp[1] != 'X':
                        event_times["S"][tmp[0]]["data"].append(tmp[2])
                    else:
                        event_times["S"][tmp[0]]["data"].append('x'+tmp[2])

    if double.search(i) is not None:
        if advance_info.search(i) is not None:
            tmp = advance_info.split(i)[1]
            if multiple_data.search(tmp) is not None:
                tmp2 = multiple_data.split(tmp)
                for i2 in tmp2:
                    if i2[0] != 'B':
                        event_times["D"][i2[0]]["times"] += 1
                        if i2[1] != 'X':
                            event_times["D"][i2[0]]["data"].append(i2[2])
                        else:
                            event_times["D"][i2[0]]["data"].append('x'+i2[2])
            else:
                if tmp[0] != 'B':
                    event_times["D"][tmp[0]]["times"] += 1
                    if tmp[1] != 'X':
                        event_times["D"][tmp[0]]["data"].append(tmp[2])
                    else:
                        event_times["D"][tmp[0]]["data"].append('x'+tmp[2])

    if triple.search(i) is not None:
        if advance_info.search(i) is not None:
            tmp = advance_info.split(i)[1]
            if multiple_data.search(tmp) is not None:
                tmp2 = multiple_data.split(tmp)
                for i2 in tmp2:
                    if i2[0] != 'B':
                        event_times["T"][i2[0]]["times"] += 1
                        if i2[1] != 'X':
                            event_times["T"][i2[0]]["data"].append(i2[2])
                        else:
                            event_times["T"][i2[0]]["data"].append('x'+i2[2])
            else:
                if tmp[0] != 'B':
                    event_times["T"][tmp[0]]["times"] += 1
                    if tmp[1] != 'X':
                        event_times["T"][tmp[0]]["data"].append(tmp[2])
                    else:
                        event_times["T"][tmp[0]]["data"].append('x'+tmp[2])

    if strikeout.search(i) is not None:
        if advance_info.search(i) is not None:
            tmp = advance_info.split(i)[1]
            if multiple_data.search(tmp) is not None:
                tmp2 = multiple_data.split(tmp)
                for i2 in tmp2:
                    if i2[0] != 'B':
                        event_times["K"][i2[0]]["times"] += 1
                        if i2[1] != 'X':
                            event_times["K"][i2[0]]["data"].append(i2[2])
                        else:
                            event_times["K"][i2[0]]["data"].append('x'+i2[2])
            else:
                if tmp[0] != 'B':
                    event_times["K"][tmp[0]]["times"] += 1
                    if tmp[1] != 'X':
                        event_times["K"][tmp[0]]["data"].append(tmp[2])
                    else:
                        event_times["K"][tmp[0]]["data"].append('x'+tmp[2])
        else:
            event_times["K"]["total"] += 1