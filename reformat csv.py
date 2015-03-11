import csv
import os
import shutil

def rewrite(fi):
    lst = []
    with open(fi, "rb") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'play':
                lst.append(row)
    with open(fi, "wb") as f:
        writer = csv.writer(f)
        for row in lst:
            writer.writerow(row)


path = "C:/Users/Logan/Documents/Baseball/2014eve/"
contents = os.listdir(path)
for i in contents:
    if ".EVA" in i:
        i_new = i.replace(".EVA", ".csv")
        shutil.copyfile(path+i, path+i_new)
        rewrite(path+i_new)
    if ".EVN" in i:
        i_new = i.replace(".EVN", ".csv")
        shutil.copyfile(path+i, path+i_new)
        rewrite(path+i_new)
        
        
