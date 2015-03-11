import csv
import os

path = "C:/Users/Logan/Documents/Baseball/2014eve/"
contents = os.listdir(path)
master_lst = []
team_lst = []

for team in contents:
    if ".csv" in team:
        with open(path + team, "rb") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[6] != 'NP':
                    team_lst.append(row)
            master_lst.append(team_lst)
            team_lst = []

with open(path + "master.csv", "wb") as f:
    writer = csv.writer(f)
    for tmp in master_lst:
        for data in tmp:
            writer.writerow(data)