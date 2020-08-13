# R format - add, aand, oor, sll, slt, sra, srl, sub, xoor, mul, div, rem

# 0-6 opcode
# 7-11 rd
# 12-14 f3
# 15-19 rs1
# 20-24 rs2
# 25-31 f7


def binary5(num):
    li = []
    for i in range(0, 5):
        li.insert(0, int(num % 2))
        num = int(num / 2)
    return li


def add(rd, rs1, rs2):
    s1 = binary5(rs1)
    s2 = binary5(rs2)
    s3 = binary5(rd)
    li = []
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li[7:11] = s2
    li[12:16] = s1
    li.append(0)
    li.append(0)
    li.append(0)

    li[20:24] = s3
    li.append(0)
    li.append(1)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(1)
    li.append(1)
    return li


def sub(rd, rs1, rs2):
    s1 = binary5(rs1)
    s2 = binary5(rs2)
    s3 = binary5(rd)
    li = []
    li.append(0)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li[7:11] = s2
    li[12:16] = s1
    li.append(0)
    li.append(0)
    li.append(0)

    li[20:24] = s3
    li.append(0)
    li.append(1)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(1)
    li.append(1)
    return li


def sll(rd, rs1, rs2):
    s1 = binary5(rs1)
    s2 = binary5(rs2)
    s3 = binary5(rd)
    li = []
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li[7:11] = s2
    li[12:16] = s1
    li.append(0)
    li.append(0)
    li.append(1)

    li[20:24] = s3
    li.append(0)
    li.append(1)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(1)
    li.append(1)
    return li


def slt(rd, rs1, rs2):
    s1 = binary5(rs1)
    s2 = binary5(rs2)
    s3 = binary5(rd)
    li = []
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li[7:11] = s2
    li[12:16] = s1
    li.append(0)
    li.append(1)
    li.append(0)

    li[20:24] = s3
    li.append(0)
    li.append(1)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(1)
    li.append(1)
    return li


def xoor(rd, rs1, rs2):
    s1 = binary5(rs1)
    s2 = binary5(rs2)
    s3 = binary5(rd)
    li = []
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li[7:11] = s2
    li[12:16] = s1
    li.append(1)
    li.append(0)
    li.append(0)

    li[20:24] = s3
    li.append(0)
    li.append(1)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(1)
    li.append(1)
    return li


def srl(rd, rs1, rs2):
    s1 = binary5(rs1)
    s2 = binary5(rs2)
    s3 = binary5(rd)
    li = []
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li[7:11] = s2
    li[12:16] = s1
    li.append(1)
    li.append(0)
    li.append(1)

    li[20:24] = s3
    li.append(0)
    li.append(1)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(1)
    li.append(1)
    return li


def sra(rd, rs1, rs2):
    s1 = binary5(rs1)
    s2 = binary5(rs2)
    s3 = binary5(rd)
    li = []
    li.append(0)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li[7:11] = s2
    li[12:16] = s1
    li.append(1)
    li.append(0)
    li.append(1)

    li[20:24] = s3
    li.append(0)
    li.append(1)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(1)
    li.append(1)
    return li


def oor(rd, rs1, rs2):
    s1 = binary5(rs1)
    s2 = binary5(rs2)
    s3 = binary5(rd)
    li = []
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li[7:11] = s2
    li[12:16] = s1
    li.append(1)
    li.append(1)
    li.append(0)

    li[20:24] = s3
    li.append(0)
    li.append(1)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(1)
    li.append(1)
    return li


def aand(rd, rs1, rs2):
    s1 = binary5(rs1)
    s2 = binary5(rs2)
    s3 = binary5(rd)
    li = []
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li[7:11] = s2
    li[12:16] = s1
    li.append(1)
    li.append(1)
    li.append(1)

    li[20:24] = s3
    li.append(0)
    li.append(1)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(1)
    li.append(1)
    return li


def mul(rd, rs1, rs2):
    s1 = binary5(rs1)
    s2 = binary5(rs2)
    s3 = binary5(rd)
    li = []
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(1)
    li[7:11] = s2
    li[12:16] = s1
    li.append(0)
    li.append(0)
    li.append(0)

    li[20:24] = s3
    li.append(0)
    li.append(1)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(1)
    li.append(1)
    return li


def div(rd, rs1, rs2):
    s1 = binary5(rs1)
    s2 = binary5(rs2)
    s3 = binary5(rd)
    li = []
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(1)
    li[7:11] = s2
    li[12:16] = s1
    li.append(1)
    li.append(0)
    li.append(0)

    li[20:24] = s3
    li.append(0)
    li.append(1)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(1)
    li.append(1)
    return li


def rem(rd, rs1, rs2):
    s1 = binary5(rs1)
    s2 = binary5(rs2)
    s3 = binary5(rd)
    li = []
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(0)
    li.append(1)
    li[7:11] = s2
    li[12:16] = s1
    li.append(1)
    li.append(1)
    li.append(0)

    li[20:24] = s3
    li.append(0)
    li.append(1)
    li.append(1)
    li.append(0)
    li.append(0)
    li.append(1)
    li.append(1)
    return li

# li=add(9,20,21)
# for j in range(0,32):
#	print(li[j],end='')
