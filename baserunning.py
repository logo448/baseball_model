import csv
import re
import pickle


with open("C:/Users/Logan/Documents/Baseball/2014eve/master.csv", "rb") as f:
    reader = csv.reader(f, delimiter=',')
    data = []
    for tmprow in reader:
        data.append((tmprow[2], tmprow[6]))

single = re.compile("\AS[^B]")
double = re.compile("\AD")
triple = re.compile("\AT")
strikeout = re.compile("\AK")
out = re.compile("\A[0-9]+")
steal2 = re.compile("SB2")
steal3 = re.compile("SB3")
advance_info = re.compile("\.")
multiple_data = re.compile(";")

regex_list = (single, double, triple, strikeout, out)

bce_data = {"1": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
            "2": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
            "3": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}}}


def search(mode):
    if mode == "1":
        regex_list_index = 0
    elif mode == "2":
        regex_list_index = 1
    elif mode == "3":
        regex_list_index = 2
    else:
        return False

    debug = 0
    for row in data:
        debug += 1
        # catch the data
        if regex_list[regex_list_index].search(row[1]) is not None:
            # check to see if runner advancement data is present
            if advance_info.search(row[1]) is not None:
                # captures the runner advancement data and discards the rest
                split = advance_info.split(row[1])[1]
                # check to see if their are multiple runners in the runner advancement data
                if multiple_data.search(split) is not None:
                    # split data into a list of the runner data
                    split2 = multiple_data.split(split)

                    # loop through each runner in the advancement data
                    for runner in split2:
                        # make sure the runner isn't the batter
                        if runner[0] != "B":
                            # increment the variable in the event data structure that keeps track of all the times their
                            # was a runner on _ base
                            bce_data[mode][runner[0]]["times"] += 1
                            # make sure the runner didn't get out
                            if runner[1] != "X":
                                # add the base the runner reached to the event data structure
                                bce_data[mode][runner[0]]["data"].append(runner[2])
                            # runner got out
                            else:
                                # add the out to the data structure
                                bce_data[mode][runner[0]]["data"].append('x'+runner[2])
                # no data for multiple runners
                else:
                    # make sure the runner isn't the batter
                    if split[0] != "B":
                        # increment the variable in the event data structure that keeps track of all the times their
                        # was a runner on _ base
                        bce_data[mode][split[0]]["times"] += 1
                        # make sure the runner didn't get out
                        if split[1] != "X":
                            # add the base the runner reached to the event data structure
                            bce_data[mode][split[0]]["data"].append(split[2])
                        # runner got out
                        else:
                            # add the out to the data structure
                            bce_data[mode][split[0]]["data"].append('x' + split[2])

# populate data structure
search("1")
search("2")
search("3")

# output data structure
with open("C://Users/Logan/Documents/Baseball/baseball_model/data_struct.p", "wb") as f:
    pickle.dump(bce_data, f)