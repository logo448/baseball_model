# 123 234 142 143
import MySQLdb
import random
import pickle
from collections import Counter

# setup global variables and objects
_db = MySQLdb.connect("localhost", "root", "Logamund 448", "lahman")
_cursor = _db.cursor()
_outs = 0
_inning = 0
_top_or_bottom = 0
_v_score = 0
_h_score = 0
_bases = {"1": False, "2": False, "3": False}
# import the BcE advancement data
with open("C://Users/Logan/Documents/Baseball/baseball_model/data_struct.p", "rb") as f:
    bce_data = pickle.load(f)

# user input section
_v_player_list = ["Yasiel Puig", "Justin Turner", "Hanley Ramirez",
                  "Adrian Gonzalez", "Scott Van Slyke", "Juan Uribe", "Andre Ethier",
                  "A.J. Ellis", "Clayton Kershaw"]
_h_player_list = ["A.J. Pollock", "Aaron Hill", "Paul Goldschmidt",
                  "Martin Prado", "Mark Trumbo", "Miguel Montero",
                  "Chris Owings", "Gerardo Parra", "Wade Miley"]


def get_player_stats(v_player_list, h_player_list):
    """Get the player stats"""
    # init
    v_players_stats = []
    h_players_stats = []
    counter = 0

    while counter <= 8:
        # reset
        v_tmp_stats = {}
        h_tmp_stats = {}

        # create sql SELECT statements
        v_sql = """SELECT (b.AB + b.BB + b.HBP + b.SF), (b.H - (b.2B + b.3B + b.HR)), b.2B, b.3B, b.HR, b.SO, b.BB,
        ((b.AB + b.BB + b.HBP + b.SF) - (b.H + b.BB + b.SO))
        FROM batting b, master m WHERE CONCAT(m.nameFirst, ' ', m.nameLast) = '%s' AND b.yearID = 2013
        AND b.playerID = m.playerID""" % (v_player_list[counter])
        h_sql = """SELECT (b.AB + b.BB + b.HBP + b.SF), (b.H - (b.2B + b.3B + b.HR)), b.2B, b.3B, b.HR, b.SO, b.BB,
        ((b.AB + b.BB + b.HBP + b.SF) - (b.H + b.BB + b.SO))
        FROM batting b, master m WHERE CONCAT(m.nameFirst, ' ', m.nameLast) = '%s' AND b.yearID = 2013
        AND b.playerID = m.playerID""" % (h_player_list[counter])

        # run sql SELECT statements
        _cursor.execute(v_sql)
        v_results = _cursor.fetchall()
        _cursor.execute(h_sql)
        h_results = _cursor.fetchall()

        # add values to the tmp dicts
        v_tmp_stats['name'] = v_player_list[counter]
        h_tmp_stats['name'] = h_player_list[counter]
        # unpack the results into a dict
        v_tmp_stats['PA'] = v_results[0][0]
        h_tmp_stats['PA'] = h_results[0][0]
        v_tmp_stats['1B'] = v_results[0][1]
        h_tmp_stats['1B'] = h_results[0][1]
        v_tmp_stats['2B'] = v_results[0][2]
        h_tmp_stats['2B'] = h_results[0][2]
        v_tmp_stats['3B'] = v_results[0][3]
        h_tmp_stats['3B'] = h_results[0][3]
        v_tmp_stats['HR'] = v_results[0][4]
        h_tmp_stats['HR'] = h_results[0][4]
        v_tmp_stats['SO'] = v_results[0][5]
        h_tmp_stats['SO'] = h_results[0][5]
        v_tmp_stats['BB'] = v_results[0][6]
        h_tmp_stats['BB'] = h_results[0][6]
        v_tmp_stats['O'] = v_results[0][7]
        h_tmp_stats['O'] = h_results[0][7]

        # add the current tmp players stats dict to the players lists
        v_players_stats.append(v_tmp_stats)
        h_players_stats.append(h_tmp_stats)

        # increase the count by 1
        counter += 1
    return v_players_stats, h_players_stats


