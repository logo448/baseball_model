import csv
import re


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

event_times = {"S": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": [], "N": 0}, "3": {"times": 0, "data": [], "N": 0}},
               "D": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": [], "N": 0}},
               "T": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
               "K": {"total": 0, "1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
               "O": {"total": 0, "1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
               "S2": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}},
               "S3": {"1": {"times": 0, "data": []}, "2": {"times": 0, "data": []}, "3": {"times": 0, "data": []}}}


def search(mode):
    bases = {"1": False, "2": False, "3": False}
    top_bottom = 0

    if mode == "S":
        regex_list_index = 0
        default_base = "1"
    elif mode == "D":
        regex_list_index = 1
        default_base = "2"
    elif mode == "T":
        regex_list_index = 2
        default_base = "3"
    else:
        return False

    for row in data:
        # check to see if the batting team has switched
        nxt_top_bottom = row[0]
        if nxt_top_bottom != top_bottom:
            top_bottom = nxt_top_bottom
            # reset bases because of batting team switch
            bases = {"1": False, "2": False, "3": False}

        # catch the data
        if regex_list[regex_list_index].search(row[1]) is not None:
            # add runner to first base
            bases[default_base] = True
            # check to see if runner advancement data is present
            if advance_info.search(row[1]) is not None:
                # captures the runner advancement data and discards the rest
                split = advance_info.split(row[1])[1]
                # check to see if their are multiple runners in the runner advancement data
                if multiple_data.search(split) is not None:
                    # split data into a list of the runner data
                    split2 = multiple_data.split(split)

                    # check to see if some runners didn't advance
                    # init a variable to keep track of the runners in the advancement data
                    recorded_runners = []
                    # loop through each runner in the advancement data
                    for runner in split2:
                        # add the base where the runner was initially to recorded runners
                        recorded_runners.append(runner[0])
                    # loop through the bases
                    for base in bases.keys():
                        # check to see if a runner wasn't mentioned in the advancement data
                        if bases[base] is True and base not in recorded_runners and base != default_base:
                            # increment variable in data structure representing the number of times a runner was on_base
                            event_times[mode][base]["times"] += 1
                            # record that a runner didn't move
                            event_times[mode][base]["N"] += 1

                    # loop through each runner in the advancement data
                    for runner in split2:
                        # make sure the runner isn't the batter
                        if runner[0] != "B":
                            # increment the variable in the event data structure that keeps track of all the times their
                            # was a runner on _ base
                            event_times[mode][runner[0]]["times"] += 1
                            # set the bool value that correlates to the base the runner was initially on to false
                            bases[runner[0]] = False
                            # make sure the runner didn't get out
                            if runner[1] != "X":
                                # add the base the runner reached to the event data structure
                                event_times[mode][runner[0]]["data"].append(runner[2])
                                # make sure the runner didn't reach home
                                if runner[2] != "H":
                                    # set the bool value of the base the runner reached to true
                                    bases[runner[2]] = True
                            # runner got out
                            else:
                                # add the out to the data structure
                                event_times[mode][runner[0]]["data"].append('x'+runner[2])
                # no data for multiple runners
                else:
                    # check to see if runner didn't advance
                    # loop through the bases
                    for base in bases.keys():
                        # check to see if a runner wasn't mentioned in the advancement data
                        if bases[base] is True and base != split[0] and base != default_base:
                            # increment variable in data structure representing the number of times a runner was on_base
                            event_times[mode][base]["times"] += 1
                            # record that a runner didn't move
                            event_times[mode][base]["N"] += 1

                    # make sure the runner isn't the batter
                    if split[0] != "B":
                        # increment the variable in the event data structure that keeps track of all the times their
                        # was a runner on _ base
                        event_times[mode][split[0]]["times"] += 1
                        # set the bool value that correlates to the base the split was initially on to false
                        bases[split[0]] = False
                        # make sure the runner didn't get out
                        if split[1] != "X":
                            # add the base the runner reached to the event data structure
                            event_times[mode][split[0]]["data"].append(split[2])
                            # make sure the runner didn't reach home
                            if split[2] != "H":
                                # set the bool value of the base the runner reached to true
                                bases[split[2]] = True
                        # runner got out
                        else:
                            # add the out to the data structure
                            event_times[mode][split[0]]["data"].append('x' + split[2])
            # no runner advancement data
            else:
                # loop through the bases
                for base in bases.keys():
                    if bases[base] is True and base != default_base:
                        # increment variable in data structure representing the number of times a runner was on _ base
                        event_times[mode][base]["times"] += 1
                        # record that a runner didn't move
                        event_times[mode][base]["N"] += 1
search("D")
for i in event_times["D"]["3"]["data"]:
    if i != "H":
        print i
print event_times["D"]["3"]["times"]
print event_times["D"]["3"]["N"]
print len(event_times["D"]["3"]["data"])