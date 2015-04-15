import MySQLdb
import batting

# setup mysql
db = MySQLdb.connect("localhost", "root", "Logamund 448", "lahman")
_cursor = db.cursor()


def get_players(num):
    v_command = """SELECT v1, v2, v3, v4, v5, v6, v7, v8, v9 FROM Gamelog WHERE id = %i""" % num
    h_command = """SELECT h1, h2, h3, h4, h5, h6, h7, h8, h9 FROM Gamelog WHERE id = %i""" % num

    _cursor.execute(v_command)
    v_results = _cursor.fetchall()
    _cursor.execute(h_command)
    h_results = _cursor.fetchall()

    return v_results[0], h_results[0]


def get_scores(num):
    command = """SELECT visiting_score, home_score FROM Gamelog WHERE %i = id""" % num

    _cursor.execute(command)
    results = _cursor.fetchall()

    return results[0]


def game():
    v_win_v_predict = 0
    v_win_v_npredict = 0
    v_lose_v_predict = 0
    v_lose_v_npredict = 0
    for i in range(1, 2431):
        if i % 5 == 0:
            print i
        sim = batting.BattingSim(get_players(i)[0], get_players(i)[1])
        sim.sim()
        if sim.v_wins > sim.h_wins and get_scores(i)[0] > get_scores(i)[1]:
            v_win_v_predict += 1
        elif not sim.v_wins > sim.h_wins and get_scores(i)[0] > get_scores(i)[1]:
            v_win_v_npredict += 1
        elif sim.v_wins > sim.h_wins and not get_scores(i)[0] > get_scores(i)[1]:
            v_lose_v_predict += 1
        elif not sim.v_wins > sim.h_wins and not get_scores(i)[0] > get_scores(i)[1]:
            v_lose_v_npredict += 1
    return v_win_v_predict, v_win_v_npredict, v_lose_v_predict, v_lose_v_npredict

print game()