def get_perc(v_players_stats, h_players_stats):
    """convert the stats of the player to percentages"""
    # init
    v_players_perc = []
    h_players_perc = []
    counter = 0

    while counter <= 8:
        # reset
        v_tmp_perc = {}
        h_tmp_perc = {}

        # get the stats of player counter
        v_stats = v_players_stats[counter]
        h_stats = h_players_stats[counter]

        # populate the v_tmp_perc dictionary
        v_tmp_perc['1B'] = round(float(v_stats['1B'])/v_stats['PA'], 3)
        h_tmp_perc['1B'] = round(float(h_stats['1B'])/h_stats['PA'], 3)
        v_tmp_perc['2B'] = round(float(v_stats['2B'])/v_stats['PA'], 3)
        h_tmp_perc['2B'] = round(float(h_stats['2B'])/h_stats['PA'], 3)
        v_tmp_perc['3B'] = round(float(v_stats['3B'])/v_stats['PA'], 3)
        h_tmp_perc['3B'] = round(float(h_stats['3B'])/h_stats['PA'], 3)
        v_tmp_perc['HR'] = round(float(v_stats['HR'])/v_stats['PA'], 3)
        h_tmp_perc['HR'] = round(float(h_stats['HR'])/h_stats['PA'], 3)
        v_tmp_perc['SO'] = round(float(v_stats['SO'])/v_stats['PA'], 3)
        h_tmp_perc['SO'] = round(float(h_stats['SO'])/h_stats['PA'], 3)
        v_tmp_perc['BB'] = round(float(v_stats['BB'])/v_stats['PA'], 3)
        h_tmp_perc['BB'] = round(float(h_stats['BB'])/h_stats['PA'], 3)
        v_tmp_perc['O'] = round(float(v_stats['O'])/v_stats['PA'], 3)
        h_tmp_perc['O'] = round(float(h_stats['O'])/h_stats['PA'], 3)

        # add the tmp dict full of player stats in percentage form to a list
        v_players_perc.append(v_tmp_perc)
        h_players_perc.append(h_tmp_perc)

        # increment a counter variable by 1
        counter += 1
    return v_players_perc, h_players_perc


def get_event(v_players_perc, h_players_perc, batter, team):
    """Returns the event that is selected randomly, according to prior situations"""
    # gets the stats for a certain batter
    # if the desired batter is on visiting team
    if team == 0:
        # get the dict from the batterth element of the visiting player list
        stats = v_players_perc[batter]
    # if the desired batter is on home team
    else:
        # get the dict from the batterth element of the home player list
        stats = h_players_perc[batter]

    # set the thresholds for each event
    b1 = stats['1B'] * 1000
    b2 = (stats['2B'] * 1000) + b1
    b3 = (stats['3B'] * 1000) + b2
    hr = (stats['HR'] * 1000) + b3
    so = (stats['SO'] * 1000) + hr
    bb = (stats['BB'] * 1000) + so
    o = (stats['O'] * 1000) + bb
    # print(b1, b2, b3, hr, so, bb, o, b1+b2+b3+hr+so+bb+o)

    # generate the random number that determines the event that is simulated
    num = random.randint(1, 1000)

    # figure out what event should be simulated
    if num <= b1:
        return '1B'
    elif b1 < num <= b2:
        return '2B'
    elif b2 < num <= b3:
        return '3B'
    elif b3 < num <= hr:
        return 'HR'
    elif hr < num <= so:
        return 'SO'
    elif so < num <= bb:
        return 'BB'
    elif bb < num <= o:
        return 'O'
    else:
        get_event(v_players_perc, h_players_perc, batter, team)


def increment_score():
    """Increments the score of the team on offense"""
    # allow access to global variables in this function
    global _v_score
    global _h_score

    # if visiting team is on offense
    if _top_or_bottom == 0:
        # increase the visiting teams score
        _v_score += 1
    # home team on offense
    else:
        # increase home teams score by 1
        _h_score += 1


