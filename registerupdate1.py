import globalss


def registerupdate(reg):
    # reg[rd,rs1,rs2,imm,type,oriname,execute_result,memoryaccessreult]
    # global register
    # global PC_execution

    if reg[4] == 'R' or reg[4] == 'I_1':
        if reg[0] == 2:
            globalss.register[reg[0]] = int(reg[6])
        else:
            globalss.register[reg[0]] = int(reg[6])
            # execution result has been stored in destination register

    elif reg[4] == 'I_2':
        globalss.register[reg[0]] = int(reg[7])  # this is load instruction

    elif reg[4] == 'I_3':
        return

    elif reg[4] == 'S':
        return

    elif reg[4] == 'SB':
        return

    elif reg[4] == 'UJ':
        globalss.register[reg[0]] = reg[6]
        return

    elif reg[4] == 'U_lui' or reg[4] == 'U_auipc':
        globalss.register[reg[0]] = int(reg[6])
    return
