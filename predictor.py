import linecache
import sys

from converttomachinecode1 import *
from decode1 import *
from error_handling import *
from execute1 import *
from fetch1 import *
from memoryaccess1 import *
from registerupdate1 import *


# print(lisss)
def b_predict(PC, table):  # change0
    print("table is " + str(table))
    l = len(table)
    if (l < PC):
        print("less")
        return -1  # no data found
    else:
        if (type(table[PC]) == list):
            print("found")
            return table[PC][0]
        else:
            print("not foung")
            return -1  # no data found


def b_update(PC, branch, p, table):
    print("updating " + str(PC))
    list = [p, branch]  # p is 1 if taken else 0
    table[PC] = list


def new_branch(PC, branch, prediction, table):
    print("given PC is" + str(PC))
    l = len(table)
    if (l < PC):
        for i in range(l, PC):
            table.append(0)
        list = [prediction, branch]
        table.append(list)
    else:
        list = [prediction, branch]
        table[PC] = list


def pipeline_predictor_func():
    assign_labelled_instruction()
    globalss.assign_register()
    a = error_handling()
    if a == 1:
        # print('not passed')
        sys.exit()
    # print('passed')
    convert_to_machinecode()
    globalss.assign_memory()
    globalss.assign_stack()

    pipeline = []
    parameter = []
    lii_list = []
    b_PC = 0
    b1 = -2
    b = -2
    b_PC1 = 0
    offset = 0
    flag3 = 0
    # printing the  stats of program
    cycle_count = 0
    instructions_executed = 0
    CPI = 0
    load_store_count = 0
    ALU_count = 0
    control_instructions = 0
    stalls = 0
    data_hazard = 0
    control_hazard = 0
    stalls_data_hazard = 0
    stalls_control_hazard = 0
    cnt = 1
    oops = 0
    lisss = []
    table = []
    branch_miss = 0
    fl = open('machinecode.txt', 'r')
    Lines = fl.readlines()
    for line in Lines:
        each = line.split()
        if cnt != 1: lisss.append(len(each))
        cnt = cnt - 1

    fl.close()
    lisss.append(0)
    file2 = open('machinecode.txt', 'r')
    file6 = open('Details.txt', 'w')
    file8 = open('Stats.txt', 'w')
    i = 1
    each = str(linecache.getline('machinecode.txt', i))
    flag = 0
    flag1 = 0
    change = 0
    while 1 == 1:
        change = 0
        global reg
        reg.clear()
        print("i is " + str(i))
        if each != '':
            if flag == 0:
                each = each.split()
                if (len(each) == 1):
                    globalss.PC_execution = globalss.PC_execution + 4
                    i = int(globalss.PC_execution / 4) + 1
                    each = (linecache.getline('machinecode.txt', i))
                    continue
                instructions_executed = instructions_executed + 1
                parameter.append(0)
                pipeline.append(list(reg))
                lii_list.append('')
        else:
            change = 1

        j = 0
        if len(parameter) > 0:
            cycle_count = cycle_count + 1
        if len(parameter) == 0:
            break
        flag = 0
        while j < len(parameter):

            reg.clear()
            if parameter[j] == 0:
                temp = lii_list[j]
                lii_list.pop(j)

                lii_list.insert(j, str(fetch(each)))
                parameter[j] = 1  # fetch has been done
                file6.write("F " + "Cycle:" + str(cycle_count) + " " + str(globalss.PC_execution) + " " + str(
                    lii_list[j]) + "\n")
                if lii_list[j][25:32] == '1100011':
                    # mark=0
                    if (b_PC == 0):
                        b_PC = globalss.PC_execution
                        b = b_predict(b_PC, table)
                    else:
                        b_PC1 = globalss.PC_execution
                        b1 = b_predict(b_PC1, table)
                    # print("j of list is"+str(j))
                    c = b_predict(globalss.PC_execution, table)

                    print("predicted" + str(b))
                    if c == 1:  # case no data found by default assume not taken
                        offset = 2 * binary_2_decimal(
                            lii_list[j][20:24] + lii_list[j][1:7] + lii_list[j][24:25] + lii_list[j][0:1])
                        globalss.PC_execution = globalss.PC_execution + offset
                        print("b is 1 and PC changed to " + str(globalss.PC_execution))
                        flag1 = 1  # change_1 ends
                    # parameter[j]=4

                if lii_list[j][25:32] == '1100111' or lii_list[j][25:32] == '1101111':
                    c_stall = 1
                    control_hazard = control_hazard + 1
                    flag = 1
                # flag1=1

            elif parameter[j] == 1:

                t = pipeline[j]
                pipeline.pop(j)
                reg = decode(lii_list[j])
                # print(reg)
                file6.write("D " + "Cycle:" + str(cycle_count) + " " + str(globalss.PC_execution) + " " + str(
                    lii_list[j]) + "\n")
                pipeline.insert(j, list(determine_exact_instruction(lii_list[j], reg)))
                if pipeline[j][4] == 'SB' or pipeline[j][4] == 'UJ' or pipeline[j][4] == 'I_3':
                    flag = 1
                parameter[j] = 2
                if flag3 == 1:
                    print("flush " + str(lii_list[j]))
                    pipeline.pop(j)
                    r = [0, 0, -1, 0, 'I_1', 'addi', 0]
                    pipeline.insert(j, r)
                    oops = oops + 1
                    flag3 = 0
                    lii_list[j] = '00000000000000000000000000010011'
            elif parameter[j] == 2:

                # check if any resister is creatinh problem or not
                # reg[rd,rs1,rs2,imm,type,oriname,execute_result,memoryaccessreult]
                if j - 1 < 0:
                    reg = pipeline[j]
                    pipeline.pop(j)
                    pipeline.insert(j, list(execute(reg)))
                else:
                    if (pipeline[j - 1][0] == pipeline[j][1] and pipeline[j][1] != -1) or (
                            pipeline[j - 1][0] == pipeline[j][2] and pipeline[j][2] != -1):
                        data_hazard = data_hazard + 1
                        if pipeline[j - 1][4] != 'I_2':
                            globalss.register[pipeline[j - 1][0]] = int(pipeline[j - 1][6])
                        else:
                            globalss.register[pipeline[j - 1][0]] = int(pipeline[j - 1][7])
                    reg = pipeline[j]
                    pipeline.pop(j)
                    pipeline.insert(j, list(execute(reg)))
                parameter[j] = 3
                file6.write("E " + "Cycle:" + str(cycle_count) + " " + str(globalss.PC_execution) + " " + str(
                    lii_list[j]) + "\n")
                if (reg[4] == 'SB'):
                    offset = 2 * binary_2_decimal(
                        lii_list[j][20:24] + lii_list[j][1:7] + lii_list[j][24:25] + lii_list[j][0:1])
                    u = reg[6]

                    mark = lisss[int(b_PC / 4)]
                    # print("mark is "+str(mark))
                    # print("u is "+str(u)) #contains T or NT
                    if b == 1 and u == 1:
                        globalss.PC_execution = globalss.PC_execution - offset

                    if b == 1:
                        b_update(b_PC, offset, u, table)

                    if b == 0:
                        b_update(b_PC, offset, u, table)

                    if b == -1:
                        print("PC_u" + str(globalss.PC_execution))

                        new_branch(b_PC, offset, u, table)

                    if b == 1 and u == 0:  # it should not be taken but it is taken
                        branch_miss = branch_miss + 1
                        globalss.PC_execution = b_PC + 4
                        flag1 = 1
                        print("here1")
                        flag3 = 1
                    # parameter[j+1]=0 #marked next instruction which is fetched as not fetched...check it is j-1 or j+1
                    if b != 1 and u == 1:  # it should be taken but it is not
                        branch_miss = branch_miss + 1
                        offset = 2 * binary_2_decimal(
                            lii_list[j][20:24] + lii_list[j][1:7] + lii_list[j][24:25] + lii_list[j][0:1])
                        print("offset is " + str(offset))
                        print("PC_0 is" + str(b_PC))

                        globalss.PC_execution = b_PC + offset
                        print("PC is" + str(globalss.PC_execution))
                        flag1 = 1
                        flag3 = 1
                        flag = 1
                        print("here2")
                    # print ("j is "+str(j))
                    # print("j1 is"+str(j1))
                    # print("m_code is")
                    # print(lii_list[j1-1])

                    # pipeline.pop(j1)

                    if (b_PC1 != 0):
                        b_PC = b_PC1
                        b = b1
                        b1 = -2
                        b_PC1 = 0
                    else:
                        b_PC = 0
                        b = -2
                    offset = 0  # changing offset to default  change2 ends
                if (pipeline[j][4] == 'UJ') or (pipeline[j][4] == 'I_3'):
                    change = 0
                    flag1 = 1

            elif parameter[j] == 3:
                reg = pipeline[j]
                pipeline.pop(j)
                pipeline.insert(j, list(memoryaccess(reg)))
                parameter[j] = 4
                file6.write("M " + "Cycle:" + str(cycle_count) + " " + str(globalss.PC_execution) + " " + str(
                    lii_list[j]) + "\n")

            elif parameter[j] == 4:

                reg = pipeline[j]
                # reg[rd,rs1,rs2,imm,type,oriname,execute_result,memoryaccessreult]
                file6.write("W " + "Cycle:" + str(cycle_count) + " " + str(globalss.PC_execution) + " " + str(
                    lii_list[j]) + "\n")
                if reg[4] == 'I_2' or reg[4] == 'S':
                    load_store_count = load_store_count + 1
                elif reg[4] == 'I_3' or reg[4] == 'SB' or reg[4] == 'UJ':
                    control_instructions = control_instructions + 1
                # flag3=0
                elif reg[4] == 'R' or reg[4] == 'I_1' or reg[4] == 'U_lui' or reg[4] == 'U_auipc':
                    ALU_count = ALU_count + 1

                pipeline.pop(j)
                parameter.pop(j)
                lii_list.pop(j)
                registerupdate(reg)
                reg.clear()
                j = j - 1

            j = j + 1

        globalss.register[0] = 0

        for x in pipeline:
            print(x)
        print("done")

        if flag == 1:
            stalls_control_hazard = stalls_control_hazard + 1
            stalls = stalls + 1
        if flag == 1 or change == 1:
            continue
        if flag1 == 0:
            globalss.PC_execution = globalss.PC_execution + 4
            i = int(globalss.PC_execution / 4) + 1
        else:
            print("ipc " + str(globalss.PC_execution))
            i = int(globalss.PC_execution / 4) + 1
            flag1 = 0
        each = (linecache.getline('machinecode.txt', i))

    file2.close()
    file6.close()
    print(memory_array)
    print(register)
    cycle_count = cycle_count - oops
    instructions_executed = instructions_executed - oops
    ALU_count = ALU_count - oops

    print('\n')
    print(":: STATS ::")
    print('The number of cycles are ' + str(cycle_count))
    print('The number of instructions executed are ' + str(instructions_executed))
    print('The CPI of program is ' + str(cycle_count / instructions_executed))
    print('The number of load and store instructions executed are ' + str(load_store_count))
    print('The number of ALU instructions executed are ' + str(ALU_count))
    print('The number of control instructions exeucted are ' + str(control_instructions))
    print('The number of stalls/bubbles in pipeline are ' + str(stalls))
    print('The number of data hazards are ' + str(data_hazard))
    print('The number of control hazards are ' + str(control_hazard))
    print("The number of Branch mispredictions are: " + str(branch_miss))
    print('The number of stalls due to data hazard are ' + str(stalls_data_hazard))
    print('The number of stalls due to control hazard are ' + str(stalls_control_hazard))
    print("----------------------------------------------------------------------------")

    file8.write(":: STATS :: \n")
    file8.write('The number of cycles are ' + str(cycle_count) + ' \n')
    file8.write('The number of instructions executed are ' + str(instructions_executed) + ' \n')
    file8.write('The CPI of program is ' + str(cycle_count / instructions_executed) + ' \n')
    file8.write('The number of load and store instructions executed are ' + str(load_store_count) + ' \n')
    file8.write('The number of ALU instructions executed are ' + str(ALU_count) + ' \n')
    file8.write('The number of control instructions exeucted are ' + str(control_instructions) + ' \n')
    file8.write('The number of stalls/bubbles in pipeline are ' + str(stalls) + ' \n')
    file8.write('The number of data hazards are ' + str(data_hazard) + ' \n')
    file8.write('The number of control hazards are ' + str(control_hazard) + ' \n')
    file8.write('The number of Branch mispredictions are ' + str(branch_miss) + ' \n')
    file8.write('The number of stalls due to data hazard are ' + str(stalls_data_hazard) + ' \n')  # look
    file8.write('The number of stalls due to control hazard are ' + str(stalls_control_hazard) + ' \n')
    file8.close()

if __name__ == '__main__':
    pipeline_predictor_func()