def walk():
    """Function that readjusts the bases in the occurrence of a walk"""
    # allow access to global variables in this function
    global _bases
    global _v_score
    global _h_score
    # list created to keep track of which bases need to be set to occupied
    set_true = ["1"]

    # loop through all the bases
    for base in _bases.keys():
        # if the base is occupied
        if _bases[base]:
            # if the base is first base
            if base == "1":
                # add second base to the occupied list
                set_true.append("2")
            # if the base behind it and first base are occupied. Needed because of force movement principle of baseball
            elif _bases[str(int(base) - 1)] and _bases["1"]:
                # set the base in question to unoccupied
                _bases[base] = False
                # if the next base isn't home plate
                if int(base) + 1 != 4:
                    # add the next base to the occupied bases list
                    set_true.append(str(int(base) + 1))
                # next base is home plate
                else:
                    increment_score()
    # loop through list of newly occupied bases
    for base in set_true:
        # set base to occupied
        _bases[base] = True


def homerun():
    """Adjusts bases and score if a homerun is hit"""
    # allow access to global variables in this function
    global _bases
    global _v_score
    global _h_score

    # add one point for the batter scoring
    increment_score()

    # loop through the bases
    for base in _bases:
        # if base is occupied
        if _bases[base]:
            # set base to unoccupied
            _bases[base] = False
            increment_score()


def strikeout():
    """Adjusts the game variables if a strikeout occurs"""
    global _outs
    _outs += 1


def out():
    """Readjusts game variables if an out occurs"""
    # allows access to global variables in this function
    global _bases
    global _v_score
    global _h_score
    global _outs

    # increments outs by one
    _outs += 1

    # check to see if runners will advance
    # if one is occupied and tow isn't
    if _bases["1"] and not _bases["2"]:
        # randomly select if runner advances or not
        # random number
        rand = random.randint(1, 1000)
        # if random number falls in the right range. Happens 13 percent of the time
        if rand <= 133:
            # move runner from first to second
            _bases["1"] = False
            _bases["2"] = True
    # if first if above fails and second is occupied but 3 isn't
    elif _bases["2"] and not _bases["3"]:
        # randomly select if runner advances or not
        # random number
        rand = random.randint(1, 1000)
        # if random number falls in the right range. Happens 46 percent of the time
        if rand <= 456:
            # move runner from second to third
            _bases["2"] = False
            _bases["3"] = True
    # if first two ifs fail and guy on 3
    elif _bases["3"]:
        # randomly select if runner advances or not
        # random number
        rand = random.randint(1, 1000)
        # if random number falls in the right range. Happens 56 percent of the time
        if rand <= 557:
            # move runner to home/increment score and remove runner on 3
            _bases["3"] = False
            increment_score()


def get_sb():
    """check if a runner is going to steal a base, if so is he successful?"""
    # allow access to these global variables in this function
    global _bases
    global _outs

    # if runner on first but not on second
    if _bases["1"] and not _bases["2"]:
        # randomly see if runner will attempt to steal 2
        if random.randint(1, 1000) <= 74:
            # set first to unoccupied, either way success or fail their is no one on first
            _bases["1"] = False
            # randomly see if runner made it safely
            if random.randint(1, 1000) <= 728:
                # set second to occupied
                _bases["2"] = True
            # runner didn't make it to second
            else:
                # add an out
                _outs += 1
    # if their is a runner on second but not third
    elif _bases["2"] and not _bases["3"]:
        # randomly see if runner will attempt to steal 2
        if random.randint(1, 1000) <= 17:
            # set 2 to unoccupied, either way success or fail their is no one on second anymore
            _bases["2"] = False
            # randomly see if runner made it safely
            if random.randint(1, 1000) <= 765:
                # set third to occupied
                _bases["3"] = True
            # runner got caught
            else:
                # add an out
                _outs += 1


