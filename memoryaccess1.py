import globalss


def memoryaccess(reg):
    # global memory_array
    # global PC_execution
    # global register
    # reg[rd,rs1,rs2,imm,type,oriname,execute_result]
    if reg[4] == 'R' or reg[4] == 'I_1' or reg[4] == 'SB' or reg[4] == 'U_lui' or reg[4] == 'U_auipc' or reg[4] == 'UJ':
        reg.append(-1)
        return reg
    elif reg[4] == 'I_2':
        print(reg[6])
        if reg[1] == 2:
            reg.append(globalss.stack_array[reg[6]])
        else:
            reg.append(globalss.memory_array[reg[6]])
        return reg
    elif reg[4] == 'I_3':
        reg.append(-1)
        # globalss.PC_execution=globalss.PC_execution+reg[6]
    elif reg[4] == 'S':
        reg.append(-1)
        if reg[1] == 2:
            pos = reg[6]
            if reg[5] == 'sb':
                globalss.stack_array[pos] = globalss.register[reg[2]]
            elif reg[5] == 'sw':
                globalss.stack_array[pos] = globalss.register[reg[2]]
                globalss.stack_array[pos + 1] = 0
                globalss.stack_array[pos + 2] = 0
                globalss.stack_array[pos + 3] = 0
            elif reg[5] == 'sd':
                globalss.stack_array[pos] = globalss.register[reg[2]]
                globalss.stack_array[pos + 1] = 0
                globalss.stack_array[pos + 2] = 0
                globalss.stack_array[pos + 3] = 0
                globalss.stack_array[pos + 4] = 0
                globalss.stack_array[pos + 5] = 0
                globalss.stack_array[pos + 6] = 0
                globalss.stack_array[pos + 7] = 0
            elif reg[5] == 'sh':
                globalss.stack_array[pos] = globalss.register[reg[2]]
                globalss.stack_array[pos + 1] = 0


        else:
            pos = int(reg[6]) - 65536
            if reg[5] == 'sb':
                globalss.memory_array[pos] = globalss.register[reg[2]]
            elif reg[5] == 'sw':
                globalss.memory_array[pos] = globalss.register[reg[2]]
                globalss.memory_array[pos + 1] = 0
                globalss.memory_array[pos + 2] = 0
                globalss.memory_array[pos + 3] = 0
            elif reg[5] == 'sd':
                globalss.memory_array[pos] = globalss.register[reg[2]]
                globalss.memory_array[pos + 1] = 0
                globalss.memory_array[pos + 2] = 0
                globalss.memory_array[pos + 3] = 0
                globalss.memory_array[pos + 4] = 0
                globalss.memory_array[pos + 5] = 0
                globalss.memory_array[pos + 6] = 0
                globalss.memory_array[pos + 7] = 0
            elif reg[5] == 'sh':
                globalss.memory_array[pos] = globalss.register[reg[2]]
                globalss.memory_array[pos + 1] = 0
    # elif reg[4]=='jal':
    # store the return address in ra register i.e store PC_execution+4
    # then PC_execution=PC_execution+ imm
    return reg
