lisss = []

cnt = 1
fl = open('machinecode.txt', 'r')
Lines = fl.readlines()
for line in Lines:
    each = line.split()
    if cnt != 1: lisss.append(len(each))
    cnt = cnt - 1

fl.close()
print("HERE")
print(lisss)
