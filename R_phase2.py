# register is global variable
# PC = PC + 4 at each instruction read
from globalss import *


def addinst(rs1, rs2):
    return register[rs1] + register[rs2]


def subinst(rs1, rs2):
    return register[rs1] - register[rs2]


def mulinst(rs1, rs2):
    return register[rs1] * register[rs2]


def divinst(rs1, rs2):
    return int(register[rs1] / register[rs2])


def reminst(rs1, rs2):
    return register[rs1] % register[rs2]


def xoorinst(rs1, rs2):
    return register[rs1] ^ register[rs2]


def aandinst(rs1, rs2):
    return register[rs1] & register[rs2]


def oorinst(rs1, rs2):
    return register[rs1] | register[rs2]


def sllinst(rs1, rs2):
    return register[rs1] << register[rs2]


def srlinst(rs1, rs2):
    return register[rs1] >> register[rs2]


def sltinst(rs1, rs2):
    if (register[rs1] < register[rs2]):
        return 1
    else:
        return 0


# incomplete
def srainst(rs1, rs2):
    return register[rs1] >> register[rs2]