def hit(e):
    # allow access to global variables in this function
    global _bases
    global _v_score
    global _h_score
    global _outs

    # variable to figure out home many runners are on base
    number_runners = 0
    # list of where the runners are located
    runner_bases = []

    # loop through each base
    for base in _bases.keys():
        # if the base is occupied
        if _bases[base]:
            # increase the number of runners by 1
            number_runners += 1
            # add the base to the list of bases
            runner_bases.append(base)
    # sort list of bases from greatest (3) to smallest (1)
    runner_bases.sort(reverse=True)

    # if there are no runners
    if number_runners == 0:
        # if single
        if e == "1":
            # set first to occupied
            _bases["1"] = True
        # if double
        elif e == "2":
            # set second to occupied
            _bases["2"] = True
        # if triple
        elif e == "3":
            # set third to occupied
            _bases["3"] = True

    # one runner
    elif number_runners == 1:
        # turn the runner advancement data into a counter object
        data = Counter(bce_data[e][runner_bases[0]]["data"])

        # single
        if e == "1":
            # get the probabilities required for the first runner
            attempt_2 = round(float(data["2"] + data["x2"]) / bce_data[e][runner_bases[0]]["times"], 4) * 10000
            attempt_3 = round(float(data["3"] + data["x3"]) / bce_data[e][runner_bases[0]]["times"], 4) * 10000
            attempt_h = round(float(data["H"] + data["xH"]) / bce_data[e][runner_bases[0]]["times"], 4) * 10000
            if runner_bases[0] != "3":
                success_2 = round(float(data["2"]) / (data["2"] + data["x2"]), 4) * 10000
            success_3 = round(float(data["3"]) / (data["3"] + data["x3"]), 4) * 10000
            success_h = round(float(data["H"]) / (data["H"] + data["xH"]), 4) * 10000

            # infinite loop until all runners have been moved
            while True:
                # set the base where the runner is located to unoccupied cuz runner is going to move
                _bases[runner_bases[0]] = False

                # generate random number to determine new runner position
                rand = random.randint(1, 10000)
                # random number correlates with the runner attempting to go to second base
                if rand <= attempt_2:
                    # generate random number to determine if the runner safely reaches second
                    rand = random.randint(1, 10000)
                    # safe
                    if rand <= success_2:
                        # set second to occupied
                        _bases["2"] = True
                    # out
                    else:
                        # add an out
                        _outs += 1
                    # exit while because placement is complete
                    break
                # random number correlates with the runner attempting to go to third base
                elif attempt_2 < rand <= attempt_3 + attempt_2:
                    # generate random number to determine if runner reaches 3 safely
                    rand = random.randint(1, 10000)
                    # safe
                    if rand <= success_3:
                        _bases["3"] = True
                    # out
                    else:
                        _outs += 1
                    # exit while because placement is complete
                    break
                # random number correlates with the runner attempting to go to score
                elif attempt_3 < rand <= attempt_h + attempt_3:
                    # generate random number to determine if runner scores safely
                    rand = random.randint(1, 10000)
                    # safe
                    if rand <= success_h:
                        increment_score()
                    # out
                    else:
                        _outs += 1
                    # exit while because placement is complete
                    break
                # runner placement not complete
                else:
                    # go through the loop again
                    continue
            # set first base to occupied because a single was hit
            _bases["1"] = True

        # double
        elif e == "2":
            # get the probabilities required for the first runner
            attempt_3 = round(float(data["3"] + data["x3"]) / bce_data[e][runner_bases[0]]["times"], 4) * 10000
            attempt_h = round(float(data["H"] + data["xH"]) / bce_data[e][runner_bases[0]]["times"], 4) * 10000
            if runner_bases[0] != "3":
                success_3 = round(float(data["3"]) / (data["3"] + data["x3"]), 4) * 10000
            success_h = round(float(data["H"]) / (data["H"] + data["xH"]), 4) * 10000

            # infinite loop until all runners have been moved
            while True:
                # set the base where the runner is located to unoccupied cuz runner is going to move
                _bases[runner_bases[0]] = False

                # generate random number to determine new runner position
                rand = random.randint(1, 10000)
                # random number correlates with runner attempting to go to 3
                if rand <= attempt_3:
                    # generate random number to determine if runner reaches 3 safely
                    rand = random.randint(1, 10000)
                    # safe
                    if rand <= success_3:
                        _bases["3"] = True
                    # out
                    else:
                        _outs += 1
                    # exit while loop because runner was moved
                    break
                # random number correlates with runner trying to score
                elif attempt_3 < rand <= attempt_h + attempt_3:
                    # generate random number to determine if runner will score safely
                    rand = random.randint(1, 10000)
                    # safe
                    if rand <= success_h:
                        increment_score()
                    # out
                    else:
                        _outs += 1
                    # exit while loop because the runner has moved
                    break
                # runner movement not complete
                else:
                    # go through loop again
                    continue
            # set second base to occupied because a double was hit
            _bases["2"] = True

        # triple
        elif e == "3":
            # get the probabilities required for the first runner
            success_h = round(float(data["H"]) / (data["H"] + data["xH"]), 4) * 10000

            # set the base the runner occupied to unoccupied cuz runner is going to move
            _bases[runner_bases[0]] = False

            # generate random number to determine if runner scores safely
            rand = random.randint(1, 10000)
            # safe
            if rand <= success_h:
                increment_score()
            # out
            else:
                _outs += 1
            # set third base to occupied because a triple was hit.
            _bases["3"] = True

    # two runners
    elif number_runners == 2:
        # turn the runner advancement data into counter objects for each runner
        data = Counter(bce_data[e][runner_bases[0]]["data"])
        data1 = Counter(bce_data[e][runner_bases[1]]["data"])

        # single
        if e == "1":
            # get the probabilities for the lead runner
            attempt_2 = round(float(data["2"] + data["x2"]) / bce_data[e][runner_bases[0]]["times"], 4) * 10000
            attempt_3 = round(float(data["3"] + data["x3"]) / bce_data[e][runner_bases[0]]["times"], 4) * 10000
            attempt_h = round(float(data["H"] + data["xH"]) / bce_data[e][runner_bases[0]]["times"], 4) * 10000
            if runner_bases[0] != "3":
                success_2 = round(float(data["2"]) / (data["2"] + data["x2"]), 4) * 10000
            success_3 = round(float(data["3"]) / (data["3"] + data["x3"]), 4) * 10000
            success_h = round(float(data["H"]) / (data["H"] + data["xH"]), 4) * 10000

            # get the probabilities for the other runner
            attempt1_2 = round(float(data1["2"] + data1["x2"]) / bce_data[e][runner_bases[1]]["times"], 4) * 10000
            attempt1_3 = round(float(data1["3"] + data1["x3"]) / bce_data[e][runner_bases[1]]["times"], 4) * 10000
            attempt1_h = round(float(data1["H"] + data1["xH"]) / bce_data[e][runner_bases[1]]["times"], 4) * 10000
            if runner_bases[1] != "3":
                success1_2 = round(float(data1["2"]) / (data1["2"] + data1["x2"]), 4) * 10000
            success1_3 = round(float(data1["3"]) / (data1["3"] + data1["x3"]), 4) * 10000
            success1_h = round(float(data1["H"]) / (data1["H"] + data1["xH"]), 4) * 10000

            # lead runner
            while True:
                # set the base where the lead runner is coming from to unoccupied cuz the runner is going to move
                _bases[runner_bases[0]] = False
                # generate random number to determine where lead runner is going
                rand = random.randint(1, 10000)
                # random number correlates to attempting to go to 2
                if rand <= attempt_2:
                    # generate random number to determine if runner reaches 2 safely
                    rand = random.randint(1, 10000)
                    # safe
                    if rand <= success_2:
                        _bases["2"] = True
                    # out
                    else:
                        _outs += 1
                    # exit while loop because runner has been moved
                    break

                # attempting to go to 3
                elif attempt_2 < rand <= attempt_3 + attempt_2:
                    # generate random number to determine if runner reaches 3 safely
                    rand = random.randint(1, 10000)
                    # safe
                    if rand <= success_3:
                        _bases["3"] = True
                    # out
                    else:
                        _outs += 1
                    # exit while loop because runner has been moved
                    break
                # attempting to score
                elif attempt_3 < rand <= attempt_h + attempt_3:
                    # generate random number to determine if runner scores safely
                    rand = random.randint(1, 10000)
                    # safe
                    if rand <= success_h:
                        increment_score()
                    # out
                    else:
                        _outs += 1
                    # exit while loop because runner has been moved
                    break
                else:
                    continue

            # last runner
            while True:
                rand = random.randint(1, 10000)
                _bases[runner_bases[1]] = False
                # attempting to go to 2
                if rand <= attempt1_2:
                    # generate random number to determine if runner reaches 2 safely
                    rand = random.randint(1, 10000)
                    # safe
                    if rand <= success1_2:
                        # no one on 2
                        if not _bases["2"]:
                            _bases["2"] = True
                        # someone on 2
                        else:
                            # readjust lead runner too 3
                            _bases["3"] = True
                    # out
                    else:
                        _outs += 1
                    # exit while loop because runner has been moved
                    break
                # attempting to go to 3
                elif attempt1_2 < rand <= attempt1_3 + attempt1_2:
                    # generate random number to determine if runner reaches 3 safely
                    rand = random.randint(1, 10000)
                    # safe
                    if rand <= success1_3:
                        # no one on third
                        if not _bases["3"]:
                            _bases["3"] = True
                        # someone on third
                        else:
                            # readjust runner back to second
                            _bases["2"] = True
                    # out
                    else:
                        _outs += 1
                    # exit while loop because runner has been moved
                    break
                # attempting to score
                elif attempt1_3 < rand <= attempt1_h + attempt1_3:
                    # generate random number to determine if runner scores safely
                    rand = random.randint(1, 10000)
                    # safe
                    if rand <= success1_h:
                        increment_score()
                    # break
                    else:
                        _outs += 1
                    # exit while loop because runner has been moved
                    break
                # runner movement failed
                else:
                    # retry
                    continue
            # set first to occupied because a single was hit
            _bases["1"] = True

        # double
        if e == "2":
            # get the probabilities for the lead runner
            attempt_3 = round(float(data["3"] + data["x3"]) / bce_data[e][runner_bases[0]]["times"], 4) * 10000
            attempt_h = round(float(data["H"] + data["xH"]) / bce_data[e][runner_bases[0]]["times"], 4) * 10000
            if runner_bases[0] != "3":
                success_3 = round(float(data["3"]) / (data["3"] + data["x3"]), 4) * 10000
            success_h = round(float(data["H"]) / (data["H"] + data["xH"]), 4) * 10000

            # get the probabilities for the other runner
            attempt1_3 = round(float(data1["3"] + data1["x3"]) / bce_data[e][runner_bases[1]]["times"], 4) * 10000
            attempt1_h = round(float(data1["H"] + data1["xH"]) / bce_data[e][runner_bases[1]]["times"], 4) * 10000
            if runner_bases[1] != "3":
                success1_3 = round(float(data1["3"]) / (data1["3"] + data1["x3"]), 4) * 10000
            success1_h = round(float(data1["H"]) / (data1["H"] + data1["xH"]), 4) * 10000

            # lead runner
            while True:
                # set the base where the lead runner came from to unoccupied cuz runner has to move
                _bases[runner_bases[0]] = False
                # generate random number to determine where the runner ends up
                rand = random.randint(1, 10000)
                # random number correlates to attempting to go to 3
                if rand <= attempt_3:
                    # generate random number to determine if runner reaches 3 safely
                    rand = random.randint(1, 10000)
                    # safe
                    if rand <= success_3:
                        _bases["3"] = True
                    # out
                    else:
                        _outs += 1
                    # exit while loop because runner has been moved
                    break

                # attempting to score
                elif attempt_3 < rand <= attempt_h + attempt_3:
                    # generate random number to determine if runner scores safely
                    rand = random.randint(1, 10000)
                    # safe
                    if rand <= success_h:
                        increment_score()
                    # out
                    else:
                        _outs += 1
                    # exit while loop because runner has been moved
                    break
                # runner movement failed
                else:
                    # retry
                    continue

            # last runner
            while True:
                # set the base where the lead runner came from to unoccupied cuz runner has to move
                _bases[runner_bases[1]] = False
                # generate random number to determine where the runner ends up
                rand = random.randint(1, 10000)
                # attempting to go to 3
                if rand <= attempt1_3:
                    # generate random number to determine if runner reaches 3 safely
                    rand = random.randint(1, 10000)
                    # safe
                    if rand <= success1_3:
                        # no one on 3
                        if not _bases["3"]:
                            _bases["3"] = True
                        # someone on 3
                        else:
                            # readjust lead runner to home
                            increment_score()
                    # out
                    else:
                        _outs += 1
                    # exit while loop because runner has been moved
                    break

                # attempting to score
                elif attempt1_3 < rand <= attempt1_h + attempt1_3:
                    # generate random number to determine if runner scores safely
                    rand = random.randint(1, 10000)
                    # safe
                    if rand <= success1_h:
                        increment_score()
                    # out
                    else:
                        _outs += 1
                    # exit while loop because runner has been moved
                    break
                # runner readjustment failed
                else:
                    # retry
                    continue
            # set second base to occupied because a double was hit
            _bases["2"] = True

        # triple
        if e == "3":
            # get the probabilities for the lead runner
            success_h = round(float(data["H"]) / (data["H"] + data["xH"]), 4) * 10000

            # get the probabilities for the other runner
            success1_h = round(float(data1["H"]) / (data1["H"] + data1["xH"]), 4) * 10000

            # lead runner
            _bases[runner_bases[0]] = False
            # generate random number to determine if runner reaches 2 safely
            rand = random.randint(1, 10000)
            # safe
            if rand <= success_h:
                increment_score()
            # out
            else:
                _outs += 1

            # last runner
            _bases[runner_bases[1]] = False
            # generate random number to determine if runner reaches 2 safely
            rand = random.randint(1, 10000)
            # safe
            if rand <= success1_h:
                increment_score()
            # out
            else:
                _outs += 1
            # set the third to occupied because a triple was hit
            _bases["3"] = True

    # three runners
    elif number_runners == 3:
        # data for runner on 3
        data = Counter(bce_data[e]["3"]["data"])
        # data for runner on 2
        data1 = Counter(bce_data[e]["2"]["data"])
        # data for runner on 1
        data2 = Counter(bce_data[e]["1"]["data"])

        # single
        if e == "1":
            # necessary data for runner on 3
            success_h = round(float(data["H"]) / (data["H"] + data["xH"]), 4) * 10000
            # necessary data for runner on 2
            attempt1_3 = round(float(data1["3"] + data1["x3"]) / bce_data[e]["2"]["times"], 4) * 10000
            attempt1_h = round(float(data1["H"] + data1["xH"]) / bce_data[e]["2"]["times"], 4) * 10000
            success1_3 = round(float(data1["3"]) / (data1["3"] + data1["x3"]), 4) * 10000
            success1_h = round(float(data1["H"]) / (data1["H"] + data1["xH"]), 4) * 10000
            # necessary data for runner on 1
            attempt2_2 = round(float(data2["2"] + data2["x2"]) / bce_data[e]["1"]["times"], 4) * 10000
            attempt2_3 = round(float(data2["3"] + data2["x3"]) / bce_data[e]["1"]["times"], 4) * 10000
            attempt2_h = round(float(data2["H"] + data2["xH"]) / bce_data[e]["1"]["times"], 4) * 10000
            success2_2 = round(float(data2["2"]) / (data2["2"] + data2["x2"]), 4) * 10000
            success2_3 = round(float(data2["3"]) / (data2["3"] + data2["x3"]), 4) * 10000
            success2_h = round(float(data2["H"]) / (data2["H"] + data2["xH"]), 4) * 10000

            # runner on 3
            rand = random.randint(1, 10000)
            _bases["3"] = False
            if rand <= success_h:
                increment_score()
            else:
                _outs += 1

            # runner on 2
            while True:
                rand = random.randint(1, 10000)
                _bases["2"] = False
                # attempting to go to 3
                if rand <= attempt1_3:
                    print 'm3'
                    rand = random.randint(1, 10000)
                    if rand <= success1_3:
                        _bases["3"] = True
                    else:
                        _outs += 1
                    break
                # attempting to score
                elif attempt1_3 < rand <= attempt1_h + attempt1_3:
                    print 'mh'
                    rand = random.randint(1, 10000)
                    if rand <= success1_h:
                        increment_score()
                    else:
                        _outs += 1
                    break
                else:
                    continue

            # runner on 1
            while True:
                rand = random.randint(1, 10000)
                _bases["1"] = False
                # attempting to go to 2
                if rand <= attempt2_2:
                    print 'la2'
                    rand = random.randint(1, 10000)
                    if rand <= success2_2:
                        if not _bases["2"]:
                            _bases["2"] = True
                        else:
                            _bases["3"] = True
                    else:
                        _outs += 1
                    break
                # attempting to go to 3
                elif attempt2_2 < rand <= attempt2_3 + attempt2_2:
                    print 'la3'
                    rand = random.randint(1, 10000)
                    if rand <= success2_3:
                        if not _bases["3"]:
                            _bases["3"] = True
                        else:
                            _bases["2"] = True
                    else:
                        _outs += 1
                    break
                # attempting to score
                elif attempt2_3 < rand <= attempt2_h + attempt2_3:
                    print 'lah'
                    rand = random.randint(1, 10000)
                    if rand <= success2_h:
                        increment_score()
                    else:
                        _outs += 1
                    break
                else:
                    continue
            _bases["1"] = True

        # double
        if e == "2":
            # necessary data for runner on 3
            success_h = round(float(data["H"]) / (data["H"] + data["xH"]), 4) * 10000
            # necessary data for runner on 2
            success1_h = round(float(data1["H"]) / (data1["H"] + data1["xH"]), 4) * 10000
            # necessary data for runner on 1
            attempt2_3 = round(float(data2["3"] + data2["x3"]) / bce_data[e]["1"]["times"], 4) * 10000
            attempt2_h = round(float(data2["H"] + data2["xH"]) / bce_data[e]["1"]["times"], 4) * 10000
            success2_3 = round(float(data2["3"]) / (data2["3"] + data2["x3"]), 4) * 10000
            success2_h = round(float(data2["H"]) / (data2["H"] + data2["xH"]), 4) * 10000

            # runner on 3
            rand = random.randint(1, 10000)
            _bases["3"] = False
            if rand <= success_h:
                increment_score()
            else:
                _outs += 1

            # runner on 2
            rand = random.randint(1, 10000)
            _bases["2"] = False
            if rand <= success1_h:
                increment_score()
            else:
                _outs += 1

            # runner on 1
            while True:
                rand = random.randint(1, 10000)
                _bases["1"] = False
                # attempting to go to 3
                if rand <= attempt2_3:
                    rand = random.randint(1, 10000)
                    if rand <= success2_3:
                        if not _bases["3"]:
                            _bases["3"] = True
                        else:
                            _bases["2"] = True
                    else:
                        _outs += 1
                    break
                # attempting to score
                elif attempt2_3 < rand <= attempt2_h + attempt2_3:
                    rand = random.randint(1, 10000)
                    if rand <= success2_h:
                        increment_score()
                    else:
                        _outs += 1
                    break
                else:
                    continue
            _bases["2"] = True

        # triple
        if e == "3":
            # necessary data for runner on 3
            success_h = round(float(data["H"]) / (data["H"] + data["xH"]), 4) * 10000
            # necessary data for runner on 2
            success1_h = round(float(data1["H"]) / (data1["H"] + data1["xH"]), 4) * 10000
            # necessary data for runner on 1
            success2_h = round(float(data2["H"]) / (data2["H"] + data2["xH"]), 4) * 10000

            # runner on 3
            rand = random.randint(1, 10000)
            _bases["3"] = False
            if rand <= success_h:
                increment_score()
            else:
                _outs += 1

            # runner on 2
            rand = random.randint(1, 10000)
            _bases["2"] = False
            if rand <= success1_h:
                increment_score()
            else:
                _outs += 1

            # runner on 1
            rand = random.randint(1, 10000)
            _bases["1"] = False
            if rand <= success2_h:
                increment_score()
            else:
                _outs += 1
            _bases["3"] = True