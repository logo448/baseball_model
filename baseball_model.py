import MySQLdb

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
    v_players = []
    h_players = []
    counter = 0

    while counter <= 8:
        # reset
        v_tmp_player_stats = {}
        h_tmp_player_stats = {}

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
        v_tmp_player_stats['name'] = v_player_list[counter]
        h_tmp_player_stats['name'] = h_player_list[counter]
        # unpack the results into a dict
        v_tmp_player_stats['PA'] = v_results[0][0]
        h_tmp_player_stats['PA'] = h_results[0][0]
        v_tmp_player_stats['1B'] = v_results[0][1]
        h_tmp_player_stats['1B'] = h_results[0][1]
        v_tmp_player_stats['2B'] = v_results[0][2]
        h_tmp_player_stats['2B'] = h_results[0][2]
        v_tmp_player_stats['3B'] = v_results[0][3]
        h_tmp_player_stats['3B'] = h_results[0][3]
        v_tmp_player_stats['HR'] = v_results[0][4]
        h_tmp_player_stats['HR'] = h_results[0][4]
        v_tmp_player_stats['SO'] = v_results[0][5]
        h_tmp_player_stats['SO'] = h_results[0][5]
        v_tmp_player_stats['BB'] = v_results[0][6]
        h_tmp_player_stats['BB'] = h_results[0][6]
        v_tmp_player_stats['O'] = v_results[0][7]
        h_tmp_player_stats['O'] = h_results[0][7]

        v_players.append(v_tmp_player_stats)
        h_players.append(h_tmp_player_stats)

        counter += 1
    return v_players, h_players