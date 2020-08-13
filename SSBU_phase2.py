# m_register global memory list
# register is normal register
from globalss import *

global register


def sbinst(rs1, imm):
    return register[rs1] + imm


def swinst(rs1, imm):
    return register[rs1] + imm


def shinst(rs1, imm):
    return register[rs1] + imm


def sdinst(rs1, imm):
    return register[rs1] + imm


def beqinst(rs1, rs2):
    if (register[rs1] == register[rs2]):
        return 1
    else:
        return 0


def bltinst(rs1, rs2):
    if (register[rs1] < register[rs2]):
        return 1
    else:
        return 0


def bneinst(rs1, rs2):
    if (register[rs1] != register[rs2]):
        return 1
    else:
        return 0


def bgeinst(rs1, rs2):
    if (register[rs1] >= register[rs2]):
        return 1
    else:
        return 0


def auipcinst(string):
    i = ''
    for j in range(0, 20):
        i = i + string[j]
    for j in range(20, 32):
        i = i + '0'
    imm = int(i, 2)
    imm = PC_execution + imm
    return imm


def luiinst(string):
    i = ''
    for j in range(0, 20):
        i = i + string[j]
    for j in range(20, 32):
        i = i + '0'
    imm = int(i, 2)
    return imm
