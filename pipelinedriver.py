import linecache
import sys

from converttomachinecode1 import *
from decode1 import *
from error_handling import *
from execute1 import *
from fetch1 import *
from memoryaccess1 import *
from registerupdate1 import *

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

cycle_count = 0
stalls = 0

file2 = open('machinecode.txt', 'r')
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
            parameter.append(0)
            pipeline.append(list(reg))
            lii_list.append('')
    else:
        change = 1

    j = 0
    if len(parameter) == 0:
        break
    flag = 0
    while j < len(parameter):
        cycle_count = cycle_count + 1
        reg.clear()

        if parameter[j] == 0:
            lii_list.pop(j)
            lii_list.insert(j, str(fetch(each)))
            parameter[j] = 1  # fetch has been done
            if lii_list[j][25:32] == '1100111' or lii_list[j][25:32] == '1100011' or lii_list[j][25:32] == '1101111':
                flag = 1

        elif parameter[j] == 1:
            pipeline.pop(j)
            reg = decode(lii_list[j])
            # print(reg)
            pipeline.insert(j, list(determine_exact_instruction(lii_list[j], reg)))
            if pipeline[j][4] == 'SB' or pipeline[j][4] == 'UJ' or pipeline[j][4] == 'I_3':
                flag = 1
            parameter[j] = 2

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
                    if pipeline[j - 1][4] != 'I_2':
                        globalss.register[pipeline[j - 1][0]] = int(pipeline[j - 1][6])
                    else:
                        globalss.register[pipeline[j - 1][0]] = int(pipeline[j - 1][7])
                reg = pipeline[j]
                pipeline.pop(j)
                pipeline.insert(j, list(execute(reg)))
            parameter[j] = 3
            if (pipeline[j][6] == 1 and pipeline[j][4] == 'SB') or (pipeline[j][4] == 'UJ') or (
                    pipeline[j][4] == 'I_3'):
                change = 0
            if ((pipeline[j][6] == 1 and pipeline[j][4] == 'SB') or (pipeline[j][4] == 'UJ') or (
                    pipeline[j][4] == 'I_3')):
                flag1 = 1

        elif parameter[j] == 3:
            reg = pipeline[j]
            pipeline.pop(j)
            pipeline.insert(j, list(memoryaccess(reg)))
            parameter[j] = 4


        elif parameter[j] == 4:
            reg = pipeline[j]

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

    if flag == 1 or change == 1:
        stalls = stalls + 1
        continue
    if flag1 == 0:
        globalss.PC_execution = globalss.PC_execution + 4
        i = int(globalss.PC_execution / 4) + 1
    else:
        i = int(globalss.PC_execution / 4) + 1
        flag1 = 0
    each = (linecache.getline('machinecode.txt', i))

file2.close()
print(memory_array)
print(register)
print('The number of cycles are ' + str(cycle_count))
print('The number of stalls are' + str(stalls))
