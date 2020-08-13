def print_the_instruction(Parameter, List, cycle_count):
    file1 = open("instruction_data.txt", 'a')
    if Parameter == 1:
        file1.write('Fetch has been done in cycle number ' + str(cycle_count) + '\n')
        file1.write(str(List) + '\n')

    elif Parameter == 2:
        file1.write('Decode has been done in cycle number ' + str(cycle_count) + '\n')
        file1.write(str(List) + '\n')

    elif Parameter == 3:
        file1.write('Execute has been done in cycle number ' + str(cycle_count) + '\n')
        file1.write(str(List) + '\n')

    elif Parameter == 4:
        file1.write(' Memory access has been done in cycle number ' + str(cycle_count) + '\n')
        file1.write(str(List) + '\n')

    elif Parameter == 5:
        file1.write('Memory access has been done in cycle number ' + str(cycle_count) + '\n')
        file1.write('Instruction has been completely executed and moved out of pipeline' + '\n')

    file1.close()
    return


def print_the_buffer(pipeline):
    for x in pipeline:
        print(x)


def print_the_registerfile(register):
    print(register)
    return
