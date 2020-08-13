# S format - sb, sw, sd, sh
# SB format - beq, bne, bge, blt
# U format - auipc, lui

def binary12(num):
    li = []
    if num >= 0:
        for i in range(0, 12):
            li.insert(0, int(num % 2))
            num = int(num / 2)

    else:
        num3 = 4096 + num
        for i in range(0, 12):
            li.insert(0, int(num3 % 2))
            num3 = int(num3 / 2)
    return li


def binary13(num):
    li = []
    if num >= 0:
        for i in range(0, 13):
            li.insert(0, int(num % 2))
            num = int(num / 2)

    else:
        num3 = 8192 + num
        for i in range(0, 13):
            li.insert(0, int(num3 % 2))
            num3 = int(num3 / 2)
    return li


def binary32(num):
    li = []
    for i in range(0, 32):
        li.insert(0, int(num % 2))
        num = int(num / 2)
    return li


def binary5(num):
    li = []
    for i in range(0, 5):
        li.insert(0, int(num % 2))
        num = int(num / 2)
    return li


def sb(rs1, rs2, imm):
    s1 = binary5(rs1)
    s2 = binary5(rs2)
    i = binary12(imm)
    li = []
    li[0:7] = i[5:12]
    li[7:12] = s2
    li[12:17] = s1
    li.append(0)
    li.append(0)
    li.append(0)
    li[20:25] = i[0:5]
    li.append(0)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(1)
    li.append(1)
    return li


def sd(rs1, rs2, imm):
    s1 = binary5(rs1)
    s2 = binary5(rs2)
    i = binary12(imm)
    li = []
    li[0:7] = i[5:12]
    li[7:12] = s2
    li[12:17] = s1
    li.append(0)
    li.append(1)
    li.append(1)
    li[20:25] = i[0:5]
    li.append(0)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(1)
    li.append(1)
    return li


def sh(rs1, rs2, imm):
    s1 = binary5(rs1)
    s2 = binary5(rs2)
    i = binary12(imm)
    li = []
    li[0:7] = i[5:12]
    li[7:12] = s2
    li[12:17] = s1
    li.append(0)
    li.append(0)
    li.append(1)
    li[20:25] = i[0:5]
    li.append(0)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(1)
    li.append(1)
    return li


def sw(rs1, rs2, imm):
    s1 = binary5(rs1)
    s2 = binary5(rs2)
    i = binary12(imm)
    li = []
    li[0:7] = i[5:12]
    li[7:12] = s2
    li[12:17] = s1
    li.append(0)
    li.append(1)
    li.append(0)
    li[20:25] = i[0:5]
    li.append(0)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(1)
    li.append(1)
    return li


def beq(rs1, rs2, imm):
    s1 = binary5(rs1)
    s2 = binary5(rs2)
    i = binary13(imm)
    li = []
    li.append(i[11])
    li[1:7] = i[4:10]
    li[7:12] = s2
    li[12:17] = s1
    li.append(0)
    li.append(0)
    li.append(0)
    li[20:24] = i[0:4]
    li.append(i[10])
    li.append(1)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(1)
    li.append(1)
    return li


def bne(rs1, rs2, imm):
    s1 = binary5(rs1)
    s2 = binary5(rs2)
    i = binary13(imm)
    li = []
    li.append(i[11])
    li[1:7] = i[4:10]
    li[7:12] = s2
    li[12:17] = s1
    li.append(0)
    li.append(0)
    li.append(1)
    li[20:24] = i[0:4]
    li.append(i[10])
    li.append(1)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(1)
    li.append(1)
    return li


def blt(rs1, rs2, imm):
    s1 = binary5(rs1)
    s2 = binary5(rs2)
    i = binary13(imm)
    li = []
    li.append(i[11])
    li[1:7] = i[4:10]
    li[7:12] = s2
    li[12:17] = s1
    li.append(1)
    li.append(0)
    li.append(0)
    li[20:24] = i[0:4]
    li.append(i[10])
    li.append(1)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(1)
    li.append(1)
    print(li)
    return li


def bge(rs1, rs2, imm):
    s1 = binary5(rs1)
    s2 = binary5(rs2)
    i = binary13(imm)
    print('i is ' + str(i))
    li = []
    li.append(i[11])
    li[1:7] = i[4:10]
    li[7:12] = s2
    li[12:17] = s1
    li.append(1)
    li.append(0)
    li.append(1)
    li[20:24] = i[0:4]
    li.append(i[10])
    li.append(1)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(1)
    li.append(1)
    return li


def auipc(rd, imm):
    r = binary5(rd)
    i = binary32(imm)
    li = []
    li[0:20] = i[0:20]
    li[20:25] = r[0:5]
    li.append(0)
    li.append(0)
    li.append(1)
    li.append(0)
    li.append(1)
    li.append(1)
    li.append(1)
    return li


def lui(rd, imm):
    r = binary5(rd)
    i = binary32(imm)
    li = []
    li[0:20] = i[0:20]
    li[20:25] = r[0:5]
    li.append(0)
    li.append(1)
    li.append(1)
    li.append(0)
    li.append(1)
    li.append(1)
    li.append(1)
    return li

# li=beq(10,9,8)
# for j in range(0,32):
#    print(li[j] , end='')
