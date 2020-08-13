def binary21(num):
    li = []
    if num >= 0:
        for i in range(0, 21):
            li.insert(0, int(num % 2))
            num = int(num / 2)

    else:
        num3 = 2097152 + num
        for i in range(0, 21):
            li.insert(0, int(num3 % 2))
            num3 = int(num3 / 2)
    return li


def binary5(num):
    li = []
    for i in range(0, 5):
        li.insert(0, int(num % 2))
        num = int(num / 2)
    return li


def jal(rd, imm):
    i = binary21(int(imm))
    s1 = binary5(int(rd))
    li = []
    li[0:20] = i[0:20]
    li[20:25] = s1
    li.append(1)
    li.append(1)
    li.append(0)
    li.append(1)
    li.append(1)
    li.append(1)
    li.append(1)
    return li
