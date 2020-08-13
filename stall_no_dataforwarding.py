import linecache
import sys

from converttomachinecode1 import *
from decode1 import *
from error_handling import *
from execute1 import *
from fetch1 import *
from memoryaccess1 import *
from print_the_instruction import *
from registerupdate1 import *


def stall_no_dataforwarding_func():
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

    buffer = -1
    register_file = -1
    particular_instruction = -1

    print("\n")
    # kn1 = input("Print register values after every cycle ? (y/n) ")
    # if kn1=="y":
    #  buffer=1
    #
    # kn2 = input("Print pipeline interstate buffer reg values after every cycle ? (y/n) ")
    # if kn2=="y":
    #  register_file=1
    #
    # particular_instruction = int(input("Enter specific instruction to see it's pipeline reg info :"))

    current_string = ''
    file = open("instruction_data.txt", "r+")
    file.truncate(0)
    file.close()

    pipeline = []
    parameter = []
    lii_list = []

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

    file2 = open('machinecode.txt', 'r')
    file6 = open('Details.txt', 'w')
    file8 = open('Stats.txt', 'w')
    # file3=open('check.txt','w')
    stalls = 0
    cycle_count = 0
    i = 1
    each = str(linecache.getline('machinecode.txt', i))
    flag = 0
    flag1 = 0
    change = 0
    while 1 == 1:
        change = 0
        global reg
        reg.clear()
        if each != '':
            if flag == 0:
                each = each.split()
                if (len(each) == 1):
                    globalss.PC_execution = globalss.PC_execution + 4
                    i = int(globalss.PC_execution / 4) + 1
                    each = (linecache.getline('machinecode.txt', i))
                    continue
                instructions_executed = instructions_executed + 1
                if instructions_executed == particular_instruction:
                    current_string = str(fetch(each))
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
                lii_list.pop(j)
                lii_list.insert(j, str(fetch(each)))
                parameter[j] = 1  # fetch has been done
                file6.write("F " + "Cycle:" + str(cycle_count) + " " + str(globalss.PC_execution) + " " + str(
                    lii_list[j]) + "\n")  # new
                if lii_list[j][25:32] == '1100111' or lii_list[j][25:32] == '1100011' or lii_list[j][
                                                                                         25:32] == '1101111':
                    control_hazard = control_hazard + 1
                    stalls_control_hazard = stalls_control_hazard + 1
                    flag = 1
                if current_string == lii_list[j]:
                    print_the_instruction(1, pipeline[j], cycle_count)

            elif parameter[j] == 1:
                if j - 1 < 0:
                    pipeline.pop(j)
                    reg = decode(lii_list[j])
                    file6.write("D " + "Cycle:" + str(cycle_count) + " " + str(globalss.PC_execution) + " " + str(
                        lii_list[j]) + "\n")
                    pipeline.insert(j, list(determine_exact_instruction(lii_list[j], reg)))
                    parameter[j] = 2;
                    if current_string == lii_list[j]:
                        print_the_instruction(2, pipeline[j], cycle_count)

                    if pipeline[j][4] == 'SB' or pipeline[j][4] == 'UJ' or pipeline[j][4] == 'I_3':
                        flag = 1
                        stalls_control_hazard = stalls_control_hazard + 1


                else:
                    # print(reg)
                    pipeline.pop(j)
                    reg = decode(lii_list[j])
                    pipeline.insert(j, list(determine_exact_instruction(lii_list[j], reg)))
                    if current_string == lii_list[j]:
                        print_the_instruction(2, pipeline[j], cycle_count)

                    if (pipeline[j - 1][0] == pipeline[j][1] and pipeline[j][1] != -1 and pipeline[j - 1][0] != 0) or (
                            pipeline[j - 1][0] == pipeline[j][2] and pipeline[j][2] != -1 and pipeline[j - 1][0] != 0):
                        flag = 1;
                        stalls_data_hazard = stalls_data_hazard + 1
                        if parameter[j - 1] == 3:
                            data_hazard = data_hazard + 1
                        break;
                    elif ((j - 2) >= 0 and pipeline[j - 2][0] == pipeline[j][1] and pipeline[j][1] != -1 and
                          pipeline[j - 2][0] != 0) or (
                            (j - 2) >= 0 and pipeline[j - 2][0] == pipeline[j][2] and pipeline[j][2] != -1 and
                            pipeline[j - 2][0] != 0):
                        flag = 1;
                        stalls_data_hazard = stalls_data_hazard + 1
                        if parameter[j - 2] == 4:
                            data_hazard = data_hazard + 1
                        break;
                    else:

                        parameter[j] = 2;
                        if pipeline[j][4] == 'SB' or pipeline[j][4] == 'UJ' or pipeline[j][4] == 'I_3':
                            flag = 1
                            stalls_control_hazard = stalls_control_hazard + 1


            elif parameter[j] == 2:
                file6.write("E " + "Cycle:" + str(cycle_count) + " " + str(globalss.PC_execution) + " " + str(
                    lii_list[j]) + "\n")
                reg = pipeline[j]
                pipeline.pop(j)
                pipeline.insert(j, list(execute(reg)))
                if current_string == lii_list[j]:
                    print_the_instruction(3, pipeline[j], cycle_count)
                parameter[j] = 3
                if (pipeline[j][6] == 1 and pipeline[j][4] == 'SB') or (pipeline[j][4] == 'UJ') or (
                        pipeline[j][4] == 'I_3'):
                    change = 0
                    flag1 = 1


            elif parameter[j] == 3:
                file6.write("M " + "Cycle:" + str(cycle_count) + " " + str(globalss.PC_execution) + " " + str(
                    lii_list[j]) + "\n")
                reg = pipeline[j]
                pipeline.pop(j)
                pipeline.insert(j, list(memoryaccess(reg)))
                parameter[j] = 4
                if current_string == lii_list[j]:
                    print_the_instruction(4, pipeline[j], cycle_count)

            elif parameter[j] == 4:
                file6.write("W " + "Cycle:" + str(cycle_count) + " " + str(globalss.PC_execution) + " " + str(
                    lii_list[j]) + "\n")
                reg = pipeline[j]
                if reg[4] == 'I_2' or reg[4] == 'S':
                    load_store_count = load_store_count + 1
                elif reg[4] == 'I_3' or reg[4] == 'SB' or reg[4] == 'UJ':
                    control_instructions = control_instructions + 1
                elif reg[4] == 'R' or reg[4] == 'I_1' or reg[4] == 'U_lui' or reg[4] == 'U_auipc':
                    ALU_count = ALU_count + 1

                if current_string == lii_list[j]:
                    print_the_instruction(5, pipeline[j], cycle_count)
                    current_string = ''

                pipeline.pop(j)
                parameter.pop(j)
                lii_list.pop(j)
                registerupdate(reg)
                reg.clear()
                j = j - 1

            j = j + 1

        globalss.register[0] = 0
        if buffer == 1:
            print(cycle_count)
            print_the_buffer(pipeline)

        if register_file == 1:
            print(cycle_count)
            print_the_registerfile(globalss.register)

        if flag == 1:
            stalls = stalls + 1
        if flag == 1 or change == 1:
            continue
        if flag1 == 0:
            globalss.PC_execution = globalss.PC_execution + 4
            i = int(globalss.PC_execution / 4) + 1
        else:
            i = int(globalss.PC_execution / 4) + 1
            flag1 = 0
        each = (linecache.getline('machinecode.txt', i))

    file2.close()
    file6.close()
    print(memory_array)
    print(register)

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
    print("The number of Branch mispredictions are: 0")
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
    file8.write('The number of Branch mispredictions are: 0' + ' \n')
    file8.write('The number of stalls due to data hazard are ' + str(stalls_data_hazard) + ' \n')  # look
    file8.write('The number of stalls due to control hazard are ' + str(stalls_control_hazard) + ' \n')
    file8.close()


if __name__ == '__main__':
    stall_no_dataforwarding_func()
