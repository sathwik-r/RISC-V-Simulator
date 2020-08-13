import linecache
import sys

from converttomachinecode1 import *
from decode1 import *
from error_handling import *
from execute0 import *
from fetch0 import *
from memoryaccess1 import *
from registerupdate1 import *


def unpipelined_func():
    assign_labelled_instruction()  # Labelled instruction has been stored in list
    globalss.assign_register()  # a 32 length array nas been assigned for register
    a = error_handling()  # checking for error
    if a == 1:
        print('not passed')  # if error exist
        sys.exit()
    print('passed')  # no error
    convert_to_machinecode()  # Phase 1 portion ...A machinecode.txt file has been created
    globalss.assign_memory()  # 1000 size array has been assigned for memory
    globalss.assign_stack()  # 1000 size array has been assigned for stack

    file2 = open('machinecode.txt', 'r')
    i = 1
    CLOCK = 0
    each = str(linecache.getline('machinecode.txt', i))  # Execution will be done now
    while each != '':
        print((each))
        global reg
        each = each.split()
        if (len(each) == 1):
            globalss.PC_execution = globalss.PC_execution + 4
            i = int(globalss.PC_execution / 4) + 1
            each = (linecache.getline('machinecode.txt', i))
            continue
        lii = fetch(each)
        CLOCK = CLOCK + 1
        # print("Instruction fetched!!")
        # We will update the reg[] list after the execution of every step

        reg = decode(lii)  # now exact instruction name will be appended #reg[rd,rs1,rs2,imm,type]
        CLOCK = CLOCK + 1
        # print("Instruction Decoded!!")
        reg = determine_exact_instruction(lii,
                                          reg)  # now exact instruction name will be appended #reg[rd,rs1,rs2,imm,type,oriname]

        reg = execute(reg)  # execution result will be appended in the reg list
        CLOCK = CLOCK + 1
        # print("Instruction executed!!")

        reg = memoryaccess(reg)  # a new value has been appended. We will use this value in regsiter update
        CLOCK = CLOCK + 1
        # print("Memory accessed")                 # reg[rd,rs1,rs2,imm,type,oriname,execute_result,memoryaccessreult]

        registerupdate(reg)
        CLOCK = CLOCK + 1
        # print("Writeback done!!")

        print(reg)  # It is printing the contents of a instruction
        i = int(globalss.PC_execution / 4) + 1  # It contains the line number of next instruction to be executed
        print(i)
        each = (linecache.getline('machinecode.txt', i))  # each will contain  the next instruction
        reg.clear()  # reg list is cleared
        globalss.register[0] = 0  # register x0 is updated to value zero.Because it is constant
    file2.close()
    print("Number of cycles: ", CLOCK)  # Run this to print clock cycles
    # print(globalss.memory_array)           #Run this to print the memory
    print(register)  # Run this to print the register


if __name__ == '__main__':
    unpipelined_func()
