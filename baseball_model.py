import MySQLdb
import random

# setup global variables and objects
_db = MySQLdb.connect("localhost", "root", "Logamund 448", "lahman")
_cursor = _db.cursor()

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
    num = random.randint(1, 1001)

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

tmp1, tmp2 = get_player_stats(_v_player_list, _h_player_list)
tmp1, tmp2 = get_perc(tmp1, tmp2)
print get_event(tmp1, tmp2, 3, 0)